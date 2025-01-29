import librosa
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import torchaudio
import torch
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForCTC

def extract_tensorflow_embeddings(audio_path, max_length=123):
    """
    Extract TensorFlow embeddings from an audio file using a pre-trained speech embedding model.
    
    Args:
        audio_path (str): Path to the audio file.
        max_length (int): Maximum length for the embeddings (default is 123).

    Returns:
        np.ndarray: Processed embeddings as a numpy array.
    """
    try:
        # Load the audio file
        audio, rate = librosa.load(audio_path, sr=16000)
        
        # Ensure the input audio is in the correct shape (batch size, time)
        audio_tensor = tf.constant(audio[np.newaxis, :], dtype=tf.float32)

        # Load the pre-trained speech embedding model from TensorFlow Hub
        model_url = "https://tfhub.dev/google/speech_embedding/1"
        model = hub.load(model_url)

        # Use the model's default signature to extract embeddings
        if "default" in model.signatures:
            embeddings = model.signatures["default"](audio_tensor)["default"]
        else:
            raise ValueError("The model does not have a callable default signature.")
        
        # Convert embeddings to numpy array and reshape
        embeddings = embeddings.numpy().squeeze()  # Remove batch and channel dimensions
        
        # Handle the case where embeddings have extra dimensions (e.g., (123, 1, 96))
        if len(embeddings.shape) == 3:
            embeddings = embeddings[:, 0, :]  # Remove the extra dimension
        
        # Pad or truncate embeddings to ensure uniform shape
        if embeddings.shape[0] < max_length:
            padding = np.zeros((max_length - embeddings.shape[0], embeddings.shape[1]))
            embeddings = np.vstack([embeddings, padding])  # Pad with zeros
        elif embeddings.shape[0] > max_length:
            embeddings = embeddings[:max_length, :]  # Truncate to max_length
        
        return embeddings
    
    except FileNotFoundError:
        raise FileNotFoundError(f"The audio file at path '{audio_path}' was not found.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while extracting embeddings: {str(e)}")


# Define a function to predict emotion from audio
def predict_emotion(audio_path):
    # Load the audio file
    audio, rate = librosa.load(audio_path, sr=16000)

    # Load the pre-trained model and feature extractor
    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("r-f/wav2vec-english-speech-emotion-recognition")
    model = Wav2Vec2ForCTC.from_pretrained("r-f/wav2vec-english-speech-emotion-recognition")

    # Print available labels for debugging
    # print("Available labels:", model.config.id2label)
    
    # Extract features
    inputs = feature_extractor(audio, sampling_rate=rate, return_tensors="pt", padding=True)
    
    # Make predictions
    with torch.no_grad():
        outputs = model(inputs.input_values)
    
    # Process predictions
    predictions = torch.nn.functional.softmax(outputs.logits.mean(dim=1), dim=-1)  # Average over sequence length
    predicted_label = torch.argmax(predictions, dim=-1)

    # Check if predicted label exists in id2label mapping
    try:
        emotion = model.config.id2label[predicted_label.item()]
    except KeyError:
        print(f"KeyError: Predicted label {predicted_label.item()} not found in id2label.")
        return None
    
    return emotion
