import whisper

import streamlit as st
from audio_recorder_streamlit import audio_recorder

import tempfile
from pathlib import Path

from ollama_functions import ollama_chat, ollama_generate

# ----- CONFIG -----

st.set_page_config(layout="wide")

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_CHAT_MODEL = "llama3.2"
OLLAMA_EVAL_MODEL = "llama3.2"
TIMEOUT = 600

WHISPER_MODEL_NAME = "base.en"
WHISPER_MODELS_PATH = "whisper/models"

CHAT_PROMPT = {"role": "system", "content": "Engage in a natural and friendly conversation on any topic provided by the user. Respond clearly and conversationally as a human would."}

EVAL_PROMPT = ("You are an English teacher. You will receive text that is a transcription of the user's recorded statements.\n" "Evaluate the user's speaking skills. \n" "Give short evaluation, 1-2 paragraphs, about grammar, vocabulary and give suggestions for improvement.\n\n")

MESSAGES_NUMBER_TO_EVAL = 4

USER_STYLE = "background-color:#DCF8C6; color:#000000; padding:8px; border-radius:8px"
ASSISTANT_STYLE = "background-color:#F1F0F0; color:#000000; padding:8px; border-radius:8px"
EVAL_STYLE = "background-color:#59A4F0; color:#000000; padding:8px; border-radius:8px"

PAUSE_THRESHOLD = 10

# --- END CONFIG ---

def Write_message(msg):
    col_left, col_right = st.columns(2)

    if msg["role"] == "user":
        with col_right:
            st.markdown(f'<div style="{USER_STYLE}">{msg["content"]}</div>', unsafe_allow_html = True)
        # end with
    elif msg["role"] == "assistant":
        with col_left:
            st.markdown(f'<div style="{ASSISTANT_STYLE}">{msg["content"]}</div>', unsafe_allow_html = True)
        # end with
    elif msg["role"] == "eval":
        with col_left:
            st.markdown(f'<div style="{EVAL_STYLE}">{msg["content"]}</div>', unsafe_allow_html = True)
        # end with
    # end if
# end def

if "whisper_model" not in st.session_state:
    st.session_state.whisper_model = whisper.load_model(WHISPER_MODEL_NAME, download_root = WHISPER_MODELS_PATH)
# end if

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [CHAT_PROMPT]
# end if 

if "user_messages" not in st.session_state:
    st.session_state.user_messages = []
# end if 

if "all_messages" not in st.session_state:
    st.session_state.all_messages = []
# end if 

if "last_recording" not in st.session_state:
    st.session_state.last_recording = None
# end if 

history_placeholder = st.container()

audio_button = audio_recorder(
    text = "Start / Stop recording",
    pause_threshold = PAUSE_THRESHOLD,
    sample_rate = 41_000,
    key="main_recorder"
)

if audio_button and (audio_button !=  st.session_state.last_recording):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        wav_path = tmpdir / "recording.wav"

        with open(wav_path, "wb") as file:
            file.write(audio_button)
        # end with

        st.session_state.last_recording = audio_button

        transcript = st.session_state.whisper_model.transcribe(str(wav_path))
        user_text = transcript["text"]

        st.session_state.chat_messages.append({"role": "user", "content": user_text})
        st.session_state.user_messages.append(user_text)
        st.session_state.all_messages.append({"role": "user", "content": user_text})

        with history_placeholder:

            for msg in st.session_state.all_messages:
                Write_message(msg)
            # end for
        # end with 

        print("Ollama chat START")
        assistant_text = ollama_chat(st.session_state.chat_messages, OLLAMA_CHAT_MODEL, OLLAMA_CHAT_URL, TIMEOUT)
        print("Ollama chat STOP")

        st.session_state.chat_messages.append({"role": "assistant", "content": assistant_text})
        st.session_state.all_messages.append({"role": "assistant", "content": assistant_text})

        with history_placeholder:
            Write_message(st.session_state.all_messages[-1])
        # end with 

        if len(st.session_state.user_messages) >= MESSAGES_NUMBER_TO_EVAL:
            user_text = "\n\n".join(st.session_state.user_messages)
            st.session_state.user_messages = []
            
            prompt = EVAL_PROMPT

            prompt = prompt + "User's statements:\n" + user_text
            
            print("Ollama eval START")
            eval_text = ollama_generate(prompt, OLLAMA_EVAL_MODEL, OLLAMA_URL, TIMEOUT)
            print("Ollama eval STOP")

            st.session_state.all_messages.append({"role": "eval", "content": eval_text})

            with history_placeholder:
                Write_message(st.session_state.all_messages[-1])
            # end with 
        # end if

    # end with

# end if

