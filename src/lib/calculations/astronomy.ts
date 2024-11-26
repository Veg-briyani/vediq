// src/lib/calculations/astronomy.ts
export class AstronomicalCalculator {
    static readonly J2000 = 2451545.0;
    
    static calculateJulianDate(date: Date): number {
      const y = date.getFullYear();
      const m = date.getMonth() + 1;
      const d = date.getDate();
      const h = date.getHours() + date.getMinutes()/60 + date.getSeconds()/3600;
  
      let jd = 367 * y - Math.floor(7 * (y + Math.floor((m + 9) / 12)) / 4);
      jd += Math.floor(275 * m / 9) + d + 1721013.5 + h/24;
      jd -= 0.5 * Math.sign(100 * y + m - 190002.5) + 0.5;
  
      return jd;
    }
  
    static calculateObliquityOfEcliptic(jd: number): number {
      const T = (jd - this.J2000) / 36525;
      const eps = 23.43929111 - (46.8150/3600)*T - (0.00059/3600)*T*T + (0.001813/3600)*T*T*T;
      return eps;
    }
  
    static calculateSunPosition(jd: number): {longitude: number; latitude: number; distance: number} {
      const T = (jd - this.J2000) / 36525;
      
      // Mean elements
      const L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T;
      const M = 357.52911 + 35999.05029 * T - 0.0001537 * T * T;
      const e = 0.016708634 - 0.000042037 * T - 0.0000001267 * T * T;
      
      // Equation of center
      const C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(this.toRadians(M)) +
                (0.019993 - 0.000101 * T) * Math.sin(2 * this.toRadians(M)) +
                0.000289 * Math.sin(3 * this.toRadians(M));
      
      // Sun's true longitude and true anomaly
      const Ltrue = L0 + C;
      const v = M + C;
      
      // Sun's radius vector (distance)
      const R = (1.000001018 * (1 - e * e)) / (1 + e * Math.cos(this.toRadians(v)));
      
      return {
        longitude: this.normalizeAngle(Ltrue),
        latitude: 0,
        distance: R
      };
    }
  
    static calculateMoonPosition(jd: number): {longitude: number; latitude: number; distance: number} {
      const T = (jd - this.J2000) / 36525;
      
      // Mean elements
      const Lp = 218.3164477 + 481267.88123421 * T - 0.0015786 * T * T + T * T * T / 538841 - T * T * T * T / 65194000;
      const D = 297.8501921 + 445267.1114034 * T - 0.0018819 * T * T + T * T * T / 545868 - T * T * T * T / 113065000;
      const M = 357.5291092 + 35999.0502909 * T - 0.0001536 * T * T + T * T * T / 24490000;
      const Mp = 134.9633964 + 477198.8675055 * T + 0.0087414 * T * T + T * T * T / 69699 - T * T * T * T / 14712000;
      const F = 93.2720950 + 483202.0175233 * T - 0.0036539 * T * T - T * T * T / 3526000 + T * T * T * T / 863310000;
      
      let perturbation = 0;
      perturbation += 6288.06 * Math.sin(this.toRadians(Mp));
      perturbation += 1274.2 * Math.sin(this.toRadians(2 * D - Mp));
      perturbation += 658.45 * Math.sin(this.toRadians(2 * D));
      perturbation += 214.26 * Math.sin(this.toRadians(2 * Mp));
      perturbation += -186.0 * Math.sin(this.toRadians(M));
      
      const lambda = Lp + perturbation/1000000;
      
      let latitude = 0;
      latitude += 5128.0 * Math.sin(this.toRadians(F));
      latitude += 280.0 * Math.sin(this.toRadians(Mp + F));
      latitude += 277.0 * Math.sin(this.toRadians(Mp - F));
      latitude = latitude/1000000;
      
      const distance = 385000.56;  // Mean distance in kilometers
      
      return {
        longitude: this.normalizeAngle(lambda),
        latitude: latitude,
        distance: distance
      };
    }
  
    static calculatePlanetPosition(planet: string, jd: number): {longitude: number; latitude: number; distance: number} {
      // Implement VSOP87 theory for planetary positions
      // This is a complex calculation that requires extensive data tables
      return {longitude: 0, latitude: 0, distance: 0};
    }
  
    private static toRadians(degrees: number): number {
      return degrees * Math.PI / 180;
    }
  
    private static toDegrees(radians: number): number {
      return radians * 180 / Math.PI;
    }
  
    private static normalizeAngle(angle: number): number {
      return angle - 360 * Math.floor(angle / 360);
    }
  }