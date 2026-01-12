// src/clientModules/chatbot.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';
import Chatbot from '../components/Chatbot';
import './chatbot.css';

if (ExecutionEnvironment.canUseDOM) {
    const chatbotContainer = document.createElement('div');
    chatbotContainer.id = 'chatbot-container';
    document.body.appendChild(chatbotContainer);

    const root = createRoot(chatbotContainer);
    root.render(<Chatbot />);

    // Add Google Icons link to head
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0';
    document.head.appendChild(link);
}