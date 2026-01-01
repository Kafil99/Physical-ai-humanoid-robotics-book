import React from 'react';

/**
 * Renders the small button that appears near selected text.
 */
export default function FloatingActionButton({ onClick, style }) {
  return (
    <button
      onClick={onClick}
      className="absolute bg-gray-800 text-white text-xs font-semibold px-3 py-1.5 rounded-lg shadow-lg hover:bg-black transition-all"
      style={style}
    >
      Ask about this
    </button>
  );
}