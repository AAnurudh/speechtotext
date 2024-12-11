import whisper
import logging

logging.basicConfig(filename='transcription_errors.log', level=logging.ERROR)

def load_medium_model():
    model = whisper.load_model("base")  
    return model

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
