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
        <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
        <p className="mt-2 text-gray-600">Financial insights and analytics</p>
      </div>

      {/* Date Range Filter */}
      <div className="bg-white rounded-lg shadow mb-8 p-6">
        <div className="flex items-center space-x-4">
          <CalendarIcon className="h-5 w-5 text-gray-400" />
          <div className="flex space-x-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Start Date</label>
              <input
                type="date"
                value={dateRange.startDate}
                onChange={(e) => setDateRange({ ...dateRange, startDate: e.target.value })}
                className="mt-1 block border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">End Date</label>
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

      {/* Financial Summary */}
      {financialSummary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CurrencyDollarIcon className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Balance</p>
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
                <p className="text-sm font-medium text-gray-500">Total Income</p>
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
                <p className="text-sm font-medium text-gray-500">Total Expenses</p>
                <p className="text-2xl font-bold text-red-600">
                  {formatCurrency(financialSummary.total_expenses)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Movements</p>
                <p className="text-2xl font-bold text-blue-600">
                  {financialSummary.movement_count}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Budget Summary */}
      {budgetSummary && (
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Budget Overview</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
              <div className="text-center">
                <p className="text-2xl font-bold text-gray-900">{budgetSummary.total_budgets}</p>
                <p className="text-sm text-gray-500">Total Budgets</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-600">
                  {formatCurrency(budgetSummary.total_allocated)}
                </p>
                <p className="text-sm text-gray-500">Total Allocated</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-red-600">
                  {formatCurrency(budgetSummary.total_spent)}
                </p>
                <p className="text-sm text-gray-500">Total Spent</p>
              </div>
              <div className="text-center">
                <p className={`text-2xl font-bold ${budgetSummary.total_remaining >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {formatCurrency(budgetSummary.total_remaining)}
                </p>
                <p className="text-sm text-gray-500">Total Remaining</p>
              </div>
            </div>

            {/* Budget Details */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-gray-900">Budget Details</h3>
              {budgetSummary.budgets.length > 0 ? (
                budgetSummary.budgets.map((budget) => (
                  <div key={budget.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <div>
                        <h4 className="font-medium text-gray-900">{budget.category}</h4>
                        <p className="text-sm text-gray-500">
                          {formatDate(budget.start_date)} - {formatDate(budget.end_date)}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900">
                          {budget.percentage_used.toFixed(1)}%
                        </p>
                        <p className="text-xs text-gray-500">
                          {formatCurrency(budget.current_amount)} / {formatCurrency(budget.max_amount)}
                        </p>
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${getProgressColor(budget.percentage_used)}`}
                        style={{ width: `${Math.min(budget.percentage_used, 100)}%` }}
                      ></div>
                    </div>
                    <div className="mt-2 flex justify-between text-xs text-gray-500">
                      <span>Remaining: {formatCurrency(budget.remaining_amount)}</span>
                      <span>{budget.period}</span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8">
                  <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No budgets</h3>
                  <p className="mt-1 text-sm text-gray-500">Create budgets to see detailed reports.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Insights */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Insights</h2>
        </div>
        <div className="p-6">
          {financialSummary && (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Net Income</p>
                  <p className="text-sm text-gray-500">
                    {financialSummary.total_income > financialSummary.total_expenses 
                      ? 'You are saving money' 
                      : 'You are spending more than you earn'}
                  </p>
                </div>
                <div className={`text-lg font-bold ${
                  financialSummary.total_income > financialSummary.total_expenses 
                    ? 'text-green-600' 
                    : 'text-red-600'
                }`}>
                  {formatCurrency(financialSummary.total_income - financialSummary.total_expenses)}
                </div>
              </div>

              {financialSummary.total_expenses > 0 && (
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">Expense Ratio</p>
                    <p className="text-sm text-gray-500">Percentage of income spent</p>
                  </div>
                  <div className="text-lg font-bold text-gray-900">
                    {((financialSummary.total_expenses / financialSummary.total_income) * 100).toFixed(1)}%
                  </div>
                </div>
              )}

              {budgetSummary && budgetSummary.budgets.length > 0 && (
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">Budget Utilization</p>
                    <p className="text-sm text-gray-500">Average budget usage</p>
                  </div>
                  <div className="text-lg font-bold text-gray-900">
                    {(budgetSummary.budgets.reduce((acc, budget) => acc + budget.percentage_used, 0) / budgetSummary.budgets.length).toFixed(1)}%
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Reports; 