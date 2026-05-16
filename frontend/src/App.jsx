import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { useSelector } from 'react-redux';
import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';
import Dashboard from './pages/Dashboard';
import Learning from './pages/Learning';
import Login from './pages/Login';
import Landing from './pages/Landing';

const Layout = ({ children }) => (
  <Box sx={{ display: 'flex', minHeight: '100vh' }}>
    <Sidebar />
    <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
      <Navbar />
      <Box component="main" sx={{ flexGrow: 1, px: { xs: 2, sm: 4, md: 6 }, pb: 8 }}>
        {children}
      </Box>
    </Box>
  </Box>
);

function App() {
  const { isAuthenticated } = useSelector((state) => state.auth);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" />} />
        
        <Route path="/" element={
          isAuthenticated ? <Layout><Dashboard /></Layout> : <Landing />
        } />
        
        <Route path="/learning" element={
          isAuthenticated ? <Layout><Learning /></Layout> : <Navigate to="/login" />
        } />
        
        <Route path="/analytics" element={
          isAuthenticated ? <Layout><Dashboard /></Layout> : <Navigate to="/login" />
        } />
        
        <Route path="/profile" element={
          isAuthenticated ? <Layout><Dashboard /></Layout> : <Navigate to="/login" />
        } />
      </Routes>
    </Router>
  );
}

export default App;
