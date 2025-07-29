import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  Filler
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';
import { apiService } from '../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  Filler
);

interface FinancialData {
  month: string;
  income: number;
  expenses: number;
  balance: number;
}

const FinancialChart: React.FC = () => {
  const [chartData, setChartData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState<3 | 6 | 12>(6);
  const [chartType, setChartType] = useState<'bar' | 'line'>('bar');

  useEffect(() => {
    fetchFinancialData();
  }, [period]);

  const fetchFinancialData = async () => {
    try {
      setLoading(true);
      
      // Calcular fechas basadas en el período seleccionado
      const endDate = new Date();
      const startDate = new Date();
      startDate.setMonth(endDate.getMonth() - period);
      
      // Obtener movimientos del período
      const response = await apiService.getMovements();
      const movements = response.data || [];
      
      // Filtrar movimientos por período
      const filteredMovements = movements.filter((movement: any) => {
        const movementDate = new Date(movement.movement_date);
        return movementDate >= startDate && movementDate <= endDate;
      });
      
      // Agrupar por mes
      const monthlyData: { [key: string]: FinancialData } = {};
      
      for (let i = 0; i < period; i++) {
        const date = new Date();
        date.setMonth(date.getMonth() - i);
        const monthKey = date.toISOString().slice(0, 7); // YYYY-MM
        const monthName = date.toLocaleDateString('es-ES', { month: 'short', year: 'numeric' });
        
        monthlyData[monthKey] = {
          month: monthName,
          income: 0,
          expenses: 0,
          balance: 0
        };
      }
      
      // Procesar movimientos
      filteredMovements.forEach((movement: any) => {
        const monthKey = movement.movement_date.slice(0, 7);
        if (monthlyData[monthKey]) {
          if (movement.movement_type === 'INGRESO') {
            monthlyData[monthKey].income += movement.amount;
          } else {
            monthlyData[monthKey].expenses += movement.amount;
          }
          monthlyData[monthKey].balance = monthlyData[monthKey].income - monthlyData[monthKey].expenses;
        }
      });
      
      // Ordenar por fecha (más antigua primero)
      const sortedData = Object.values(monthlyData).reverse();
      
      // Preparar datos para el gráfico
      const labels = sortedData.map(d => d.month);
      const incomeData = sortedData.map(d => d.income);
      const expensesData = sortedData.map(d => d.expenses);
      const balanceData = sortedData.map(d => d.balance);
      
      setChartData({
        labels,
        datasets: [
          {
            label: 'Ingresos',
            data: incomeData,
            backgroundColor: 'rgba(34, 197, 94, 0.8)',
            borderColor: 'rgba(34, 197, 94, 1)',
            borderWidth: 2,
            fill: false,
            tension: 0.4
          },
          {
            label: 'Gastos',
            data: expensesData,
            backgroundColor: 'rgba(239, 68, 68, 0.8)',
            borderColor: 'rgba(239, 68, 68, 1)',
            borderWidth: 2,
            fill: false,
            tension: 0.4
          },
          {
            label: 'Balance',
            data: balanceData,
            backgroundColor: 'rgba(59, 130, 246, 0.8)',
            borderColor: 'rgba(59, 130, 246, 1)',
            borderWidth: 2,
            fill: false,
            tension: 0.4
          }
        ]
      });
      
    } catch (error) {
      console.error('Error fetching financial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: '#ffffff',
          font: {
            family: 'Roboto Mono',
            size: 12
          }
        }
      },
      title: {
        display: true,
        text: `Análisis Financiero - Últimos ${period} meses`,
        color: '#ffffff',
        font: {
          family: 'Roboto Mono',
          size: 16,
          weight: 'bold' as const
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        borderColor: '#374151',
        borderWidth: 1,
        callbacks: {
          label: function(context: any) {
            const label = context.dataset.label || '';
            const value = context.parsed.y;
            return `${label}: $${value.toLocaleString()}`;
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: '#ffffff',
          font: {
            family: 'Roboto Mono',
            size: 11
          }
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      },
      y: {
        ticks: {
          color: '#ffffff',
          font: {
            family: 'Roboto Mono',
            size: 11
          },
          callback: function(value: any) {
            return '$' + value.toLocaleString();
          }
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Controles */}
      <div className="flex flex-wrap items-center justify-between mb-6 gap-4">
        <div className="flex items-center space-x-4">
          <label className="text-sm font-medium text-gray-700">Período:</label>
          <div className="flex space-x-2">
            {[3, 6, 12].map((months) => (
              <button
                key={months}
                onClick={() => setPeriod(months as 3 | 6 | 12)}
                className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                  period === months
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {months} meses
              </button>
            ))}
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <label className="text-sm font-medium text-gray-700">Tipo de gráfico:</label>
          <div className="flex space-x-2">
            <button
              onClick={() => setChartType('bar')}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                chartType === 'bar'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Barras
            </button>
            <button
              onClick={() => setChartType('line')}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                chartType === 'line'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Líneas
            </button>
          </div>
        </div>
      </div>

      {/* Gráfico */}
      <div className="bg-main-bg rounded-lg p-4">
        {chartData && (
          <div className="h-96">
            {chartType === 'bar' ? (
              <Bar data={chartData} options={options} />
            ) : (
              <Line data={chartData} options={options} />
            )}
          </div>
        )}
      </div>

      {/* Resumen */}
      {chartData && (
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 className="text-sm font-medium text-green-800">Total Ingresos</h3>
            <p className="text-2xl font-bold text-green-600">
              ${chartData.datasets[0].data.reduce((a: number, b: number) => a + b, 0).toLocaleString()}
            </p>
          </div>
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <h3 className="text-sm font-medium text-red-800">Total Gastos</h3>
            <p className="text-2xl font-bold text-red-600">
              ${chartData.datasets[1].data.reduce((a: number, b: number) => a + b, 0).toLocaleString()}
            </p>
          </div>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="text-sm font-medium text-blue-800">Balance Neto</h3>
            <p className="text-2xl font-bold text-blue-600">
              ${chartData.datasets[2].data.reduce((a: number, b: number) => a + b, 0).toLocaleString()}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default FinancialChart; 