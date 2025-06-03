"""
Codi: An Interactive Python Code Explainer with Voice Assistant and History Tracking

This Streamlit application allows users to upload Python files and 
receive natural language explanations
generated using Hugging Face language models. It includes support for:
- Uploading and previewing `.py` files
- Generating explanations in different styles (Concise, In-depth, Reiterate)
- Text-to-speech output with gendered voice selection and audio playback
- Persisting and managing upload, explanation, and chat histories
- Downloading explanations and chats as PDF and MP3 files

Modules:
- CodeExplainer: Handles interaction with LLMs
- VoiceAssistant: Converts text to speech and saves audio
- CustomAudioPlayer: Renders an audio UI in Streamlit
- HistoryManager: Manages persistent storage of user history
- SettingsManager: Handles app settings and state

Requirements:
- Hugging Face token (via `.env` file)
- Streamlit, FPDF, pyttsx3, python-dotenv, etc.

Usage:
Run this script with `streamlit run` to launch the web interface.
"""


import base64
import uuid
import os
import streamlit as st
from fpdf import FPDF
from dotenv import load_dotenv
from modules.audio_bar import CustomAudioPlayer
from modules.settings_manager import SettingsManager
from modules.voice_assistant import VoiceAssistant
from modules.explainer import CodeExplainer
from modules.history_manager import HistoryManager

# Load environment variables from custom file
load_dotenv("codi.env")

# --------------------- App Initialization --------------------- #
HF_TOKEN = os.getenv("HF_TOKEN")
settings_mgr = SettingsManager()
voice_mgr = VoiceAssistant()
explainer = CodeExplainer(HF_TOKEN)
history_mgr = HistoryManager()

# --------------------- Page Config --------------------- #
st.set_page_config(page_title="project_Codi", layout="wide")
st.markdown("<h1 style='text-align: center;'>👩‍💻 Codi</h1>", unsafe_allow_html=True)
tabs = st.tabs(["📘 File upload", "🕘 History"])

# --------------------- Session State Initialization --------------------- #
if "settings_loaded" not in st.session_state:
    loaded_settings = settings_mgr.load_settings()
    if loaded_settings:
        for key, value in loaded_settings.items():
            st.session_state[key] = value
        st.session_state.settings_loaded = True

if "upload_history" not in st.session_state:
    st.session_state.upload_history = history_mgr.load_upload_history()

if "explanation_history" not in st.session_state:
    st.session_state.explanation_history = history_mgr.load_explanation_history()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = history_mgr.load_chat_history()

# --------------------- Sidebar: Settings UI --------------------- #
st.sidebar.header("⚙️ Settings")

# Voice Assistant Toggle
va_toggle = st.sidebar.toggle("🎙️ Enable Voice Assistant", st.session_state.voice_assistant)
if va_toggle != st.session_state.voice_assistant:
    st.session_state.voice_assistant = va_toggle

# Gender selection for TTS voice
st.session_state.voice_gender = st.sidebar.selectbox(
    "Assistant Voice Gender", 
    ["Neutral", "Female", "Male"],
    index=["Neutral", "Female", "Male"].index(st.session_state.voice_gender)
)

# Explanation style
st.sidebar.header("📖 Explanation Style")
if st.sidebar.button("Reiterate"):
    st.session_state.explanation_style = "Reiterate"
if st.sidebar.button("Concise"):
    st.session_state.explanation_style = "concise"
if st.sidebar.button("In-Depth"):
    st.session_state.explanation_style = "in-depth"
st.sidebar.write(f"Current Style: {st.session_state.explanation_style.capitalize()}")

# Save button to persist settings
if st.sidebar.button("💾 Save Settings"):
    settings_to_save = {
        "voice_assistant": st.session_state.voice_assistant,
        "voice_activation": st.session_state.voice_activation,
        "voice_gender": st.session_state.voice_gender,
        "explanation_style": st.session_state.explanation_style,
    }
    settings_mgr.save_settings(settings_to_save)
    st.sidebar.success("Settings saved!")

