import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  HomeIcon, 
  PlusIcon, 
  ChartBarIcon, 
  CogIcon, 
  ArrowRightOnRectangleIcon,
  UserIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline';

const Sidebar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const location = useLocation();
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);

  const handleLogout = () => {
    logout();
  };

  if (!isAuthenticated) {
    return null;
  }

  const navigationItems = [
    {
      name: 'Dashboard',
      icon: HomeIcon,
      path: '/',
      description: 'Vista general de tus finanzas'
    },
    {
      name: 'Movimientos',
      icon: PlusIcon,
      path: '/movements',
      description: 'Gestionar ingresos y gastos'
    },
    {
      name: 'Presupuestos',
      icon: ChartBarIcon,
      path: '/budgets',
      description: 'Controlar presupuestos'
    },
    {
      name: 'Reportes',
      icon: DocumentTextIcon,
      path: '/reports',
      description: 'Ver reportes financieros'
    }
  ];

  const userItems = [
    {
      name: 'Perfil',
      icon: CogIcon,
      path: '/profile',
      description: 'Configurar tu perfil'
    },
    {
      name: 'Cerrar Sesión',
      icon: ArrowRightOnRectangleIcon,
      path: '#',
      description: 'Salir de la aplicación',
      action: handleLogout
    }
  ];

  return (
    <div className="fixed left-0 top-0 h-full w-16 bg-white shadow-lg border-r border-gray-200 z-50">
      {/* Logo */}
      <div className="flex items-center justify-center h-16 border-b border-gray-200">
        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-sm">FC</span>
        </div>
      </div>

      {/* Navigation Items */}
      <div className="flex flex-col items-center py-4 space-y-2">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <div
              key={item.name}
              className="relative group"
              onMouseEnter={() => setHoveredItem(item.name)}
              onMouseLeave={() => setHoveredItem(null)}
            >
              <Link
                to={item.path}
                className={`flex items-center justify-center w-12 h-12 rounded-lg transition-all duration-200 ${
                  isActive 
                    ? 'bg-blue-100 text-blue-600' 
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                <Icon className="h-6 w-6" />
              </Link>
              
              {/* Tooltip */}
              {hoveredItem === item.name && (
                <div className="absolute left-14 top-1/2 transform -translate-y-1/2 bg-gray-900 text-white text-sm px-3 py-2 rounded-lg shadow-lg whitespace-nowrap z-50">
                  <div className="font-medium">{item.name}</div>
                  <div className="text-gray-300 text-xs">{item.description}</div>
                  {/* Arrow */}
                  <div className="absolute right-full top-1/2 transform -translate-y-1/2 border-4 border-transparent border-r-gray-900"></div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* User Section */}
      <div className="absolute bottom-0 left-0 right-0 border-t border-gray-200">
        <div className="flex flex-col items-center py-4 space-y-2">
          {/* User Info */}
          <div
            className="relative group"
            onMouseEnter={() => setHoveredItem('user')}
            onMouseLeave={() => setHoveredItem(null)}
          >
            <div className="flex items-center justify-center w-12 h-12 rounded-lg bg-gray-100">
              <UserIcon className="h-6 w-6 text-gray-600" />
            </div>
            
            {hoveredItem === 'user' && (
              <div className="absolute left-14 bottom-0 transform -translate-y-1/2 bg-gray-900 text-white text-sm px-3 py-2 rounded-lg shadow-lg whitespace-nowrap z-50">
                <div className="font-medium">{user?.name}</div>
                <div className="text-gray-300 text-xs">Usuario actual</div>
                <div className="absolute right-full bottom-1/2 transform translate-y-1/2 border-4 border-transparent border-r-gray-900"></div>
              </div>
            )}
          </div>

          {/* User Actions */}
          {userItems.map((item) => {
            const Icon = item.icon;
            
            return (
              <div
                key={item.name}
                className="relative group"
                onMouseEnter={() => setHoveredItem(item.name)}
                onMouseLeave={() => setHoveredItem(null)}
              >
                {item.action ? (
                  <button
                    onClick={item.action}
                    className="flex items-center justify-center w-12 h-12 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-all duration-200"
                  >
                    <Icon className="h-6 w-6" />
                  </button>
                ) : (
                  <Link
                    to={item.path}
                    className="flex items-center justify-center w-12 h-12 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-all duration-200"
                  >
                    <Icon className="h-6 w-6" />
                  </Link>
                )}
                
                {/* Tooltip */}
                {hoveredItem === item.name && (
                  <div className="absolute left-14 top-1/2 transform -translate-y-1/2 bg-gray-900 text-white text-sm px-3 py-2 rounded-lg shadow-lg whitespace-nowrap z-50">
                    <div className="font-medium">{item.name}</div>
                    <div className="text-gray-300 text-xs">{item.description}</div>
                    <div className="absolute right-full top-1/2 transform -translate-y-1/2 border-4 border-transparent border-r-gray-900"></div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Sidebar; 