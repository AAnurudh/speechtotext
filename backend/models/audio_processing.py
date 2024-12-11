import os
import logging
from pydub import AudioSegment
from pydub.utils import make_chunks
from concurrent.futures import ProcessPoolExecutor
from backend.models.whisper_model import load_medium_model, transcribe
from backend.models.marian_translate import MarianTranslate
import gc

logging.basicConfig(level=logging.DEBUG)

AUDIO_CHUNKS_FOLDER = os.path.join(os.path.dirname(__file__), 'audio_chunks')
os.makedirs(AUDIO_CHUNKS_FOLDER, exist_ok=True)

def split_audio(audio_path, chunk_length_ms=30000):  
    audio = AudioSegment.from_file(audio_path)
    chunks = make_chunks(audio, chunk_length_ms)
    chunk_paths = []
    
    for i, chunk in enumerate(chunks):
        if chunk.duration_seconds == 0:
            logging.warning(f"Chunk {i} is empty.")
        chunk_path = os.path.join(AUDIO_CHUNKS_FOLDER, f"{os.path.basename(audio_path)}_chunk_{i}.wav")
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
        #print(f"Exported chunk {i} as {chunk_path}")
        logging.info(f"Exported chunk {i} as {chunk_path} with duration {chunk.duration_seconds} seconds.")

    
    return chunk_paths

def transcribe_chunk(model, chunk_path):
    try:
        result = transcribe(model, chunk_path)
        if isinstance(result, tuple) and len(result) == 2:
            transcription, _ = result
        else:
            transcription = result  # Handle cases where a single value is returned
            
        if not transcription:
            logging.warning(f"Transcription for {chunk_path} returned empty.")

        return transcription
    except Exception as e:
        print(f"Error in transcribe_chunk: {e}")
        return ""

def translate_chunk(transcription):
    if not transcription.strip():
        logging.warning("Empty transcription provided for translation.")
        return ""

    try:
        translator = MarianTranslate(tgt_lang='en')
        translated_text = translator.translate(transcription)
        if not translated_text:
            logging.warning("Translation returned empty.")
        return translated_text
    except Exception as e:
        logging.error(f"Error in translate_chunk: {e}")
        return ""

def split_text_into_chunks(text, max_chars=1000):
    """Splits text into chunks of a specified character length."""
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

def process_audio(file_path, segment_duration=60):
    model = load_medium_model()
    chunk_paths = split_audio(file_path)
    transcriptions = []
    translations = []

    with ProcessPoolExecutor(max_workers=8) as executor:
        transcription_futures = {
            executor.submit(transcribe_chunk, model, chunk_path): chunk_path for chunk_path in chunk_paths
        }
        
        for future in transcription_futures:
            chunk_path = transcription_futures[future]
            try:
                transcription = future.result(timeout=30)
                transcriptions.append(transcription)

                # Check if transcription exceeds max length for translation
                '''if len(transcription) > 1000:
                    transcription_chunks = split_text_into_chunks(transcription)
                    # Translate each text chunk separately
                    translation_chunks = [translate_chunk(chunk) for chunk in transcription_chunks]
                    translations.append(' '.join(translation_chunks))
                else:
                    # Translate directly if it's within manageable length
                    translation_future = executor.submit(translate_chunk, transcription)
                    translations.append(translation_future.result())'''
                
                if transcription:
                    translation_future = executor.submit(translate_chunk, transcription)
                    translations.append(translation_future.result())
                else:
                    translations.append("")

            except Exception as e:
                logging.error(f"Timeout or error processing chunk {chunk_path}: {e}")
                print(f"Error processing chunk {chunk_path}: {e}")
                transcriptions.append("")
                translations.append("")
     # Clean up chunk files
    for chunk_path in chunk_paths:
        try:
            os.remove(chunk_path)
            logging.info(f"Deleted chunk file: {chunk_path}")
        except Exception as e:
            logging.error(f"Error deleting chunk file {chunk_path}: {e}")
        
    del model
    gc.collect()

    return transcriptions, translations



