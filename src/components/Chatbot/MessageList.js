import React from 'react';
import Message from './Message';

export default function MessageList({ messages }) {
  // Dummy messages for now
  // const messages = [
  //   { id: 1, sender: 'agent', content: 'Hello! Ask me anything about the book.' },
  //   { id: 2, sender: 'user', content: 'What is a URDF?' },
  // ];

  return (
    <div className="flex-1 p-4 overflow-y-auto">
      {messages.map(msg => <Message key={msg.id} message={msg} />)}
    </div>
  );
}
