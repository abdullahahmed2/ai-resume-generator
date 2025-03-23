import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create an axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token in requests
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

// Authentication API calls
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/token', new URLSearchParams(credentials), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  }),
  getUser: () => api.get('/auth/me'),
};

// Resume API calls
export const resumeAPI = {
  createResume: (resumeData) => api.post('/resume/create', resumeData),
  getResumes: (params = {}) => api.get('/resume/list', { params }),
  getResume: (id) => api.get(`/resume/${id}`),
  updateResume: (id, resumeData) => api.put(`/resume/${id}`, resumeData),
  deleteResume: (id) => api.delete(`/resume/${id}`),
  
  // Version-related endpoints
  createVersion: (versionData) => api.post('/resume/version/create', versionData),
  getVersion: (id) => api.get(`/resume/version/${id}`),
  getVersions: (resumeId, params = {}) => api.get(`/resume/versions/${resumeId}`, { params }),
  downloadPdf: (versionId) => api.get(`/resume/download/${versionId}`, { responseType: 'blob' }),
};

// Template API calls
export const templateAPI = {
  getTemplates: (params = {}) => api.get('/template/list', { params }),
  getTemplate: (id) => api.get(`/template/${id}`),
};

// AI API calls
export const aiAPI = {
  generateSuggestions: (data) => api.post('/ai/generate-suggestions', data),
};

// Share API calls
export const shareAPI = {
  createShareLink: (data) => api.post('/share/generate', data),
  getShareLinks: (params = {}) => api.get('/share/list', { params }),
  deactivateShareLink: (id) => api.put(`/share/deactivate/${id}`),
  getSharedResume: (token) => api.get(`/share/resume/${token}`),
};

export default api; 