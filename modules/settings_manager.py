import os
import json
import streamlit as st
from typing import Optional


class SettingsManager:
    def __init__(self, path: Optional[str] = None):
        self.settings_path = os.path.expanduser(path or "./modules/data/settings.json")
        self.default_settings = {
            'last_uploaded_file_id': None,
            'explanation_style': "concise",
            'voice_assistant': False,
            'speech_state': "paused",
            'current_block_index': 0,
            'speech_rate': 165,
            'voice_activation': False,
            'voice_gender': "Neutral",
            # 'enable_ide_integration': False,
        }

    def load_settings(self) -> dict:
        """Load settings from file or initialize with defaults."""
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r") as f:
                    settings = json.load(f)
                    self._apply_to_session_state(settings)
                    return settings
            except json.JSONDecodeError:
                pass

        self._apply_to_session_state(self.default_settings)
        return self.default_settings

    def save_settings(self, settings: dict):
        """Save settings to file."""
        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
        with open(self.settings_path, "w") as f:
            json.dump(settings, f, indent=2)

    def _apply_to_session_state(self, settings: dict):
        """Initialize or update Streamlit session state with loaded settings."""
        for key, value in settings.items():
            st.session_state.setdefault(key, value)
