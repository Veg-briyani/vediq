import React from 'react';
import { BirthChart, PlanetaryPosition } from '@/types/astrology';

interface BirthChartProps {
  data: BirthChart;
  className?: string;
}

export default function BirthChartVisualization({ data, className = '' }: BirthChartProps) {
  // Constants for SVG dimensions and calculations
  const SIZE = 600;
  const CENTER = SIZE / 2;
  const RADIUS = SIZE * 0.45;

  // Calculate position for a planet in the chart
  const calculatePlanetPosition = (position: PlanetaryPosition) => {
    const angle = ((position.longitude - data.planets.ascendant.longitude + 360) % 360);
    const radians = (angle - 90) * (Math.PI / 180);
    const distance = RADIUS * 0.8; // Place planets at 80% of radius
    
    return {
      x: CENTER + distance * Math.cos(radians),
      y: CENTER + distance * Math.sin(radians),
      angle
    };
  };

  // Draw the basic chart structure
  const renderChartStructure = () => (
    <>
      {/* Main square */}
      <rect 
        x="0" 
        y="0" 
        width={SIZE} 
        height={SIZE} 
        fill="none" 
        stroke="black" 
        strokeWidth="2"
      />
      
      {/* Diagonal lines */}
      <line 
        x1="0" 
        y1="0" 
        x2={SIZE} 
        y2={SIZE} 
        stroke="black" 
      />
      <line 
        x1="0" 
        y1={SIZE} 
        x2={SIZE} 
        y2="0" 
        stroke="black" 
      />
      
      {/* Central square */}
      <rect
        x={CENTER - RADIUS/2}
        y={CENTER - RADIUS/2}
        width={RADIUS}
        height={RADIUS}
        fill="none"
        stroke="black"
      />
    </>
  );

  // Render a single planet
  const renderPlanet = (planet: keyof BirthChart['planets'], position: PlanetaryPosition) => {
    const { x, y, angle } = calculatePlanetPosition(position);
    const symbol = planet.charAt(0).toUpperCase() + planet.slice(1, 3);

    return (
      <g key={planet} transform={`translate(${x},${y})`}>
        <circle r="15" fill="white" stroke="black" />
        <text
          textAnchor="middle"
          dy=".3em"
          className="text-xs font-bold"
        >
          {symbol}
        </text>
      </g>
    );
  };

  // Render house numbers
  const renderHouseNumbers = () => {
    return Array.from({ length: 12 }, (_, i) => {
      const angle = (i * 30 - 90) * (Math.PI / 180);
      const x = CENTER + RADIUS * 0.9 * Math.cos(angle);
      const y = CENTER + RADIUS * 0.9 * Math.sin(angle);
      
      return (
        <text
          key={i}
          x={x}
          y={y}
          textAnchor="middle"
          dy=".3em"
          className="text-sm fill-gray-600"
        >
          {i + 1}
        </text>
      );
    });
  };

  return (
    <div className={`relative ${className}`}>
      <svg
        viewBox={`0 0 ${SIZE} ${SIZE}`}
        className="w-full h-full"
      >
        {renderChartStructure()}
        {renderHouseNumbers()}
        {Object.entries(data.planets).map(([planet, position]) => 
          renderPlanet(planet as keyof BirthChart['planets'], position)
        )}
      </svg>
    </div>
  );
}