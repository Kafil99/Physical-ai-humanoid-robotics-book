// src/components/Message.js
import React from 'react';

const Message = ({ message }) => {
    return (
        <li className={`chat ${message.role === 'user' ? 'outgoing' : 'incoming'}`}>
            <p>{message.content}</p>
        </li>
    );
};

export default Message;
