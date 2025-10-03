// authService.js
import api from "./api"; // import your axios instance

// User registration function
export const registerUser = async (userData) => {
  try {
    // POST request to Django endpoint /api/users/register/
    const response = await api.post("users/register/", userData);

    // If your backend returns JWT tokens, store them
    if (response.data.access && response.data.refresh) {
      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);
    }

    return { success: true, data: response.data };
  } catch (error) {
    // Handle errors
    return {
      success: false,
      message: error.response?.data?.message || "Registration failed",
    };
  }
};

// Optional: You can add login/logout functions here later
