import React, { useState } from 'react';
import { BsSend, BsArrowRepeat } from 'react-icons/bs';

/**
 * Renders the input field and send button at the bottom of the chat window.
 */
export default function ChatInput({ onSendMessage, loading }) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim() || loading) return;
    onSendMessage(inputValue);
    setInputValue('');
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-white border-t border-gray-200 rounded-b-xl">
      <div className="flex items-center gap-3">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 w-full border-gray-300 rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
          disabled={loading}
        />
        <button
          type="submit"
          className="w-12 h-12 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed flex items-center justify-center transition-colors"
          disabled={loading}
          aria-label="Send message"
        >
          {loading ? <BsArrowRepeat className="animate-spin" size={20} /> : <BsSend size={18} />}
        </button>
      </div>
    </form>
  );
}