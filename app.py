import streamlit as st
from modules import code_parser, explainer, voice_engine, ide_connector, history_manager

st.set_page_config(page_title="Programmer's Assistant", layout="wide")

st.title("Voice-Activated Programmer's Assistant")

# Sidebar controls
st.sidebar.title("Assistant Settings")
voice_enabled = st.sidebar.toggle("Voice Activation", value=True)
ide_enabled = st.sidebar.toggle("IDE Integration", value=False)
voice_gender = st.sidebar.radio("Voice Type", ["Neutral", "Male", "Female"])

# Store settings
settings = {
    "voice_enabled": voice_enabled,
    "ide_enabled": ide_enabled,
    "voice_gender": voice_gender
}
# Save settings
# (TODO: Write to settings.json if needed)

# Code upload section
st.header("Upload Your Code")
uploaded_file = st.file_uploader("Choose a Python file", type="py")

if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
    st.code(code, language='python')

    blocks = code_parser.split_into_blocks(code)
    for i, block in enumerate(blocks):
        st.subheader(f"Block {i+1}")
        explanation = explainer.explain_block(block)
        st.write(explanation)
        if voice_enabled:
            voice_engine.speak(explanation, gender=voice_gender)

# Chat section
st.header("Chat with Assistant")
user_input = st.text_input("Ask a question...")
if user_input:
    response = explainer.answer_question(user_input)
    st.write(response)
    if voice_enabled:
        voice_engine.speak(response, gender=voice_gender)

# History display (placeholder)
st.sidebar.title("History")
st.sidebar.info("Coming soon: browse past uploads and conversations.")
