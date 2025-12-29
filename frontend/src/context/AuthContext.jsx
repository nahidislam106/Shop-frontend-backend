import React, { createContext, useEffect, useState } from 'react';
import api from '../api/client';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const access = localStorage.getItem('access');
    if (!access) {
      setLoading(false);
      return;
    }
    api
      .get('/auth/me/')
      .then((res) => setUser(res.data))
      .catch(() => {
        setUser(null);
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (username, password) => {
    const { data } = await api.post('/auth/token/', { username, password });
    localStorage.setItem('access', data.access);
    localStorage.setItem('refresh', data.refresh);
    const me = await api.get('/auth/me/');
    setUser(me.data);
  };

  const register = async (payload) => {
    await api.post('/auth/register/', payload);
    await login(payload.username, payload.password);
  };

  const logout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    setUser(null);
  };

  const refreshUser = async () => {
    const me = await api.get('/auth/me/');
    setUser(me.data);
  };

  const value = { user, login, register, logout, refreshUser, loading };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
