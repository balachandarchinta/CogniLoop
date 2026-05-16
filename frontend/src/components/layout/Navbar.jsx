import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Box, Avatar, Badge } from '@mui/material';
import { Bell, Search, Settings, Grid } from 'lucide-react';

const Navbar = () => {
  return (
    <AppBar position="sticky" elevation={0} sx={{ 
      background: 'rgba(15, 23, 42, 0.8)', 
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
      zIndex: (theme) => theme.zIndex.drawer + 1 
    }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box sx={{ 
            width: 32, 
            height: 32, 
            borderRadius: 1, 
            background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
            mr: 1.5,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Grid size={20} color="white" />
          </Box>
          <Typography variant="h6" sx={{ 
            fontWeight: 800, 
            fontFamily: 'Outfit',
            letterSpacing: -0.5,
            display: { xs: 'none', sm: 'block' }
          }}>
            CogniLoop
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <IconButton color="inherit" sx={{ display: { xs: 'none', md: 'flex' } }}>
            <Search size={20} />
          </IconButton>
          <IconButton color="inherit">
            <Badge badgeContent={4} color="error">
              <Bell size={20} />
            </Badge>
          </IconButton>
          <IconButton color="inherit">
            <Settings size={20} />
          </IconButton>
          <Box sx={{ ml: 2, display: 'flex', alignItems: 'center', gap: 1.5 }}>
            <Box sx={{ textAlign: 'right', display: { xs: 'none', sm: 'block' } }}>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>Alex Rivers</Typography>
              <Typography variant="caption" color="text.secondary">Intermediate Learner</Typography>
            </Box>
            <Avatar sx={{ 
              width: 36, 
              height: 36, 
              border: '2px solid #6366f1',
              background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)' 
            }}>A</Avatar>
          </Box>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
