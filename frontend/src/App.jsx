import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        <Sidebar />
        <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
          <Navbar />
          <Box component="main" sx={{ flexGrow: 1, px: { xs: 2, sm: 4, md: 6 }, pb: 8 }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/learning" element={<Box sx={{ py: 4 }}><Dashboard /></Box>} /> {/* Placeholder */}
              <Route path="/analytics" element={<Box sx={{ py: 4 }}><Dashboard /></Box>} /> {/* Placeholder */}
              <Route path="/profile" element={<Box sx={{ py: 4 }}><Dashboard /></Box>} /> {/* Placeholder */}
            </Routes>
          </Box>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
