import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

def setup_voice():
    # Get all available voices
    voices = engine.getProperty('voices')
    
    # Print available voices (run once to see options)
    for i, voice in enumerate(voices):
        print(f"Voice {i}: {voice.name}")
    
    # Set female voice (index 1) — sounds better for tutor
    # If only one voice available, use index 0
    try:
        engine.setProperty('voice', voices[1].id)  # Female
    except:
        engine.setProperty('voice', voices[0].id)  # Male fallback
    
    # Set speaking speed (150 = natural pace)
    engine.setProperty('rate', 150)
    
    # Set volume (0.0 to 1.0)
    engine.setProperty('volume', 1.0)

def speak(text):
    print(f"\n🔊 Riva speaking...")
    engine.say(text)
    engine.runAndWait()

def speak_welcome():
    welcome = "Hello! I am Riva, your personal English speaking tutor. Please speak after the beep and I will help you improve your English!"
    speak(welcome)

# TEST — run this file directly
if __name__ == "__main__":
    print("=== TTS Test ===\n")
    
    # Setup voice first
    setup_voice()
    
    print("\nTest 1 — Welcome message:")
    speak_welcome()
    
    print("\nTest 2 — Grammar correction:")
    speak("Small correction! Say I am going to school, not I is going to school. We use am with I, not is. Great effort though!")
    
    print("\nTest 3 — Encouragement:")
    speak("Excellent English! You are improving very fast. Keep it up!")
    
    print("\n✅ TTS test complete!")