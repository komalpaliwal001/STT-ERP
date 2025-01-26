import React from 'react';
import AudioRecorder from './components/AudioRecorder';
import AudioUpload from './components/AudioUpload';

function App() {
    return (
        <div className="App">
            <div className="container">
                <h1 className="text-4xl text-white font-bold">Speech-to-Text and Emotion Recognition from Audio</h1>
                <AudioRecorder />
                <AudioUpload />
            </div>
        </div>
    );
}

export default App;
