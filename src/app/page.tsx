// src/app/page.tsx

'use client';

import { useState, useEffect } from 'react';
import { PlanetaryPositions } from '@/lib/calculations/planetaryPositions';
import BirthChartVisualization from '@/components/BirthChartVisualization';

export default function Home() {
 const [birthData, setBirthData] = useState(null);
 const [planetaryData, setPlanetaryData] = useState(null);

 const calculatePlanetaryPositions = (date: Date) => {
   const jd = calculateJulianDate(date);
   
   const positions = {
     sun: PlanetaryPositions.calculateGeocentricPosition('sun', jd),
     moon: calculateLunarPosition(jd),
     mercury: PlanetaryPositions.calculateGeocentricPosition('mercury', jd),
     venus: PlanetaryPositions.calculateGeocentricPosition('venus', jd),
     mars: PlanetaryPositions.calculateGeocentricPosition('mars', jd),
     jupiter: PlanetaryPositions.calculateGeocentricPosition('jupiter', jd),
     saturn: PlanetaryPositions.calculateGeocentricPosition('saturn', jd)
   };

   const sphericalPositions = {};
   Object.entries(positions).forEach(([planet, pos]) => {
     sphericalPositions[planet] = PlanetaryPositions.calculateSphericalCoordinates(
       pos.x, pos.y, pos.z
     );
   });

   return sphericalPositions;
 };

 const handleSubmit = async (formData) => {
   const birthDate = new Date(`${formData.date}T${formData.time}`);
   const positions = calculatePlanetaryPositions(birthDate);
   
   const birthChart = {
     datetime: birthDate.toISOString(),
     latitude: parseFloat(formData.latitude),
     longitude: parseFloat(formData.longitude),
     planets: positions
   };

   setBirthData(birthChart);
   setPlanetaryData(positions);
 };

 return (
   <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
     <main className="container mx-auto px-4 py-8">
       <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
         <div>
           <InputForm onSubmit={handleSubmit} />
         </div>
         
         {birthData && (
           <div className="lg:col-span-2">
             <BirthChartVisualization data={birthData} />
             <PlanetaryTable positions={planetaryData} />
           </div>
         )}
       </div>
     </main>
   </div>
 );
}

function calculateJulianDate(date: Date): number {
 const y = date.getUTCFullYear();
 const m = date.getUTCMonth() + 1;
 const d = date.getUTCDate();
 const h = date.getUTCHours() + date.getUTCMinutes()/60 + date.getUTCSeconds()/3600;

 let jd = 367 * y - Math.floor(7 * (y + Math.floor((m + 9) / 12)) / 4);
 jd += Math.floor(275 * m / 9) + d + 1721013.5 + h/24;
 
 return jd;
}

function calculateLunarPosition(jd: number) {
 // Implement lunar position calculation
 // This requires additional terms and calculations specific to the Moon
 return { x: 0, y: 0, z: 0 }; // Placeholder
}