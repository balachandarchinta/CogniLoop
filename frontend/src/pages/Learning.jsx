import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Grid, Button, IconButton, LinearProgress, Divider, Chip } from '@mui/material';
import { Play, SkipForward, CheckCircle, Info, Clock, Award, Zap } from 'lucide-react';
import { cognitiveService } from '../services/cognitiveService';
import { adaptiveService } from '../services/adaptiveService';
import { motion, AnimatePresence } from 'framer-motion';

const Learning = () => {
  const [progress, setProgress] = useState(0);
  const [activeConcept, setActiveConcept] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [directive, setDirective] = useState(null);

  const concepts = [
    { title: 'Introduction to Quantum States', duration: '5m', type: 'Video' },
    { title: 'Superposition & Entanglement', duration: '12m', type: 'Interactive' },
    { title: 'Qubits vs Classical Bits', duration: '8m', type: 'Article' },
    { title: 'Initial Assessment', duration: '10m', type: 'Quiz' },
  ];

  useEffect(() => {
    const fetchDirective = async () => {
      const data = await adaptiveService.getAdaptationDirective();
      setDirective(data);
    };
    fetchDirective();
  }, []);

  useEffect(() => {
    if (progress < 100) {
      const timer = setInterval(() => {
        setProgress((old) => Math.min(old + 0.5, 100));
        
        // Every 5% progress, send engagement data
        if (Math.floor(progress) % 5 === 0 && progress > 0) {
          cognitiveService.updateRealTimeEngagement({
            session_id: "active", // In real case, use real session ID
            engagement_score: 0.85,
            comprehension_speed: "fast"
          });
        }
      }, 500);
      return () => clearInterval(timer);
    } else {
      setIsCompleted(true);
    }
  }, [progress]);

  return (
    <Box sx={{ py: 4 }}>
      <Grid container spacing={4}>
        {/* Content Viewer Area */}
        <Grid item xs={12} lg={8}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <Paper sx={{ 
              height: { xs: 300, sm: 450 }, 
              mb: 3, 
              position: 'relative',
              overflow: 'hidden',
              background: '#000',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              {/* Mock Video/Content Area */}
              <Box sx={{ textAlign: 'center', zIndex: 1 }}>
                <Typography variant="h5" sx={{ mb: 2, color: 'white' }}>
                  {concepts[activeConcept].title}
                </Typography>
                <IconButton sx={{ 
                  width: 80, 
                  height: 80, 
                  background: 'rgba(99, 102, 241, 0.8)',
                  '&:hover': { background: '#6366f1' }
                }}>
                  <Play size={40} color="white" />
                </IconButton>
              </Box>
              <Box sx={{ 
                position: 'absolute', 
                bottom: 0, 
                left: 0, 
                right: 0, 
                height: 4, 
                background: 'rgba(255,255,255,0.1)' 
              }}>
                <Box sx={{ 
                  width: `${progress}%`, 
                  height: '100%', 
                  background: '#6366f1',
                  transition: 'width 0.5s ease'
                }} />
              </Box>
            </Paper>

            <Box sx={{ mb: 4 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h5" sx={{ fontWeight: 700 }}>
                  Principles of Quantum Computing
                </Typography>
                <Chip icon={<Zap size={14} />} label="Active Learning" color="secondary" size="small" />
              </Box>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                In this session, we explore the fundamental building blocks of quantum information. 
                You'll learn how particles exist in multiple states simultaneously and how this 
                exponentially increases processing power.
              </Typography>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button variant="outlined" startIcon={<Info size={18} />}>Resources</Button>
                <Button variant="outlined" startIcon={<Clock size={18} />}>Set Reminder</Button>
              </Box>
            </Box>
          </motion.div>
        </Grid>

        {/* Sidebar / Progress Area */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3, position: 'sticky', top: 100 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Learning Path</Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {concepts.map((c, i) => (
                <Box 
                  key={i} 
                  onClick={() => setActiveConcept(i)}
                  sx={{ 
                    p: 2, 
                    borderRadius: 2, 
                    cursor: 'pointer',
                    background: i === activeConcept ? 'rgba(99, 102, 241, 0.1)' : 'transparent',
                    border: i === activeConcept ? '1px solid rgba(99, 102, 241, 0.3)' : '1px solid transparent',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 2,
                    '&:hover': { background: 'rgba(255,255,255,0.03)' }
                  }}
                >
                  <Box sx={{ 
                    width: 32, 
                    height: 32, 
                    borderRadius: '50%', 
                    background: i < activeConcept ? '#10b981' : 'rgba(255,255,255,0.05)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: i < activeConcept ? 'white' : 'text.secondary'
                  }}>
                    {i < activeConcept ? <CheckCircle size={18} /> : i + 1}
                  </Box>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>{c.title}</Typography>
                    <Typography variant="caption" color="text.secondary">{c.type} • {c.duration}</Typography>
                  </Box>
                </Box>
              ))}
            </Box>

            <Divider sx={{ my: 4 }} />

            <Box sx={{ textAlign: 'center' }}>
              <Box sx={{ mb: 2, display: 'flex', justifyContent: 'center' }}>
                <Award size={48} color={isCompleted ? '#f59e0b' : '#334155'} />
              </Box>
              <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>Mastery Progress</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Complete this module to earn 250 XP
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={progress} 
                sx={{ height: 8, borderRadius: 4, mb: 3 }} 
              />
              <Button 
                fullWidth 
                variant="contained" 
                disabled={!isCompleted}
                sx={{ py: 1.5 }}
              >
                Claim Achievement
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Learning;
