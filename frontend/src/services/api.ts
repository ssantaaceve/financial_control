import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  User,
  UserCreate,
  UserLogin,
  UserUpdate,
  Movement,
  MovementCreate,
  MovementUpdate,
  MovementFilter,
  Budget,
  BudgetCreate,
  BudgetUpdate,
  ApiResponse,
  AuthResponse,
  Category,
  MovementType
} from '../types';

// Interfaces locales para reportes
interface FinancialSummary {
  total_income: number;
  total_expenses: number;
  balance: number;
  movement_count: number;
}

interface BudgetSummary {
  total_budgets: number;
  total_allocated: number;
  total_spent: number;
  total_remaining: number;
  budgets: Budget[];
}

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para agregar el token de autenticación
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Interceptor para manejar errores de respuesta
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Métodos de autenticación
  async register(userData: UserCreate): Promise<AuthResponse> {
    console.log('🔍 Register API call:', {
      url: `${this.api.defaults.baseURL}/auth/register`,
      data: userData
    });
    
    try {
      const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/register', userData);
      console.log('✅ Register response:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Register error:', error);
      throw error;
    }
  }

  async login(credentials: UserLogin): Promise<AuthResponse> {
    const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/login', credentials);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response: AxiosResponse<User> = await this.api.get('/users/me');
    return response.data;
  }

  async updateUserProfile(updateData: UserUpdate): Promise<ApiResponse<User>> {
    const response: AxiosResponse<ApiResponse<User>> = await this.api.put('/users/me', updateData);
    return response.data;
  }

  // Métodos de movimientos
  async createMovement(movementData: MovementCreate): Promise<ApiResponse<Movement>> {
    const response: AxiosResponse<ApiResponse<Movement>> = await this.api.post('/movements', movementData);
    return response.data;
  }

  async getMovements(filters?: MovementFilter): Promise<ApiResponse<Movement[]>> {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response: AxiosResponse<ApiResponse<Movement[]>> = await this.api.get(`/movements?${params.toString()}`);
    return response.data;
  }

  async getMovementById(id: string): Promise<ApiResponse<Movement>> {
    const response: AxiosResponse<ApiResponse<Movement>> = await this.api.get(`/movements/${id}`);
    return response.data;
  }

  async updateMovement(id: string, updateData: MovementUpdate): Promise<ApiResponse<Movement>> {
    const response: AxiosResponse<ApiResponse<Movement>> = await this.api.put(`/movements/${id}`, updateData);
    return response.data;
  }

  async deleteMovement(id: string): Promise<ApiResponse<void>> {
    const response: AxiosResponse<ApiResponse<void>> = await this.api.delete(`/movements/${id}`);
    return response.data;
  }

  // Métodos de presupuestos
  async getBudgets(): Promise<ApiResponse<Budget[]>> {
    const response: AxiosResponse<ApiResponse<Budget[]>> = await this.api.get('/budgets');
    return response.data;
  }

  async createBudget(budget: BudgetCreate): Promise<ApiResponse<Budget>> {
    const response: AxiosResponse<ApiResponse<Budget>> = await this.api.post('/budgets', budget);
    return response.data;
  }

  async updateBudget(id: string, budget: BudgetUpdate): Promise<ApiResponse<Budget>> {
    const response: AxiosResponse<ApiResponse<Budget>> = await this.api.put(`/budgets/${id}`, budget);
    return response.data;
  }

  async deleteBudget(id: string): Promise<ApiResponse<null>> {
    const response: AxiosResponse<ApiResponse<null>> = await this.api.delete(`/budgets/${id}`);
    return response.data;
  }

  // Método para obtener resumen financiero
  async getFinancialSummary(startDate?: string, endDate?: string): Promise<ApiResponse<FinancialSummary>> {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);

    const response: AxiosResponse<ApiResponse<FinancialSummary>> = await this.api.get(`/reports/financial-summary?${params.toString()}`);
    return response.data;
  }

  // Métodos de categorías
  async getCategories(type?: MovementType): Promise<ApiResponse<Category[]>> {
    const params = new URLSearchParams();
    if (type) {
      params.append('type', type);
    }

    const response: AxiosResponse<ApiResponse<Category[]>> = await this.api.get(`/categories?${params.toString()}`);
    return response.data;
  }

  async createCategory(categoryData: { name: string; type: MovementType; icon?: string; color?: string }): Promise<ApiResponse<Category>> {
    const response: AxiosResponse<ApiResponse<Category>> = await this.api.post('/categories', categoryData);
    return response.data;
  }

  // Métodos de utilidad
  setAuthToken(token: string) {
    localStorage.setItem('auth_token', token);
  }

  getAuthToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  removeAuthToken() {
    localStorage.removeItem('auth_token');
  }

  setUser(user: User) {
    localStorage.setItem('user', JSON.stringify(user));
  }

  getUser(): User | null {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  removeUser() {
    localStorage.removeItem('user');
  }

  clearAuth() {
    this.removeAuthToken();
    this.removeUser();
  }
}

export const apiService = new ApiService();
export default apiService; 