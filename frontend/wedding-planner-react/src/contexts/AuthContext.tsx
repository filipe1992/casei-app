import React, { createContext, useState, useEffect, useContext } from 'react';
import { setAuthToken } from '../lib/api/apiClient.ts';
import { API_CONFIG } from '../configs/api.ts';
import { authApi, LoginCredentials, User } from '../lib/api/auth.ts';

interface AuthContextData {
  isAuthenticated: boolean;
  token: string | null;
  user: User | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextData>({} as AuthContextData);

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const loadUser = async () => {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        setAuthToken(storedToken);
        try {
          const userData = await authApi.getMe();
          setUser(userData);
          setToken(storedToken);
          setIsAuthenticated(true);
        } catch (error) {
          localStorage.removeItem('token');
          setAuthToken(null);
        }
      }
    };
    loadUser();
  }, []);

  useEffect(() => {
    if (token) {
      const intervalId = setInterval(async () => {
        try {
          const response = await authApi.refreshToken(token);
          const newToken = response.access_token;
          setToken(newToken);
          setAuthToken(newToken);
        } catch (error) {
          console.error('Erro ao atualizar token:', error);
          setToken(null);
          setIsAuthenticated(false);
          localStorage.removeItem('token');
          setAuthToken(null);
        }
      }, API_CONFIG.tokenRefreshInterval);

      return () => clearInterval(intervalId);
    } else {
      localStorage.removeItem('token');
      setAuthToken(null);
    }
  }, [token]);

  const login = async (credentials: LoginCredentials) => {
    const response = await authApi.login(credentials);
    const newToken = response.access_token;

    setAuthToken(newToken);
    localStorage.setItem('token', newToken);

    const userData = await authApi.getMe();
    setUser(userData);
    setToken(newToken);
    setIsAuthenticated(true);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
    localStorage.removeItem('token');
    setAuthToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        token,
        user,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};