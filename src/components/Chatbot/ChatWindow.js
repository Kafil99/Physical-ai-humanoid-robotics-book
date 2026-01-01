import React, { useEffect, useRef } from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import { BsRobot, BsPaperclip, BsX } from 'react-icons/bs';

/**
 * Renders the main chat window panel, including the header,
 * message list, and input area.
 */
export default function ChatWindow({ messages, onSendMessage, loading, selectedText, clearSelectedText }) {
  const messagesEndRef = useRef(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="w-96 h-[70vh] max-h-[700px] bg-white rounded-xl shadow-2xl flex flex-col border border-gray-200/80">
      {/* Header */}
      <div className="p-4 bg-gray-50 border-b border-gray-200 rounded-t-xl flex items-center space-x-3">
        <div className="p-2 bg-blue-100 rounded-full">
          <BsRobot className="text-blue-600" size={20} />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-gray-800">Robotics Book AI</h2>
          <p className="text-xs text-gray-500">Your assistant for the book</p>
        </div>
      </div>

      {/* Message List */}
      <MessageList messages={messages} ref={messagesEndRef} />

      {/* Selected Text Indicator */}
      {selectedText && (
        <div className="p-3 bg-blue-50 border-t border-b border-blue-200 text-xs text-blue-800 flex justify-between items-center">
          <div className="flex items-center min-w-0">
            <BsPaperclip className="mr-2 flex-shrink-0" />
            <p className="truncate font-medium">Using selected text: "{selectedText}"</p>
          </div>
          <button onClick={clearSelectedText} className="p-1 rounded-full hover:bg-blue-200 ml-2">
            <BsX className="text-blue-800" />
          </button>
        </div>
      )}

      {/* Input Area */}
      <ChatInput onSendMessage={onSendMessage} loading={loading} />
    </div>
  );
}