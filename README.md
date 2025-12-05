# 🧾 English Speaking Practice AI Chat

A Python + Streamlit app for practising English speaking with an AI by recording your voice. The app transcribes your speech with Whisper, chats with you in English, and every few of your responses a separate LLM evaluates your speaking skills.

## 🚀 Features
- Streamlit-based web UI (https://streamlit.io)
- Record your voice and transcribe it with Whisper (https://github.com/openai/whisper)
- Chat with locally installed LLM via Ollama (https://github.com/ollama/ollama)
- Every few of your responses a separate Ollama LLM evaluates your speaking skills
- Easily configurable choice of Whisper and Ollama models used by the app

## ⚙️ Requirements
- Python 3.11+
- Ollama installed and running locally
- Whisper installed together with its system dependencies (e.g. ffmpeg)
- installed libraries from requirements.txt 

## 🧰 Usage
### Installing
git clone https://github.com/S2ym0d/EnglishSpeakingPracticeAIChat.git

cd EnglishSpeakingPracticeAIChat

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

### Running the app
streamlit run app.py
