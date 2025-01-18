import librosa
import numpy as np

# Function to extract features from an audio file
def extract_features(file_path):
    """
    Extract audio features (MFCCs, Chroma, ZCR, Spectral Contrast) from an audio file.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        np.ndarray: Combined features as a single numpy array.
    """
    try:
        # Load the audio file
        audio, sample_rate = librosa.load(file_path, sr=16000)

        # Extract features
        mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13).T, axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(y=audio, sr=sample_rate).T, axis=0)
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=audio).T, axis=0)
        spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=audio, sr=sample_rate).T, axis=0)

        # Combine all features into a single array
        return np.hstack([mfccs, chroma, zcr, spectral_contrast])

    except FileNotFoundError:
        raise FileNotFoundError(f"The audio file at '{file_path}' was not found.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while extracting features: {str(e)}")


# Function to extract features from an audio waveform
def extract_features_from_waveform(waveform, sample_rate=16000):
    """
    Extract audio features (MFCCs, Chroma, ZCR, Spectral Contrast) from a waveform.

    Args:
        waveform (np.ndarray): Audio waveform as a numpy array.
        sample_rate (int): Sample rate of the waveform (default: 16000).

    Returns:
        np.ndarray: Combined features as a single numpy array.
    """
    try:
        # Ensure waveform is a flattened numpy array
        audio = waveform.flatten()

        # Extract features
        mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13).T, axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(y=audio, sr=sample_rate).T, axis=0)
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=audio).T, axis=0)
        spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=audio, sr=sample_rate).T, axis=0)

        # Combine all features into a single array
        return np.hstack([mfccs, chroma, zcr, spectral_contrast])

    except Exception as e:
        raise RuntimeError(f"An error occurred while extracting features from waveform: {str(e)}")
