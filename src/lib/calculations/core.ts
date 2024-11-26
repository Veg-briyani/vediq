// src/lib/calculations/core.ts

import { 
    PlanetaryPosition, 
    CelestialPosition, 
    BirthChart,
    SignLord 
  } from '@/types/astrology';
  
  /**
   * AstrologyCalculator class handles all core astrological calculations
   * including planetary positions, aspects, and astrological interpretations
   */
  export class AstrologyCalculator {
    // Constants used in calculations
    private static readonly NAKSHATRA_SPAN = 13.333333; // Each nakshatra spans 13°20'
    private static readonly PADA_SPAN = 3.333333;      // Each pada spans 3°20'
    private static readonly SIGN_SPAN = 30;            // Each zodiac sign spans 30°
    
    /**
     * Converts decimal degrees to degrees, minutes, and seconds
     * Example: 45.5 degrees = 45° 30' 00"
     */
    static decimalToDMS(decimal: number): { degrees: number; minutes: number; seconds: number } {
      const degrees = Math.floor(decimal);
      const minutesDecimal = (decimal - degrees) * 60;
      const minutes = Math.floor(minutesDecimal);
      const seconds = Math.floor((minutesDecimal - minutes) * 60);
      
      return { degrees, minutes, seconds };
    }
  
    /**
     * Converts degrees, minutes, seconds to decimal degrees
     * Example: 45° 30' 00" = 45.5 degrees
     */
    static dmsToDecimal(degrees: number, minutes: number, seconds: number): number {
      return degrees + (minutes / 60) + (seconds / 3600);
    }
  
    /**
     * Normalizes an angle to be between 0 and 360 degrees
     */
    static normalizeAngle(angle: number): number {
      return ((angle % 360) + 360) % 360;
    }
  
    /**
     * Calculates nakshatra and pada from longitude
     * Each nakshatra spans 13°20' and has 4 padas of 3°20' each
     */
    static calculateNakshatra(longitude: number): { nakshatra: number; pada: number } {
      const normalizedLongitude = this.normalizeAngle(longitude);
      const nakshatraIndex = Math.floor(normalizedLongitude / this.NAKSHATRA_SPAN);
      const nakshatra = nakshatraIndex + 1;
      
      const degreeInNakshatra = normalizedLongitude % this.NAKSHATRA_SPAN;
      const pada = Math.floor(degreeInNakshatra / this.PADA_SPAN) + 1;
      
      return { nakshatra, pada };
    }
  
    /**
     * Calculates zodiac sign from longitude
     * Each sign spans 30 degrees
     */
    static calculateSign(longitude: number): number {
      return Math.floor(this.normalizeAngle(longitude) / this.SIGN_SPAN) + 1;
    }
  
    /**
     * Calculates house position relative to ascendant
     * Houses are counted counterclockwise from the ascendant
     */
    static calculateHouse(longitude: number, ascendant: number): number {
      const distance = this.normalizeAngle(longitude - ascendant);
      return Math.floor(distance / this.SIGN_SPAN) + 1;
    }
  
    /**
     * Checks if two planets are in conjunction
     * Default orb is 10 degrees
     */
    static isConjunction(p1: CelestialPosition, p2: CelestialPosition, orb: number = 10): boolean {
      const diff = Math.abs(p1.longitude - p2.longitude);
      return diff <= orb || (360 - diff) <= orb;
    }
  
    /**
     * Calculates aspect angle between two planets
     * Returns the smaller angle between two planets (0-180 degrees)
     */
    static calculateAspect(p1: CelestialPosition, p2: CelestialPosition): number {
      const diff = Math.abs(p1.longitude - p2.longitude);
      return diff > 180 ? 360 - diff : diff;
    }
  
    /**
     * Returns the planetary ruler of a zodiac sign
     */
    static getSignLord(sign: number): string {
      const lords: SignLord = {
        1: 'mars',     // Aries
        2: 'venus',    // Taurus
        3: 'mercury',  // Gemini
        4: 'moon',     // Cancer
        5: 'sun',      // Leo
        6: 'mercury',  // Virgo
        7: 'venus',    // Libra
        8: 'mars',     // Scorpio
        9: 'jupiter',  // Sagittarius
        10: 'saturn',  // Capricorn
        11: 'saturn',  // Aquarius
        12: 'jupiter'  // Pisces
      };
      return lords[sign] || '';
    }
  
    /**
     * Returns the ruling planet of a nakshatra
     * Follows the cycle: Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury
     */
    static getNakshatraLord(nakshatra: number): string {
      const lords = [
        'ketu', 'venus', 'sun', 'moon', 'mars',
        'rahu', 'jupiter', 'saturn', 'mercury'
      ];
      return lords[(nakshatra - 1) % 9];
    }
  
    /**
     * Calculates the strength of a planet based on various factors
     * Returns a value between 0 and 100
     */
    static calculatePlanetStrength(position: PlanetaryPosition): number {
      let strength = 0;
      
      // Directional strength (dig bala)
      if (position.house === 1 || position.house === 10) {
        strength += 20;
      }
      
      // Sign strength
      if (this.getSignLord(position.sign) === position.planet) {
        strength += 30; // Planet in own sign
      }
      
      // Degree strength
      const degreeInSign = position.degree;
      if (degreeInSign > 10 && degreeInSign < 20) {
        strength += 20; // Planet in deep degrees
      }
      
      // Directional aspects
      if (!position.isRetrograde) {
        strength += 15;
      }
      
      return Math.min(100, strength);
    }
  
    /**
     * Determines if a planet is in its exaltation sign
     */
    static isExalted(planet: string, sign: number): boolean {
      const exaltations: Record<string, number> = {
        sun: 1,      // Aries
        moon: 2,     // Taurus
        mars: 10,    // Capricorn
        mercury: 6,  // Virgo
        jupiter: 4,  // Cancer
        venus: 12,   // Pisces
        saturn: 7    // Libra
      };
      return exaltations[planet] === sign;
    }
  
    /**
     * Determines if a planet is in its debilitation sign
     */
    static isDebilitated(planet: string, sign: number): boolean {
      const debilitations: Record<string, number> = {
        sun: 7,      // Libra
        moon: 8,     // Scorpio
        mars: 4,     // Cancer
        mercury: 12, // Pisces
        jupiter: 10, // Capricorn
        venus: 6,    // Virgo
        saturn: 1    // Aries
      };
      return debilitations[planet] === sign;
    }
  
    /**
     * Calculates ayanamsa (precession of equinoxes)
     * Using Lahiri ayanamsa
     */
    static calculateAyanamsa(julianDay: number): number {
      // This is a simplified calculation
      const t = (julianDay - 2451545.0) / 36525;
      return 23.85 + 0.0137 * t;
    }
  
    /**
     * Converts tropical longitude to sidereal longitude
     */
    static tropicalToSidereal(longitude: number, ayanamsa: number): number {
      return this.normalizeAngle(longitude - ayanamsa);
    }
  }
  
  // Export singleton instance
  export const astroCalc = new AstrologyCalculator();