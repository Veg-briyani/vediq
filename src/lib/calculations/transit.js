// src/lib/calculations/transit.ts

import { CelestialPosition, PlanetaryPosition } from '@/types/astrology';
import { AstrologyCalculator } from './core';

export class TransitCalculator {
  // Mean daily motions of planets in degrees
  private static readonly DAILY_MOTION = {
    sun: 0.9856,
    moon: 13.1763,
    mars: 0.5240,
    mercury: 1.3833,
    venus: 1.2097,
    jupiter: 0.0831,
    saturn: 0.0334,
    rahu: -0.0529,
    ketu: -0.0529
  };

  static calculateTransitPosition(
    birthPosition: PlanetaryPosition,
    transitDate: Date,
    birthDate: Date
  ): PlanetaryPosition {
    const daysDiff = this.daysBetween(birthDate, transitDate);
    const motion = this.DAILY_MOTION[birthPosition.planet as keyof typeof this.DAILY_MOTION];
    
    // Calculate new longitude
    let newLongitude = birthPosition.longitude + (motion * daysDiff);
    newLongitude = ((newLongitude % 360) + 360) % 360;

    // Calculate new position details
    const { nakshatra, pada } = AstrologyCalculator.calculateNakshatra(newLongitude);
    const sign = AstrologyCalculator.calculateSign(newLongitude);
    const { degrees, minutes } = AstrologyCalculator.decimalToDMS(newLongitude % 30);

    return {
      ...birthPosition,
      longitude: newLongitude,
      sign,
      nakshatra,
      nakshatraPada: pada,
      degree: degrees,
      minutes: minutes,
      house: AstrologyCalculator.calculateHouse(newLongitude, birthPosition.longitude)
    };
  }

  private static daysBetween(date1: Date, date2: Date): number {
    const oneDay = 24 * 60 * 60 * 1000;
    return Math.round(Math.abs((date2.getTime() - date1.getTime()) / oneDay));
  }

  static calculateAllTransits(
    birthChart: BirthChart,
    transitDate: Date
  ): Record<string, PlanetaryPosition> {
    const birthDate = new Date(birthChart.datetime);
    const transits: Record<string, PlanetaryPosition> = {};

    for (const [planet, position] of Object.entries(birthChart.planets)) {
      if (planet !== 'ascendant') {
        transits[planet] = this.calculateTransitPosition(
          position,
          transitDate,
          birthDate
        );
      } else {
        transits[planet] = position; // Ascendant doesn't transit
      }
    }

    return transits;
  }

  static calculateTransitAspects(
    birthChart: BirthChart,
    transitPositions: Record<string, PlanetaryPosition>
  ): Array<TransitAspect> {
    const aspects: TransitAspect[] = [];
    
    for (const [transitPlanet, transitPos] of Object.entries(transitPositions)) {
      if (transitPlanet === 'ascendant') continue;

      for (const [natalPlanet, natalPos] of Object.entries(birthChart.planets)) {
        const aspect = this.calculateAspect(transitPos, natalPos);
        if (aspect) {
          aspects.push({
            transitPlanet,
            natalPlanet,
            aspect: aspect.type,
            orb: aspect.orb
          });
        }
      }
    }

    return aspects;
  }

  private static calculateAspect(
    pos1: PlanetaryPosition,
    pos2: PlanetaryPosition,
    maxOrb = 6
  ): { type: string; orb: number } | null {
    const angle = Math.abs(pos1.longitude - pos2.longitude) % 360;
    
    const aspects = [
      { angle: 0, type: 'conjunction', maxOrb },
      { angle: 60, type: 'sextile', maxOrb },
      { angle: 90, type: 'square', maxOrb },
      { angle: 120, type: 'trine', maxOrb },
      { angle: 180, type: 'opposition', maxOrb }
    ];

    for (const aspectDef of aspects) {
      const orb = Math.abs(angle - aspectDef.angle);
      if (orb <= aspectDef.maxOrb) {
        return { type: aspectDef.type, orb };
      }
    }

    return null;
  }
}

interface TransitAspect {
  transitPlanet: string;
  natalPlanet: string;
  aspect: string;
  orb: number;
}