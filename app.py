import streamlit as st
import speech_recognition as sr
from transformers import pipeline
import tempfile
import os

# Load Hugging Face pipeline for sentiment analysis
sentiment_analyzer = pipeline("sentiment-analysis")

# Define abusive keywords (you can expand this)
abusive_keywords = ["abuse", "hate", "stupid", "idiot", "fool"]

def is_abusive(text):
    found = [word for word in abusive_keywords if word in text.lower()]
    return found

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, couldn't understand the audio."
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service."

# Streamlit UI
st.title("🎙️ Real-time Abuse & Sentiment Detector")

# Text Input
st.subheader("📝 Text Message Check")
text_input = st.text_area("Enter your message:")
if st.button("Analyze Text"):
    sentiment = sentiment_analyzer(text_input)[0]
    abuse = is_abusive(text_input)

    st.write(f"**Sentiment:** {sentiment['label']} (score: {sentiment['score']:.2f})")
    if abuse:
        st.error(f"⚠️ Abusive language detected: {', '.join(abuse)}")
    else:
        st.success("✅ No abusive keywords found.")

# Voice Input
st.subheader("🎤 Upload Voice Message")
audio_file = st.file_uploader("Upload .wav audio file", type=["wav"])
if audio_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_path = tmp_file.name

    st.audio(audio_file, format="audio/wav")

    if st.button("Analyze Audio"):
        transcribed = transcribe_audio(tmp_path)
        st.write(f"**Transcribed Text:** {transcribed}")
        sentiment = sentiment_analyzer(transcribed)[0]
        abuse = is_abusive(transcribed)

        st.write(f"**Sentiment:** {sentiment['label']} (score: {sentiment['score']:.2f})")
        if abuse:
            st.error(f"⚠️ Abusive language detected: {', '.join(abuse)}")
        else:
            st.success("✅ No abusive keywords found.")

    # Clean up temp file
    os.remove(tmp_path)
