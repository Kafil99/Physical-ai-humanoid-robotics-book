import React from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';

export default function ChatWindow({ messages, onSendMessage, loading }) {
  return (
    <div className="w-96 h-[32rem] bg-white rounded-lg shadow-xl flex flex-col">
      <div className="p-4 bg-gray-100 rounded-t-lg">
        <h2 className="text-lg font-semibold">Chat with the book</h2>
      </div>
      <MessageList messages={messages} />
      <ChatInput onSendMessage={onSendMessage} loading={loading} />
    </div>
  );
}
