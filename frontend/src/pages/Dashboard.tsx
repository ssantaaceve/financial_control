import React, { useState, useEffect, useCallback } from 'react';
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
import AddMovementModal from '../components/AddMovementModal';

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<FinancialSummary | null>(null);
  const [recentMovements, setRecentMovements] = useState<Movement[]>([]);
  const [loading, setLoading] = useState(true);
  const [dateLoading, setDateLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [dateRange, setDateRange] = useState({
    startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0], // Primer día del mes actual
    endDate: new Date().toISOString().split('T')[0] // Hoy
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
  }, []); // Solo se ejecuta una vez al montar el componente

  // Debounce para cambios de fecha
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchDashboardData(dateRange.startDate, dateRange.endDate);
    }, 500); // Espera 500ms después del último cambio

    return () => clearTimeout(timeoutId);
  }, [dateRange, fetchDashboardData]);

  const handleMovementAdded = () => {
    // Recargar datos después de agregar un movimiento
    fetchDashboardData(dateRange.startDate, dateRange.endDate);
  };

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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-white mb-2">FINELIVE Dashboard</h1>
        <p className="text-xl text-gray-300 mb-6">Tu resumen financiero personal</p>
        
        {/* Date Range Selector */}
        <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6">
          <div className="inline-flex items-center px-4 py-2 bg-card-bg border border-border-color text-text-color rounded-lg">
            <CalendarIcon className="h-5 w-5 mr-2" />
            <span className="font-medium">
              Período: {formatDate(dateRange.startDate)} - {formatDate(dateRange.endDate)}
            </span>
            {dateLoading && (
              <div className="ml-2 w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            )}
          </div>
          
          {/* Date Range Inputs */}
          <div className="flex flex-col sm:flex-row items-center space-y-2 sm:space-y-0 sm:space-x-4">
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-text-color">Desde:</label>
              <input
                type="date"
                value={dateRange.startDate}
                onChange={(e) => handleDateChange('startDate', e.target.value)}
                className="border border-border-color rounded-lg px-3 py-2 text-sm text-text-color bg-card-bg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-text-color">Hasta:</label>
              <input
                type="date"
                value={dateRange.endDate}
                onChange={(e) => handleDateChange('endDate', e.target.value)}
                className="border border-border-color rounded-lg px-3 py-2 text-sm text-text-color bg-card-bg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Financial Summary Cards */}
      <div className={`grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 transition-opacity duration-300 ${dateLoading ? 'opacity-50' : 'opacity-100'}`}>
        {summary && (
          <>
            <div className="bg-card-bg border border-border-color rounded-lg shadow-lg p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <BanknotesIcon className="h-8 w-8 text-green-500" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-text-color opacity-70">Balance Total</p>
                  <p className="text-2xl font-bold text-text-color">
                    {formatCurrency(summary.balance)}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-card-bg border border-border-color rounded-lg shadow-lg p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <ArrowUpIcon className="h-8 w-8 text-green-500" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-text-color opacity-70">Ingresos Totales</p>
                  <p className="text-2xl font-bold text-green-500">
                    {formatCurrency(summary.total_income)}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-card-bg border border-border-color rounded-lg shadow-lg p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <ArrowDownIcon className="h-8 w-8 text-red-500" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-text-color opacity-70">Gastos Totales</p>
                  <p className="text-2xl font-bold text-red-500">
                    {formatCurrency(summary.total_expenses)}
                  </p>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Quick Actions */}
      <div className="bg-card-bg border border-border-color rounded-lg shadow-lg mb-8">
        <div className="px-6 py-4 border-b border-border-color">
          <h2 className="text-lg font-medium text-text-color">Acciones Rápidas</h2>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => setIsModalOpen(true)}
              className="flex items-center p-4 border border-border-color rounded-lg hover:bg-card-bg transition-colors text-left"
            >
              <PlusIcon className="h-6 w-6 text-blue-500 mr-3" />
              <div>
                <p className="font-medium text-text-color">Agregar Movimiento</p>
                <p className="text-sm text-text-color opacity-70">Registrar ingreso o gasto</p>
              </div>
            </button>

            <Link
              to="/budgets"
              className="flex items-center p-4 border border-border-color rounded-lg hover:bg-card-bg transition-colors"
            >
              <ChartBarIcon className="h-6 w-6 text-green-500 mr-3" />
              <div>
                <p className="font-medium text-text-color">Gestionar Presupuestos</p>
                <p className="text-sm text-text-color opacity-70">Configurar y seguir presupuestos</p>
              </div>
            </Link>

            <Link
              to="/reports"
              className="flex items-center p-4 border border-border-color rounded-lg hover:bg-card-bg transition-colors"
            >
              <CalendarIcon className="h-6 w-6 text-purple-500 mr-3" />
              <div>
                <p className="font-medium text-text-color">Ver Reportes</p>
                <p className="text-sm text-text-color opacity-70">Analizar tus finanzas</p>
              </div>
            </Link>
          </div>
        </div>
      </div>

      {/* Recent Movements */}
      <div className="bg-card-bg border border-border-color rounded-lg shadow-lg">
        <div className="px-6 py-4 border-b border-border-color flex justify-between items-center">
          <h2 className="text-lg font-medium text-text-color">Movimientos Recientes</h2>
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
              <button
                onClick={() => setIsModalOpen(true)}
                className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                <PlusIcon className="h-4 w-4 mr-2" />
                Add Movement
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Add Movement Modal */}
      <AddMovementModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onMovementAdded={handleMovementAdded}
      />
    </div>
  );
};

export default Dashboard; 