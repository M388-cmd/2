from ai_engine import AIEngine
import traceback
from dotenv import load_dotenv

load_dotenv('.env.local')

print("Starting debug script...")
try:
    ai = AIEngine()
    print("Attempting to generate text...")
    # This will trigger load_reasoning_model() (implicitly via reason call)
    response = ai.reason("Hello")
    print(f"Success! Response: {response}")
except Exception:
    print("CRITICAL ERROR CAUGHT:")
    traceback.print_exc()
