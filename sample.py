import whisper
import logging
# Load the large model
model = whisper.load_model("large")

def transcribe(model, audio_path):
    try:
        result = model.transcribe(audio_path, fp16=False, beam_size=5)
        transcription_text = result.get("text", "")

        if not transcription_text:
            logging.error(f"Transcription failed for {audio_path}. No text returned.")
            return "Transcription failed. No text returned.", ""

        return transcription_text, ""  # No language detection

    except Exception as e:
        logging.error(f"Transcription failed for {audio_path}: {str(e)}")
        return "Transcription failed due to an error.", ""

# Process your audio file
transcription = transcribe(model,"uploads/Projectvid.wav")

print(transcription['text'])