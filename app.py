import streamlit as st
import base64
import uuid
import os
from fpdf import FPDF
from dotenv import load_dotenv
from modules.audio_bar import display_audio_bar

from modules import settings_manager, voice_assistant, explainer,history_manager


load_dotenv("codi.env")  # specify the custom filename

HF_TOKEN = os.getenv("HF_TOKEN")

# --------------------- Page Config --------------------- #
st.set_page_config(page_title="project_Codi", layout="wide")
# st.title("👩‍💻 Codi")
st.markdown("<h1 style='text-align: center;'>👩‍💻 Codi</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📘 file upload", "💬 Chat", "🕘 History"])

audio_file_url = "./modules/data/audio/test.mp3"

# --------------------- Initialize Settings --------------------- #
if "settings_loaded" not in st.session_state:
    loaded_settings = settings_manager.load_settings()
    if loaded_settings:
        for key, value in loaded_settings.items():
            st.session_state[key] = value
        st.session_state.settings_loaded = True

# Save upload to history if not already present
if "upload_history" not in st.session_state:
    st.session_state.upload_history = history_manager.load_history()
# save explanation history
if "explanation_history" not in st.session_state:
    st.session_state.explanation_history = history_manager.load_explanation_history()

# --------------------- Sidebar --------------------- #
st.sidebar.header("⚙️ Settings")

# Toggles with tracked updates
va_toggle = st.sidebar.toggle("🎙️ Enable Voice Assistant", st.session_state.voice_assistant)
if va_toggle != st.session_state.voice_assistant:
    st.session_state.voice_assistant = va_toggle

va_activation_toggle = st.sidebar.toggle("🧠 Voice Activation (e.g., 'Hey Codi')", value=st.session_state.get("voice_activation", False))
if va_activation_toggle != st.session_state.get("voice_activation", False):
    st.session_state.voice_activation = va_activation_toggle


st.session_state.voice_gender = st.sidebar.selectbox("Assistant Voice Gender", ["Neutral", "Female", "Male"], index=["Neutral", "Female", "Male"].index(st.session_state.voice_gender))
# ide_enabled = st.sidebar.checkbox("Enable IDE Integration", value=False)

# Explanation style buttons
st.sidebar.header("📖 Explanation Style")
if st.sidebar.button("Reiterate"):
    st.session_state.explanation_style = "Reiterate"
if st.sidebar.button("Concise"):
    st.session_state.explanation_style = "concise"
if st.sidebar.button("In-Depth"):
    st.session_state.explanation_style = "in-depth"
st.sidebar.write(f"Current Style: {st.session_state.explanation_style.capitalize()}")

# Save button
if st.sidebar.button("💾 Save Settings"):
    settings_to_save = {
        "voice_assistant": st.session_state.voice_assistant,
        "voice_activation": st.session_state.voice_activation,
        "voice_gender": st.session_state.voice_gender,
        "explanation_style": st.session_state.explanation_style,
    }
    settings_manager.save_settings(settings_to_save)
    st.sidebar.success("Settings saved!")

