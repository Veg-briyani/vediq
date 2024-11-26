// src/lib/calculations/vsop87.ts
import { EARTH_L_TERMS, EARTH_B_TERMS } from './vsop87/earthTerms';

export class VSOP87Calculator {
  static calculatePlanetPosition(planet: string, T: number) {
    const terms = this.getTerms(planet);
    let L = 0, B = 0, R = 0;

    terms.L.forEach(term => {
      L += term[0] * Math.cos(term[1] + term[2] * T);
    });

    terms.B.forEach(term => {
      B += term[0] * Math.cos(term[1] + term[2] * T);
    });

    terms.R.forEach(term => {
      R += term[0] * Math.cos(term[1] + term[2] * T);
    });

    return { longitude: L, latitude: B, distance: R };
  }
}