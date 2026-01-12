// src/components/ChatWindow.js
import React, { useState, useEffect, useRef } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatWindow = ({ isOpen, onClose }) => {
    const [messages, setMessages] = useState([]);
    const [selectedText, setSelectedText] = useState('');
    const chatboxRef = useRef(null);

    const API_URL = "http://localhost:8000/chat";

    // This effect now correctly captures text selection without accidentally clearing it.
    useEffect(() => {
        const handleSelection = () => {
            const text = window.getSelection().toString().trim();
            if (text) {
                setSelectedText(text);
            }
        };

        document.addEventListener('mouseup', handleSelection);
        return () => document.removeEventListener('mouseup', handleSelection);
    }, []);

    useEffect(() => {
        if (chatboxRef.current) {
            chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
        }
    }, [messages]);
    
    // This function will be called by the MessageInput component
    const clearSelectedText = () => {
        setSelectedText('');
    }

    const handleSendMessage = async (inputValue) => {
        if (!inputValue.trim()) return;

        const question = inputValue.trim();
        const userMessage = { role: 'user', content: question };
        setMessages(prev => [...prev, userMessage]);

        setTimeout(() => {
            const thinkingMessage = { role: 'assistant', content: 'Thinking...' };
            setMessages(prev => [...prev, thinkingMessage]);
            if (chatboxRef.current) {
                chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
            }
        }, 600);


        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: question,
                    selected_text: selectedText || null, // The selected text is now reliably sent
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const assistantMessage = { role: 'assistant', content: data.answer };
            
            setMessages(prev => prev.filter(msg => msg.content !== 'Thinking...'));
            setMessages(prev => [...prev, assistantMessage]);

        } catch (error) {
            const errorMessage = { role: 'assistant', content: 'Oops! Something went wrong. Please try again.' };
            setMessages(prev => prev.filter(msg => msg.content !== 'Thinking...'));
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            // The selection is now correctly cleared only after the message is sent.
            setSelectedText(''); 
        }
    };

    return (
        <div className={`chatbot ${isOpen ? 'show-chatbot' : ''}`}>
            <header className="chatbot-header">
                <h2>Chatbot</h2>
                <span className="chatbot-close-btn material-symbols-outlined" onClick={onClose}>close</span>
            </header>
            <MessageList messages={messages} chatboxRef={chatboxRef} />
            <MessageInput 
                onSendMessage={handleSendMessage} 
                selectedText={selectedText}
                clearSelectedText={clearSelectedText}
            />
        </div>
    );
};

export default ChatWindow;
