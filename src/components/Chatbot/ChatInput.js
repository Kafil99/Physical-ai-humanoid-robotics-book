import React, { useState } from 'react';

export default function ChatInput({ onSendMessage, loading }) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    onSendMessage(inputValue);
    setInputValue('');
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-gray-100 rounded-b-lg">
      <div className="flex">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 border rounded-l-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 rounded-r-lg hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </form>
  );
}
