import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

def get_voice_by_gender(gender: str):
    engine = pyttsx3.init()
    engine.setProperty("rate",175)
    voices = engine.getProperty('voices')

    # Normalize input
    gender = gender.lower()
    
    # Find voice by gender keyword
    male_voice = next((v for v in voices if 'male' in v.name.lower() or 'david' in v.name.lower()), None)
    female_voice = next((v for v in voices if 'female' in v.name.lower() or 'zira' in v.name.lower()), None)
    
    # Neutral fallback is third voice if it exists
    neutral_voice = voices[2] if len(voices) >= 3 else female_voice

    if gender == 'male' and male_voice:
        engine.setProperty('voice', male_voice.id)
    elif gender == 'female' and female_voice:
        engine.setProperty('voice', female_voice.id)
    elif gender == 'neutral':
        engine.setProperty('voice', neutral_voice.id)
    else:
        print("Invalid gender or voice not found. Using default voice.")

    return engine


# # Example usage
# gender_choice = "neutral"  # change to "male", "female", or "neutral"
# engine = get_voice_by_gender(gender_choice)
# engine.say(f"This is the {gender_choice} voice speaking.")
# engine.runAndWait()

def save_audio(explanation:str, engine):
    engine.save_to_file(explanation , './modules/data/audio/test.mp3')
    engine.runAndWait()
