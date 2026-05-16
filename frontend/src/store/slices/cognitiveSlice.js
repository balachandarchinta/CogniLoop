import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  profile: null,
  recommendations: [],
  activeSession: null,
  loading: false,
};

const cognitiveSlice = createSlice({
  name: 'cognitive',
  initialState,
  reducers: {
    setProfile: (state, action) => {
      state.profile = action.payload;
    },
    setRecommendations: (state, action) => {
      state.recommendations = action.payload;
    },
    updateMetrics: (state, action) => {
      if (state.profile) {
        state.profile.metrics = { ...state.profile.metrics, ...action.payload };
      }
    },
  },
});

export const { setProfile, setRecommendations, updateMetrics } = cognitiveSlice.actions;
export default cognitiveSlice.reducer;
