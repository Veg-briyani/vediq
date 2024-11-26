// src/lib/calculations/predictions.ts
import { BirthChart, PlanetaryPosition } from '@/types/astrology';

export class PredictionCalculator {
  static generatePredictions(birthChart: BirthChart, transits: Record<string, PlanetaryPosition>): string[] {
    const predictions: string[] = [];
    
    // House lords in their houses
    Object.entries(birthChart.planets).forEach(([planet, position]) => {
      const houseLord = AstrologyCalculator.getSignLord(position.sign);
      if (houseLord === planet) {
        predictions.push(`${planet} is lord of its own house, indicating strong ${this.getHouseSignificance(position.house)}`);
      }
    });

    // Transit impacts
    Object.entries(transits).forEach(([planet, position]) => {
      const natalPosition = birthChart.planets[planet as keyof typeof birthChart.planets];
      if (position.house !== natalPosition.house) {
        predictions.push(`Transiting ${planet} in house ${position.house} affects ${this.getHouseSignificance(position.house)}`);
      }
    });

    return predictions;
  }

  private static getHouseSignificance(house: number): string {
    const significances = {
      1: "personality and self-expression",
      2: "finances and values",
      3: "communication and siblings",
      // ... add other houses
    };
    return significances[house] || "";
  }
}