import librosa
import numpy as np

# Function to extract features
def extract_features(file_path):
    audio, sample_rate = librosa.load(file_path, sr=16000)
    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=audio, sr=sample_rate).T, axis=0)
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=audio).T, axis=0)
    spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=audio, sr=sample_rate).T, axis=0)
    return np.hstack([mfccs, chroma, zcr, spectral_contrast])

# Function to extract features from audio waveform
def extract_features_from_waveform(waveform, sample_rate):
    audio = waveform.numpy().flatten()  # Convert PyTorch tensor to numpy array
    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=audio, sr=sample_rate).T, axis=0)
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=audio).T, axis=0)
    spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=audio, sr=sample_rate).T, axis=0)
    return np.hstack([mfccs, chroma, zcr, spectral_contrast])