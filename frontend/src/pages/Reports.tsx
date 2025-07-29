import React, { useState, useEffect, useCallback } from 'react';
import { 
  ChartBarIcon,
  CalendarIcon,
  CurrencyDollarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon
} from '@heroicons/react/24/outline';
import { FinancialSummary, BudgetSummary } from '../types';
import { apiService } from '../services/api';
import FinancialChart from '../components/FinancialChart';

const Reports: React.FC = () => {
  const [financialSummary, setFinancialSummary] = useState<FinancialSummary | null>(null);
  const [budgetSummary, setBudgetSummary] = useState<BudgetSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState({
    startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
    endDate: new Date().toISOString().split('T')[0]
  });

  const fetchReports = useCallback(async () => {
    try {
      setLoading(true);
      const [financialData, budgetData] = await Promise.all([
        apiService.getFinancialSummary(dateRange.startDate, dateRange.endDate),
        apiService.getBudgetSummary()
      ]);
      setFinancialSummary(financialData.data || null);
      setBudgetSummary(budgetData.data || null);
    } catch (error) {
      console.error('Error fetching reports:', error);
    } finally {
      setLoading(false);
    }
  }, [dateRange]);

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 90) return 'bg-red-500';
    if (percentage >= 75) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Reportes Financieros</h1>
        <p className="mt-2 text-gray-600">Análisis detallado de tus finanzas</p>
      </div>

      {/* Gráfico de Análisis Financiero */}
      <div className="mb-8">
        <FinancialChart />
      </div>

      {/* Resumen Financiero */}
      {financialSummary && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CurrencyDollarIcon className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Balance Total</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(financialSummary.balance)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ArrowTrendingUpIcon className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Ingresos</p>
                <p className="text-2xl font-bold text-green-600">
                  {formatCurrency(financialSummary.total_income)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ArrowTrendingDownIcon className="h-8 w-8 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Gastos</p>
                <p className="text-2xl font-bold text-red-600">
                  {formatCurrency(financialSummary.total_expenses)}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filtro de Fechas */}
      <div className="bg-white rounded-lg shadow mb-8 p-6">
        <div className="flex items-center space-x-4">
          <CalendarIcon className="h-5 w-5 text-gray-400" />
          <div className="flex space-x-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Fecha Inicio</label>
              <input
                type="date"
                value={dateRange.startDate}
                onChange={(e) => setDateRange({ ...dateRange, startDate: e.target.value })}
                className="mt-1 block border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Fecha Fin</label>
              <input
                type="date"
                value={dateRange.endDate}
                onChange={(e) => setDateRange({ ...dateRange, endDate: e.target.value })}
                className="mt-1 block border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Resumen de Presupuestos */}
      {budgetSummary && (
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Resumen de Presupuestos</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-sm font-medium text-gray-500 mb-4">Presupuestos Activos</h3>
                <div className="space-y-4">
                  {budgetSummary.budgets?.map((budget) => (
                    <div key={budget.id} className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{budget.category}</p>
                        <p className="text-sm text-gray-500">
                          {formatCurrency(budget.current_amount)} / {formatCurrency(budget.max_amount)}
                        </p>
                      </div>
                      <div className="flex items-center">
                        <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            className={`h-2 rounded-full ${getProgressColor(budget.percentage_used)}`}
                            style={{ width: `${Math.min(budget.percentage_used, 100)}%` }}
                          />
                        </div>
                        <span className="text-sm text-gray-500">
                          {budget.percentage_used.toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              <div>
                <h3 className="text-sm font-medium text-gray-500 mb-4">Estadísticas</h3>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Total Presupuestos:</span>
                    <span className="text-sm font-medium text-gray-900">
                      {budgetSummary.total_budgets || 0}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Presupuestos Activos:</span>
                    <span className="text-sm font-medium text-gray-900">
                      {budgetSummary.budgets?.length || 0}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Total Gastado:</span>
                    <span className="text-sm font-medium text-gray-900">
                      {formatCurrency(budgetSummary.total_spent || 0)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Total Asignado:</span>
                    <span className="text-sm font-medium text-gray-900">
                      {formatCurrency(budgetSummary.total_allocated || 0)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports; 