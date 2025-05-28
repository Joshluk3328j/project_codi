# project_codi/modules/voice_activation.py

import threading
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "vosk-model-small-en-us-0.15")
hotword_detected = False
q = queue.Queue()

def init_vosk_model():
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path does not exist: {model_path}")
    try:
        print(f"Loading model from: {model_path}")
        model = Model(model_path)
        return KaldiRecognizer(model, 16000)
    except Exception as e:
        raise Exception(f"Failed to initialize Vosk model: {e}")

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio callback status: {status}")
    q.put(bytes(indata))

def listen_for_hotword():
    def background_listener():
        global hotword_detected
        try:
            recognizer = init_vosk_model()
            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                   channels=1, callback=audio_callback):
                print("Listening for hotword 'Hey Codi'...")
                while not hotword_detected:
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "")
                        print(f"Heard: {text}")
                        if "hey codi" in text.lower():
                            hotword_detected = True
                            print("🎤 Hotword 'Hey Codi' Detected!")
        except Exception as e:
            print(f"Hotword detection error: {e}")

    thread = threading.Thread(target=background_listener, daemon=True)
    thread.start()