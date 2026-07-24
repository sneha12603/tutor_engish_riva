import streamlit as st
import os
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv
import tempfile
import base64

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are Riva, a friendly AI English speaking tutor.
When the user speaks to you:
1. If there are grammar mistakes, politely correct them
2. Explain WHY it was wrong in simple words
3. Give the correct sentence
4. Then respond naturally
5. Keep response short — max 3 to 4 sentences
6. Always be encouraging and positive
7. If English is correct, say "Great English!" and reply naturally
"""

# ── SESSION STATE ────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None
if "last_text" not in st.session_state:
    st.session_state.last_text = None
if "audio_html" not in st.session_state:
    st.session_state.audio_html = None

# ── FUNCTIONS ────────────────────────────────────────────
def get_ai_response(user_text):
    st.session_state.conversation.append({
        "role": "user", "content": user_text
    })
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.conversation,
        max_tokens=200,
        temperature=0.7
    )
    ai_reply = response.choices[0].message.content.strip()
    st.session_state.conversation.append({
        "role": "assistant", "content": ai_reply
    })
    return ai_reply

def transcribe_audio(audio_file):
    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3",
        language="en"
    )
    return transcription.text.strip()

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name

def get_audio_html(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    # ⭐ autoplay=false stops the loop!
    return f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

# ── UI ───────────────────────────────────────────────────
st.set_page_config(page_title="Riva", page_icon="🎙", layout="centered")
st.title("🎙 Riva — AI English Tutor")
st.caption("Speak or type — Riva corrects your grammar and replies!")
st.divider()

# ── CHAT DISPLAY ─────────────────────────────────────────
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["content"])
    else:
        st.chat_message("assistant").write(chat["content"])

# ── PLAY AUDIO ONCE ──────────────────────────────────────
if st.session_state.audio_html:
    st.markdown(st.session_state.audio_html, unsafe_allow_html=True)
    st.session_state.audio_html = None  # ⭐ clear after playing once

st.divider()

# ── VOICE INPUT ──────────────────────────────────────────
st.markdown("### 🎙 Speak to Riva:")
audio = st.audio_input("🔴 Click to record — click again to stop")

if audio:
    audio_bytes = audio.read()

    # ⭐ Only process if NEW audio
    if audio_bytes != st.session_state.last_audio:
        st.session_state.last_audio = audio_bytes

        with st.spinner("🔄 Transcribing your voice..."):
            audio.seek(0)
            user_text = transcribe_audio(audio)

        if user_text:
            st.session_state.chat_history.append({
                "role": "user", "content": f"🎙 {user_text}"
            })

            with st.spinner("🧠 Riva is thinking..."):
                ai_reply = get_ai_response(user_text)

            st.session_state.chat_history.append({
                "role": "assistant", "content": ai_reply
            })

            # Save audio html to session — plays once only
            audio_path = text_to_speech(ai_reply)
            st.session_state.audio_html = get_audio_html(audio_path)
            st.rerun()

st.divider()

# ── TEXT INPUT ───────────────────────────────────────────
st.markdown("### ⌨️ Or type:")
user_input = st.chat_input("Type your message here...")

if user_input:
    # ⭐ Only process if NEW text
    if user_input != st.session_state.last_text:
        st.session_state.last_text = user_input

        st.session_state.chat_history.append({
            "role": "user", "content": user_input
        })

        with st.spinner("🧠 Riva is thinking..."):
            ai_reply = get_ai_response(user_input)

        st.session_state.chat_history.append({
            "role": "assistant", "content": ai_reply
        })

        audio_path = text_to_speech(ai_reply)
        st.session_state.audio_html = get_audio_html(audio_path)
        st.rerun()

# ── CLEAR ────────────────────────────────────────────────
st.divider()
if st.button("🗑 Clear Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.conversation = []
    st.session_state.last_audio = None
    st.session_state.last_text = None
    st.session_state.audio_html = None
    st.rerun()