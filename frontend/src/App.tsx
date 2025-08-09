import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Movements from './pages/Movements';
import Budgets from './pages/Budgets';
import Profile from './pages/Profile';
import PrivateRoute from './components/PrivateRoute';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Rutas públicas */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Rutas privadas */}
            <Route path="/dashboard" element={
              <PrivateRoute>
                <div className="flex">
                  <Sidebar />
                  <main className="main-content">
                    <Dashboard />
                  </main>
                </div>
              </PrivateRoute>
            } />
            
            <Route path="/movements" element={
              <PrivateRoute>
                <div className="flex">
                  <Sidebar />
                  <main className="main-content">
                    <Movements />
                  </main>
                </div>
              </PrivateRoute>
            } />
            
            <Route path="/budgets" element={
              <PrivateRoute>
                <div className="flex">
                  <Sidebar />
                  <main className="main-content">
                    <Budgets />
                  </main>
                </div>
              </PrivateRoute>
            } />
            
            <Route path="/profile" element={
              <PrivateRoute>
                <div className="flex">
                  <Sidebar />
                  <main className="main-content">
                    <Profile />
                  </main>
                </div>
              </PrivateRoute>
            } />
            
            {/* Redirección por defecto */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
