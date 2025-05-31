# 🛠️ Core Python modules
import os
import uuid
import base64

# 🖼️ UI and Web app
import streamlit as st

# 📄 PDF generation
from fpdf import FPDF

# 🧠 Custom Modules (assuming these are in your modules folder)
from modules.settings_manager import SettingsManager
from modules.voice_assistant import VoiceAssistant
from modules.audio_bar import CustomAudioPlayer
from modules.history_manager import HistoryManager
from modules import explainer

class CodiApp:
    def __init__(self):
        self.HF_TOKEN = os.getenv("HF_TOKEN_1")
        self.tabs = None
        self.uploaded_code = None
        self.uploaded_file = None
        self.question = None

        # Instantiate class objects
        self.settings_mgr = SettingsManager()
        self.voice_mgr = VoiceAssistant()
        self.history_mgr = HistoryManager()

        self.init_session_state()
        self.setup_page()

    def setup_page(self):
        st.set_page_config(page_title="project_Codi", layout="wide")
        st.markdown("<h1 style='text-align: center;'>👩‍💻 Codi</h1>", unsafe_allow_html=True)
        self.tabs = st.tabs(["📘 file upload", "🕘 History"])

    def init_session_state(self):
        if "settings_loaded" not in st.session_state:
            settings = self.settings_mgr.load_settings()
            for key, value in settings.items():
                st.session_state[key] = value
            st.session_state.settings_loaded = True

        st.session_state.setdefault("upload_history", self.history_mgr.load_upload_history())
        st.session_state.setdefault("explanation_history", self.history_mgr.load_explanation_history())
        st.session_state.setdefault("chat_history", self.history_mgr.load_chat_history())

    def sidebar(self):
        st.sidebar.header("⚙️ Settings")

        # Voice Assistant Toggle
        va_toggle = st.sidebar.toggle("🎙️ Enable Voice Assistant", st.session_state.voice_assistant)
        if va_toggle != st.session_state.voice_assistant:
            st.session_state.voice_assistant = va_toggle

        # Voice gender
        st.session_state.voice_gender = st.sidebar.selectbox(
            "Assistant Voice Gender", ["Neutral", "Female", "Male"],
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

        if st.sidebar.button("💾 Save Settings"):
            self.settings_mgr.save_settings({
                "voice_assistant": st.session_state.voice_assistant,
                "voice_activation": st.session_state.voice_activation,
                "voice_gender": st.session_state.voice_gender,
                "explanation_style": st.session_state.explanation_style,
            })
            st.sidebar.success("Settings saved!")

    def display_explanation_block(self, explanation):
        with st.expander("📘 View Explanation", expanded=True):
            st.text_area("Explanation", explanation, height=200, disabled=True, label_visibility="collapsed")
            b64 = base64.b64encode(explanation.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="explanation.txt">📄 Download as .txt</a>'
            st.markdown(href, unsafe_allow_html=True)

    def tab_upload(self):
        with self.tabs[0]:
            st.header("Upload Your File")
            left, _, right = st.columns([2, 0.5, 2])
            with left:
                self.uploaded_file = st.file_uploader("Upload a python file", type="py")
                if self.uploaded_file:
                    self.uploaded_code = self.uploaded_file.read().decode("utf-8")
                    st.code(self.uploaded_code, language="python", height=415)
                    self._update_upload_history()

            with right:
                if self.uploaded_file and self.uploaded_code:
                    self._generate_and_display_explanation()


            self._chat_ui()

    def _update_upload_history(self):
        filename = self.uploaded_file.name
        if not st.session_state.get("uploaded_file_saved") or st.session_state.get("last_uploaded_filename") != filename:
            st.session_state.upload_history.insert(0, {
                "filename": filename,
                "content": self.uploaded_code,
            })
            self.history_mgr.save_upload_history(st.session_state.upload_history)
            st.session_state.uploaded_file_saved = True
            st.session_state.last_uploaded_filename = filename

    def _generate_and_display_explanation(self):
        explanation = explainer.CodeExplainer.explain_code(self.uploaded_code, self.HF_TOKEN, st.session_state.explanation_style)
        self.display_explanation_block(explanation)

        file_id = str(uuid.uuid4())
        filename = self.uploaded_file.name

        # PDF
        pdf_path = f"./modules/data/expl_{file_id}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in explanation.split("\n"):
            pdf.multi_cell(0, 10, line)
        pdf.output(pdf_path)

        self.display_explanation_block(explanation)

        # MP3
        # engine = self.voice_mgr.set_voice_by_gender(st.session_state.voice_gender)
        self.voice_mgr.set_voice_by_gender(st.session_state.voice_gender)
        audio_path = f"./modules/data/audio/{file_id}.mp3"
        self.voice_mgr.save_audio(explanation,audio_path)

        # Save explanation history
        if not st.session_state.get("explanation_saved") or st.session_state.get("last_explained_filename") != filename:
            st.session_state.explanation_history.insert(0, {
                "filename": filename,
                "explanation": explanation,
                "pdf_path": pdf_path,
                "audio_path": audio_path
            })
            self.history_mgr.save_explanation_history(st.session_state.explanation_history)
            st.session_state.explanation_saved = True
            st.session_state.last_explained_filename = filename

        if st.session_state.voice_assistant:
            CustomAudioPlayer(audio_path)

    def _chat_ui(self):
        question = st.chat_input("Ask a question about your code")
        if question:
            answer = explainer.CodeExplainer.answer_question(question, st.session_state.explanation_style, self.HF_TOKEN, self.uploaded_code)
            with st.chat_message("user"):
                st.markdown(question)
            with st.chat_message("assistant"):
                st.markdown(answer)

            st.session_state.chat_history.append({"question": question, "answer": answer})
            self.history_mgr.save_chat_history(st.session_state.chat_history)

    def tab_history(self):
        with self.tabs[1]:
            st.header("History")
            view = st.selectbox("View Your History", ["Uploads", "Explanation", "Chat"])
            if view == "Uploads":
                self.history_mgr.render_upload_history()
            elif view == "Explanation":
                self.history_mgr.render_explanation_history()
            elif view == "Chat":
                self.history_mgr.render_chat_history()

    def run(self):
        self.sidebar()
        self.tab_upload()
        self.tab_history()


app = CodiApp()
app.run()