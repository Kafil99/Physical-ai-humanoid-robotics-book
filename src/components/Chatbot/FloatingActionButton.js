import React from 'react';

export default function FloatingActionButton({ onClick, children, style }) {
  return (
    <button
      onClick={onClick}
      className="absolute bg-blue-500 text-white text-xs px-2 py-1 rounded shadow-md hover:bg-blue-600 z-50"
      style={style}
    >
      {children}
    </button>
  );
}
