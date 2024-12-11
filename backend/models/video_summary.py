import os
import logging
from transformers import pipeline
from moviepy.editor import VideoFileClip
from backend.models.audio_processing import process_audio

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_audio_in_chunks(video_path, chunk_duration=60):
    """Extract audio in segments of specified duration (in seconds)."""
    video_clip = VideoFileClip(video_path)
    audio_clips = []
    
    for start_time in range(0, int(video_clip.duration), chunk_duration):
        end_time = min(start_time + chunk_duration, video_clip.duration)
        audio_clip = video_clip.subclip(start_time, end_time)
        chunk_audio_path = f"{video_path.rsplit('.', 1)[0]}_chunk_{start_time}.wav"
        audio_clip.audio.write_audiofile(chunk_audio_path)
        audio_clips.append(chunk_audio_path)
    
    logging.info(f"Extracted {len(audio_clips)} audio chunks.")
    return audio_clips

def summarize_text(text):
    """Summarize the given text using a summarization model."""
    if not text.strip():
        logging.warning("Empty transcription provided for summarization.")
        return "No content to summarize."
    
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def summarize_video(video_path):
    try:
        logging.info(f"Video path received: {video_path}")
        
        # Extract audio in chunks from the video
        audio_chunks = extract_audio_in_chunks(video_path)
        if not audio_chunks:
            logging.error("Audio extraction failed.")
            return "Audio extraction failed."

        combined_transcriptions = []
        
        # Process each audio chunk for transcription
        for audio_chunk in audio_chunks:
            # Transcribe audio chunk
            transcriptions, _ = process_audio(audio_chunk)
            if not transcriptions:
                logging.error("Transcription failed or returned empty for a chunk.")
                continue  # Skip this chunk
            
            # Combine transcriptions into a single string
            combined_transcriptions.append(' '.join(transcriptions))
        
        if not combined_transcriptions:
            logging.error("All transcription attempts failed.")
            return "Transcription failed. Please try again."
        
        # Combine all transcriptions into a single string
        full_transcription = ' '.join(combined_transcriptions)
        
        # Summarize the combined transcription
        summary = summarize_text(full_transcription)
        logging.info("Summarization completed successfully.")

    except Exception as e:
        logging.error(f"Error processing video {video_path}: {str(e)}")
        return f"An error occurred while processing the video: {str(e)}"

    finally:
        # Clean up the temporary audio chunk files
        for audio_chunk in audio_chunks:
            if os.path.exists(audio_chunk):
                os.remove(audio_chunk)
                logging.info(f"Deleted temporary audio file: {audio_chunk}")

    return summary
