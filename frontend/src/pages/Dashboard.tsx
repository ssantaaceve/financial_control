import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  PlusIcon, 
  ArrowUpIcon, 
  ArrowDownIcon, 
  BanknotesIcon,
  ChartBarIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import { Movement, FinancialSummary, MovementType } from '../types';
import { apiService } from '../services/api';

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<FinancialSummary | null>(null);
  const [recentMovements, setRecentMovements] = useState<Movement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [summaryData, movementsData] = await Promise.all([
          apiService.getFinancialSummary(),
          apiService.getMovements()
        ]);
        setSummary(summaryData.data || null);
        setRecentMovements((movementsData.data || []).slice(0, 5));
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const getCurrentMonth = () => {
    const now = new Date();
    return now.toLocaleDateString('en-US', { 
      month: 'long', 
      year: 'numeric' 
    });
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
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">Your financial overview</p>
        <div className="mt-4 inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-lg">
          <CalendarIcon className="h-5 w-5 mr-2" />
          <span className="font-medium">Current Period: {getCurrentMonth()}</span>
        </div>
      </div>

      {/* Financial Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BanknotesIcon className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Balance</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(summary.balance)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ArrowUpIcon className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Income</p>
                <p className="text-2xl font-bold text-green-600">
                  {formatCurrency(summary.total_income)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ArrowDownIcon className="h-8 w-8 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Expenses</p>
                <p className="text-2xl font-bold text-red-600">
                  {formatCurrency(summary.total_expenses)}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow mb-8">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Quick Actions</h2>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link
              to="/movements"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <PlusIcon className="h-6 w-6 text-blue-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">Add Movement</p>
                <p className="text-sm text-gray-500">Record income or expense</p>
              </div>
            </Link>

            <Link
              to="/budgets"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <ChartBarIcon className="h-6 w-6 text-green-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">Manage Budgets</p>
                <p className="text-sm text-gray-500">Set and track budgets</p>
              </div>
            </Link>

            <Link
              to="/reports"
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <CalendarIcon className="h-6 w-6 text-purple-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">View Reports</p>
                <p className="text-sm text-gray-500">Analyze your finances</p>
              </div>
            </Link>
          </div>
        </div>
      </div>

      {/* Recent Movements */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Recent Movements</h2>
          <Link
            to="/movements"
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            View all
          </Link>
        </div>
        <div className="divide-y divide-gray-200">
          {recentMovements.length > 0 ? (
            recentMovements.map((movement) => (
              <div key={movement.id} className="px-6 py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className={`flex-shrink-0 w-2 h-2 rounded-full ${
                      movement.movement_type === MovementType.INGRESO ? 'bg-green-400' : 'bg-red-400'
                    }`} />
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-900">
                        {movement.description}
                      </p>
                      <p className="text-sm text-gray-500">
                        {movement.category} • {new Date(movement.movement_date).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`text-sm font-medium ${
                      movement.movement_type === MovementType.INGRESO ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {movement.movement_type === MovementType.INGRESO ? '+' : '-'}{formatCurrency(movement.amount)}
                    </p>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="px-6 py-8 text-center">
              <p className="text-gray-500">No movements yet. Add your first movement to get started!</p>
              <Link
                to="/movements"
                className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                <PlusIcon className="h-4 w-4 mr-2" />
                Add Movement
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 