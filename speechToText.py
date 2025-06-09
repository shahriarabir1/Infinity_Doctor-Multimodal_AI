import logging
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
from groq import Groq

from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def record_audio(audio_file_path,timeout=20,phrase_time_limit=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            # Adjust for ambient noise to improve transcription accuracy
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logging.info("Start speaking...")
            # Listen for audio input
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete. Processing audio...")
            
            #convert and save audio in mp3 format
            wav_data=audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(audio_file_path, format="mp3",bitrate="118k")
            logging.info(f"Audio saved to {audio_file_path}")
            
    except Exception as e:
        logging.error(f"Error saving audio: {e}")

audio_file_path = "patient_voice.mp3"
#save_audio(audio_file_path,timeout=20)

def transcribe_audio(audio_file_path,model):
    audioModel = Groq()
    model=model
    audio=open(audio_file_path, "rb")
    transcription = audioModel.audio.transcriptions.create(
        model=model,
        file=audio,
        language="en",
        response_format="text"
    )
    return transcription.strip()


