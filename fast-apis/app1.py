from flask import Flask, request, render_template, jsonify
import librosa
import numpy as np
from transformers import pipeline
import joblib
from utils.FeatureExetraction import extract_features

# Initialize app
app = Flask(__name__)

# Load pre-trained models
stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-small")
emotion_model = joblib.load("emotion_model.pkl")

from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.route('/')
def home():
    return render_template('../templates/index.html')

@app.route('/process', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    file_path = "uploaded_audio.wav"
    audio_file.save(file_path)

    # Speech-to-Text
    text = stt_pipeline(file_path)['text']

    # Emotion Recognition
    features = extract_features(file_path)
    emotion = emotion_model.predict([features])[0]

    return jsonify({"text": text, "emotion": emotion})

if __name__ == "__main__":
    app.run(debug=True)