# --------------------- Helper Functions --------------------- #
def display_explanation(explanation_txt: str) -> None:
    """
    Display a collapsible explanation text area and download link.

    Parameters
    ----------
    explanation_txt : str
        The explanation text to display and make downloadable.
    """
    with st.expander("📘 View Explanation", expanded=True):
        st.text_area("Explanation",
                     explanation_txt, height=200,
                     disabled=True,
                     label_visibility="collapsed")
        b64 = base64.b64encode(explanation_txt.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="explanation.txt">📄 Download as .txt</a>'
        st.markdown(href, unsafe_allow_html=True)

# --------------------- Main Tab: File Upload & Explanation --------------------- #
with tabs[0]:
    # uploaded_code = None=
    st.header("Upload Your File")
    left_col, mid_col, right_col = st.columns([2, 0.5, 2])

    with left_col:
        uploaded_file = st.file_uploader(label="Upload a python file", type="py")
        has_uploaded = uploaded_file is not None

        if has_uploaded:
            uploaded_code = uploaded_file.read().decode("utf-8")
            st.code(uploaded_code, language="python", height=415)

            # Prevent re-saving on rerun
            if not st.session_state.get("uploaded_file_saved") or st.session_state.get("last_uploaded_filename") != uploaded_file.name:
                new_entry = {
                    "filename": uploaded_file.name,
                    "content": uploaded_code,
                }
                st.session_state.upload_history.insert(0, new_entry)
                history_mgr.save_upload_history(st.session_state.upload_history)
                st.session_state.uploaded_file_saved = True
                st.session_state.last_uploaded_filename = uploaded_file.name
        else:
            st.session_state.uploaded_file_saved = False
            st.session_state.last_uploaded_filename = None

    with right_col:
        if has_uploaded:
            explanation = explainer.explain_code(uploaded_code, st.session_state.explanation_style)
            display_explanation(explanation)
            file_id = str(uuid.uuid4())

            # PDF generation
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_font("DejaVu", "", "./modules/data/fonts/DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", size=12)
            for line in explanation.split('\n'):
                pdf.multi_cell(0, 10, txt=line)

            pdf_path = f"./modules/data/expl_{file_id}.pdf"
            pdf.output(pdf_path)

            # Audio generation
            engine = voice_mgr.set_voice_by_gender(st.session_state.voice_gender)
            audio_path = f"./modules/data/audio/{file_id}.mp3"
            voice_mgr.save_audio(explanation, audio_path)

            # Save explanation history
            if not st.session_state.get("explanation_saved") or st.session_state.get("last_explained_filename") != uploaded_file.name:
                explanation_entry = {
                    "filename": uploaded_file.name,
                    "explanation": explanation,
                    "pdf_path": pdf_path,
                    "audio_path": audio_path
                }
                st.session_state.explanation_history.insert(0, explanation_entry)
                history_mgr.save_explanation_history(st.session_state.explanation_history)
                st.session_state.explanation_saved = True
                st.session_state.last_explained_filename = uploaded_file.name

            # Render audio player if VA is on
            if st.session_state.voice_assistant:
                engine = voice_mgr.set_voice_by_gender(st.session_state.voice_gender)
                audio_path = voice_mgr.save_audio(explanation, f"./modules/data/audio/{file_id}.mp3")
                audio_bar = CustomAudioPlayer(audio_path)
                audio_bar.render()
        else:
            st.subheader("Explanation")
            st.info("Upload a file to see the explanation here.")
            st.session_state.explanation_saved = False
            st.session_state.last_explained_filename = None

    # --------------------- Chat with Assistant --------------------- #
    question = st.chat_input("Ask a question about your code")

    if question:
        answer = explainer.answer_question(question, st.session_state.explanation_style, uploaded_code)

        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Save chat history
        st.session_state.chat_history.insert(0, {"question": question, "answer": answer})
        history_mgr.save_chat_history(st.session_state.chat_history)

# --------------------- History Tab --------------------- #
with tabs[1]:
    st.header("History")
    history_tabs = st.selectbox("View Your History", ["Uploads", "Explanation", "Chat"])

    # Upload History
    if history_tabs == "Uploads":
        st.header("📜 Upload History")
        if st.button("🗑️ Clear History"):
            st.session_state.upload_history.clear()
            history_mgr.clear_upload_history()
            st.success("Upload history cleared.")

        for idx, entry in enumerate(st.session_state.upload_history):
            with st.expander(f"{entry['filename']}"):
                st.code(entry["content"], language="python", height=300)
                b64_py = base64.b64encode(entry["content"].encode()).decode()
                py_href = f'<a href="data:file/python;base64,{b64_py}" download="{entry["filename"]}">🐍 Download as .py</a>'
                st.markdown(py_href, unsafe_allow_html=True)

    # Explanation History
    elif history_tabs == "Explanation":
        st.header("🧠 Explanation History")
        if st.button("🗑️ Clear Explanation History"):
            st.session_state.explanation_history.clear()
            history_mgr.clear_explanation_history()
            st.success("Explanation history cleared.")

        for idx, entry in enumerate(st.session_state.explanation_history):
            with st.expander(f"{entry['filename']}"):
                st.text_area("Explanation History", entry["explanation"], height=200, disabled=True, label_visibility="collapsed", key=f"explanation_{idx}")
                
                # PDF download
                if entry.get("pdf_path") and os.path.exists(entry["pdf_path"]):
                    with open(entry["pdf_path"], "rb") as pdf_file:
                        b64_pdf = base64.b64encode(pdf_file.read()).decode()
                        href_pdf = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{entry["filename"]}_explanation.pdf">📄 Download as PDF</a>'
                        st.markdown(href_pdf, unsafe_allow_html=True)

                # Audio download
                if entry.get("audio_path") and os.path.exists(entry["audio_path"]):
                    with open(entry["audio_path"], "rb") as audio_file:
                        b64_mp3 = base64.b64encode(audio_file.read()).decode()
                        href_mp3 = f'<a href="data:audio/mp3;base64,{b64_mp3}" download="{entry["filename"]}_explanation.mp3">🔊 Download MP3</a>'
                        st.markdown(href_mp3, unsafe_allow_html=True)

    # Chat History
    elif history_tabs == "Chat":
        st.header("💬 Chat History")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history.clear()
            if hasattr(history_mgr, "clear_chat_history"):
                history_mgr.clear_chat_history()
            st.success("Chat history cleared.")

        for idx, entry in enumerate(st.session_state.chat_history):
            question = entry.get("question", "")
            answer = entry.get("answer", "")
            with st.expander(f"🗨️ Q{len(st.session_state.chat_history)-(idx)}: {question[:60]}..."):
                st.markdown(f"**Question:**\n{question}")
                st.markdown(f"**Answer:**\n{answer}")

                # PDF download of chat
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_font("DejaVu", "", "./modules/data/fonts/DejaVuSans.ttf", uni=True)
                pdf.set_font("DejaVu", size=12)
                pdf.multi_cell(0, 10, txt=f"Q: {question}\n\nA: {answer}")

                chat_file_id = str(uuid.uuid4())
                pdf_path = f"./modules/data/chat_{chat_file_id}.pdf"
                pdf.output(pdf_path)

                with open(pdf_path, "rb") as chat_pdf:
                    b64_pdf = base64.b64encode(chat_pdf.read()).decode()
                    href_pdf = f'<a href="data:application/pdf;base64,{b64_pdf}" download="chat_{chat_file_id}.pdf">📄 Download Chat PDF</a>'
                    st.markdown(href_pdf, unsafe_allow_html=True)
