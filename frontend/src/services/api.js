import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

// Auth APIs
export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (userData) => api.post('/auth/register', userData),
};

// Performance APIs
export const performanceAPI = {
  getPrediction: (studentId) => api.get(`/performance/predict/${studentId}`),
  getDashboard: (studentId) => api.get(`/dashboard/${studentId}`),
};

// Test APIs
export const testAPI = {
  startAdaptiveTest: (data) => api.post('/tests/adaptive/start', data),
  submitAnswer: (data) => api.post('/tests/adaptive/submit', data),
  getTestHistory: (studentId) => api.get(`/tests/history/${studentId}`),
};

// Paper Analysis APIs
export const paperAPI = {
  analyzePaper: (formData) => {
    const config = {
      headers: { 'Content-Type': 'multipart/form-data' }
    };
    return api.post('/papers/analyze', formData, config);
  },
};

// Learning APIs
export const learningAPI = {
  getRecommendations: (studentId) => api.get(`/recommendations/${studentId}`),
  getContent: (topicId, type) => api.get(`/content/${topicId}/${type}`),
};

// Utility APIs
export const utilityAPI = {
  healthCheck: () => api.get('/health'),
};

export default api;