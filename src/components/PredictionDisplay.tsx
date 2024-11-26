// src/components/PredictionDisplay.tsx
import React from 'react';

interface PredictionDisplayProps {
  predictions: string[];
}

export default function PredictionDisplay({ predictions }: PredictionDisplayProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Predictions</h2>
      <ul className="space-y-2">
        {predictions.map((prediction, index) => (
          <li key={index} className="text-sm">{prediction}</li>
        ))}
      </ul>
    </div>
  );
}