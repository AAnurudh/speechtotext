from transformers import MarianMTModel, MarianTokenizer

class MarianTranslate:
    def __init__(self, tgt_lang="en"):
        self.tgt_lang = tgt_lang
        self.model_name = 'Helsinki-NLP/opus-mt-mul-en'
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    def translate(self, text):
        if not text:
            return ""
        
        # Log the source and target languages
        #print(f"Translating to {self.tgt_lang}: {text}")
        
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = self.model.generate(**inputs)
        return self.tokenizer.decode(translated[0], skip_special_tokens=True)

# Example translation call
def translate_text(transcription, tgt_lang="en"):
    translator = MarianTranslate(tgt_lang=tgt_lang)
    try:
        return translator.translate(transcription)
    except Exception as e:
        print(f'Translation failed: {str(e)}')
        return "Translation failed due to an error."
