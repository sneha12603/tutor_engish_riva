from stt import listen_until_stop
from llm import get_ai_response
from tts import setup_voice, speak

print("=== Quick Combined Test ===")

# Setup voice
setup_voice()

# Speak welcome
speak("Hello! I am Riva. Please speak now and press ENTER when done!")

# Record your voice — no time limit!
print("\nSpeak freely, press ENTER when done...")
user_text = listen_until_stop()
print(f"\n📝 You said: {user_text}")

# Get AI response
ai_reply = get_ai_response(user_text)
print(f"\n🤖 Riva says: {ai_reply}")

# Speak the reply
speak(ai_reply)