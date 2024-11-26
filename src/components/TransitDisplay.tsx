// src/components/TransitDisplay.tsx

import React from 'react';
import { PlanetaryPosition } from '@/types/astrology';

interface TransitDisplayProps {
  birthPositions: Record<string, PlanetaryPosition>;
  transitPositions: Record<string, PlanetaryPosition>;
  className?: string;
}

export default function TransitDisplay({
  birthPositions,
  transitPositions,
  className = ''
}: TransitDisplayProps) {
  const formatDegrees = (pos: PlanetaryPosition) => {
    return `${pos.degree}° ${pos.minutes.toString().padStart(2, '0')}'`;
  };

  return (
    <div className={`overflow-x-auto ${className}`}>
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-gray-100 dark:bg-gray-800">
            <th className="px-4 py-2 text-left">Planet</th>
            <th className="px-4 py-2 text-left">Natal Position</th>
            <th className="px-4 py-2 text-left">Transit Position</th>
            <th className="px-4 py-2 text-left">Movement</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(transitPositions).map(([planet, transitPos]) => {
            const birthPos = birthPositions[planet];
            const movement = ((transitPos.longitude - birthPos.longitude + 360) % 360);
            
            return (
              <tr key={planet} className="border-b dark:border-gray-700">
                <td className="px-4 py-2 capitalize">{planet}</td>
                <td className="px-4 py-2">
                  {formatDegrees(birthPos)} in {birthPos.sign}
                </td>
                <td className="px-4 py-2">
                  {formatDegrees(transitPos)} in {transitPos.sign}
                </td>
                <td className="px-4 py-2">
                  {movement.toFixed(2)}°
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}