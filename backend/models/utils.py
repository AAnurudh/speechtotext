import os
import time
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from backend.models.marian_translate import MarianTranslate
from backend.models.whisper_model import load_medium_model

model = load_medium_model()

def transcribe(model, audio_path):
    try:
        start_time = time.time()
        result = model.transcribe(audio_path, fp16=False, beam_size=5)
        transcription_text = result.get("text", "")
        
        if not transcription_text:
            print("No text returned in transcription.")
            return "Transcription failed. No text returned."

        print(f"Transcription completed in {time.time() - start_time:.2f} seconds.")
        return transcription_text
    
    except Exception as e:
        print(f'Transcription failed: {str(e)}')
        return "Transcription failed due to an error."

def translate_text(transcription, tgt_lang="en"):
    translator = MarianTranslate(tgt_lang=tgt_lang)
    try:
        return translator.translate(transcription)
    except Exception as e:
        print(f'Translation failed: {str(e)}')
        return "Translation failed due to an error."

def add_subtitles_to_video(video_path, subtitles_text, output_path):
    video = VideoFileClip(video_path)
    duration = video.duration

    words = subtitles_text.split()
    subtitle_clips = []
    line_duration = 2

    current_time = 0
    line = []
    for word in words:
        line.append(word)
        if len(line) >= 5:
            text = ' '.join(line)
            subtitle = TextClip(text, fontsize=24, color='white', font='Arial-Bold', bg_color='black')
            subtitle = subtitle.set_position(("center", "bottom")).set_duration(line_duration).set_start(current_time)
            subtitle_clips.append(subtitle)

            line = []
            current_time += line_duration

    if line:
        text = ' '.join(line)
        subtitle = TextClip(text, fontsize=24, color='white', font='Arial-Bold', bg_color='black')
        subtitle = subtitle.set_position(("center", "bottom")).set_duration(duration - current_time).set_start(current_time)
        subtitle_clips.append(subtitle)

    final = CompositeVideoClip([video] + subtitle_clips)
    final.write_videofile(output_path, codec="libx264", fps=24)

    print(f"Video with subtitles saved to: {output_path}")
    return output_path
