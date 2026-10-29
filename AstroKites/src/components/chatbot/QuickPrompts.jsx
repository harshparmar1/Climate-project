import React from 'react';

const SUGGESTIONS = [
  "Which crops grow in Gujarat?",
  "What is the temperature in Ahmedabad?",
  "Will it rain tomorrow in Mumbai?",
  "Best crops for Maharashtra climate",
  "Explain T2M metric",
  "Compare temperature: Ahmedabad vs Mumbai"
];

export default function QuickPrompts({ onSelectPrompt }) {
  return (
    <div className="quick-prompts-container" aria-label="Suggested questions">
      {SUGGESTIONS.map((prompt, idx) => (
        <button
          key={idx}
          className="quick-prompt-chip"
          onClick={() => onSelectPrompt(prompt)}
          type="button"
        >
          {prompt}
        </button>
      ))}
    </div>
  );
}
