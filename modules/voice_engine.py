import pyttsx3

engine = pyttsx3.init()

def speak(text: str, gender: str = "Neutral"):
    voices = engine.getProperty('voices')
    # Select voice (basic logic, system-dependent)
    if gender == "Male":
        engine.setProperty('voice', voices[0].id)
    elif gender == "Female" and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    else:
        engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
