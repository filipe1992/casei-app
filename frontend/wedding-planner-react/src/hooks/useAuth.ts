import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext.tsx';
import { authApi, LoginCredentials, RegisterData } from '../lib/api/auth.ts';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const useAuthApi = () => {
  const context = useAuth();

  const login = async (credentials: LoginCredentials) => {
    try {
      context.login(credentials)
      console.log("Login realizado com Sucesso!!")
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      throw error;
    }
  };

  const register = async (data: RegisterData) => {
    try {
      const response = await authApi.register(data);
      return response;
    } catch (error) {
      console.error('Erro ao registrar:', error);
      throw error;
    }
  };

  const logout = () => {
    context.logout();
  };

  return {
    isAuthenticated: context.isAuthenticated,
    token: context.token,
    user: context.user,
    login,
    register,
    logout,
  };
};