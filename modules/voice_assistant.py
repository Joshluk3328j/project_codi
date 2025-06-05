"""
Text-to-speech engine wrapper using pyttsx3.

Allows saving synthesized speech as MP3 and speaking directly from text.
Supports voice selection by gender and adjustable speech rate.
"""

import pyttsx3
import os

class VoiceAssistant:
    """
    A text-to-speech utility class using the pyttsx3 engine.
    Supports saving audio to files and selecting voices by gender.
    """

    def __init__(self, rate: int = 175):
        """
        Initializes the TTS engine with a given speech rate.

        Args:
            rate (int): Speed of the spoken text (default is 175 words per minute).
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.voices = self.engine.getProperty('voices')  # Get available voices

    def set_voice_by_gender(self, gender: str):
        """
        Sets the voice for speech synthesis based on the specified gender.

        Args:
            gender (str): Gender of the desired voice ('male', 'female', or 'neutral').

        Notes:
            - Falls back to a default voice if the specified one isn't found.
            - Common voices include 'David' (male) and 'Zira' (female) on Windows.
        """
        gender = gender.lower()

        # Attempt to find male or female voices using common naming patterns
        male_voice = next((v for v in self.voices if 'male' in v.name.lower() or 'david' in v.name.lower()), None)
        female_voice = next((v for v in self.voices if 'female' in v.name.lower() or 'zira' in v.name.lower()), None)

        # Default to third voice if available, otherwise use female voice
        neutral_voice = self.voices[2] if len(self.voices) >= 3 else female_voice

        # Assign selected voice based on gender
        if gender == 'male' and male_voice:
            self.engine.setProperty('voice', male_voice.id)
        elif gender == 'female' and female_voice:
            self.engine.setProperty('voice', female_voice.id)
        elif gender == 'neutral':
            self.engine.setProperty('voice', neutral_voice.id)
        else:
            print("⚠️ Invalid gender or voice not found. Using default voice.")

        return self.engine

    def save_audio(self, text: str, output_path: str = './modules/data/audio/output.mp3') -> str:
        """
        Saves spoken text as an audio file.

        Args:
            text (str): Text to be converted into speech.
            output_path (str): File path to save the generated audio (default is ./modules/data/audio/output.mp3).

        Returns:
            str: Path to the saved audio file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure directory exists
        self.engine.save_to_file(text, output_path)
        self.engine.runAndWait()  # Complete the speech task
        return output_path

    # currently not being used
    def speak(self, text: str) -> None:
        """
        Speaks the given text aloud using the selected voice.

        Args:
            text (str): The text to be spoken.
        """
        self.engine.say(text)
        self.engine.runAndWait()
