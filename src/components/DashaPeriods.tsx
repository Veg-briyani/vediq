// src/components/DashaPeriods.tsx

import React from 'react';
import { DashaPeriod } from '@/types/astrology';
import { format, differenceInDays } from 'date-fns';

interface DashaPeriodsProps {
  periods: DashaPeriod[];
  className?: string;
}

export default function DashaPeriods({ periods, className = '' }: DashaPeriodsProps) {
  const formatDate = (dateString: string) => {
    return format(new Date(dateString), 'dd MMM yyyy');
  };

  const renderPeriod = (period: DashaPeriod, level: number = 0) => {
    const paddingLeft = level * 1.5;
    
    return (
      <React.Fragment key={`${period.planet}-${period.startDate}`}>
        <tr className={`${level === 0 ? 'bg-gray-50 dark:bg-gray-800' : ''}`}>
          <td 
            className="px-4 py-2 capitalize"
            style={{ paddingLeft: `${paddingLeft + 1}rem` }}
          >
            {period.planet}
          </td>
          <td className="px-4 py-2">{formatDate(period.startDate)}</td>
          <td className="px-4 py-2">{formatDate(period.endDate)}</td>
          <td className="px-4 py-2">
            {period.years.toFixed(2)} years
          </td>
        </tr>
        {period.subPeriods?.map(subPeriod => 
          renderPeriod(subPeriod, level + 1)
        )}
      </React.Fragment>
    );
  };

  return (
    <div className={`overflow-x-auto ${className}`}>
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-gray-100 dark:bg-gray-800">
            <th className="px-4 py-2 text-left">Planet</th>
            <th className="px-4 py-2 text-left">Start Date</th>
            <th className="px-4 py-2 text-left">End Date</th>
            <th className="px-4 py-2 text-left">Duration</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
          {periods.map(period => renderPeriod(period))}
        </tbody>
      </table>
    </div>
  );
}