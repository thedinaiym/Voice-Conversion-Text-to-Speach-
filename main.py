import streamlit as st
import pyttsx3
import tempfile
import os
import librosa
import soundfile as sf
import io
import numpy as np

st.title("Voice Generator and Conversion App")

mode = st.sidebar.selectbox("Select Mode:", options=["Text-to-Speech", "Voice Conversion"])

if mode == "Text-to-Speech":
    st.header("Text-to-Speech using pyttsx3")
    
    engine = pyttsx3.init()

    def get_voices_by_gender(engine, gender):
        """
        Функция для фильтрации голосов по гендеру.
        Проверяет свойство name голосов для определения подходящего варианта.
        """
        voices = engine.getProperty('voices')
        filtered_voices = []
        for voice in voices:
            name_lower = voice.name.lower()
            if gender.lower() == 'female':
                if "zira" in name_lower or "female" in name_lower:
                    filtered_voices.append(voice)
            elif gender.lower() == 'male':
                if "david" in name_lower or "male" in name_lower:
                    filtered_voices.append(voice)
        return filtered_voices

    selected_gender = st.radio("Select voice gender:", options=["Female", "Male"])

    voices = get_voices_by_gender(engine, selected_gender)

    if not voices:
        st.warning("No voices found for the selected gender. Check your system's available voices.")
    else:
        voice_names = [voice.name for voice in voices]
        selected_voice_name = st.selectbox("Select a voice:", voice_names)

        for voice in voices:
            if voice.name == selected_voice_name:
                engine.setProperty('voice', voice.id)
                break

    input_text = st.text_area("Enter text for audio generation:", "Hello, my dog is cute")

    if st.button("Generate Audio (TTS)"):
        if input_text.strip():
            with st.spinner("Generating audio..."):
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
                    output_path = fp.name
                engine.save_to_file(input_text, output_path)
                engine.runAndWait()
                
                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/wav")
                st.success("Audio generated successfully!")
            
                os.remove(output_path)
        else:
            st.warning("Please enter some text for audio generation.")

elif mode == "Voice Conversion":
    st.header("Voice Conversion with Pitch Shifting")
    st.write("Upload your audio file and choose target gender and language to convert the voice.")
    
    uploaded_file = st.file_uploader("Upload your voice recording", type=["wav", "mp3", "ogg"])
    
    target_gender = st.radio("Select target voice gender:", options=["Female", "Male"])
    
    target_language = st.radio("Select target language:", options=["Russian", "English"])
    
    if target_gender == "Male":
        n_steps = -4
    else:
        n_steps = 4

    if st.button("Convert Voice"):
        if uploaded_file is not None:
            with st.spinner("Processing audio..."):
                audio, sr = librosa.load(uploaded_file, sr=None)
                
                audio_shifted = librosa.effects.pitch_shift(y=audio, sr=sr, n_steps=n_steps)
                
                buffer = io.BytesIO()
                sf.write(buffer, audio_shifted, sr, format="WAV")
                buffer.seek(0)
                
                st.audio(buffer.read(), format="audio/wav")
                st.success("Voice conversion completed!")
        else:
            st.warning("Please upload an audio file first.")

if st.button("Clear and Restart"):
    st.experimental_rerun()
