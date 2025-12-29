import React from 'react';
import clsx from 'clsx';

export default function Message({ message }) {
  const { sender, content } = message;
  const isUser = sender === 'user';

  return (
    <div
      className={clsx('flex mb-4', {
        'justify-end': isUser,
        'justify-start': !isUser,
      })}
    >
      <div
        className={clsx('rounded-lg px-4 py-2 max-w-xs', {
          'bg-blue-500 text-white': isUser,
          'bg-gray-200 text-gray-800': !isUser,
        })}
      >
        {content}
      </div>
    </div>
  );
}
