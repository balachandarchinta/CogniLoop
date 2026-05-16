import api from './api';

export const adaptiveService = {
  getAdaptationDirective: async () => {
    const response = await api.get('/adaptive/suggest');
    return response.data;
  },
  
  applyAdaptation: async (adaptationId, feedback) => {
    const response = await api.post('/adaptive/apply', { adaptation_id: adaptationId, feedback });
    return response.data;
  },
  
  getPersonalizedPath: async () => {
    const response = await api.get('/recommendations/path');
    return response.data;
  }
};
