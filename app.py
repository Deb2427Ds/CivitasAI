import streamlit as st
import speech_recognition as sr
from plyer import notification
import tempfile
import os

# Define abusive keywords
abusive_keywords = [
    "idiot", "stupid", "dumb", "moron", "loser", "freak", "jerk", "creep", "psycho",
    "pathetic", "clown", "fool", "trash", "worthless", "useless", "nonsense", "dirtbag",
    "fuck", "shit", "bitch", "asshole", "dick", "bastard", "slut", "whore", "cunt",
    "prick", "piss", "damn", "hell", "fucked", "fucker", "bullshit", "motherfucker",
    "racist", "nazi", "terrorist", "bigot", "homophobe", "xenophobe", "pervert", "rapist",
    "pedo", "pedophile", "retard", "faggot", "tranny", "chink", "spic", "nigger", "kike", "dyke",
    "kill you", "go die", "beat you", "burn you", "i'll hurt you", "stab you", "shoot you",
    "break your", "punch you", "rip you", "i'll destroy you", "you're dead", "cut you",
    "slap", "kick", "punch", "hit", "smack", "choke", "strangle", "throw", "bite", "scratch",
    "push", "shove", "whip", "break", "cut", "stab", "burn", "bleed", "drag", "pin down",
    "nobody likes you", "you're worthless", "go away", "you're a mistake", "you're fat",
    "ugly", "disgusting", "cringe", "you should die", "why don't you die", "drown yourself",
    "end your life", "nobody cares", "shut up", "no one asked", "get lost", "stay away",
    "kys", "die pls", "fatass", "lard", "airhead", "sissy", "maniac", "crazy", "nutcase",
    "weirdo", "wannabe", "doormat", "bootlicker", "simp", "twat", "hoe", "dumbfuck"
]

# Abuse check function
def is_abusive(text):
    found = [word for word in abusive_keywords if word in text.lower()]
    return found

# Audio transcription function
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, couldn't understand the audio."
    except sr.RequestError:
        return "Could not connect to Google Speech Recognition service."

# System notification function
def send_abuse_alert():
    notification.notify(
        title='⚠ Abuse Detected!',
        message='Abusive language or threat identified.',
        app_name='Live Abuse Detection App',
        timeout=5
    )

# Streamlit UI
st.title("🛡️ Real-Time Abuse Detection")

# Text input section
st.subheader("📝 Text Input")
text_input = st.text_area("Enter your message:")
if st.button("Check Text"):
    abuse = is_abusive(text_input)
    if abuse:
        st.error(f"⚠️ Abusive content detected: {', '.join(abuse)}")
        send_abuse_alert()
    else:
        st.success("✅ No abusive keywords detected.")

# Audio input section
st.subheader("🎤 Upload Voice (.wav)")
audio_file = st.file_uploader("Choose a .wav audio file", type=["wav"])
if audio_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_path = tmp_file.name

    st.audio(audio_file, format="audio/wav")

    if st.button("Analyze Audio"):
        transcribed = transcribe_audio(tmp_path)
        st.write(f"**Transcribed Text:** {transcribed}")
        abuse = is_abusive(transcribed)
        if abuse:
            st.error(f"⚠️ Abusive content detected: {', '.join(abuse)}")
            send_abuse_alert()
        else:
            st.success("✅ No abusive keywords detected.")

        os.remove(tmp_path)
