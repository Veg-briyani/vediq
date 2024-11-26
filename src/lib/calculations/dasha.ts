// src/lib/calculations/dasha.ts

import { DashaPeriod } from '@/types/astrology';
import { addYears, addMonths, addDays, format } from 'date-fns';

/**
 * DashaCalculator handles all Vimshottari Dasha calculations.
 * The Vimshottari Dasha system operates on a 120-year cycle,
 * with each planet ruling for a specific number of years.
 */
export class DashaCalculator {
  // Dasha periods for each planet in years
  private static readonly DASHA_YEARS: Record<string, number> = {
    sun: 6,
    moon: 10,
    mars: 7,
    rahu: 18,
    jupiter: 16,
    saturn: 19,
    mercury: 17,
    ketu: 7,
    venus: 20
  };

  // Nakshatra lords in order
  private static readonly NAKSHATRA_LORDS = [
    'ketu', 'venus', 'sun', 'moon', 'mars',
    'rahu', 'jupiter', 'saturn', 'mercury'
  ];

  /**
   * Calculates the starting Dasha lord based on birth Moon's Nakshatra
   * @param nakshatra - The Nakshatra number (1-27)
   * @returns The ruling planet of the Nakshatra
   */
  static getNakshatraLord(nakshatra: number): string {
    return this.NAKSHATRA_LORDS[(nakshatra - 1) % 9];
  }

  /**
   * Calculates the balance of the first Dasha at birth
   * @param nakshatra - The Nakshatra number (1-27)
   * @param degrees - Degrees traversed in the Nakshatra
   * @returns Balance in years
   */
  static calculateDashaBalance(nakshatra: number, degrees: number): number {
    const lord = this.getNakshatraLord(nakshatra);
    const totalYears = this.DASHA_YEARS[lord];
    const nakshatraSpan = 13 + 1/3; // 13°20'
    const balanceDegrees = nakshatraSpan - degrees;
    
    return (balanceDegrees / nakshatraSpan) * totalYears;
  }

  /**
   * Calculates the complete Vimshottari Dasha sequence
   * @param birthDate - Date of birth
   * @param nakshatra - Birth Moon's Nakshatra
   * @param degrees - Degrees in Nakshatra
   * @returns Array of Dasha periods
   */
  static calculateDashaPeriods(
    birthDate: Date,
    nakshatra: number,
    degrees: number
  ): DashaPeriod[] {
    const dashas: DashaPeriod[] = [];
    const balance = this.calculateDashaBalance(nakshatra, degrees);
    const startLord = this.getNakshatraLord(nakshatra);
    
    let currentDate = birthDate;
    let foundStart = false;
    
    // Calculate the sequence starting from the birth Nakshatra lord
    for (let i = 0; i < 9; i++) {
      const lordIndex = (this.NAKSHATRA_LORDS.indexOf(startLord) + i) % 9;
      const lord = this.NAKSHATRA_LORDS[lordIndex];
      const years = foundStart ? this.DASHA_YEARS[lord] : balance;
      foundStart = true;

      const startDate = currentDate;
      const endDate = addYears(startDate, years);
      
      dashas.push({
        planet: lord,
        startDate: format(startDate, 'yyyy-MM-dd'),
        endDate: format(endDate, 'yyyy-MM-dd'),
        years,
        subPeriods: this.calculateAntarDasha(lord, startDate, years)
      });
      
      currentDate = endDate;
    }
    
    return dashas;
  }

  /**
   * Calculates Antar Dasha (sub-periods) for a main Dasha period
   * @param mainLord - The main period lord
   * @param startDate - Start date of the main period
   * @param years - Duration of the main period
   * @returns Array of sub-periods
   */
  private static calculateAntarDasha(
    mainLord: string,
    startDate: Date,
    years: number
  ): DashaPeriod[] {
    const antarDashas: DashaPeriod[] = [];
    let currentDate = startDate;
    
    // Calculate sub-periods starting from the main lord
    const startIndex = this.NAKSHATRA_LORDS.indexOf(mainLord);
    for (let i = 0; i < 9; i++) {
      const lordIndex = (startIndex + i) % 9;
      const lord = this.NAKSHATRA_LORDS[lordIndex];
      
      // Calculate sub-period duration
      const subPeriodYears = (years * this.DASHA_YEARS[lord]) / 120;
      const endDate = addYears(currentDate, Math.floor(subPeriodYears));
      const remainingMonths = (subPeriodYears % 1) * 12;
      const finalEndDate = addMonths(endDate, Math.floor(remainingMonths));
      
      antarDashas.push({
        planet: lord,
        startDate: format(currentDate, 'yyyy-MM-dd'),
        endDate: format(finalEndDate, 'yyyy-MM-dd'),
        years: subPeriodYears,
        subPeriods: [] // We could add Pratyantar Dasha (sub-sub periods) here if needed
      });
      
      currentDate = finalEndDate;
    }
    
    return antarDashas;
  }
}