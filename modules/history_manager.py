import json
import os
import streamlit as st


class HistoryManager:
    def __init__(
        self,
        upload_history_path: str = "./modules/data/upload_history.json",
        explanation_history_path: str = "./modules/data/explanation_history.json",
        chat_history_path: str = "./modules/data/chat_history.json",
        audio_dir: str = "./modules/data/audio",
        pdf_dir: str = "./modules/data"
    ):
        self.upload_history_path = upload_history_path
        self.explanation_history_path = explanation_history_path
        self.chat_history_path = chat_history_path
        self.audio_dir = audio_dir
        self.pdf_dir = pdf_dir

        # Ensure necessary directories exist
        os.makedirs(os.path.dirname(self.upload_history_path), exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.pdf_dir, exist_ok=True)

    # === Upload History ===
    def save_upload_history(self, data: list) -> None:
        with open(self.upload_history_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_upload_history(self) -> list:
        if os.path.exists(self.upload_history_path):
            try:
                with open(self.upload_history_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def clear_upload_history(self) -> None:
        if os.path.exists(self.upload_history_path):
            os.remove(self.upload_history_path)

    # === Explanation History ===
    def save_explanation_history(self, data: list) -> None:
        with open(self.explanation_history_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_explanation_history(self) -> list:
        if os.path.exists(self.explanation_history_path):
            try:
                with open(self.explanation_history_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def clear_explanation_history(self) -> None:
        # Clear explanation history JSON
        with open(self.explanation_history_path, "w", encoding="utf-8") as f:
            json.dump([], f)

        # Remove MP3 files in audio directory
        for file in os.listdir(self.audio_dir):
            if file.endswith(".mp3"):
                os.remove(os.path.join(self.audio_dir, file))

        # Remove explanation PDFs
        for file in os.listdir(self.pdf_dir):
            if file.startswith("expl_") and file.endswith(".pdf"):
                os.remove(os.path.join(self.pdf_dir, file))

    # === Chat History ===
    def save_chat_history(self, data: list) -> None:
        with open(self.chat_history_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_chat_history(self) -> list:
        if os.path.exists(self.chat_history_path):
            try:
                with open(self.chat_history_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def clear_chat_history(self) -> None:
        if os.path.exists(self.chat_history_path):
            os.remove(self.chat_history_path)