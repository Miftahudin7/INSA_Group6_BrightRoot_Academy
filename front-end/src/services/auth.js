import api from "./api";

// Login: get tokens
export const login = async (username, password) => {
  const response = await api.post("token/", { username, password });
  if (response.data.access && response.data.refresh) {
    localStorage.setItem("access", response.data.access);
    localStorage.setItem("refresh", response.data.refresh);
  }
  return response.data;
};

// Refresh token
export const refreshToken = async () => {
  const refresh = localStorage.getItem("refresh");
  if (!refresh) throw new Error("No refresh token found");

  const response = await api.post("token/refresh/", { refresh });
  localStorage.setItem("access", response.data.access);
  return response.data;
};

// Register new user
export const register = async (username, email, password) => {
  const response = await api.post("users/register/", {
    username,
    email,
    password,
  });
  return response.data;
};

// Logout
export const logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};
