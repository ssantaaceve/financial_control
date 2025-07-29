import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
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
  const { isDark } = useTheme();
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
      path: '/dashboard',
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
    <div className="fixed left-0 top-0 h-full w-16 bg-card-bg shadow-lg border-r border-border-color z-40">
      {/* Logo */}
      <div className="flex items-center justify-center h-16 border-b border-border-color">
        <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#d9ed92' }}>
          <span className="text-gray-800 font-bold text-xs">FL</span>
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
                    : 'text-text-color hover:bg-card-bg hover:text-blue-600'
                }`}
              >
                <Icon className="w-6 h-6" />
              </Link>
              
              {/* Tooltip */}
              {hoveredItem === item.name && (
                <div className="absolute left-14 top-1/2 transform -translate-y-1/2 bg-card-bg border border-border-color text-text-color text-sm px-3 py-2 rounded-lg shadow-lg whitespace-nowrap z-50">
                  <div className="font-medium">{item.name}</div>
                  <div className="opacity-70 text-xs">{item.description}</div>
                  {/* Arrow */}
                  <div className="absolute right-full top-1/2 transform -translate-y-1/2 border-4 border-transparent border-r-card-bg"></div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* User Section */}
      <div className="absolute bottom-0 left-0 right-0 border-t border-border-color">
        <div className="flex flex-col items-center py-4 space-y-2">
          {/* User Info */}
          <div
            className="relative group"
            onMouseEnter={() => setHoveredItem('user')}
            onMouseLeave={() => setHoveredItem(null)}
          >
            <div className="flex items-center justify-center w-12 h-12 rounded-lg bg-card-bg border border-border-color">
              <UserIcon className="w-6 h-6 text-text-color" />
            </div>
            
            {hoveredItem === 'user' && (
              <div className="absolute left-14 bottom-0 transform -translate-y-1/2 bg-card-bg border border-border-color text-text-color text-sm px-3 py-2 rounded-lg shadow-lg whitespace-nowrap z-50">
                <div className="font-medium">{user?.name}</div>
                <div className="opacity-70 text-xs">Usuario actual</div>
                <div className="absolute right-full bottom-1/2 transform translate-y-1/2 border-4 border-transparent border-r-card-bg"></div>
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
                    className="flex items-center justify-center w-12 h-12 rounded-lg text-text-color hover:bg-card-bg hover:text-red-600 transition-all duration-200"
                  >
                    <Icon className="w-6 h-6" />
                  </button>
                ) : (
                  <Link
                    to={item.path}
                    className="flex items-center justify-center w-12 h-12 rounded-lg text-text-color hover:bg-card-bg hover:text-blue-600 transition-all duration-200"
                  >
                    <Icon className="w-6 h-6" />
                  </Link>
                )}
                
                {/* Tooltip */}
                {hoveredItem === item.name && (
                  <div className="absolute left-14 top-1/2 transform -translate-y-1/2 bg-card-bg border border-border-color text-text-color text-sm px-3 py-2 rounded-lg shadow-lg whitespace-nowrap z-50">
                    <div className="font-medium">{item.name}</div>
                    <div className="opacity-70 text-xs">{item.description}</div>
                    <div className="absolute right-full top-1/2 transform -translate-y-1/2 border-4 border-transparent border-r-card-bg"></div>
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