import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import cognitiveReducer from './slices/cognitiveSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    cognitive: cognitiveReducer,
  },
});
