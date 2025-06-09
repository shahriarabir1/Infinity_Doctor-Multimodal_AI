from neuron_phase import analyze_image_with_groq
from speechToText import transcribe_audio
from textToSpeech import text_to_speech
import gradio as gr
from dotenv import load_dotenv
import os

load_dotenv()

def reset_session():
    # Delete audio files if they exist
    if os.path.exists("final.mp3"):
        os.remove("final.mp3")
        print("🗑 Deleted: final.mp3")
    if os.path.exists("final.wav"):
        os.remove("final.wav")
        print("🗑 Deleted: final.wav")

    # Clear chat history and text/audio outputs
    return [], "", "", None

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_path, text_input, image_path, history):
    # Prefer text input if provided, else transcribe audio
    if text_input and text_input.strip():
        voice_of_patient = text_input.strip()
    elif audio_path is not None:
        voice_of_patient = transcribe_audio(audio_path, model="whisper-large-v3")
    else:
        return history, "No input detected.", "Please provide voice or text input.", None

    # Format conversation history for the model
    conversation_context = ""
    for patient_msg, doctor_msg in history:
        conversation_context += f"Patient: {patient_msg}\nDoctor: {doctor_msg}\n"
    conversation_context += f"Patient: {voice_of_patient}\n"

    full_query = system_prompt + "\n" + conversation_context

    if image_path:
        doctor_response = analyze_image_with_groq(
            image_path=image_path,
            query=full_query,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "Please provide an image so I can assess your condition."

    voice_of_doctor_path = text_to_speech(text=doctor_response, output_file="final.mp3")

    # Append the new conversation turn
    history.append([voice_of_patient, doctor_response])

    return history, voice_of_patient, doctor_response, voice_of_doctor_path

with gr.Blocks(title="Infinity Doctor Consultation") as iface:
    chatbot = gr.Chatbot(label="🩺 Consultation History")
    audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Describe Your Symptoms (Voice)")
    text_input = gr.Textbox(label="✍️ Type Your Symptoms (Text)", placeholder="Or type here if you don't want to speak")
    image_input = gr.Image(type="filepath", label="🖼 Upload Affected Area")

    transcribed_text = gr.Textbox(label="📄 Transcribed Speech")
    doctor_reply = gr.Textbox(label="🧠 Doctor's Response")
    doctor_audio = gr.Audio(type="filepath", label="🔊 Doctor Voice Response")

    state = gr.State([])

    submit_btn = gr.Button("🔍 Analyze")
    reset_btn = gr.Button("♻️ Reset")

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, text_input, image_input, state],
        outputs=[chatbot, transcribed_text, doctor_reply, doctor_audio]
    )

    reset_btn.click(
        fn=reset_session,
        inputs=[],
        outputs=[chatbot, transcribed_text, doctor_reply, doctor_audio]
    )

iface.launch(debug=True, share=True)
