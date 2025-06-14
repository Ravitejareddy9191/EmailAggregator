import axios from 'axios';

const API_URL = 'http://localhost:8000/api/orders';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login on unauthorized
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  // Register new user
  async signup(userData) {
    try {
      const response = await api.post('/signup/', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Login user
  async login(credentials) {
    try {
      const response = await api.post('/login/', credentials);
      if (response.data.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Google OAuth login
  async googleLogin(token) {
    try {
      const response = await api.post('/oauth/', { token });
      if (response.data.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Logout user
  async logout() {
    try {
      await api.post('/logout/');
      localStorage.removeItem('user');
    } catch (error) {
      // Even if logout fails on server, clear local storage
      localStorage.removeItem('user');
    }
  },

  // Check authentication status
  async checkAuth() {
    try {
      const response = await api.get('/check-auth/');
      if (response.data.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      return response.data;
    } catch (error) {
      localStorage.removeItem('user');
      return { authenticated: false, user: null };
    }
  },

  // Get current user from localStorage
  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.getCurrentUser();
  },

  // Get user orders
  async getOrders() {
    try {
      const response = await api.get('/orders/');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get user profile
  async getProfile() {
    try {
      const response = await api.get('/profile/');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }
};

export default authService;
