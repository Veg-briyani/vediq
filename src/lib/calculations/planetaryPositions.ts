// src/lib/calculations/planetaryPositions.ts

import { MERCURY, VENUS, MARS, JUPITER, SATURN } from '../vsop87/planetaryTerms';

export class PlanetaryPositions {
 static calculatePosition(planet: string, T: number) {
   const terms = this.getPlanetTerms(planet);
   const L = this.calculateSeries(terms.L_TERMS, T);
   const B = this.calculateSeries(terms.B_TERMS, T);
   const R = this.calculateSeries(terms.R_TERMS, T);

   return {
     longitude: this.normalizeAngle(L),
     latitude: B,
     radius: R
   };
 }

 private static calculateSeries(terms: number[][], T: number): number {
   let result = 0;
   terms.forEach(([A, B, C]) => {
     result += A * Math.cos(B + C * T);
   });
   return result * 1e-8; // Convert to radians
 }

 private static getPlanetTerms(planet: string) {
   const terms = {
     mercury: MERCURY,
     venus: VENUS,
     mars: MARS,
     jupiter: JUPITER,
     saturn: SATURN
   };
   return terms[planet.toLowerCase()];
 }

 static calculateHeliocentricCoordinates(planet: string, jd: number) {
   const T = (jd - 2451545.0) / 36525; // Julian centuries since J2000.0
   const position = this.calculatePosition(planet, T);
   
   return this.convertToEcliptic(position.longitude, position.latitude, position.radius);
 }

 static convertToEcliptic(L: number, B: number, R: number) {
   const x = R * Math.cos(B) * Math.cos(L);
   const y = R * Math.cos(B) * Math.sin(L);
   const z = R * Math.sin(B);
   
   return { x, y, z };
 }

 static calculateGeocentricPosition(planet: string, jd: number) {
   const planetPos = this.calculateHeliocentricCoordinates(planet, jd);
   const earthPos = this.calculateHeliocentricCoordinates('earth', jd);

   return {
     x: planetPos.x - earthPos.x,
     y: planetPos.y - earthPos.y,
     z: planetPos.z - earthPos.z
   };
 }

 private static normalizeAngle(angle: number): number {
   return angle - 2 * Math.PI * Math.floor(angle / (2 * Math.PI));
 }

 static calculateSphericalCoordinates(x: number, y: number, z: number) {
   const r = Math.sqrt(x*x + y*y + z*z);
   const longitude = Math.atan2(y, x);
   const latitude = Math.asin(z/r);
   
   return {
     longitude: this.normalizeAngle(longitude),
     latitude,
     distance: r
   };
 }
}