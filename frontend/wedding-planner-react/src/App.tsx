import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext.tsx';
import Login from './pages/Login.tsx';
import Settings from './pages/Settings.tsx';
import PrivateRoute from './components/PrivateRoute/PrivateRoute.tsx';
import Register from './pages/Register.tsx';
import { CssBaseline } from '@mui/material';
import Layout from './components/Layout/Layout.tsx';
import Guests from './pages/Guests.tsx';

function App() {
  return (
    <AuthProvider>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/settings"
            element={
              <PrivateRoute>
                <Layout>
                  <Settings />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/guests"
            element={
              <PrivateRoute>
                <Layout>
                  <Guests />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;