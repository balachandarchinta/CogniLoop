import React from 'react';
import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Box, Typography } from '@mui/material';
import { LayoutDashboard, BookOpen, Target, BarChart3, User, LogOut } from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const menuItems = [
    { text: 'Dashboard', icon: <LayoutDashboard size={20} />, path: '/' },
    { text: 'My Learning', icon: <BookOpen size={20} />, path: '/learning' },
    { text: 'Goals', icon: <Target size={20} />, path: '/goals' },
    { text: 'Analytics', icon: <BarChart3 size={20} />, path: '/analytics' },
    { text: 'Profile', icon: <User size={20} />, path: '/profile' },
  ];

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { 
          width: 240, 
          boxSizing: 'border-box',
          background: '#0f172a',
          borderRight: '1px solid rgba(255, 255, 255, 0.05)',
          pt: 10
        },
      }}
    >
      <Box sx={{ overflow: 'auto', px: 2 }}>
        <List sx={{ gap: 0.5, display: 'flex', flexDirection: 'column' }}>
          {menuItems.map((item) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton
                onClick={() => navigate(item.path)}
                selected={location.pathname === item.path}
                sx={{
                  borderRadius: 2,
                  '&.Mui-selected': {
                    background: 'rgba(99, 102, 241, 0.1)',
                    color: '#818cf8',
                    '& .MuiListItemIcon-root': { color: '#818cf8' },
                    '&:hover': { background: 'rgba(99, 102, 241, 0.15)' }
                  },
                  '&:hover': {
                    background: 'rgba(255, 255, 255, 0.03)'
                  }
                }}
              >
                <ListItemIcon sx={{ minWidth: 40, color: 'text.secondary' }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} primaryTypographyProps={{ fontWeight: 500, fontSize: '0.9rem' }} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>

        <Box sx={{ mt: 'auto', pt: 4 }}>
          <ListItem disablePadding>
            <ListItemButton sx={{ borderRadius: 2, color: 'error.light' }}>
              <ListItemIcon sx={{ minWidth: 40, color: 'error.light' }}>
                <LogOut size={20} />
              </ListItemIcon>
              <ListItemText primary="Logout" primaryTypographyProps={{ fontWeight: 500, fontSize: '0.9rem' }} />
            </ListItemButton>
          </ListItem>
        </Box>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
