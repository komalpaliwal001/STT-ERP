import { useState, useRef } from 'react';
import axios from 'axios';

const AudioRecorder = () => {
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const [emotion, setEmotion] = useState('');

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);

        mediaRecorderRef.current.start();
        setIsRecording(true);

        mediaRecorderRef.current.ondataavailable = (event) => {
            audioChunksRef.current.push(event.data);
        };

        mediaRecorderRef.current.onstop = async () => {
            const audioBlob = new Blob(audioChunksRef.current);
            const formData = new FormData();
            formData.append("audio", audioBlob);

            try {
                const response = await axios.post('http://localhost:5003/process', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
                setEmotion(response.data)
                console.log(response.data); // Handle the response data here
            } catch (error) {
                console.error("Error uploading audio:", error);
            }

            // Reset the chunks for the next recording
            audioChunksRef.current = [];
        };
    };

    const stopRecording = () => {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
    };

    return (
        <div className="audio-recoder">
            <h3 className="h3 text-3xl mb-10 ">Audio Recorder</h3>
            <button
                className="btn-default text-white p-2 rounded-lg"
                title={isRecording ? 'Stop Recording' : 'Start Recording'}
                onClick={isRecording ? stopRecording : startRecording}>
                {isRecording
                    ?
                    (<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="32" height="32" viewBox="0 0 48 48">
                        <path
                            d="M 23.919922 4 C 12.873922 4 3.9199219 12.954 3.9199219 24 C 3.9199219 35.046 12.873922 44 23.919922 44 C 34.965922 44 43.919922 35.046 43.919922 24 C 43.919922 12.954 34.965922 4 23.919922 4 z M 19.5 17 L 28.5 17 C 29.879 17 31 18.122 31 19.5 L 31 28.5 C 31 29.878 29.879 31 28.5 31 L 19.5 31 C 18.121 31 17 29.878 17 28.5 L 17 19.5 C 17 18.122 18.121 17 19.5 17 z"></path>
                    </svg>)
                    :
                    <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="32" height="32" viewBox="0 0 32 32">
                        <path
                            d="M 13 4 C 11.906937 4 11 4.9069372 11 6 L 11 18 C 11 19.093063 11.906937 20 13 20 L 19 20 C 20.093063 20 21 19.093063 21 18 L 21 6 C 21 4.9069372 20.093063 4 19 4 L 13 4 z M 13 6 L 19 6 L 19 18 L 13 18 L 13 6 z M 7 14 L 7 18 C 7 21.309 9.691 24 13 24 L 15 24 L 15 26 L 11 26 L 11 28 L 21 28 L 21 26 L 17 26 L 17 24 L 19 24 C 22.309 24 25 21.309 25 18 L 25 14 L 23 14 L 23 18 C 23 20.206 21.206 22 19 22 L 17 22 L 13 22 C 10.794 22 9 20.206 9 18 L 9 14 L 7 14 z M 16 14 A 1 1 0 0 0 16 16 A 1 1 0 0 0 16 14 z"></path>
                    </svg>
                }
            </button>
            {emotion && <div className={`emotions ${emotion}`} ></div> }
        </div>
    );
};

export default AudioRecorder;
