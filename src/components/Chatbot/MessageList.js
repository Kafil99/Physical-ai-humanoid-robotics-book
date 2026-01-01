import React from 'react';
import Message from './Message';

/**
 * Renders the scrollable list of messages.
 * Uses React.forwardRef to allow the parent to pass a ref for auto-scrolling.
 */
const MessageList = React.forwardRef(({ messages }, ref) => {
  return (
    <div className="flex-1 p-6 overflow-y-auto bg-gray-50/50">
      <div className="space-y-6">
        {messages.map((msg) => (
          <Message key={msg.id} message={msg} />
        ))}
      </div>
      <div ref={ref} />
    </div>
  );
});

export default MessageList;