import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { authApi } from "../api/services";

const AuthContext = createContext(null);

const USER_KEY = "milkman_user";
const ACCESS_KEY = "milkman_access_token";
const REFRESH_KEY = "milkman_refresh_token";

export function AuthProvider({ children }) {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem(ACCESS_KEY));
  const [loading, setLoading] = useState(true);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  useEffect(() => {
    const serializedUser = localStorage.getItem(USER_KEY);
    if (serializedUser) {
      try {
        setUser(JSON.parse(serializedUser));
      } catch {
        localStorage.removeItem(USER_KEY);
      }
    }
    setLoading(false);
  }, []);

  const saveSession = (payload) => {
    setAccessToken(payload.access);
    setUser(payload.user);
    localStorage.setItem(ACCESS_KEY, payload.access);
    localStorage.setItem(REFRESH_KEY, payload.refresh);
    localStorage.setItem(USER_KEY, JSON.stringify(payload.user));
  };

  const clearSession = () => {
    setAccessToken(null);
    setUser(null);
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
  };

  const login = async (email, password) => {
    const response = await authApi.login({ email, password });
    saveSession(response.data);
    setIsLoginModalOpen(false);
    navigate(response.data.redirect_to, { replace: true });
    return response.data;
  };

  const register = async (payload) => {
    return authApi.register(payload);
  };

  const refreshProfile = async () => {
    const response = await authApi.profile();
    setUser(response.data);
    localStorage.setItem(USER_KEY, JSON.stringify(response.data));
    return response.data;
  };

  const updateProfile = async (payload) => {
    const response = await authApi.updateProfile(payload);
    setUser(response.data);
    localStorage.setItem(USER_KEY, JSON.stringify(response.data));
    return response.data;
  };

  const logout = () => {
    clearSession();
    navigate("/", { replace: true });
  };

  const value = {
    user,
    accessToken,
    loading,
    isAuthenticated: Boolean(accessToken && user),
    isAdmin: user?.role === "ADMIN" || user?.is_superuser,
    isCustomer: user?.role === "CUSTOMER",
    login,
    register,
    logout,
    refreshProfile,
    updateProfile,
    isLoginModalOpen,
    setIsLoginModalOpen,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
