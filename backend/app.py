import os
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from moviepy.editor import VideoFileClip
from models.utils import transcribe, translate_text, add_subtitles_to_video
from models.whisper_model import load_medium_model
from models.audio_processing import process_audio
from models.video_summary import summarize_video   
from moviepy.config import change_settings
from werkzeug.utils import secure_filename
import numpy as np

# Configure ImageMagick for subtitle handling in MoviePy
change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})  # Ensure this points to the ImageMagick binary

app = Flask(__name__)
CORS(app)

# Initialize SocketIO with threading mode as a fallback
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)

# Define the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define folders for uploads and subtitles
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
SUBTITLES_FOLDER = os.path.join(BASE_DIR, 'subtitles')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUBTITLES_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


whisper_model = load_medium_model()

# Route for favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_FOLDER, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400

        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'No file uploaded or no selected file'}), 400

        # Save uploaded video
        filename = secure_filename(file.filename)
        video_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(video_path)
        print("Video saved to:", video_path)

        # Extract audio and process
        audio_path = extract_audio(video_path)
        if not audio_path:
            return jsonify({'error': 'Audio extraction failed'}), 500

        # Transcription and translation
        transcriptions, translations = process_audio(audio_path, segment_duration=60)
        transcription_text = ' '.join(transcriptions)
        translation = ' '.join(translations)

        # Save results
        transcription_path = os.path.join(SUBTITLES_FOLDER, 'transcription.txt')
        translation_path = os.path.join(SUBTITLES_FOLDER, 'translation.txt')
        with open(transcription_path, 'w', encoding='utf-8') as f:
            f.write(transcription_text)
        with open(translation_path, 'w', encoding='utf-8') as f:
            f.write(translation)

        # Summarization
        summarization_text = summarize_video(video_path)
        summarization_path = os.path.join(SUBTITLES_FOLDER, 'summarization.txt')
        with open(summarization_path, 'w', encoding='utf-8') as f:
            f.write(summarization_text)

        # Video subtitles
        output_video_path = os.path.join(SUBTITLES_FOLDER, f"output_{os.path.basename(video_path)}")
        add_subtitles_to_video(video_path, translation, output_video_path)

        return jsonify({
            "transcription": transcription_text,
            "translation": translation,
            "summarization": summarization_text,
            'transcription_url': f'http://localhost:5000/download/transcription.txt',
            'translation_url': f'http://localhost:5000/download/translation.txt',
            'summarization_url': f'http://localhost:5000/download/summarization.txt',
            'video_url': f"http://localhost:5000/videos/{os.path.basename(output_video_path)}"
        }), 200

    except Exception as e:
        print(f"Upload processing error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(SUBTITLES_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_file(file_path, as_attachment=True)

@app.route('/videos/<filename>', methods=['GET'])
def serve_video(filename):
    file_path_subtitles = os.path.join(SUBTITLES_FOLDER, filename)
    file_path_uploads = os.path.join(UPLOAD_FOLDER, filename)
    
    if os.path.exists(file_path_subtitles):
        return send_file(file_path_subtitles, as_attachment=True)
    elif os.path.exists(file_path_uploads):
        return send_file(file_path_uploads, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

def extract_audio(video_path):
    """Extract audio from video file."""
    try:
        audio_path = video_path.rsplit('.', 1)[0] + '.wav'
        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(audio_path)
        return audio_path if os.path.exists(audio_path) else None
    except Exception as e:
        print(f'Error extracting audio: {str(e)}')
        return None

@socketio.on('audioData')
def handle_audio_data(data):
    audio_data = data['audioData']
    source_language = data['sourceLanguage']
    target_language = data['targetLanguage']

    # Convert the audio data to a format suitable for transcription
    audio_np = np.frombuffer(audio_data, dtype=np.float32)

    # Transcribe the audio using the Whisper model
    transcription_text, detected_language = transcribe(whisper_model, audio_np)
    translation = translate_text(transcription_text, target_language)

    # Emit the translated transcription back to the client
    emit('translatedTranscription', {'transcription': translation})
    

@app.route('/summarize_video', methods=['POST'])
def summarize_video_endpoint():
    # Ensure 'video' exists in request.files
    if 'video' not in request.files:
        return jsonify({'error': 'No video file in request'}), 400
    video_file = request.files['video']
    
    video_path = os.path.join(UPLOAD_FOLDER, secure_filename(video_file.filename))
    video_file.save(video_path)
    # Use the extract_audio function defined in this file
    audio_path = extract_audio(video_path)  # Save the video file first
    if not audio_path:
        return jsonify({'error': 'Audio extraction failed'}), 500

    summary = summarize_video(video_path, extract_audio)  # Call the function from the new file
    return jsonify({"summary": summary})

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)
