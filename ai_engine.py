import torch
from google import genai
from google.genai import types
from PIL import Image
import os

class AIEngine:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Initializing AI Engine on {self.device}...")
        
        # Initialize Google GenAI Client
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            print("WARNING: GOOGLE_API_KEY not found in environment variables.")
            self.client = None

        # Placeholders for models
        self.video_pipe = None

    def load_video_model(self):
        if not self.video_pipe:
            print("Loading Video Model (ModelScope)...")
            from diffusers import DiffusionPipeline
            try:
                # Using ModelScope text-to-video (Free/Open Source via Diffusers)
                if self.device == "cuda":
                    self.video_pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
                    self.video_pipe.enable_model_cpu_offload()
                else:
                    self.video_pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b")
                    self.video_pipe = self.video_pipe.to("cpu")
                print("Video Model Loaded.")
            except Exception as e:
                print(f"FAILED TO LOAD VIDEO MODEL: {e}")
                raise e

    def reason(self, prompt):
        """Generates text/reasoning using Gemini 2.5 Pro"""
        if not self.client:
            return "Error: Google GenAI Client not initialized (missing API Key)."

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                config=types.GenerateContentConfig(
                    system_instruction="You are a helpful AI assistant."
                ),
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating reasoning: {str(e)}"

    def generate_image(self, prompt, output_path):
        """Generates an image using Gemini 2.5 Flash Image"""
        if not self.client:
            print("Error: Google GenAI Client not initialized.")
            return None

        try:
            print(f"Generating image with prompt: {prompt}")
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[prompt],
            )
            
            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    image.save(output_path)
                    print(f"Image saved to {output_path}")
                    return output_path
            
            print("No image found in response.")
            return None
        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    def generate_video(self, prompt, output_path):
        try:
            from diffusers.utils import export_to_video
            self.load_video_model()
            video_frames = self.video_pipe(prompt, num_inference_steps=25).frames
            export_to_video(video_frames[0], output_path, fps=8)
            return output_path
        except Exception as e:
            print(f"Error: {e}")
            return None
