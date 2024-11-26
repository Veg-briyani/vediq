// src/types/astrology.ts
export interface CelestialPosition {
    longitude: number;
    latitude: number;
    speed: number;
  }
  
  export interface PlanetaryPosition extends CelestialPosition {
    planet: string;
    house: number;
    sign: number;
    nakshatra: number;
    nakshatraPada: number;
    degree: number;
    minutes: number;
    isRetrograde: boolean;
  }
  
  export interface BirthChart {
    datetime: string;
    timezone: string;
    latitude: number;
    longitude: number;
    houses: number[];
    planets: {
      ascendant: PlanetaryPosition;
      sun: PlanetaryPosition;
      moon: PlanetaryPosition;
      mars: PlanetaryPosition;
      mercury: PlanetaryPosition;
      jupiter: PlanetaryPosition;
      venus: PlanetaryPosition;
      saturn: PlanetaryPosition;
      rahu: PlanetaryPosition;
      ketu: PlanetaryPosition;
    };
  }
  
  export interface DashaPeriod {
    planet: string;
    startDate: string;
    endDate: string;
    years: number;
    subPeriods?: DashaPeriod[];
  }
  
  export type SignLord = {
    [key: number]: string;
  };