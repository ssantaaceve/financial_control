import React, { useState } from 'react';
import { 
  XMarkIcon,
  PlusIcon,
  MinusIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import { MovementType } from '../types';
import { apiService } from '../services/api';
import CategoryAutocomplete from './CategoryAutocomplete';

interface AddMovementModalProps {
  isOpen: boolean;
  onClose: () => void;
  onMovementAdded: () => void;
}

const AddMovementModal: React.FC<AddMovementModalProps> = ({ isOpen, onClose, onMovementAdded }) => {
  const [formData, setFormData] = useState({
    amount: '',
    category: '',
    description: '',
    movement_type: MovementType.GASTO,
    movement_date: new Date().toISOString().split('T')[0]
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Función para formatear moneda
  const formatCurrency = (value: string): string => {
    // Si está vacío, retornar vacío
    if (!value) return '';
    
    // Remover todo excepto números y punto decimal
    const cleanValue = value.replace(/[^\d.]/g, '');
    
    // Si no hay números, retornar vacío
    if (!cleanValue) return '';
    
    // Manejar múltiples puntos decimales (solo permitir el primero)
    const parts = cleanValue.split('.');
    if (parts.length > 2) {
      return parts[0] + '.' + parts.slice(1).join('');
    }
    
    // Si solo hay un número sin punto decimal
    if (parts.length === 1) {
      const integerPart = parts[0];
      // Si el usuario está escribiendo y no ha terminado, no formatear aún
      if (integerPart.length < 4) {
        return integerPart;
      }
      // Si ya tiene varios dígitos, formatear con comas
      const number = parseInt(integerPart);
      if (isNaN(number)) return integerPart;
      return new Intl.NumberFormat('en-US').format(number);
    }
    
    // Si hay punto decimal
    const integerPart = parts[0] || '0';
    const decimalPart = parts[1] || '';
    
    // Limitar decimales a 2 dígitos
    const limitedDecimal = decimalPart.slice(0, 2);
    
    // Si el usuario está escribiendo decimales, mostrar como está
    if (decimalPart.length <= 2) {
      const formattedInteger = integerPart.length >= 4 
        ? new Intl.NumberFormat('en-US').format(parseInt(integerPart))
        : integerPart;
      return formattedInteger + (limitedDecimal ? '.' + limitedDecimal : '');
    }
    
    // Formateo completo
    const number = parseFloat(integerPart + '.' + limitedDecimal);
    if (isNaN(number)) return value;
    
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(number);
  };

  // Función para convertir formato de moneda a número
  const parseCurrency = (formattedValue: string): number => {
    return parseFloat(formattedValue.replace(/[^\d.]/g, '')) || 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!formData.amount || !formData.category || !formData.description) {
      setError('Please fill in all required fields');
      return;
    }

    const amount = parseCurrency(formData.amount);
    if (amount <= 0) {
      setError('Please enter a valid amount');
      return;
    }

    setIsLoading(true);

    try {
      await apiService.createMovement({
        ...formData,
        amount
      });
      
      // Reset form
      setFormData({
        amount: '',
        category: '',
        description: '',
        movement_type: MovementType.GASTO,
        movement_date: new Date().toISOString().split('T')[0]
      });
      
      onMovementAdded();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add movement');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (field: string, value: string) => {
    if (field === 'amount') {
      // Para el campo amount, permitir escribir y formatear inmediatamente
      const formattedValue = formatCurrency(value);
      setFormData(prev => ({
        ...prev,
        [field]: formattedValue
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [field]: value
      }));
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">Add Movement</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          {/* Movement Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Type *
            </label>
            <div className="flex space-x-2">
              <button
                type="button"
                onClick={() => handleChange('movement_type', MovementType.GASTO)}
                className={`flex-1 flex items-center justify-center py-2 px-4 rounded-lg border-2 transition-colors ${
                  formData.movement_type === MovementType.GASTO
                    ? 'border-red-500 bg-red-50 text-red-700'
                    : 'border-gray-300 text-gray-700 hover:border-gray-400'
                }`}
              >
                <MinusIcon className="h-5 w-5 mr-2" />
                Expense
              </button>
              <button
                type="button"
                onClick={() => handleChange('movement_type', MovementType.INGRESO)}
                className={`flex-1 flex items-center justify-center py-2 px-4 rounded-lg border-2 transition-colors ${
                  formData.movement_type === MovementType.INGRESO
                    ? 'border-green-500 bg-green-50 text-green-700'
                    : 'border-gray-300 text-gray-700 hover:border-gray-400'
                }`}
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Income
              </button>
            </div>
          </div>

          {/* Amount */}
          <div>
            <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
              Amount *
            </label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                $
              </span>
              <input
                id="amount"
                type="text"
                value={formData.amount}
                onChange={(e) => handleChange('amount', e.target.value)}
                className="block w-full pl-8 pr-3 py-2 border border-gray-300 rounded-lg text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="0.00"
              />
            </div>
          </div>

          {/* Category */}
          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">Category *</label>
            <CategoryAutocomplete
              value={formData.category}
              onChange={(category) => handleChange('category', category)}
              type={formData.movement_type}
              placeholder="Select or type a category"
            />
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Description *
            </label>
            <textarea
              id="description"
              rows={3}
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              placeholder="Brief description of the movement"
            />
          </div>

          {/* Date */}
          <div>
            <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-2">
              Date *
            </label>
            <div className="relative">
              <input
                id="date"
                type="date"
                value={formData.movement_date}
                onChange={(e) => handleChange('movement_date', e.target.value)}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <CalendarIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            </div>
          </div>

          {/* Actions */}
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                'Add Movement'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddMovementModal; 