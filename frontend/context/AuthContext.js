import AsyncStorage from "@react-native-async-storage/async-storage";
import { createContext, useContext, useEffect, useState } from "react";
import authService from "../services/authService";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load user from storage on app start
  useEffect(() => {
    loadUserFromStorage();
  }, []);

  const loadUserFromStorage = async () => {
    try {
      const token = await AsyncStorage.getItem("accessToken");
      const savedUser = await AsyncStorage.getItem("user");

      if (token && savedUser) {
        setAccessToken(token);
        setUser(JSON.parse(savedUser));
      }
    } catch (error) {
      console.error("Failed to load user from storage", error);
    } finally {
      setLoading(false);
    }
  };

  // Login Function
  const login = async (email, password) => {
    try {
      const data = await authService.login({ email, password });

      await AsyncStorage.setItem("accessToken", data.accessToken);
      await AsyncStorage.setItem("user", JSON.stringify(data.user));

      setAccessToken(data.accessToken);
      setUser(data.user);

      return data;
    } catch (error) {
      throw error;
    }
  };

  // Register Function
  const register = async (userData) => {
    try {
      const data = await authService.register(userData);
      return data;
    } catch (error) {
      throw error;
    }
  };

  // Logout Function
  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      await AsyncStorage.removeItem("accessToken");
      await AsyncStorage.removeItem("user");
      setUser(null);
      setAccessToken(null);
    }
  };

  const value = {
    user,
    accessToken,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
