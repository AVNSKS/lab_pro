#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from gtts import gTTS
import pygame
import time
import os

# Initialize pygame mixer (for playing sound)
pygame.mixer.init()

# Supported languages for gTTS
LANGUAGES = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Spanish (Español)": "es",
    "French (Français)": "fr",
    "German (Deutsch)": "de",
    "Italian (Italiano)": "it",
    "Chinese (中文)": "zh-CN",
    "Japanese (日本語)": "ja",
    "Russian (Русский)": "ru",
    "Arabic (العربية)": "ar",
    "Portuguese (Português)": "pt",
    "Korean (한국어)": "ko",
    "Bengali (বাংলা)": "bn",
    "Urdu (اردو)": "ur",
}

# Function to play audio
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Function to convert text to speech
def convert_text_to_speech(text, language, voice, speed):
    if not text.strip():
        st.error("❌ Please enter some text or upload a file.")
        return None

    # Set the appropriate voice (affects only English variants)
    if voice == "Male" and language == "en":
        tld = "co.uk"  # British English (Male)
    elif voice == "Robotic" and language == "en":
        tld = "com.au"  # Australian English (Robotic)
    else:
        tld = "com"  # Default (Female or other languages)

    slow = True if speed == "Slow" else False

    # Generate speech
    tts = gTTS(text=text, lang=language, tld=tld, slow=slow)

    output_file = "output.mp3"
    tts.save(output_file)

    return output_file

# Streamlit App
st.title("🎤 Multi-Language Text-to-Speech Converter")

# Input Section
text = st.text_area("Enter your text below:")
uploaded_file = st.file_uploader("Or upload a text file (.txt)", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    st.text_area("File content:", text, height=150)

# Language Selection
language_option = st.selectbox("🌐 Select Language:", list(LANGUAGES.keys()))
language_code = LANGUAGES[language_option]

# Voice and Speed Options (Only affects English)
voice_option = st.selectbox("🔊 Select Voice (English only):", ["Female (Default)", "Male", "Robotic"])
speed_option = st.selectbox("⚡ Select Speed:", ["Normal", "Slow"])

# Convert Button
if st.button("🔊 Convert and Play"):
    output_file = convert_text_to_speech(text, language_code, voice_option, speed_option)

    if output_file:
        st.success("✅ Conversion successful! You can play or download the speech below.")
        
        # Play audio
        st.audio(output_file, format="audio/mp3")

        # Download Button
        with open(output_file, "rb") as f:
            st.download_button("⬇️ Download Speech", f, file_name="speech.mp3", mime="audio/mp3")

# Cleanup (optional)
if os.path.exists("output.mp3"):
    os.remove("output.mp3")

