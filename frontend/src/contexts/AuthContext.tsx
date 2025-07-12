import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, UserCreate, AuthContextType } from '../types';
import apiService from '../services/api';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar si hay un token guardado al cargar la aplicación
    const savedToken = apiService.getAuthToken();
    const savedUser = apiService.getUser();

    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(savedUser);
      
      // Verificar que el token sea válido
      apiService.getCurrentUser()
        .then((currentUser) => {
          setUser(currentUser);
          apiService.setUser(currentUser);
        })
        .catch(() => {
          // Token inválido, limpiar datos
          apiService.clearAuth();
          setUser(null);
          setToken(null);
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await apiService.login({ email, password });
      
      if (response.success) {
        const { user: userData, token: authToken } = response;
        
        setUser(userData);
        setToken(authToken.access_token);
        
        apiService.setAuthToken(authToken.access_token);
        apiService.setUser(userData);
      } else {
        throw new Error(response.message || 'Error en el login');
      }
    } catch (error) {
      console.error('Error en login:', error);
      throw error;
    }
  };

  const register = async (userData: UserCreate) => {
    try {
      const response = await apiService.register(userData);
      
      if (response.success) {
        const { user: newUser, token: authToken } = response;
        
        setUser(newUser);
        setToken(authToken.access_token);
        
        apiService.setAuthToken(authToken.access_token);
        apiService.setUser(newUser);
      } else {
        throw new Error(response.message || 'Error en el registro');
      }
    } catch (error) {
      console.error('Error en registro:', error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    apiService.clearAuth();
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated: !!user && !!token,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
}; 