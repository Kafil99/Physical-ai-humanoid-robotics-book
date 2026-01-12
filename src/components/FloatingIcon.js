// src/components/FloatingIcon.js
import React from 'react';

const FloatingIcon = ({ onClick, isOpen }) => {
    return (
        <button className="chatbot-toggler" onClick={onClick}>
            <span className="material-symbols-outlined">{isOpen ? 'close' : 'chat_bubble'}</span>
        </button>
    );
};

export default FloatingIcon;
