// src/lib/print.ts
import { BirthChart } from '@/types/astrology';

export const printHelper = {
  printChart(birthChart: BirthChart): void {
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;

    const content = `
      <!DOCTYPE html>
      <html>
        <head>
          <title>Birth Chart - ${new Date(birthChart.datetime).toLocaleDateString()}</title>
          <style>
            body { font-family: system, -apple-system, sans-serif; padding: 40px; }
            .chart-container { max-width: 800px; margin: 0 auto; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background: #f5f5f5; }
            h1, h2 { color: #333; }
          </style>
        </head>
        <body>
          <div class="chart-container">
            <h1>Birth Chart Details</h1>
            <p>Date: ${new Date(birthChart.datetime).toLocaleString()}</p>
            <p>Location: ${birthChart.latitude}°, ${birthChart.longitude}°</p>
            
            <h2>Planetary Positions</h2>
            <table>
              <thead>
                <tr>
                  <th>Planet</th>
                  <th>Sign</th>
                  <th>Degree</th>
                  <th>House</th>
                </tr>
              </thead>
              <tbody>
                ${Object.entries(birthChart.planets)
                  .map(([planet, pos]) => `
                    <tr>
                      <td>${planet}</td>
                      <td>${pos.sign}</td>
                      <td>${pos.degree}°${pos.minutes}'</td>
                      <td>${pos.house}</td>
                    </tr>
                  `).join('')}
              </tbody>
            </table>
          </div>
        </body>
      </html>
    `;

    printWindow.document.write(content);
    printWindow.document.close();
    setTimeout(() => {
      printWindow.print();
      printWindow.close();
    }, 250);
  }
};