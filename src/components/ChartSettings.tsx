// src/components/ChartSettings.tsx
import React from 'react';

interface ChartSettingsProps {
  onSettingsChange: (settings: ChartSettings) => void;
}

interface ChartSettings {
  showAspects: boolean;
  aspectOrb: number;
  houseSystem: 'placidus' | 'equal' | 'whole';
  zodiacType: 'tropical' | 'sidereal';
}

export default function ChartSettings({ onSettingsChange }: ChartSettingsProps) {
  const [settings, setSettings] = React.useState<ChartSettings>({
    showAspects: true,
    aspectOrb: 6,
    houseSystem: 'placidus',
    zodiacType: 'tropical'
  });

  // Component implementation...
}