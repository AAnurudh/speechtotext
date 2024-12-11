from googletrans import Translator
import json

def translate_text(transcription, target_language='en'):
    translator = Translator()
    try:
        result = translator.translate(transcription, dest=target_language)
        return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        return "Translation failed due to API error."
