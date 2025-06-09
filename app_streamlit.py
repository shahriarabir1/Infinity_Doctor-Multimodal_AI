import os
import streamlit as st
from dotenv import load_dotenv
from neuron_phase import analyze_image_with_groq
from speechToText import transcribe_audio
from textToSpeech import text_to_speech
from tempfile import NamedTemporaryFile

load_dotenv()

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Title and Instructions
st.set_page_config(page_title="Infinity Doctor Consultation", layout="centered")
st.title("🩺 Infinity Doctor Consultation")
st.caption("Describe your symptoms, upload an image, and consult the virtual doctor.")

# Inputs
text_input = st.text_input("✍️ Type Your Symptoms (Text)", placeholder="Or type here if you don't want to speak")
audio_input = st.file_uploader("🎤 Or Upload Voice File (WAV/MP3)", type=["wav", "mp3"])
image_input = st.file_uploader("🖼 Upload Image of Affected Area", type=["jpg", "jpeg", "png"])

# Actions
if st.button("🔍 Analyze"):

    # Transcribe if no text input
    if text_input.strip():
        patient_input = text_input.strip()
    elif audio_input:
        with NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_input.name)[-1]) as tmp_audio:
            tmp_audio.write(audio_input.read())
            patient_input = transcribe_audio(tmp_audio.name, model="whisper-large-v3")
            os.unlink(tmp_audio.name)
    else:
        st.warning("Please provide either text or voice input.")
        st.stop()

    # Build full conversation context
    conversation_context = ""
    for patient_msg, doctor_msg in st.session_state.chat_history:
        conversation_context += f"Patient: {patient_msg}\nDoctor: {doctor_msg}\n"
    conversation_context += f"Patient: {patient_input}\n"
    full_query = system_prompt + "\n" + conversation_context

    if image_input:
        with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
            tmp_img.write(image_input.read())
            doctor_response = analyze_image_with_groq(
                image_path=tmp_img.name,
                query=full_query,
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
            os.unlink(tmp_img.name)
    else:
        doctor_response = "Please provide an image so I can assess your condition."

    # Text-to-Speech
    audio_response_path = text_to_speech(text=doctor_response, output_file="final.mp3")

    # Update chat history
    st.session_state.chat_history.append((patient_input, doctor_response))

    # Display conversation
    st.subheader("📜 Consultation History")
    for patient, doctor in st.session_state.chat_history:
        st.markdown(f"**🧑‍⚕️ You:** {patient}")
        st.markdown(f"**👨‍⚕️ Doctor:** {doctor}")

    st.subheader("📄 Doctor's Voice Response")
    st.audio(audio_response_path, format="audio/mp3")

# Reset
if st.button("♻️ Reset Session"):
    st.session_state.chat_history = []
    if os.path.exists("final.mp3"):
        os.remove("final.mp3")
    if os.path.exists("final.wav"):
        os.remove("final.wav")
    st.success("Session reset and audio files cleaned.")
