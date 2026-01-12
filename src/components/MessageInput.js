// src/components/MessageInput.js
import React, { useState, useEffect } from 'react';

const MessageInput = ({ onSendMessage, selectedText, clearSelectedText }) => {
    const [inputValue, setInputValue] = useState('');

    // When a selection is made, pre-fill the input to guide the user.
    useEffect(() => {
        if (selectedText) {
            setInputValue("What is this about?");
        }
    }, [selectedText]);

    const handleSend = () => {
        if (!inputValue.trim()) return;
        onSendMessage(inputValue);
        setInputValue('');
    };
    
    const handleClearSelection = (e) => {
        e.stopPropagation();
        clearSelectedText();
        setInputValue('');
    }

    return (
        <div className="chat-input-container">
            {selectedText && (
                <div className="selected-text-bar">
                    <p className="text-black">Ask about your selected text:</p>
                    <button onClick={handleClearSelection} className="clear-selection-btn">
                        &times;
                    </button>
                </div>
            )}
            <div className="chat-input">
                <textarea 
                    placeholder={selectedText ? "e.g., Summarize this..." : "Enter a message..."}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
                    required
                />
                <span id="send-btn" className="material-symbols-outlined" onClick={handleSend}>send</span>
            </div>
        </div>
    );
};

export default MessageInput;