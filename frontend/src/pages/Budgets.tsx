import React, { useState, useEffect } from 'react';
import { 
  PlusIcon, 
  PencilIcon, 
  TrashIcon,
  ChartBarIcon,
  CalendarIcon,
  CurrencyDollarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon
} from '@heroicons/react/24/outline';
import { 
  BudgetItem, 
  BudgetItemCreate, 
  BudgetItemType, 
  BudgetPeriod, 
  BudgetSummary,
  BudgetProjection 
} from '../types';
import { apiService } from '../services/api';

const Budgets: React.FC = () => {
  const [budgetItems, setBudgetItems] = useState<BudgetItem[]>([]);
  const [projections, setProjections] = useState<BudgetSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingItem, setEditingItem] = useState<BudgetItem | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<number>(12);
  const [formData, setFormData] = useState<BudgetItemCreate>({
    name: '',
    amount: 0,
    type: BudgetItemType.INGRESO_RECURRENTE,
    category: '',
    frequency: BudgetPeriod.MENSUAL,
    start_date: new Date().toISOString().split('T')[0],
    end_date: undefined
  });

  useEffect(() => {
    fetchBudgetData();
  }, [selectedPeriod]);

  const fetchBudgetData = async () => {
    try {
      setLoading(true);
      const [itemsResponse, projectionsResponse] = await Promise.all([
        apiService.getBudgetItems(),
        apiService.getBudgetProjections(selectedPeriod)
      ]);
      
      setBudgetItems(itemsResponse.data || []);
      setProjections(projectionsResponse.data || null);
    } catch (error) {
      console.error('Error fetching budget data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await apiService.updateBudgetItem(editingItem.id, formData);
      } else {
        await apiService.createBudgetItem(formData);
      }
      setShowForm(false);
      setEditingItem(null);
      resetForm();
      fetchBudgetData();
    } catch (error) {
      console.error('Error saving budget item:', error);
    }
  };

  const handleEdit = (item: BudgetItem) => {
    setEditingItem(item);
    setFormData({
      name: item.name,
      amount: item.amount,
      type: item.type,
      category: item.category,
      frequency: item.frequency,
      start_date: item.start_date,
      end_date: item.end_date
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este elemento del presupuesto?')) {
      try {
        await apiService.deleteBudgetItem(id);
        fetchBudgetData();
      } catch (error) {
        console.error('Error deleting budget item:', error);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      amount: 0,
      type: BudgetItemType.INGRESO_RECURRENTE,
      category: '',
      frequency: BudgetPeriod.MENSUAL,
      start_date: new Date().toISOString().split('T')[0],
      end_date: undefined
    });
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long'
    });
  };

  const getTypeLabel = (type: BudgetItemType) => {
    return type === BudgetItemType.INGRESO_RECURRENTE ? 'Ingreso Recurrente' : 'Gasto Proyectado';
  };

  const getFrequencyLabel = (frequency: BudgetPeriod) => {
    switch (frequency) {
      case BudgetPeriod.SEMANAL: return 'Semanal';
      case BudgetPeriod.MENSUAL: return 'Mensual';
      case BudgetPeriod.ANUAL: return 'Anual';
      default: return frequency;
    }
  };

  const getTypeIcon = (type: BudgetItemType) => {
    return type === BudgetItemType.INGRESO_RECURRENTE ? 
      <ArrowTrendingUpIcon className="h-5 w-5 text-green-500" /> : 
      <ArrowTrendingDownIcon className="h-5 w-5 text-red-500" />;
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
        <h1 className="text-3xl font-bold text-white mb-2" style={{ fontFamily: 'var(--font-display)' }}>
          Planificación Presupuestaria
        </h1>
        <p className="text-lg text-gray-300" style={{ fontFamily: 'var(--font-body)' }}>
          Crea tu presupuesto estratégico con ingresos recurrentes y gastos proyectados
        </p>
      </div>

      {/* Period Selector */}
      <div className="mb-6">
        <div className="flex items-center space-x-4">
          <label className="text-white font-medium">Período de proyección:</label>
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(Number(e.target.value))}
            className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-white/50"
          >
            <option value={3}>3 meses</option>
            <option value={6}>6 meses</option>
            <option value={12}>12 meses</option>
          </select>
        </div>
      </div>

      {/* Summary Cards */}
      {projections && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg p-6">
            <div className="flex items-center">
              <ArrowTrendingUpIcon className="h-8 w-8 text-green-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-white/70">Ingresos Proyectados</p>
                <p className="text-2xl font-bold text-green-400">
                  {formatCurrency(projections.total_projected_income)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg p-6">
            <div className="flex items-center">
              <ArrowTrendingDownIcon className="h-8 w-8 text-red-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-white/70">Gastos Proyectados</p>
                <p className="text-2xl font-bold text-red-400">
                  {formatCurrency(projections.total_projected_expenses)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg p-6">
            <div className="flex items-center">
              <CurrencyDollarIcon className="h-8 w-8 text-blue-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-white/70">Balance Proyectado</p>
                <p className={`text-2xl font-bold ${projections.total_projected_balance >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {formatCurrency(projections.total_projected_balance)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg p-6">
            <div className="flex items-center">
              <ChartBarIcon className="h-8 w-8 text-purple-400 mr-3" />
              <div>
                <p className="text-sm font-medium text-white/70">Balance Real</p>
                <p className={`text-2xl font-bold ${projections.total_actual_balance >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {formatCurrency(projections.total_actual_balance)}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Budget Items Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Budget Items List */}
        <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-white" style={{ fontFamily: 'var(--font-display)' }}>
              Elementos del Presupuesto
            </h2>
            <button
              onClick={() => {
                setShowForm(true);
                setEditingItem(null);
                resetForm();
              }}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Agregar Elemento
            </button>
          </div>

          <div className="space-y-4">
            {budgetItems.length > 0 ? (
              budgetItems.map((item) => (
                <div key={item.id} className="flex items-center justify-between p-4 bg-white/10 rounded-lg">
                  <div className="flex items-center space-x-3">
                    {getTypeIcon(item.type)}
                    <div>
                      <p className="font-medium text-white">{item.name}</p>
                      <p className="text-sm text-white/70">
                        {getTypeLabel(item.type)} • {getFrequencyLabel(item.frequency)} • {item.category}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`font-medium ${
                      item.type === BudgetItemType.INGRESO_RECURRENTE ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {formatCurrency(item.amount)}
                    </span>
                    <button
                      onClick={() => handleEdit(item)}
                      className="p-1 text-white/70 hover:text-white"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(item.id)}
                      className="p-1 text-white/70 hover:text-red-400"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <p className="text-white/70">No hay elementos en el presupuesto</p>
                <button
                  onClick={() => {
                    setShowForm(true);
                    setEditingItem(null);
                    resetForm();
                  }}
                  className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                >
                  <PlusIcon className="h-4 w-4 mr-2" />
                  Crear Primer Elemento
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Projections Chart */}
        <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-6" style={{ fontFamily: 'var(--font-display)' }}>
            Proyección Mensual
          </h2>
          {projections && projections.projections.length > 0 ? (
            <div className="space-y-4">
              {projections.projections.map((projection) => (
                <div key={projection.month} className="p-4 bg-white/10 rounded-lg">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-medium text-white">{formatDate(projection.month)}</h3>
                    <span className={`font-bold ${
                      projection.variance_balance >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {formatCurrency(projection.variance_balance)}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-white/70">Proyectado</p>
                      <p className="text-green-400">+{formatCurrency(projection.projected_income)}</p>
                      <p className="text-red-400">-{formatCurrency(projection.projected_expenses)}</p>
                    </div>
                    <div>
                      <p className="text-white/70">Real</p>
                      <p className="text-green-400">+{formatCurrency(projection.actual_income)}</p>
                      <p className="text-red-400">-{formatCurrency(projection.actual_expenses)}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-white/70">No hay proyecciones disponibles</p>
            </div>
          )}
        </div>
      </div>

      {/* Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-white mb-4" style={{ fontFamily: 'var(--font-display)' }}>
              {editingItem ? 'Editar Elemento' : 'Nuevo Elemento'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-white mb-1">Nombre</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-white/50"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">Tipo</label>
                <select
                  value={formData.type}
                  onChange={(e) => setFormData({...formData, type: e.target.value as BudgetItemType})}
                  className="w-full bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-white/50"
                >
                  <option value={BudgetItemType.INGRESO_RECURRENTE}>Ingreso Recurrente</option>
                  <option value={BudgetItemType.GASTO_PROYECTADO}>Gasto Proyectado</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">Categoría</label>
                <input
                  type="text"
                  value={formData.category}
                  onChange={(e) => setFormData({...formData, category: e.target.value})}
                  className="w-full bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-white/50"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">Monto</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) => setFormData({...formData, amount: Number(e.target.value)})}
                  className="w-full bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-white/50"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">Frecuencia</label>
                <select
                  value={formData.frequency}
                  onChange={(e) => setFormData({...formData, frequency: e.target.value as BudgetPeriod})}
                  className="w-full bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-white/50"
                >
                  <option value={BudgetPeriod.SEMANAL}>Semanal</option>
                  <option value={BudgetPeriod.MENSUAL}>Mensual</option>
                  <option value={BudgetPeriod.ANUAL}>Anual</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-1">Fecha de Inicio</label>
                <input
                  type="date"
                  value={formData.start_date}
                  onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                  className="w-full bg-white/15 backdrop-blur-sm border border-white/20 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-white/50"
                  required
                />
              </div>

              <div className="flex space-x-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                  {editingItem ? 'Actualizar' : 'Crear'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingItem(null);
                    resetForm();
                  }}
                  className="flex-1 bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Budgets; 