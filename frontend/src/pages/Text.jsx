import React, { useState } from 'react';
import './Text.css';

const Text = () => {
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [chatResponse, setChatResponse] = useState(null);
    const [error, setError] = useState(null);

    const backendUrl = process.env.REACT_APP_BACKEND_URL;

    const handleSend = async (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        setLoading(true);
        setError(null);
        setChatResponse(null);

        console.log(`Sending message to backend: "${message}"`);

        try {
            const response = await fetch(`${backendUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    model: 'llama-3.3-70b-versatile',
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Received response from /chat:', data);
            setChatResponse(data);
        } catch (err) {
            console.error('Error during send:', err);
            setError(err.message || 'Something went wrong');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="text-page-container">
            <div className="text-page-card">
                <h1 className="text-page-title">AI Chat Gateway</h1>
                <p className="text-page-subtitle">Send messages to the DhwaniAI backend service. Responses are logged to the console.</p>

                <form onSubmit={handleSend} className="text-page-form">
                    <textarea
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Type your message here..."
                        className="text-page-textarea"
                        rows={4}
                        disabled={loading}
                    />
                    <button type="submit" className="text-page-button" disabled={loading || !message.trim()}>
                        {loading ? 'Sending...' : 'Send Message'}
                    </button>
                </form>

                {error && (
                    <div className="text-page-error">
                        <strong>Error:</strong> {error}
                    </div>
                )}

                {chatResponse && (
                    <div className="text-page-success">
                        <h3>Response (Model: {chatResponse.model})</h3>
                        <p>{chatResponse.response}</p>
                        <small className="console-tip">Check your browser Developer Tools (Console) to view the raw logged object.</small>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Text;