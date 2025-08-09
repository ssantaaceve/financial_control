import React, { useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  PlusIcon, 
  ArrowUpIcon, 
  ArrowDownIcon, 
  BanknotesIcon,
  ChartBarIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import { Movement, MovementType } from '../types';
import { apiService } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

// Interfaz local para el resumen financiero
interface FinancialSummary {
  total_income: number;
  total_expenses: number;
  balance: number;
  movement_count: number;
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [summary, setSummary] = useState<FinancialSummary | null>(null);
  const [recentMovements, setRecentMovements] = useState<Movement[]>([]);
  const [loading, setLoading] = useState(true);
  const [dateLoading, setDateLoading] = useState(false);
  const [dateRange, setDateRange] = useState({
    startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
    endDate: new Date().toISOString().split('T')[0]
  });

  // Función para obtener datos con debounce
  const fetchDashboardData = useCallback(async (startDate: string, endDate: string) => {
    try {
      setDateLoading(true);
      const [summaryData, movementsData] = await Promise.all([
        apiService.getFinancialSummary(startDate, endDate),
        apiService.getMovements()
      ]);
      setSummary(summaryData.data || null);
      setRecentMovements((movementsData.data || []).slice(0, 5));
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setDateLoading(false);
    }
  }, []);

  // Carga inicial
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setLoading(true);
        await fetchDashboardData(dateRange.startDate, dateRange.endDate);
      } finally {
        setLoading(false);
      }
    };
    loadInitialData();
  }, []);

  // Debounce para cambios de fecha
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchDashboardData(dateRange.startDate, dateRange.endDate);
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [dateRange, fetchDashboardData]);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  const handleDateChange = (field: 'startDate' | 'endDate', value: string) => {
    setDateRange(prev => ({
      ...prev,
      [field]: value
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 h-screen flex flex-col">
      {/* Header */}
      <div className="mb-6 text-center">
        <h1 className="text-3xl font-bold text-white mb-2" style={{ fontFamily: 'var(--font-display)' }}>
          ¡Bienvenido, {user?.name || 'Usuario'}!
        </h1>
        <p className="text-lg text-gray-300 mb-4" style={{ fontFamily: 'var(--font-body)' }}>
          Tu resumen financiero personal
        </p>
        
        {/* Date Range Selector */}
        <div className="flex flex-col sm:flex-row items-center justify-center space-y-2 sm:space-y-0 sm:space-x-4">
          <div className="inline-flex items-center px-4 py-2 bg-white/15 backdrop-blur-sm border border-white/20 text-white rounded-lg">
            <CalendarIcon className="h-4 w-4 mr-2" />
            <span className="font-medium text-sm">
              Período: {formatDate(dateRange.startDate)} - {formatDate(dateRange.endDate)}
            </span>
            {dateLoading && (
              <div className="ml-2 w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            )}
          </div>
          
          {/* Date Range Inputs */}
          <div className="flex flex-col sm:flex-row items-center space-y-2 sm:space-y-0 sm:space-x-4">
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-white">Desde:</label>
              <input
                type="date"
                value={dateRange.startDate}
                onChange={(e) => handleDateChange('startDate', e.target.value)}
                className="border border-white/20 rounded-lg px-3 py-1 text-sm text-white bg-white/15 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-white/50"
              />
            </div>
            
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-white">Hasta:</label>
              <input
                type="date"
                value={dateRange.endDate}
                onChange={(e) => handleDateChange('endDate', e.target.value)}
                className="border border-white/20 rounded-lg px-3 py-1 text-sm text-white bg-white/15 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-white/50"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
        {/* Left Column - Financial Summary and Quick Actions */}
        <div className="lg:col-span-2 space-y-6">
          {/* Financial Summary Cards */}
          <div className={`grid grid-cols-1 md:grid-cols-3 gap-4 transition-opacity duration-300 ${dateLoading ? 'opacity-50' : 'opacity-100'}`}>
            {summary && (
              <>
                <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg shadow-lg p-4">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <BanknotesIcon className="h-6 w-6 text-green-400" />
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-white/70">Balance Total</p>
                      <p className="text-xl font-bold text-white">
                        {formatCurrency(summary.balance)}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg shadow-lg p-4">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <ArrowUpIcon className="h-6 w-6 text-green-400" />
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-white/70">Ingresos</p>
                      <p className="text-xl font-bold text-green-400">
                        {formatCurrency(summary.total_income)}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg shadow-lg p-4">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <ArrowDownIcon className="h-6 w-6 text-red-400" />
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-white/70">Gastos</p>
                      <p className="text-xl font-bold text-red-400">
                        {formatCurrency(summary.total_expenses)}
                      </p>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>

          {/* Quick Actions */}
          <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg shadow-lg p-6">
            <h2 className="text-lg font-medium text-white mb-4" style={{ fontFamily: 'var(--font-display)' }}>
              Acciones Rápidas
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button
                onClick={() => navigate('/movements')}
                className="flex items-center p-4 border border-white/20 rounded-lg hover:bg-white/20 transition-colors text-left"
              >
                <PlusIcon className="h-6 w-6 text-blue-400 mr-3" />
                <div>
                  <p className="font-medium text-white">Agregar Movimiento</p>
                  <p className="text-sm text-white/70">Registrar ingreso o gasto</p>
                </div>
              </button>

              <Link
                to="/budgets"
                className="flex items-center p-4 border border-white/20 rounded-lg hover:bg-white/20 transition-colors text-left"
              >
                <ChartBarIcon className="h-6 w-6 text-green-400 mr-3" />
                <div>
                  <p className="font-medium text-white">Gestionar Presupuestos</p>
                  <p className="text-sm text-white/70">Configurar límites de gasto</p>
                </div>
              </Link>
            </div>
          </div>
        </div>

        {/* Right Column - Recent Movements */}
        <div className="lg:col-span-1">
          <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg shadow-lg h-full">
            <div className="px-6 py-4 border-b border-white/20">
              <h2 className="text-lg font-medium text-white" style={{ fontFamily: 'var(--font-display)' }}>
                Movimientos Recientes
              </h2>
            </div>
            <div className="p-6 h-full overflow-y-auto">
              {recentMovements.length > 0 ? (
                <div className="space-y-4">
                  {recentMovements.map((movement) => (
                    <div key={movement.id} className="flex items-center justify-between p-3 bg-white/10 rounded-lg">
                      <div className="flex items-center">
                        <div className={`flex-shrink-0 w-3 h-3 rounded-full ${
                          movement.movement_type === MovementType.INGRESO ? 'bg-green-400' : 'bg-red-400'
                        }`} />
                        <div className="ml-3">
                          <p className="text-sm font-medium text-white">{movement.description}</p>
                          <p className="text-xs text-white/70">{movement.category}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className={`text-sm font-medium ${
                          movement.movement_type === MovementType.INGRESO ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {movement.movement_type === MovementType.INGRESO ? '+' : '-'}{formatCurrency(movement.amount)}
                        </p>
                        <p className="text-xs text-white/70">{formatDate(movement.movement_date)}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-white/70">No hay movimientos recientes</p>
                  <button
                    onClick={() => navigate('/movements')}
                    className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                  >
                    <PlusIcon className="h-4 w-4 mr-2" />
                    Agregar Movimiento
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 