"""
Manages application settings, including persistence and session state sync.

Loads and saves user settings such as explanation style, voice preferences, and UI state.
Ensures fallback to defaults and automatic session state initialization.
"""

import os
import json
import streamlit as st

class SettingsManager:
    """
    Manages persistent application settings, synchronizing them with Streamlit's session state.
    Handles loading, saving, and applying default values when necessary.
    """

    def __init__(self, path: str = "./modules/data/settings.json"  ):
        """
        Initializes the settings manager with an optional custom path.

        Args:
            path (Optional[str]): Path to the settings JSON file. Defaults to './modules/data/settings.json'.
        """
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
            # 'enable_ide_integration': False,  # Reserved for future use
        }

    def load_settings(self) -> dict:
        """
        Loads settings from a JSON file, or initializes with default settings if the file is missing or invalid.

        Returns:
            dict: Loaded or default settings.
        """
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r") as f:
                    settings = json.load(f)
                    self._apply_to_session_state(settings)
                    return settings
            except json.JSONDecodeError:
                pass  # Fallback to defaults if file is corrupted

        self._apply_to_session_state(self.default_settings)
        return self.default_settings

    def save_settings(self, settings: dict):
        """
        Saves the given settings dictionary to a JSON file.

        Args:
            settings (dict): The current settings to persist.
        """
        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
        with open(self.settings_path, "w") as f:
            json.dump(settings, f, indent=2)

    def _apply_to_session_state(self, settings: dict):
        """
        Updates Streamlit's session state with the provided settings.

        Args:
            settings (dict): A dictionary of settings to apply.
        """
        for key, value in settings.items():
            st.session_state.setdefault(key, value)
