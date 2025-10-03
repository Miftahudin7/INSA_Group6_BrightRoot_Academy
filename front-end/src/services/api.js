import axios from "axios";

// Backend base URL (change if needed)
const BASE_URL = "http://127.0.0.1:8000/api/";

// Create axios instance
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add interceptor to attach token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access"); // stored in browser
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
