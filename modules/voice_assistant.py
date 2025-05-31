import pyttsx3
import os

class VoiceAssistant:
    def __init__(self, rate: int = 175):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.voices = self.engine.getProperty('voices')

    def set_voice_by_gender(self, gender: str) -> None:
        gender = gender.lower()

        male_voice = next((v for v in self.voices if 'male' in v.name.lower() or 'david' in v.name.lower()), None)
        female_voice = next((v for v in self.voices if 'female' in v.name.lower() or 'zira' in v.name.lower()), None)
        neutral_voice = self.voices[2] if len(self.voices) >= 3 else female_voice

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
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.engine.save_to_file(text, output_path)
        self.engine.runAndWait()
        return output_path

    def speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()
