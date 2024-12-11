import os
from moviepy.editor import VideoFileClip

def process_video(video_file):
    video_path = f'uploads/{video_file.filename}'
    video_file.save(video_path)
    
    # Process video for transcription and translation (e.g., extract audio)
    audio_path = extract_audio(video_path)
    
    # Perform transcription and translation (dummy example)
    # Here you would typically call your transcription and translation functions
    # For example: transcription = transcribe_audio(audio_path)
    # translation = translate_text(transcription)
    
    return {
        "video_url": video_path,
        "audio_url": audio_path,
        # "transcription": transcription,
        # "translation": translation
    }

def extract_audio(video_path):
    clip = VideoFileClip(video_path)
    audio_path = video_path.replace('.mp4', '.wav')
    clip.audio.write_audiofile(audio_path)
    return audio_path
