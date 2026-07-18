import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";

const API_URL = "http://localhost:5000/api/auth";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem("accessToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  register: async (userData) => {
    const response = await api.post("/register", userData);
    return response.data;
  },

  login: async (credentials) => {
    const response = await api.post("/login", credentials);

    // Save access token
    if (response.data.accessToken) {
      await AsyncStorage.setItem("accessToken", response.data.accessToken);
    }

    return response.data;
  },

  logout: async () => {
    await api.post("/logout");
    await AsyncStorage.removeItem("accessToken");
  },

  getProfile: async () => {
    const response = await api.get("/profile");
    return response.data;
  },
};

export default authService;
