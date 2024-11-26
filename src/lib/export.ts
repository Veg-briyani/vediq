// src/lib/export.ts
import { BirthChart } from '@/types/astrology';

export const exportHelper = {
  exportChart(birthChart: BirthChart): void {
    const dataStr = JSON.stringify(birthChart, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `birth-chart-${birthChart.datetime}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  },

  async importChart(file: File): Promise<BirthChart> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const chart = JSON.parse(e.target?.result as string);
          resolve(chart);
        } catch (error) {
          reject(new Error('Invalid chart file'));
        }
      };
      reader.onerror = () => reject(new Error('Failed to read file'));
      reader.readAsText(file);
    });
  }
};