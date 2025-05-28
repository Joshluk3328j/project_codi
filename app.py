import streamlit as st
from modules.audio_bar import display_audio_bar
import base64
from modules import settings_manager, voice_assistant



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


# --------------------- Sidebar --------------------- #
st.sidebar.header("⚙️ Settings")

# Toggles with tracked updates
va_toggle = st.sidebar.toggle("🎙️ Enable Voice Assistant", st.session_state.voice_assistant)
if va_toggle != st.session_state.voice_assistant:
    st.session_state.voice_assistant = va_toggle

va_toggle = st.sidebar.toggle("🧠 Voice Activation (e.g., 'Hey Codi')", value=st.session_state.get("voice_activation", False))
if va_toggle != st.session_state.get("voice_activation", False):
    st.session_state.voice_activation = va_toggle


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

    with right_col:
        if has_uploaded:
            explanation = uploaded_code
            display_explanation(explanation)
            if st.session_state.voice_assistant:
                engine = voice_assistant.get_voice_by_gender(st.session_state.voice_gender)
                voice_assistant.save_audio(explanation,engine)
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
    st.header("💬 Chat with Codi")
    st.info("this feature is coming soon")
    history_tabs = st.selectbox("View Your History", ["Uploads","Explanation","Chat"])
    st.info("This feature will soon arrive")
