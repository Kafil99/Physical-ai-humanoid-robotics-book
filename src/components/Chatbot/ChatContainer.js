import React, { useState, useEffect } from 'react';
import ChatWindow from './ChatWindow';
import FloatingActionButton from './FloatingActionButton';
import { BsChatDots, BsX } from 'react-icons/bs';

/**
 * The single root component for the chatbot UI system.
 * It handles all state, including visibility (isOpen), messages, and text selection.
 * Its direct child, the main div, establishes the fixed positioning context.
 */
export default function ChatContainer() {
  // Single source of truth for chat window visibility. Defaults to closed.
  const [isOpen, setIsOpen] = useState(false);
  
  const [messages, setMessages] = useState([
    { id: 'init', sender: 'agent', content: 'Hello! Ask me a question, or select text from the book to get an explanation.' }
  ]);
  const [loading, setLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(null);
  const [selectionRect, setSelectionRect] = useState(null);
  const [isContextPrimed, setIsContextPrimed] = useState(false);

  // Reliable text selection listener
  useEffect(() => {
    const handleMouseUp = (event) => {
      // Prevents the chatbot UI from triggering text selection for itself
      if (event.target.closest('.chatbot-container')) {
        return;
      }
      const text = window.getSelection().toString().trim();
      if (text.length > 15) { // Sensible minimum selection length
        const range = window.getSelection().getRangeAt(0);
        const rect = range.getBoundingClientRect();
        setSelectedText(text);
        setSelectionRect({ left: rect.left + window.scrollX, top: rect.top + window.scrollY });
        setIsContextPrimed(false); // A new selection always requires re-priming
      } else {
        setSelectedText(null);
        setSelectionRect(null);
      }
    };
    document.addEventListener('mouseup', handleMouseUp);
    return () => document.removeEventListener('mouseup', handleMouseUp);
  }, []);

  // Handles sending the message to the backend
  const handleSendMessage = async (messageText) => {
    if (!messageText.trim() || loading) return;

    setMessages((prev) => [...prev, { id: Date.now(), sender: 'user', content: messageText }]);
    setLoading(true);

    const payload = {
      question: messageText,
      selected_text: isContextPrimed ? selectedText : null,
    };

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Backend error: ${response.status}`);
      }
      const data = await response.json();
      setMessages((prev) => [...prev, { id: Date.now() + 1, sender: 'agent', content: data.answer }]);
    } catch (error) {
      setMessages((prev) => [...prev, { id: Date.now() + 1, sender: 'agent', content: `Sorry, an error occurred: ${error.message}` }]);
    } finally {
      setLoading(false);
      setSelectedText(null);
      setSelectionRect(null);
      setIsContextPrimed(false);
    }
  };
  
  // Primes the chat with the selected text when the floating button is clicked
  const handlePrimeContext = () => {
    if (!selectedText) return;
    setIsContextPrimed(true);
    setIsOpen(true);
  };
  
  // Clears the selected text indicator from the chat window
  const clearSelection = () => {
    setSelectedText(null);
    setSelectionRect(null);
    setIsContextPrimed(false);
  }

  return (
    <div className="chatbot-container">
      {/* "Ask about selection" button - appears near the selected text */}
      {selectedText && !isContextPrimed && (
        <FloatingActionButton
          onClick={handlePrimeContext}
          style={{
            position: 'absolute', // Positioned relative to viewport via parent
            left: `${selectionRect.left}px`,
            top: `${selectionRect.top - 45}px`,
            zIndex: 9998, // High z-index
          }}
        >
          Ask about this
        </FloatingActionButton>
      )}
      
      {/* Main Container for Chat Window and Toggle Button */}
      <div className="fixed bottom-6 right-6 z-[9999]">
        {/* Chat Window with smooth transitions */}
        <div
          className={`transition-all duration-300 ease-in-out mb-4 ${isOpen ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'}`}
        >
          <ChatWindow
              messages={messages}
              onSendMessage={handleSendMessage}
              loading={loading}
              selectedText={isContextPrimed ? selectedText : null}
              clearSelectedText={clearSelection}
          />
        </div>

        {/* Main Chat Toggle Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-16 h-16 bg-blue-600 text-white rounded-full shadow-2xl flex items-center justify-center text-3xl hover:bg-blue-700 transition-all duration-200 transform hover:scale-110"
          aria-label="Toggle Chat"
        >
          {isOpen ? <BsX size={32} /> : <BsChatDots size={28} />}
        </button>
      </div>
    </div>
  );
}