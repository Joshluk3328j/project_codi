"""
Manages upload, explanation, and chat histories for the application.

Supports saving, loading, and clearing JSON-based records.
Also handles cleanup of generated audio and PDF files.
"""

import json
import os

class HistoryManager:
    """
    Manages upload, explanation, and chat history along with associated audio and PDF files.
    Stores history in JSON format and handles cleanup of media files.
    """

    def __init__(
        self,
        upload_history_path: str = "./modules/data/upload_history.json",
        explanation_history_path: str = "./modules/data/explanation_history.json",
        chat_history_path: str = "./modules/data/chat_history.json",
        audio_dir: str = "./modules/data/audio",
        pdf_dir: str = "./modules/data"
    ):
        """
        Initializes the history manager with file paths for various types of histories.

        Args:
            upload_history_path (str): File path for upload history JSON.
            explanation_history_path (str): File path for explanation history JSON.
            chat_history_path (str): File path for chat history JSON.
            audio_dir (str): Directory for storing audio (MP3) files.
            pdf_dir (str): Directory for storing PDF files.
        """
        self.upload_history_path = upload_history_path
        self.explanation_history_path = explanation_history_path
        self.chat_history_path = chat_history_path
        self.audio_dir = audio_dir
        self.pdf_dir = pdf_dir

        # Ensure all necessary directories exist
        os.makedirs(os.path.dirname(self.upload_history_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.explanation_history_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.chat_history_path), exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.pdf_dir, exist_ok=True)

    # === Upload History ===
    def save_upload_history(self, data: list) -> None:
        """
        Saves the upload history to a JSON file.

        Args:
            data (list): List of uploaded file metadata.
        """
        with open(self.upload_history_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_upload_history(self) -> list:
        """
        Loads the upload history from a JSON file.

        Returns:
            list: List of uploaded file metadata.
        """
        if os.path.exists(self.upload_history_path):
            try:
                with open(self.upload_history_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def clear_upload_history(self) -> None:
        """
        Deletes the upload history file if it exists.
        """
        with open(self.upload_history_path, "w", encoding="utf-8") as f:
            json.dump([], f)

    # === Explanation History ===
    def save_explanation_history(self, data: list) -> None:
        """
        Saves the explanation history to a JSON file.

        Args:
            data (list): List of explanation entries.
        """
        with open(self.explanation_history_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_explanation_history(self) -> list:
        """
        Loads the explanation history from a JSON file.

        Returns:
            list: List of explanation entries.
        """
        if os.path.exists(self.explanation_history_path):
            try:
                with open(self.explanation_history_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def clear_explanation_history(self) -> None:
        """
        Clears the explanation history and removes associated MP3 and PDF files.
        """
        # Clear explanation history JSON file
        with open(self.explanation_history_path, "w", encoding="utf-8") as f:
            json.dump([], f)

        # Remove all MP3 files in audio directory
        for file in os.listdir(self.audio_dir):
            if file.endswith(".mp3"):
                os.remove(os.path.join(self.audio_dir, file))

        # Remove PDF files starting with "expl_"
        for file in os.listdir(self.pdf_dir):
            if file.startswith("expl_") and file.endswith(".pdf"):
                os.remove(os.path.join(self.pdf_dir, file))

    # === Chat History ===
    def save_chat_history(self, data: list) -> None:
        """
        Saves the chat history to a JSON file.

        Args:
            data (list): List of chat message entries.
        """
        with open(self.chat_history_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_chat_history(self) -> list:
        """
        Loads the chat history from a JSON file.

        Returns:
            list: List of chat message entries.
        """
        if os.path.exists(self.chat_history_path):
            try:
                with open(self.chat_history_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def clear_chat_history(self) -> None:
        """
        Clears the chat history and removes associated chat PDF files.
        """
        # Clear chat history JSON file
        with open(self.chat_history_path, "w", encoding="utf-8") as f:
            json.dump([], f)

        # Remove PDF files starting with "chat_"
        for file in os.listdir(self.pdf_dir):
            if file.startswith("chat_") and file.endswith(".pdf"):
                os.remove(os.path.join(self.pdf_dir, file))
