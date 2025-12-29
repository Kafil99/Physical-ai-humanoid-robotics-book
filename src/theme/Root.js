import React, { useState, useEffect } from 'react';
import ChatContainer from '@site/src/components/Chatbot/ChatContainer';

export default function Root({children}) {
  const [selectedText, setSelectedText] = useState(null);
  const [selectionRect, setSelectionRect] = useState(null);

  useEffect(() => {
    const handleMouseUp = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();
      if (text.length > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        setSelectedText(text);
        setSelectionRect({
          left: rect.left + window.scrollX,
          top: rect.top + window.scrollY,
          width: rect.width,
          height: rect.height,
        });
      } else {
        setSelectedText(null);
        setSelectionRect(null);
      }
    };

    document.addEventListener('mouseup', handleMouseUp);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  return (
    <>
      {children}
      <ChatContainer selectedText={selectedText} selectionRect={selectionRect} setSelectedText={setSelectedText} setSelectionRect={setSelectionRect} />
    </>
  );
}
