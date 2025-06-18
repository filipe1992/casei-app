import React, { createContext, useState, useEffect, useContext } from 'react';
import { setAuthToken } from '../lib/api/apiClient.ts';
import { API_CONFIG } from '../configs/api.ts';
import { authApi, LoginCredentials, User } from '../lib/api/auth.ts';

interface AuthState {
  isAuthenticated: boolean;
  loading: boolean;
  token: string | null;
  user: User | null;
}

interface AuthContextData extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  updateUser: (user: User) => void;
}

const initialAuthState: AuthState = {
  isAuthenticated: false,
  loading: true,
  token: null,
  user: null,
};

export const AuthContext = createContext<AuthContextData>({} as AuthContextData);

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>(initialAuthState);

  useEffect(() => {
    const loadUser = async () => {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        setAuthToken(storedToken);
        try {
          const userData = await authApi.getMe();
          setAuthState({
            token: storedToken,
            user: userData,
            isAuthenticated: true,
            loading: false,
          });
        } catch (error) {
          localStorage.removeItem('token');
          setAuthToken(null);
          setAuthState({ ...initialAuthState, loading: false });
        }
      } else {
        setAuthState({ ...initialAuthState, loading: false });
      }
    };
    loadUser();
  }, []);

  useEffect(() => {
    if (authState.token) {
      const intervalId = setInterval(async () => {
        try {
          if (!authState.token) return;
          const response = await authApi.refreshToken(authState.token);
          const newToken = response.access_token;
          setAuthToken(newToken);
          localStorage.setItem('token', newToken);
          setAuthState(prev => ({ ...prev, token: newToken }));
        } catch (error) {
          console.error('Erro ao atualizar token:', error);
          logout();
        }
      }, API_CONFIG.tokenRefreshInterval);

      return () => clearInterval(intervalId);
    }
  }, [authState.token]);

  const login = async (credentials: LoginCredentials) => {
    const response = await authApi.login(credentials);
    const newToken = response.access_token;

    setAuthToken(newToken);
    localStorage.setItem('token', newToken);

    const userData = await authApi.getMe();
    setAuthState({
      token: newToken,
      user: userData,
      isAuthenticated: true,
      loading: false,
    });
  };

  const updateUser = (newUser: User) => {
    setAuthState(prev => ({ ...prev, user: newUser }));
  };

  const logout = () => {
    localStorage.removeItem('token');
    setAuthToken(null);
    setAuthState({ ...initialAuthState, loading: false });
  };

  return (
    <AuthContext.Provider
      value={{
        ...authState,
        login,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};