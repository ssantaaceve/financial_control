import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  HomeIcon, 
  PlusIcon, 
  ChartBarIcon, 
  CogIcon, 
  ArrowRightOnRectangleIcon,
  UserIcon
} from '@heroicons/react/24/outline';

const Navbar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <nav className="bg-white shadow-lg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">FC</span>
              </div>
              <span className="text-xl font-bold text-gray-900">Financial Control</span>
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className="flex items-center space-x-1 text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              <HomeIcon className="h-5 w-5" />
              <span>Dashboard</span>
            </Link>

            <Link
              to="/movements"
              className="flex items-center space-x-1 text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              <PlusIcon className="h-5 w-5" />
              <span>Movimientos</span>
            </Link>

            <Link
              to="/budgets"
              className="flex items-center space-x-1 text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              <ChartBarIcon className="h-5 w-5" />
              <span>Presupuestos</span>
            </Link>

            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-2 text-gray-700">
                <UserIcon className="h-4 w-4" />
                <span className="text-sm font-medium">{user?.name}</span>
              </div>

              <div className="flex items-center space-x-1">
                <Link
                  to="/profile"
                  className="text-gray-700 hover:text-primary-600 p-2 rounded-md transition-colors"
                  title="Perfil"
                >
                  <CogIcon className="h-5 w-5" />
                </Link>

                <button
                  onClick={handleLogout}
                  className="text-gray-700 hover:text-danger-600 p-2 rounded-md transition-colors"
                  title="Cerrar sesión"
                >
                  <ArrowRightOnRectangleIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 