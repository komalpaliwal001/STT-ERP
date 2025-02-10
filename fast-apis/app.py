from flask import Flask, request, render_template, jsonify, make_response
import pickle
import pandas as pd
import os
import librosa
from transformers import pipeline
from werkzeug.datastructures import FileStorage
import mimetypes
from utils.Classifier import getClassificationReport, trainingModel
from utils.AudioRecorder import record_pyaudio
from utils.FeatureExetraction import extract_features, extract_features_from_waveform
from functools import wraps
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__, template_folder='../templates/')

# Allow only the Remix frontend to access the API
CORS(app, resources={r"/*": {"origins": "http://localhost:3003"}})

# CORS Handling Functions
def add_cors_headers(response):
    if isinstance(response, tuple):
        body, status, headers = response + (None,) * (3 - len(response))
        response = make_response(body, status or 200)
        if headers:
            response.headers.extend(headers)

    response.headers['Access-Control-Allow-Origin'] = '*, http://localhost:3003'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def cors_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            response = jsonify({'message': 'CORS preflight handled'})
            return add_cors_headers(response)
        response = func(*args, **kwargs)
        return add_cors_headers(response)

    return wrapper

# Load models
stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-small")


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
            df = pd.read_csv(uploaded_file)
            features = df.drop(columns=['labels'], errors='ignore')
            labels = df['labels'] if 'labels' in df.columns else payload.get('labels')

            if labels is None:
                return jsonify({"error": "Labels are not provided in the CSV or payload"}), 400

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
# @cors_decorator
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    file_path = "recorded_audio.wav"
    audio_file.save(file_path)
    print(audio_file)

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type != 'audio/wav':
        return jsonify({"error": "Uploaded file is not a valid WAV file."}), 400

    # Validate file existence and size
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return jsonify({"error": "Uploaded file is empty or corrupted"}), 400

    # Load audio data into a NumPy array
    audio_data, _ = librosa.load(file_path, sr=16000)
    print(audio_data)
    # Extract features from the loaded audio data
    features = extract_features_from_waveform(audio_data, 16000)

    return jsonify({"emotion": features})



@app.route("/record_audio", methods=["GET"])
@cors_decorator
def record_audio_route():
    try:
        duration = request.args.get('duration', default=5, type=int)
        filename = record_pyaudio(duration=duration)
        features = extract_features(filename)
        return jsonify({"features": features})
    except Exception as e:
        return jsonify({"error": f"Audio recording failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5003)
