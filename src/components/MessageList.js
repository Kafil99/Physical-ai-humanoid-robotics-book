// src/components/MessageList.js
import React from 'react';
import Message from './Message';

const MessageList = ({ messages, chatboxRef }) => {
    return (
        <ul className="chatbox" ref={chatboxRef}>
            <li className="chat incoming">
                <p>Hello 👋<br/>How can I help you today?</p>
            </li>
            {messages.map((msg, index) => (
                <Message key={index} message={msg} />
            ))}
        </ul>
    );
};

export default MessageList;
