// src/components/Chatbot.js
import React, { useState, useEffect } from 'react';
import FloatingIcon from './FloatingIcon';
import ChatWindow from './ChatWindow';

const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        if (isOpen) {
            document.body.classList.add('show-chatbot');
        } else {
            document.body.classList.remove('show-chatbot');
        }
    }, [isOpen]);

    return (
        <>
            <FloatingIcon onClick={() => setIsOpen(!isOpen)} isOpen={isOpen} />
            <ChatWindow isOpen={isOpen} onClose={() => setIsOpen(false)} />
        </>
    );
};

export default Chatbot;