# import sounddevice as sd
import numpy as np
import pyaudio
import wave

# def record_audio(duration=5, sample_rate=16000, filename="recorded_audio.wav"):
#     """
#     Records audio in real-time and saves it as a WAV file.
#     """
#     print("Recording... Speak now!")
#     audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
#     sd.wait()  # Wait until the recording is finished
#     print("Recording finished.")
#
#     # Save audio data as a WAV file
#     audio_data = (audio_data * 32767).astype(np.int16)  # Convert to int16 for WAV format
#     with wave.open(filename, 'wb') as wf:
#         wf.setnchannels(1)  # Mono channel
#         wf.setsampwidth(2)  # 2 bytes per sample
#         wf.setframerate(sample_rate)
#         wf.writeframes(audio_data.tobytes())
#     return filename

def record_pyaudio(duration=5, sample_rate=16000, filename="recorded_audio.wav"):
    """
    Records audio in real-time and saves it as a WAV file using PyAudio.
    """
    # Audio format settings
    channels = 1  # Mono sound
    audio_format = pyaudio.paInt16  # 16-bit int format
    frames_per_buffer = 1024  # Buffer size

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open the microphone for streaming input
    stream = audio.open(format=audio_format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=frames_per_buffer)

    print("Recording... Speak now!")

    frames = []
    # Read audio input from the microphone for the specified duration
    for _ in range(0, int(sample_rate / frames_per_buffer * duration)):
        data = stream.read(frames_per_buffer)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recorded frames as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    return filename