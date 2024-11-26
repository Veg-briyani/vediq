// src/lib/calculations/houses.ts

export class HouseCalculator {
    static calculatePlacidusHouses(jd: number, latitude: number, longitude: number): number[] {
      const houses = new Array(12);
      const RAMC = this.calculateRAMC(jd, longitude);
      const obliquity = AstronomicalCalculator.calculateObliquityOfEcliptic(jd);
      
      // MC (Midheaven - 10th house cusp)
      houses[9] = this.calculateMidheaven(RAMC, obliquity);
      
      // IC (4th house cusp)
      houses[3] = this.normalizeAngle(houses[9] + 180);
   
      // Calculate intermediate house cusps
      const ascendant = this.calculateAscendant(RAMC, obliquity, latitude);
      houses[0] = ascendant;
      houses[6] = this.normalizeAngle(ascendant + 180);
   
      // Calculate remaining houses using Placidus system
      this.calculateIntermediate(RAMC, obliquity, latitude, houses, 11, 1/3); // 11th house
      this.calculateIntermediate(RAMC, obliquity, latitude, houses, 12, 2/3); // 12th house
      this.calculateIntermediate(RAMC, obliquity, latitude, houses, 2, 1/3);  // 2nd house
      this.calculateIntermediate(RAMC, obliquity, latitude, houses, 1, 2/3);  // 1st house
      this.calculateIntermediate(RAMC, obliquity, latitude, houses, 8, 1/3);  // 8th house
      this.calculateIntermediate(RAMC, obliquity, latitude, houses, 7, 2/3);  // 7th house
   
      return houses;
    }
   
    private static calculateRAMC(jd: number, longitude: number): number {
      const T = (jd - 2451545.0) / 36525;
      const GMST = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T - T * T * T / 38710000;
      return this.normalizeAngle(GMST + longitude);
    }
   
    private static calculateMidheaven(RAMC: number, obliquity: number): number {
      const tanRA = Math.tan(this.toRadians(RAMC));
      const cosObl = Math.cos(this.toRadians(obliquity));
      return this.toDegrees(Math.atan2(tanRA, cosObl));
    }
   
    private static calculateAscendant(RAMC: number, obliquity: number, latitude: number): number {
      const sinRA = Math.sin(this.toRadians(RAMC));
      const cosRA = Math.cos(this.toRadians(RAMC));
      const tanObl = Math.tan(this.toRadians(obliquity));
      const sinLat = Math.sin(this.toRadians(latitude));
      const cosLat = Math.cos(this.toRadians(latitude));
   
      const y = -cosRA;
      const x = sinRA * cosObl - tanLat * sinObl;
      
      let ascendant = this.toDegrees(Math.atan2(y, x));
      return this.normalizeAngle(ascendant);
    }
   
    private static calculateIntermediate(
      RAMC: number, 
      obliquity: number, 
      latitude: number, 
      houses: number[], 
      houseNum: number, 
      fraction: number
    ): void {
      const ra = RAMC + fraction * 90;
      const dec = this.toDegrees(Math.asin(Math.sin(this.toRadians(obliquity)) * Math.sin(this.toRadians(ra))));
      const k = 90 * fraction;
      
      const h = this.toDegrees(Math.asin(Math.sin(this.toRadians(latitude)) * Math.sin(this.toRadians(dec)) + 
                              Math.cos(this.toRadians(latitude)) * Math.cos(this.toRadians(dec)) * Math.cos(this.toRadians(k))));
                              
      const a = this.toDegrees(Math.acos((Math.sin(this.toRadians(h)) * Math.sin(this.toRadians(latitude)) - 
                              Math.sin(this.toRadians(dec))) / (Math.cos(this.toRadians(h)) * Math.cos(this.toRadians(latitude)))));
                              
      houses[houseNum - 1] = this.normalizeAngle(RAMC + (ra < 180 ? a : 360 - a));
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