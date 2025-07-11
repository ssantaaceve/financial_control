// Tipos de usuario
export interface User {
  id: string;
  email: string;
  name: string;
  created_at?: string;
  updated_at?: string;
}

export interface UserCreate {
  email: string;
  password: string;
  name: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserUpdate {
  name?: string;
  email?: string;
}

// Tipos de movimiento
export enum MovementType {
  INGRESO = 'Ingreso',
  GASTO = 'Gasto'
}

export interface Movement {
  id: string;
  user_id: string;
  amount: number;
  category: string;
  description: string;
  movement_type: MovementType;
  movement_date: string;
  created_at?: string;
  updated_at?: string;
}

export interface MovementCreate {
  amount: number;
  category: string;
  description: string;
  movement_type: MovementType;
  movement_date: string;
}

export interface MovementUpdate {
  amount?: number;
  category?: string;
  description?: string;
  movement_type?: MovementType;
  movement_date?: string;
}

export interface MovementFilter {
  movement_type?: MovementType;
  category?: string;
  date_from?: string;
  date_to?: string;
  amount_min?: number;
  amount_max?: number;
}

// Tipos de presupuesto
export enum BudgetPeriod {
  SEMANAL = 'semanal',
  MENSUAL = 'mensual',
  ANUAL = 'anual'
}

export interface Budget {
  id: string;
  user_id: string;
  category: string;
  max_amount: number;
  current_amount: number;
  remaining_amount: number;
  percentage_used: number;
  period: BudgetPeriod;
  start_date: string;
  end_date: string;
  created_at?: string;
  updated_at?: string;
}

export interface BudgetCreate {
  category: string;
  max_amount: number;
  period: BudgetPeriod;
  start_date: string;
  end_date: string;
}

export interface BudgetUpdate {
  category?: string;
  max_amount?: number;
  period?: BudgetPeriod;
  start_date?: string;
  end_date?: string;
}

// Tipos de reportes
export interface FinancialSummary {
  total_income: number;
  total_expenses: number;
  balance: number;
  movement_count: number;
}

export interface BudgetSummary {
  total_budgets: number;
  total_allocated: number;
  total_spent: number;
  total_remaining: number;
  budgets: Budget[];
}

// Tipos de respuesta de la API
export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  user: User;
  token: {
    access_token: string;
    token_type: string;
  };
}

// Tipos de contexto
export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: UserCreate) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean;
} 