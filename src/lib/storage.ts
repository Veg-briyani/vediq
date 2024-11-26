// src/lib/storage.ts
import { BirthChart } from '@/types/astrology';

export const storageHelper = {
  saveChart(birthChart: BirthChart): void {
    try {
      localStorage.setItem('birthChart', JSON.stringify(birthChart));
    } catch (error) {
      console.error('Failed to save chart:', error);
    }
  },

  loadChart(): BirthChart | null {
    try {
      const data = localStorage.getItem('birthChart');
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Failed to load chart:', error);
      return null;
    }
  }
};