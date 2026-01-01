import React from 'react';
import { createRoot } from 'react-dom/client';
import ChatContainer from '@site/src/components/Chatbot/ChatContainer';

/**
 * This client module creates a dedicated DOM node outside of Docusaurus's main
 * React tree to ensure the chatbot is not affected by parent CSS stacking contexts.
 * This is the definitive fix for the "chatbot under footer" issue.
 */
export default (function () {
  if (typeof window === 'undefined') {
    return null;
  }

  // Create a dedicated root element for the chatbot
  const chatbotRootEl = document.createElement('div');
  chatbotRootEl.id = 'chatbot-root-container';
  document.body.appendChild(chatbotRootEl);

  // Use createRoot to render the chatbot into the isolated element
  const root = createRoot(chatbotRootEl);
  root.render(<ChatContainer />);

  return null;
})();
