import React from 'react';
import clsx from 'clsx';
import { BsRobot, BsPerson } from 'react-icons/bs';

/**
 * Renders a single message bubble with distinct styling
 * for the user and the agent.
 */
export default function Message({ message }) {
  const { sender, content } = message;
  const isUser = sender === 'user';

  return (
    <div
      className={clsx('flex items-start gap-3', {
        'flex-row-reverse': isUser,
      })}
    >
      <div
        className={clsx('p-2.5 rounded-full', {
          'bg-blue-500/10 text-blue-600': isUser,
          'bg-gray-200 text-gray-600': !isUser,
        })}
      >
        {isUser ? <BsPerson size={18} /> : <BsRobot size={18} />}
      </div>
      <div
        className={clsx('rounded-lg px-4 py-3 max-w-sm shadow-sm', {
          'bg-blue-500 text-white rounded-br-none': isUser,
          'bg-white text-gray-800 border border-gray-200/80 rounded-bl-none': !isUser,
        })}
      >
        <p className="text-sm">{content}</p>
      </div>
    </div>
  );
}