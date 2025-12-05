from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
    exit(1)

client = genai.Client(api_key=api_key)

prompt = input("Enter a prompt for the image: ")
if not prompt:
    prompt = "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"

print(f"Generating image for prompt: '{prompt}'...")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt],
    )

    image_saved = False
    for part in response.parts:
        if part.text is not None:
            print(f"Text response: {part.text}")
        elif part.inline_data is not None:
            image = part.as_image()
            image.save("generated_image.png")
            print("Success! Image saved to generated_image.png")
            image_saved = True
            
    if not image_saved:
        print("No image was generated in the response.")

except Exception as e:
    print(f"An error occurred: {e}")
