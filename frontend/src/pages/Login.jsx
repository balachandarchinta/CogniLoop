import React, { useState } from 'react';
import { Box, Paper, Typography, TextField, Button, IconButton, InputAdornment, Link } from '@mui/material';
import { Eye, EyeOff, Mail, Lock, LogIn } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const Login = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // Logic for login will be added here
    console.log('Logging in...', email);
    navigate('/');
  };

  return (
    <Box sx={{ 
      height: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: 'radial-gradient(circle at top left, #1e1b4b 0%, #0f172a 100%)'
    }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Paper sx={{ 
          p: 5, 
          width: { xs: '90vw', sm: 400 }, 
          textAlign: 'center',
          background: 'rgba(30, 41, 59, 0.4)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <Box sx={{ mb: 4 }}>
            <Box sx={{ 
              width: 48, 
              height: 48, 
              borderRadius: 2, 
              background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
              mx: 'auto',
              mb: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <LogIn color="white" size={24} />
            </Box>
            <Typography variant="h5" sx={{ fontWeight: 800, fontFamily: 'Outfit' }}>
              Welcome to <span className="gradient-text">CogniLoop</span>
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Enter your credentials to access your portal
            </Typography>
          </Box>

          <form onSubmit={handleLogin}>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.5 }}>
              <TextField
                fullWidth
                label="Email Address"
                variant="outlined"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Mail size={18} color="#94a3b8" />
                    </InputAdornment>
                  ),
                }}
              />
              <TextField
                fullWidth
                label="Password"
                type={showPassword ? 'text' : 'password'}
                variant="outlined"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Lock size={18} color="#94a3b8" />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
              
              <Box sx={{ textAlign: 'right' }}>
                <Link href="#" variant="caption" color="primary" sx={{ textDecoration: 'none' }}>
                  Forgot password?
                </Link>
              </Box>

              <Button 
                fullWidth 
                size="large" 
                variant="contained" 
                type="submit"
                sx={{ py: 1.5, fontSize: '1rem', mt: 1 }}
              >
                Sign In
              </Button>

              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Don't have an account? {' '}
                <Link href="#" variant="body2" color="primary" sx={{ fontWeight: 600, textDecoration: 'none' }}>
                  Sign Up
                </Link>
              </Typography>
            </Box>
          </form>
        </Paper>
      </motion.div>
    </Box>
  );
};

export default Login;
