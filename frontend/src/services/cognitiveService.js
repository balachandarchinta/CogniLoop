import api from './api';

export const cognitiveService = {
  getLatestProfile: async () => {
    const response = await api.get('/cognitive/profile');
    return response.data;
  },
  
  getLearningStyle: async () => {
    const response = await api.get('/cognitive/style');
    return response.data;
  },
  
  getAttentionMetrics: async () => {
    const response = await api.get('/cognitive/attention');
    return response.data;
  },
  
  updateRealTimeEngagement: async (metrics) => {
    const response = await api.post('/cognitive/engagement', metrics);
    return response.data;
  }
};