# --------------------- Explanation UI --------------------- #
# Collapsible explanation display
def display_explanation(explanation_txt):
    with st.expander("📘 View Explanation", expanded=True):
        st.text_area("Explanation", explanation_txt, height=200, disabled=True, label_visibility="collapsed")
        b64 = base64.b64encode(explanation_txt.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="explanation.txt">📄 Download as .txt</a>'
        st.markdown(href, unsafe_allow_html=True)

# --------------------- Main Tabs --------------------- #
with tabs[0]:
    st.header("Upload Your File")
    left_col, mid_col, right_col = st.columns([2, 0.5, 2])

    with left_col:
        uploaded_file = st.file_uploader(label="Upload a python file", type="py")
        has_uploaded = uploaded_file is not None
        if has_uploaded:
            uploaded_code = uploaded_file.read().decode("utf-8")
            st.code(uploaded_code, language="python", height=415)
            new_entry = {
                "filename": uploaded_file.name,
                "content": uploaded_code,
            }
            st.session_state.upload_history.insert(0, new_entry)
            history_manager.save_history(st.session_state.upload_history)
    with right_col:
        if has_uploaded:
            # pass
            explanation = explainer.query_huggingface(uploaded_code,HF_TOKEN)
            display_explanation(explanation)
            explanation_entry = {
                "filename": uploaded_file.name,
                "explanation": explanation
            }
            st.session_state.explanation_history.insert(0, explanation_entry)
            history_manager.save_explanation_history(st.session_state.explanation_history)
            if st.session_state.voice_assistant:
                engine = voice_assistant.get_voice_by_gender(st.session_state.voice_gender)
                audio_path = voice_assistant.save_audio(explanation,engine)
                display_audio_bar(audio_file_url)
                
        else:
            st.subheader("Explanation")
            st.info("Upload a file to see the explanation here.")

    st.subheader("Have a question?")
    st.text_area(label="Enter your question here", height=100)

with tabs[1]:
    st.header("💬 Chat with Codi")
    st.info("this feature is coming soon")

with tabs[2]:
    st.header("History")
    history_tabs = st.selectbox("View Your History", ["Uploads","Explanation","Chat"])
    if history_tabs == "Uploads":
        st.header("📜 Upload History")

        if "upload_history" not in st.session_state:
            st.session_state.upload_history = []


        if st.session_state.upload_history:
            # Clear history button
            if st.button("🗑️ Clear History"):
                st.session_state.upload_history.clear()
                history_manager.clear_history()
                st.success("Upload history cleared.")
            for idx, entry in enumerate(st.session_state.upload_history):
                filename = entry["filename"]
                code = entry["content"]

                with st.expander(f"{filename}"):
                    st.code(code, language="python", height=300)

                    # Generate a PDF
                    # .py download link
                    b64_py = base64.b64encode(code.encode()).decode()
                    py_href = f'<a href="data:file/python;base64,{b64_py}" download="{filename}">🐍 Download as .py</a>'
                    st.markdown(py_href, unsafe_allow_html=True)
        else:
            st.info("No file uploads yet.")

    if history_tabs == "Explanation":
        st.header("🧠 Explanation History")

        if st.session_state.explanation_history:
            if st.button("🗑️ Clear Explanation History"):
                st.session_state.explanation_history.clear()
                history_manager.clear_explanation_history()
                st.success("Explanation history cleared.")

            for idx, entry in enumerate(st.session_state.explanation_history):
                filename = entry["filename"]
                explanation = entry["explanation"]

                with st.expander(f"{filename}"):
                    # Generate PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.set_font("Arial", size=12)
                    for line in explanation.split('\n'):
                        pdf.multi_cell(0, 10, txt=line)

                    file_id = str(uuid.uuid4())
                    pdf_path = f"./modules/data/expl_{file_id}.pdf"
                    pdf.output(pdf_path)

                    st.text_area("Explanation History", explanation, height=200, disabled=True, label_visibility="collapsed", key=f"explanation_{idx}")

                    with open(pdf_path, "rb") as pdf_file:
                        b64_pdf = base64.b64encode(pdf_file.read()).decode()
                        href_pdf = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{filename}_explanation.pdf">📄 Download as PDF</a>'
                        st.markdown(href_pdf, unsafe_allow_html=True)

                    # MP3
                    audio_path = f"./modules/data/audio/{file_id}.mp3"
                    engine = voice_assistant.get_voice_by_gender(st.session_state.voice_gender)
                    voice_assistant.save_audio(explanation, engine, output_path=audio_path)

                    with open(audio_path, "rb") as audio_file:
                        b64_mp3 = base64.b64encode(audio_file.read()).decode()
                        href_mp3 = f'<a href="data:audio/mp3;base64,{b64_mp3}" download="{filename}_explanation.mp3">🔊 Download MP3</a>'
                        st.markdown(href_mp3, unsafe_allow_html=True)
        else:
            st.info("No explanations generated yet.")
    else:
        st.info("This feature will soon arrive")
