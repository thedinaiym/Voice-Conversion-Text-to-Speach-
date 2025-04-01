import streamlit as st
import pyttsx3
import tempfile
import os

def get_voices_by_gender(engine, gender):

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

st.title("Voice Generator")

engine = pyttsx3.init()

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

if st.button("Generate Audio"):
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

if st.button("Clear and Restart"):
    st.experimental_rerun()
