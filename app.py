from flask import Flask, render_template, request, jsonify, send_from_directory
from ai_engine import AIEngine
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('.env.local')

app = Flask(__name__)
ai = AIEngine()

# Ensure static folders exist
os.makedirs("static/generated", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('message', '')
    if not prompt:
        return jsonify({"error": "No message provided"}), 400
    
    response = ai.reason(prompt)
    return jsonify({"response": response})

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    filename = f"img_{int(time.time())}.png"
    filepath = os.path.join("static/generated", filename)
    
    result_path = ai.generate_image(prompt, filepath)
    
    if result_path:
        return jsonify({"url": f"/static/generated/{filename}", "type": "image"})
    else:
        return jsonify({"error": "Image generation failed"}), 500

@app.route('/generate_video', methods=['POST'])
def generate_video():
    data = request.json
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    filename = f"vid_{int(time.time())}.mp4"
    filepath = os.path.join("static/generated", filename)
    
    result_path = ai.generate_video(prompt, filepath)
    
    if result_path:
        return jsonify({"url": f"/static/generated/{filename}", "type": "video"})
    else:
        return jsonify({"error": "Video generation failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
