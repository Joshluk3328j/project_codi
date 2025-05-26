import pyttsx3
#initializing the speech engine
engine = pyttsx3.init()
# seting engine as our variable

engine.setProperty('rate', 200)# Speaking rate (the speed the engine speaks the words)
engine.setProperty('volume', 1.0)# Sets the volume (0.0(silent) to 1.0(loudest))

def speak(text: str, gender: str = "Neutral"):
    voices = engine.getProperty('voices') #This Gets the voices available
    # Select voice (basic logic, system-dependent)
    if gender == "Male":
        engine.setProperty('voice', voices[1].id)
    elif gender == "Female" and len(voices) > 1:
        engine.setProperty('voice', voices[2].id)
    else:
        engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()

