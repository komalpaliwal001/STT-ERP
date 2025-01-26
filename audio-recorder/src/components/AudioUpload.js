// src/AudioUpload.js

import React, { useState } from 'react';
import axios from 'axios';

const AudioUpload = () => {
    const [audioFile, setAudioFile] = useState(null);

    const handleFileChange = (event) => {
        setAudioFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!audioFile) {
            alert("Please select an audio file first!");
            return;
        }

        const formData = new FormData();
        formData.append('audio', audioFile);

        try {
            const response = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log(response.data); // Handle response data here
            alert(`Prediction: ${response.data.prediction}`);
        } catch (error) {
            console.error("Error uploading audio:", error);
            alert("Error uploading audio");
        }
    };

    return (
        <div>
            <h3>Upload Audio</h3>
            <input type="file" accept="audio/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
        </div>
    );
};

export default AudioUpload;
