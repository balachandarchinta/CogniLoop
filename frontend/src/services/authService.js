import api from './api';

export const authService = {
  login: async (email, password) => {
    // Note: In a real FastAPI app, this might be form-data or JSON depending on OAuth2 spec
    // For now, we'll assume JSON
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },
  
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  
  getProfile: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  }
};
