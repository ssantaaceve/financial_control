import React, { useState, useEffect, useRef } from 'react';
import { MovementType, Category } from '../types';
import { apiService } from '../services/api';

interface CategoryAutocompleteProps {
  value: string;
  onChange: (value: string) => void;
  type: MovementType;
  placeholder?: string;
  className?: string;
}

const CategoryAutocomplete: React.FC<CategoryAutocompleteProps> = ({
  value,
  onChange,
  type,
  placeholder = "Select or type a category",
  className = ""
}) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [filteredCategories, setFilteredCategories] = useState<Category[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [creatingCategory, setCreatingCategory] = useState(false);
  const [inputValue, setInputValue] = useState(value);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Cargar categorías del backend
  useEffect(() => {
    const loadCategories = async () => {
      try {
        setLoading(true);
        const response = await apiService.getCategories(type);
        if (response.success && response.data) {
          setCategories(response.data);
          setFilteredCategories(response.data);
        }
      } catch (error) {
        console.error('Error loading categories:', error);
        // Si falla la carga, usar categorías por defecto
        setDefaultCategories();
      } finally {
        setLoading(false);
      }
    };

    loadCategories();
  }, [type]);

  // Categorías por defecto como fallback
  const setDefaultCategories = () => {
    const defaultCategories: Category[] = type === MovementType.GASTO ? [
      { id: '1', name: 'Alimentación', type: MovementType.GASTO, icon: '🍽️', color: '#EF4444' },
      { id: '2', name: 'Transporte', type: MovementType.GASTO, icon: '🚗', color: '#F59E0B' },
      { id: '3', name: 'Vivienda', type: MovementType.GASTO, icon: '🏠', color: '#8B5CF6' },
      { id: '4', name: 'Servicios', type: MovementType.GASTO, icon: '⚡', color: '#06B6D4' },
      { id: '5', name: 'Salud', type: MovementType.GASTO, icon: '🏥', color: '#10B981' },
      { id: '6', name: 'Educación', type: MovementType.GASTO, icon: '📚', color: '#3B82F6' },
      { id: '7', name: 'Entretenimiento', type: MovementType.GASTO, icon: '🎬', color: '#EC4899' },
      { id: '8', name: 'Ropa', type: MovementType.GASTO, icon: '👕', color: '#F97316' },
      { id: '9', name: 'Tecnología', type: MovementType.GASTO, icon: '💻', color: '#6366F1' },
      { id: '10', name: 'Deportes', type: MovementType.GASTO, icon: '⚽', color: '#84CC16' },
      { id: '11', name: 'Viajes', type: MovementType.GASTO, icon: '✈️', color: '#14B8A6' },
      { id: '12', name: 'Mascotas', type: MovementType.GASTO, icon: '🐕', color: '#F472B6' },
      { id: '13', name: 'Regalos', type: MovementType.GASTO, icon: '🎁', color: '#A855F7' },
      { id: '14', name: 'Impuestos', type: MovementType.GASTO, icon: '📋', color: '#DC2626' },
      { id: '15', name: 'Seguros', type: MovementType.GASTO, icon: '🛡️', color: '#059669' },
      { id: '16', name: 'Otros Gastos', type: MovementType.GASTO, icon: '📦', color: '#6B7280' }
    ] : [
      { id: '17', name: 'Salario', type: MovementType.INGRESO, icon: '💰', color: '#10B981' },
      { id: '18', name: 'Freelance', type: MovementType.INGRESO, icon: '💼', color: '#3B82F6' },
      { id: '19', name: 'Inversiones', type: MovementType.INGRESO, icon: '📈', color: '#F59E0B' },
      { id: '20', name: 'Negocios', type: MovementType.INGRESO, icon: '🏢', color: '#8B5CF6' },
      { id: '21', name: 'Rentas', type: MovementType.INGRESO, icon: '🏠', color: '#06B6D4' },
      { id: '22', name: 'Bonificaciones', type: MovementType.INGRESO, icon: '🎉', color: '#EC4899' },
      { id: '23', name: 'Reembolsos', type: MovementType.INGRESO, icon: '↩️', color: '#84CC16' },
      { id: '24', name: 'Préstamos', type: MovementType.INGRESO, icon: '🏦', color: '#F97316' },
      { id: '25', name: 'Herencia', type: MovementType.INGRESO, icon: '💎', color: '#A855F7' },
      { id: '26', name: 'Ventas', type: MovementType.INGRESO, icon: '🛒', color: '#14B8A6' },
      { id: '27', name: 'Comisiones', type: MovementType.INGRESO, icon: '📊', color: '#6366F1' },
      { id: '28', name: 'Otros Ingresos', type: MovementType.INGRESO, icon: '💵', color: '#6B7280' }
    ];
    
    setCategories(defaultCategories);
    setFilteredCategories(defaultCategories);
  };

  // Filtrar categorías basado en el input
  useEffect(() => {
    if (!inputValue.trim()) {
      setFilteredCategories(categories);
    } else {
      const filtered = categories.filter(category =>
        category.name.toLowerCase().includes(inputValue.toLowerCase())
      );
      setFilteredCategories(filtered);
    }
  }, [inputValue, categories]);

  // Manejar click fuera del componente
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        inputRef.current &&
        !inputRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [inputValue, categories, onChange]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setInputValue(newValue);
    onChange(newValue); // Actualizar el valor del padre inmediatamente
    setIsOpen(true);
  };

  const handleSelectCategory = (category: Category) => {
    setInputValue(category.name);
    onChange(category.name);
    setIsOpen(false);
  };

  const handleCreateCategory = async () => {
    if (!inputValue.trim()) return;
    
    // Verificar si la categoría ya existe
    const existingCategory = categories.find(cat => 
      cat.name.toLowerCase() === inputValue.toLowerCase()
    );
    
    if (existingCategory) {
      handleSelectCategory(existingCategory);
      return;
    }

    try {
      setCreatingCategory(true);
      
      // Crear nueva categoría
      const newCategoryData = {
        name: inputValue.trim(),
        type: type,
        icon: '📝', // Icono por defecto para nuevas categorías
        color: '#6B7280' // Color por defecto
      };

      const response = await apiService.createCategory(newCategoryData);
      
      if (response.success && response.data) {
        // Agregar la nueva categoría a la lista
        const newCategory = response.data;
        setCategories(prev => [...prev, newCategory]);
        
        // Seleccionar la nueva categoría
        setInputValue(newCategory.name);
        onChange(newCategory.name);
        setIsOpen(false);
      }
    } catch (error) {
      console.error('Error creating category:', error);
      // Si falla la creación, simplemente usar el texto como categoría
      setInputValue(inputValue);
      onChange(inputValue);
      setIsOpen(false);
    } finally {
      setCreatingCategory(false);
    }
  };

  const handleInputFocus = () => {
    setIsOpen(true);
  };

  const handleInputKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredCategories.length === 0 && inputValue.trim()) {
        // Si no hay categorías filtradas y hay texto, crear nueva categoría
        handleCreateCategory();
      } else if (filteredCategories.length === 1) {
        // Si hay exactamente una categoría filtrada, seleccionarla
        handleSelectCategory(filteredCategories[0]);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  // Encontrar la categoría seleccionada para mostrar el icono
  const selectedCategory = categories.find(cat => cat.name === value);
  
  // Verificar si el input actual no coincide con ninguna categoría existente
  const showCreateOption = inputValue.trim() && 
    !categories.some(cat => cat.name.toLowerCase() === inputValue.toLowerCase()) &&
    filteredCategories.length === 0;

  return (
    <div className="relative" ref={dropdownRef}>
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          onKeyDown={handleInputKeyDown}
          className={`block w-full px-3 py-2 border border-gray-300 rounded-lg text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${className}`}
          placeholder={placeholder}
        />
        {selectedCategory && selectedCategory.icon && (
          <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-lg">
            {selectedCategory.icon}
          </span>
        )}
      </div>
      
      {isOpen && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {loading ? (
            <div className="p-3 text-center text-gray-500">
              <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
              <p className="mt-2 text-sm">Loading categories...</p>
            </div>
          ) : filteredCategories.length > 0 ? (
            <div>
              {filteredCategories.map((category) => (
                <button
                  key={category.id}
                  type="button"
                  onClick={() => handleSelectCategory(category)}
                  className="w-full px-3 py-2 text-left hover:bg-gray-100 focus:bg-gray-100 focus:outline-none flex items-center"
                >
                  {category.icon && (
                    <span className="mr-3 text-lg">{category.icon}</span>
                  )}
                  <span className="text-gray-900">{category.name}</span>
                </button>
              ))}
            </div>
          ) : showCreateOption ? (
            <div className="p-3">
              <button
                type="button"
                onClick={handleCreateCategory}
                disabled={creatingCategory}
                className="w-full px-3 py-2 text-left hover:bg-blue-50 focus:bg-blue-50 focus:outline-none flex items-center text-blue-600 border-t border-gray-100"
              >
                <span className="mr-3 text-lg">📝</span>
                <span className="font-medium">
                  {creatingCategory ? 'Creating...' : `Create "${inputValue}"`}
                </span>
              </button>
            </div>
          ) : (
            <div className="p-3 text-center text-gray-500">
              <p className="text-sm">Type to search or create a new category</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CategoryAutocomplete; 