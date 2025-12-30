import React, { useState } from 'react';
import ChatWindow from './ChatWindow';
import FloatingActionButton from './FloatingActionButton';

export default function ChatContainer({ selectedText, selectionRect, setSelectedText, setSelectionRect }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    // Clear selected text when chat is closed
    if (isOpen) {
      setSelectedText(null);
      setSelectionRect(null);
    }
  };

  const handleSendMessage = async (messageText, useSelectedText = false) => {
    if (!messageText.trim()) return;

    const newMessage = { id: Date.now(), sender: 'user', content: messageText };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setLoading(true);

    const body = { question: messageText };
    if (useSelectedText && selectedText) {
      body.selected_text = selectedText;
    }

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const errorData = await response.json(); // Attempt to read error detail from backend
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const agentResponse = { id: Date.now() + 1, sender: 'agent', content: data.answer };
      setMessages((prevMessages) => [...prevMessages, agentResponse]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'agent',
        content: `Error: ${error.message}` || "Oops! Something went wrong. Please try again.",
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setLoading(false);
      setSelectedText(null); // Clear selected text after sending
      setSelectionRect(null);
    }
  };

  const handleAskAboutSelection = () => {
    setIsOpen(true); // Open chat if not already open
    handleSendMessage(selectedText, true); // Send selected text as the question
  };


  return (
    <>
      {isOpen && (
        <div className="fixed bottom-24 right-8 z-[100]">
          <ChatWindow messages={messages} onSendMessage={handleSendMessage} loading={loading} />
        </div>
      )}
      {selectedText && selectionRect && (
        <FloatingActionButton
          onClick={handleAskAboutSelection}
          style={{
            position: 'absolute',
            left: selectionRect.left,
            top: selectionRect.top - 40, // Position above the selection
            zIndex: 99, // Ensure it's above other content but below chatbot window
          }}
        >
          Ask about selection
        </FloatingActionButton>
      )}
      <button
        onClick={toggleChat}
        className="fixed bottom-8 right-8 z-[101] w-16 h-16 bg-blue-600 text-white rounded-full shadow-lg flex items-center justify-center text-3xl" // Ensure button is above chat window when closed
        aria-label="Toggle Chat"
      >
        {isOpen ? 'X' : '💬'}
      </button>
    </>
  );
}
