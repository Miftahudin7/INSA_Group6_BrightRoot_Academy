// AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Django backend

// Create the authentication context
const AuthContext = createContext();

// Custom hook
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

// Provider
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check auth on app load
  useEffect(() => {
    const checkAuthStatus = async () => {
      const access = localStorage.getItem("brightroot_token");
      const storedUser = localStorage.getItem("brightroot_user");

      if (access && storedUser) {
        try {
          // verify token is valid
          await axios.get(`${API_BASE_URL}/api/users/profile/`, {
            headers: { Authorization: `Bearer ${access}` },
          });
          setUser(JSON.parse(storedUser));
        } catch {
          await handleTokenRefresh();
        }
      }
      setIsLoading(false);
    };
    checkAuthStatus();
  }, []);

  // Token refresh
  const handleTokenRefresh = async () => {
    const refresh = localStorage.getItem("brightroot_refresh");
    if (!refresh) {
      logout();
      return;
    }
    try {
      const res = await axios.post(`${API_BASE_URL}/api/token/refresh/`, { refresh });
      localStorage.setItem("brightroot_token", res.data.access);

      // Fetch profile
      const profileRes = await axios.get(`${API_BASE_URL}/api/users/profile/`, {
        headers: { Authorization: `Bearer ${res.data.access}` },
      });

      localStorage.setItem("brightroot_user", JSON.stringify(profileRes.data));
      setUser(profileRes.data);
    } catch {
      logout();
    }
  };

  // Login
  const login = async (username, password) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/token/`, { username, password });
      const { access, refresh } = response.data;

      const profileRes = await axios.get(`${API_BASE_URL}/api/users/profile/`, {
        headers: { Authorization: `Bearer ${access}` },
      });

      const userData = profileRes.data;

      localStorage.setItem("brightroot_token", access);
      localStorage.setItem("brightroot_refresh", refresh);
      localStorage.setItem("brightroot_user", JSON.stringify(userData));
      setUser(userData);

      return { success: true, user: userData };
    } catch (err) {
      let message = "Login failed";
      if (err.response?.status === 401) message = "Invalid username or password";
      else if (err.response?.data?.detail) message = err.response.data.detail;

      setError(message);
      return { success: false, error: message };
    } finally {
      setIsLoading(false);
    }
  };

  // Logout
  const logout = () => {
    localStorage.clear();
    setUser(null);
    setError(null);
  };

  // Register
  const register = async (userData) => {
    setIsLoading(true);
    setError(null);

    try {
      // POST to Django registration endpoint
      const response = await axios.post(`${API_BASE_URL}/api/users/register/`, {
        username: userData.username,
        email: userData.email,
        password: userData.password,
      });

      // If backend returns JWT tokens
      const { access, refresh, user } = response.data;
      if (access && refresh) {
        localStorage.setItem("brightroot_token", access);
        localStorage.setItem("brightroot_refresh", refresh);
        if (user) {
          localStorage.setItem("brightroot_user", JSON.stringify(user));
          setUser(user);
        }
      }

      return { success: true, data: response.data };
    } catch (err) {
      let message = "Registration failed";

      if (err.response?.data) {
        const errors = err.response.data;
        if (errors.username) message = `Username: ${errors.username[0]}`;
        else if (errors.email) message = `Email: ${errors.email[0]}`;
        else if (errors.password) message = `Password: ${errors.password[0]}`;
        else if (errors.non_field_errors) message = errors.non_field_errors[0];
      }

      setError(message);
      return { success: false, error: message };
    } finally {
      setIsLoading(false);
    }
  };

  // Update user profile locally
  const updateUserProfile = (updates) => {
    const updatedUser = { ...user, ...updates };
    setUser(updatedUser);
    localStorage.setItem("brightroot_user", JSON.stringify(updatedUser));
  };

  const value = {
    user,
    isLoading,
    error,
    login,
    logout,
    register,
    updateUserProfile,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
