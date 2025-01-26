from flask import Flask, request, render_template, jsonify, make_response
import pickle
import pandas as pd
import librosa
import numpy as np
import os
from transformers import pipeline
from werkzeug.datastructures import FileStorage
import mimetypes
from utils.Classifier import getClassificationReport, trainingModel
from utils.AudioRecorder import record_audio
from utils.FeatureExetraction import extract_features, extract_features_from_waveform
from functools import wraps

# Initialize the Flask app
app = Flask(__name__, template_folder='../templates/')


# Updated function to handle tuple responses correctly
def add_cors_headers(response):
    if isinstance(response, tuple):
        # Unpack the tuple into body, status, and headers
        # Handle cases where the tuple may or may not include all values
        body, status, headers = response + (None,) * (3 - len(response))
        response = make_response(body, status or 200)  # Create a proper Response object
        if headers:
            response.headers.extend(headers)  # Add existing headers

    # Add CORS headers to the response
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


# Wrap routes to handle OPTIONS requests
def cors_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            response = jsonify({'message': 'CORS preflight handled'})
            return add_cors_headers(response)
        response = func(*args, **kwargs)
        return add_cors_headers(response)

    return wrapper


# Ensure models or external utilities are loaded properly
stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-small")
emotion_model = None  # Replace with actual model loading logic, e.g., using pickle or joblib


@app.route("/get_classification_report", methods=["GET"])
def get_classification_report():
    try:
        report = getClassificationReport()
        return jsonify({"classification_report": report})
    except Exception as e:
        return jsonify({"error": f"Failed to get classification report: {str(e)}"}), 500


@app.route("/prediction", methods=["POST"])
@cors_decorator
def prediction():
    try:
        payload = request.json
        if not payload or 'feature' not in payload or 'model' not in payload:
            return jsonify({"error": "Feature and model name must be provided in the payload"}), 400

        X_unknown = pd.DataFrame([payload['feature']])
        model_path = os.path.join("./model", f"{payload['model']}.pkl")

        if not os.path.exists(model_path):
            return jsonify({"error": "The specified model file does not exist"}), 404

        with open(model_path, "rb") as f:
            clf = pickle.load(f)

        prediction = clf.predict(X_unknown)
        return jsonify({"predicted_value": prediction[0]})
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route("/training", methods=["POST"])
@cors_decorator
def training():
    try:
        uploaded_file: FileStorage | None = request.files.get('file')
        payload = request.json

        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                features = df.drop(columns=['labels'], errors='ignore')
                labels = df['labels'] if 'labels' in df.columns else payload.get('labels')

                if labels is None:
                    return jsonify({"error": "Labels are not provided in the CSV or payload"}), 400

            except Exception as e:
                return jsonify({"error": f"Failed to process the uploaded CSV: {str(e)}"}), 500
        else:
            features = pd.DataFrame(payload.get('features'))
            labels = payload.get('labels')

            if features.empty or labels is None:
                return jsonify({"error": "Features and labels must be provided"}), 400

        trainingModel(features, labels, model_type='svm')
        return jsonify({"message": "Model file created successfully"})
    except Exception as e:
        return jsonify({"error": f"Model training failed: {str(e)}"}), 500


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
@cors_decorator
def process_audio():
    # try:
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    file_path = "recorded_audio.wav"
    audio_file.save(file_path)

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type != 'audio/wav':
        raise RuntimeError("Uploaded file is not a valid WAV file.")

    # Validate file existence and size
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return jsonify({"error": "Uploaded file is empty or corrupted"}), 400

    # text = stt_pipeline(file_path)['text']
    features = extract_features_from_waveform(file_path, 16000)

    return jsonify({ "emotion": features})
    # except Exception as e:
    #     return jsonify({"error": f"Audio processing failed: {str(e)}"}), 500

@app.route("/record_audio", methods=["GET"])
@cors_decorator
def record_audio_route():
    try:
        duration = request.args.get('duration', default=5, type=int)
        filename = record_audio(duration=duration)
        features = extract_features(filename)
        return jsonify({"features": features})
    except Exception as e:
        return jsonify({"error": f"Audio recording failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5003)
