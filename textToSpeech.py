import subprocess
import platform
from gtts import gTTS
from dotenv import load_dotenv
from pydub import AudioSegment


import os

load_dotenv()


def convert_mp3_to_wav(mp3_file, wav_file):
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")

def text_to_speech(text, output_file="output.mp3", lang='en'):

    """
    Convert text to speech and save it as an MP3 file.

    :param text: The text to convert to speech.
    :param output_file: The name of the output MP3 file.
    :param lang: The language for the speech synthesis (default is English).
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        print(f"Audio saved to {output_file}")
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")


    # Play the audio file
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_file])
        elif os_name == "Windows":
            wav_file = output_file.replace(".mp3", ".wav")
            convert_mp3_to_wav(output_file, wav_file)
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_file}").PlaySync();'])

        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_file])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# text_to_speech("Hello, this is a test of the text-to-speech conversion.", "output.mp3", "en")



# def text_to_speech_elevenlabs(text, output_file="output_elevenlabs.mp3", voice_id=None):
#     """
#     Convert text to speech using ElevenLabs and save it as an MP3 file.

#     :param text: The text to convert to speech.
#     :param output_file: The name of the output MP3 file.
#     :param voice_id: The ID of the voice to use (optional).
#     """
#     try:
#         client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

#         audio_stream = client.text_to_speech.convert(
#             text=text,
#             voice_id=voice_id,
#             model_id="eleven-turbo-v2",
#             output_format="mp3_44100_128",
#         )

#         # ✅ Save the streamed audio to file
#         with open(output_file, 'wb') as f:
#             for chunk in audio_stream:
#                 f.write(chunk)

#         print(f"✅ Audio saved to {output_file}")
        
#     except Exception as e:
#         print(f"❌ Error in ElevenLabs text-to-speech conversion: {e}")
    # try:
    #     if os_name == "Darwin":  # macOS
    #         subprocess.run(['afplay', 'output_elevenlabs.mp3'])
    #     elif os_name == "Windows":  # Windows
    #         subprocess.run(['powershell', '-c', '(New-Object Media.SoundPlayer "output_elevenlabs.mp3").PlaySync();'])
    #     elif os_name == "Linux":  # Linux
    #         subprocess.run(['aplay', 'output_elevenlabs.mp3'])  # Alternative: use 'mpg123' or 'ffplay'
    #     else:
    #         raise OSError("Unsupported operating system")
    # except Exception as e:
    #     print(f"An error occurred while trying to play the ElevenLabs audio: {e}")

#text_to_speech_elevenlabs("Hello, this is a test of the ElevenLabs text-to-speech conversion.", "output_elevenlabs.mp3", voice_id="EXAVITQu4vr4xnSDxMaL")
# client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
# voices = client.voices.get_all()
# for voice in voices.voices:
#     print(f"Name: {voice.name}, ID: {voice.voice_id}")