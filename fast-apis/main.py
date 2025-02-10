from ast import Await
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends, Query
from fastapi.responses import JSONResponse, HTMLResponse
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import numpy as np
import librosa
import os
import mimetypes
import wave
import json
from vosk import Model, KaldiRecognizer
from sklearn.cluster import KMeans
from transformers import pipeline
from utils.Classifier import getClassificationReport, trainingModel
from utils.AudioRecorder import record_pyaudio
from utils.FeatureExetraction import extract_features, extract_features_from_waveform

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Speech-to-Text model
stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Load Vosk model
model = Model("models/vosk-model-en-us-0.22")

# labels = {0: 'happy', 1: 'neutral', 2: 'sad'}
labels = {0: 'happy', 1: 'neutral', 2: 'sad', 3: 'angry', 4: 'disgust', 5: 'fear', 6: 'surprise'}


@app.get("/get_classification_report")
async def get_classification_report():
    """Returns classification report."""
    try:
        report = getClassificationReport()
        return {"classification_report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get classification report: {str(e)}")

@app.post("/training")
async def training(file: UploadFile = File(None),  model: str = 'svm', labels: dict = None):
    """Trains the model using uploaded file or provided data."""
    print(file)
    try:
        if file:
            df = pd.read_csv(file.file)
            features = df.drop(columns=['labels'], errors='ignore')

            # Use K-Means to cluster features into 3 groups (neutral, sad, happy)
            num_clusters = 7
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(features)

            labels = df['labels'] if 'labels' in df.columns else cluster_labels

            if labels is None:
                raise HTTPException(status_code=400, detail="Labels are not provided in the CSV or payload")
        else:
            raise HTTPException(status_code=400, detail="Features and labels must be provided")

        trainingModel(features, labels, model_type=model)
        return {"message": "Model file created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")

async def prediction(feature: np.ndarray, model: str):
    """Predicts label based on provided features."""
    global labels
    try:
        # Convert feature array to a list
        if isinstance(feature, np.ndarray):
            feature = feature.tolist()
        
        print("Extracted Features:", feature)  # Debugging

        model_path = os.path.join("./models", f"{model}_classifier.pkl")
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="The specified model file does not exist.")

        with open(model_path, "rb") as f:
            clf = pickle.load(f)

        # Ensure features match model expectation
        expected_feature_count = clf.n_features_in_
        if len(feature) != expected_feature_count:
            raise HTTPException(
                status_code=400, 
                detail=f"Feature mismatch: Expected {expected_feature_count}, got {len(feature)}."
            )

        # Convert feature list to DataFrame
        feature = pd.DataFrame([feature])  # Ensure it's in the correct format
        
        prediction = clf.predict(feature)
        print("Prediction:", prediction)  # Debugging

        return {"predicted_value": labels[int(prediction[0])]}  # Convert NumPy int to Python int for JSON serialization

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process")
async def process_audio(audio_file: UploadFile = File(...), model: str = "svm"):
    """Processes uploaded audio file and extracts features."""
    print(audio_file)
    try:
    
        file_path = os.path.join(UPLOAD_DIR, audio_file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(audio_file.file.read())

        # Validate MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type != 'audio/wav':
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid WAV file.")

        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty or corrupted.")

        # Load and extract features
        audio_data, _ = librosa.load(file_path, sr=16000)
        features = extract_features_from_waveform(audio_data, 16000)
        print(_)
        emotion = await prediction(features, model)
        print(emotion)
        # **Ensure the output is JSON-serializable**
        if isinstance(features, np.ndarray):
            features = features.tolist()  # Convert NumPy array to list

        # Open audio file
        wf = wave.open(file_path, "rb")
        recognizer = KaldiRecognizer(model, wf.getframerate())

        # Read audio & transcribe
        text_result = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                text_result += json.loads(recognizer.Result())["text"] + " "

        print("Extracted Text:", text_result)

        return {
            "emotion": emotion['predicted_value'],
            "text": text_result
            ,
            "features": features
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")

@app.get("/record_audio")
async def record_audio_route(duration: int = Query(5, description="Duration of the recording in seconds")):
    """Records audio and extracts features."""
    try:
        filename = record_pyaudio(duration=duration)
        features = extract_features(filename)
        return {"features": features}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio recording failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5003, reload=True)

# uvicorn main:app --host 0.0.0.0 --port 5003 --reload