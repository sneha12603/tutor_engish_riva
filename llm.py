import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Connect to Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Conversation history (remembers chat)
conversation_history = []

# System prompt — this makes it behave like Riva English tutor
SYSTEM_PROMPT = """
You are Riva, a friendly AI English speaking tutor.
When the user speaks to you:
1. If there are any grammar mistakes, politely correct them first
2. Explain WHY it was wrong in very simple words
3. Give the correct sentence
4. Then respond naturally to what they said
5. Keep your response short — maximum 3 to 4 sentences
6. Always be encouraging and positive
7. If the English is already correct, just say "Great English!" and reply naturally

Example:
User: "I is going to market"
Riva: "Small correction — say 'I am going to market' instead of 'I is going'. 
We use 'am' with 'I', not 'is'. Great effort though! 
What are you planning to buy at the market?"
"""

def get_ai_response(user_text):
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_text
    })
    
    # Send to Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + conversation_history,
        max_tokens=200,
        temperature=0.7
    )
    
    # Get AI reply
    ai_reply = response.choices[0].message.content.strip()
    
    # Add AI reply to history
    conversation_history.append({
        "role": "assistant",
        "content": ai_reply
    })
    
    return ai_reply

def reset_conversation():
    conversation_history.clear()

# TEST — run this file directly
if __name__ == "__main__":
    print("=== Groq API Test ===\n")
    
    # Test 1 — wrong grammar
    print("Test 1 — Wrong grammar:")
    test1 = "I is going to school yesterday"
    print(f"User: {test1}")
    reply1 = get_ai_response(test1)
    print(f"Riva: {reply1}\n")
    
    # Test 2 — correct grammar
    print("Test 2 — Correct grammar:")
    test2 = "I went to school yesterday"
    print(f"User: {test2}")
    reply2 = get_ai_response(test2)
    print(f"Riva: {reply2}\n")
    
    # Test 3 — conversation continues
    print("Test 3 — Follow up question:")
    test3 = "What did you learned today?"
    print(f"User: {test3}")
    reply3 = get_ai_response(test3)
    print(f"Riva: {reply3}")