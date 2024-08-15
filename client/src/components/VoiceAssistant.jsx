import React, { useState } from 'react';
import { ReactMic } from 'react-mic';

function VoiceAssistant() {
    const [isRecording, setIsRecording] = useState(false);
    const [conversationHistory, setConversationHistory] = useState([]);
    const [error, setError] = useState(null);

    const startRecording = () => setIsRecording(true);
    const stopRecording = () => setIsRecording(false);

    const onStop = (recordedBlob) => {
        const formData = new FormData();
        formData.append('audio', recordedBlob.blob, 'audio.wav');

        fetch('http://localhost:8000/voice-assistant', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                setError(data.error);
            } else {
                setConversationHistory(data.conversation_history);
            }
        })
        .catch(error => setError("An error occurred while processing the audio."));
    }

    const clearHistory = () => {
        fetch('http://localhost:8000/clear-history', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            setConversationHistory([]);
            setError(null);
        })
        .catch(error => setError("An error occurred while clearing the history."));
    };

    return (
        // <div className='flex justify-center'>
        //     <h1 className='text-2xl font-gaegu'>Voice Assistant</h1>
        //     <ReactMic
        //         record={isRecording}
        //         onStop={onStop}
        //         strokeColor="#000000"
        //         backgroundColor="#FF4081"
        //     />
        //     <button onClick={startRecording} type="button" className='btn navlink font-gaegu py-1 px-3 mr-2'>Start Recording</button>
        //     <button onClick={stopRecording} type="button" className='btn navlink font-gaegu py-1 px-3 mr-2'>Stop Recording</button>
        //     <button onClick={clearHistory} type="button" className='btn navlink font-gaegu py-1 px-3'>Clear History</button>

        //     {error && <p style={{ color: 'red' }}>{error}</p>}
        //     <div>
        //         <h2 className='text-2xl font-gaegu'>Conversation History:</h2>
        //         {conversationHistory.map((message, index) => (
        //             <div key={index}>
        //                 <strong>{message.role === 'user' ? 'User' : 'Assistant'}:</strong> {message.content}
        //             </div>
        //         ))}
        //     </div>
        // </div>
        <div className="flex flex-col items-center mx-auto mt-16">
    <h1 className="text-2xl font-gaegu mb-4">Voice Assistant</h1>
    <ReactMic
        record={isRecording}
        onStop={onStop}
        strokeColor="#000000"
        backgroundColor="#FF4081"
        className="mb-4"
    />
    <div className="flex mb-4">
        <button onClick={startRecording} type="button" className="btn navlink font-gaegu py-1 px-3 mr-2">Start Recording</button>
        <button onClick={stopRecording} type="button" className="btn navlink font-gaegu py-1 px-3 mr-2">Stop Recording</button>
        <button onClick={clearHistory} type="button" className="btn navlink font-gaegu py-1 px-3">Clear History</button>
    </div>
    {error && <p className="text-red-500 mb-4">{error}</p>}
    <div className="text-left w-full max-w-lg">
        <h2 className="text-2xl font-gaegu mb-4">Conversation History:</h2>
        {conversationHistory.map((message, index) => (
            <div key={index} className="mb-2 font-gaegu text-xl">
                <strong className={`${
      message.role === 'user' ? 'bg-yellow-100' : 'bg-blue-100'
    } p-1 rounded`}>{message.role === 'user' ? 'You' : 'Assistant'}:</strong> {message.content}
            </div>
        ))}
    </div>
</div>

    );
}

export default VoiceAssistant;


