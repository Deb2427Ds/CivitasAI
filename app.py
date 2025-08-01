import streamlit as st
import speech_recognition as sr
from plyer import notification
from moviepy.editor import VideoFileClip
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

def is_abusive(text):
    found = [word for word in abusive_keywords if word in text.lower()]
    return found

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, couldn't understand the audio."
    except sr.RequestError:
        return "Could not connect to Google Speech Recognition service."

def send_abuse_alert():
    st.toast("⚠️ Abusive content detected!")

st.title("🛡️ Real-Time Abuse Detection")

# Text input
st.subheader("📝 Text Input")
text_input = st.text_area("Enter your message:")
if st.button("Check Text"):
    abuse = is_abusive(text_input)
    if abuse:
        st.error(f"⚠️ Abusive content detected: {', '.join(abuse)}")
        send_abuse_alert()
    else:
        st.success("✅ No abusive keywords detected.")

# Audio or video upload
st.subheader("🎥 Upload Audio/Video (.wav or .mp4)")
uploaded_file = st.file_uploader("Choose a file", type=["wav", "mp4"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        input_path = tmp.name

    if uploaded_file.name.endswith(".mp4"):
        st.video(uploaded_file)
        st.info("Extracting audio from video...")
        audio_path = input_path.replace(".mp4", ".wav")
        video_clip = VideoFileClip(input_path)
        video_clip.audio.write_audiofile(audio_path, codec='pcm_s16le')  # Save as WAV
        video_clip.close()
    else:
        st.audio(uploaded_file)
        audio_path = input_path

    if st.button("Analyze"):
        st.write("Transcribing...")
        transcribed = transcribe_audio(audio_path)
        st.write(f"**Transcribed Text:** {transcribed}")
        abuse = is_abusive(transcribed)
        if abuse:
            st.error(f"⚠️ Abusive content detected: {', '.join(abuse)}")
            send_abuse_alert()
        else:
            st.success("✅ No abusive keywords detected.")

        os.remove(input_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
