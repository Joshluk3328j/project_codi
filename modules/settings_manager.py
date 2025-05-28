import os
import streamlit as st
import json

# --------------------- Settings File I/O --------------------- #

SETTINGS_PATH = os.path.expanduser("./data/settings.json")

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    # Default states
    st.session_state.setdefault('last_uploaded_file_id', None)
    st.session_state.setdefault('explanation_style', "concise")
    st.session_state.setdefault("voice_assistant", False)
    st.session_state.setdefault('speech_state', "paused")
    st.session_state.setdefault('current_block_index', 0)
    st.session_state.setdefault('speech_rate', 200)
    st.session_state.setdefault('voice_activation', False)
    st.session_state.setdefault('voice_gender', "Neutral")
    # st.session_state.setdefault('enable_ide_integration', False)


def save_settings(settings: dict):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)  # ✅ Ensure the directory exists
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)