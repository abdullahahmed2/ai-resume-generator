import axios from 'axios';

// Get API URL from environment variables
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create an axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true // Include cookies in requests
});

// Add request interceptor to attach auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    // Handle 401 Unauthorized errors (expired token)
    if (error.response && error.response.status === 401) {
      // Clear stored tokens
      localStorage.removeItem('accessToken');
      
      // Redirect to login page
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

// API service functions
export const apiService = {
  // Auth endpoints
  login: (credentials) => apiClient.post('/auth/token', credentials),
  register: (userData) => apiClient.post('/auth/register', userData),
  
  // Resume endpoints
  getResumes: () => apiClient.get('/resume/list'),
  getResume: (id) => apiClient.get(`/resume/${id}`),
  createResume: (data) => apiClient.post('/resume/create', data),
  createResumeWithContent: (data) => apiClient.post('/resume/create_with_content', data),
  updateResume: (id, data) => apiClient.put(`/resume/${id}`, data),
  deleteResume: (id) => apiClient.delete(`/resume/${id}`),
  
  // Resume version endpoints
  getResumeVersions: (resumeId) => apiClient.get(`/resume/versions/${resumeId}`),
  getResumeVersion: (versionId) => apiClient.get(`/resume/version/${versionId}`),
  createResumeVersion: (data) => apiClient.post('/resume/version/create', data),
  
  // Template endpoints
  getTemplates: () => apiClient.get('/template/list'),
  getTemplate: (id) => apiClient.get(`/template/${id}`),
  
  // AI assistance endpoints
  generateSummary: (data) => apiClient.post('/ai/generate-summary', data),
  improveContent: (data) => apiClient.post('/ai/improve-content', data),
  generateJobDescriptions: (data) => apiClient.post('/ai/generate-job-descriptions', data),
  getRelevantSkills: (data) => apiClient.post('/ai/get-relevant-skills', data),
  analyzeJobDescription: (data) => apiClient.post('/ai/analyze-job-description', data),
  suggestImprovements: (data) => apiClient.post('/ai/suggest-improvements', data),
  
  // PDF endpoints
  uploadPDF: (formData) => apiClient.post('/resume/upload-pdf', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  
  // Generic methods
  get: (url, config) => apiClient.get(url, config),
  post: (url, data, config) => apiClient.post(url, data, config),
  put: (url, data, config) => apiClient.put(url, data, config),
  delete: (url, config) => apiClient.delete(url, config),
};

export default apiService; 