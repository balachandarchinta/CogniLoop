import React from 'react';
import { Box, Typography, Button, Container, Grid, Card, CardContent, Paper, Stack, useTheme } from '@mui/material';
import { motion } from 'framer-motion';
import { Brain, Zap, Target, ArrowRight, Shield, Globe, Cpu } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const FeatureCard = ({ icon: Icon, title, description, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay }}
    viewport={{ once: true }}
    style={{ display: 'flex', width: '100%', height: '100%' }}
  >
    <Card sx={{ 
      height: '100%', 
      maxWidth: 340,
      mx: 'auto',
      background: 'rgba(255, 255, 255, 0.03)', 
      border: '1px solid rgba(255, 255, 255, 0.08)',
      transition: 'transform 0.3s ease',
      '&:hover': { transform: 'translateY(-4px)', background: 'rgba(255, 255, 255, 0.05)' }
    }}>
      <CardContent sx={{ p: 2.5 }}>
        <Box sx={{ 
          width: 36, 
          height: 36, 
          borderRadius: 1.5, 
          background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mb: 1.5,
          color: 'white'
        }}>
          <Icon size={18} />
        </Box>
        <Typography variant="subtitle1" sx={{ fontWeight: 700, mb: 1, lineHeight: 1.2 }}>{title}</Typography>
        <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.5, fontSize: '0.85rem' }}>
          {description}
        </Typography>
      </CardContent>
    </Card>
  </motion.div>
);

const Landing = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  return (
    <Box sx={{ background: '#0f172a', color: 'white', overflow: 'hidden' }}>
      {/* Navbar (Landing Specific) */}
      <Container maxWidth="lg">
        <Box sx={{ py: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5" sx={{ fontWeight: 900, fontFamily: 'Outfit', letterSpacing: -1 }}>
            Cogni<span className="gradient-text">Loop</span>
          </Typography>
          <Stack direction="row" spacing={2} alignItems="center">
            <Button color="inherit" onClick={() => navigate('/login')}>Login</Button>
            <Button variant="contained" onClick={() => navigate('/login')}>Get Started</Button>
          </Stack>
        </Box>
      </Container>

      {/* Hero Section */}
      <Box sx={{ 
        pt: { xs: 10, md: 15 }, 
        pb: { xs: 4, md: 6 },
        position: 'relative'
      }}>
        <Container maxWidth="lg">
          <Grid container spacing={8} alignItems="center">
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
              >
                <Typography variant="overline" sx={{ 
                  color: '#818cf8', 
                  fontWeight: 800, 
                  letterSpacing: 2,
                  mb: 2,
                  display: 'block'
                }}>
                  THE FUTURE OF EDUCATION
                </Typography>
                <Typography variant="h1" sx={{ 
                  fontSize: { xs: '3rem', md: '4.5rem' }, 
                  lineHeight: 1.1, 
                  fontWeight: 900,
                  fontFamily: 'Outfit',
                  mb: 3
                }}>
                  Learning that <br />
                  <span className="gradient-text">Adapts to You.</span>
                </Typography>
                <Typography variant="h6" sx={{ color: 'text.secondary', fontWeight: 400, mb: 5, maxWidth: 500 }}>
                  CogniLoop uses advanced AI and cognitive profiling to create a personalized educational journey that evolves with every interaction.
                </Typography>
                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                  <Button 
                    variant="contained" 
                    size="large" 
                    endIcon={<ArrowRight size={20} />}
                    onClick={() => navigate('/login')}
                    sx={{ px: 4, py: 2, fontSize: '1.1rem' }}
                  >
                    Start Your Journey
                  </Button>
                  <Button 
                    variant="outlined" 
                    size="large"
                    sx={{ px: 4, py: 2, fontSize: '1.1rem', borderColor: 'rgba(255,255,255,0.2)' }}
                  >
                    View Demo
                  </Button>
                </Stack>
              </motion.div>
            </Grid>
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 1 }}
                style={{ position: 'relative' }}
              >
                <Box sx={{ 
                  width: '100%', 
                  height: 450, 
                  background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%)',
                  borderRadius: '30% 70% 70% 30% / 30% 30% 70% 70%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  border: '1px solid rgba(255, 255, 255, 0.05)',
                  position: 'relative',
                  overflow: 'hidden'
                }}>
                   {/* Abstract AI Visual */}
                   <Box sx={{ 
                     width: 200, 
                     height: 200, 
                     borderRadius: '50%', 
                     background: 'radial-gradient(circle, #6366f1 0%, transparent 70%)',
                     filter: 'blur(40px)',
                     animation: 'pulse 4s infinite alternate'
                   }} />
                   <Brain size={120} color="#818cf8" strokeWidth={1} style={{ position: 'absolute', zIndex: 2 }} />
                </Box>
                {/* Floating Stats */}
                <Paper sx={{ 
                  position: 'absolute', 
                  bottom: 20, 
                  left: -20, 
                  p: 2, 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: 2,
                  background: 'rgba(30, 41, 59, 0.8)',
                  backdropFilter: 'blur(8px)',
                  zIndex: 3
                }}>
                  <Box sx={{ p: 1, borderRadius: 1, background: '#10b98120', color: '#10b981' }}><Zap size={20} /></Box>
                  <Box>
                    <Typography variant="h6" sx={{ fontWeight: 800 }}>+45%</Typography>
                    <Typography variant="caption" color="text.secondary">Engagement Rate</Typography>
                  </Box>
                </Paper>
              </motion.div>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 5 }}>
          <Typography variant="h2" sx={{ fontWeight: 900, mb: 2 }}>Intelligent Ecosystem</Typography>
          <Typography variant="h6" color="text.secondary">Everything you need to master any subject, at your own pace.</Typography>
        </Box>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4} sx={{ display: 'flex' }}>
            <FeatureCard 
              icon={Brain}
              title="Cognitive Profiling"
              description="Our AI maps your unique learning style, attention patterns, and memory retention curve in real-time."
              delay={0.1}
            />
          </Grid>
          <Grid item xs={12} sm={4} sx={{ display: 'flex' }}>
            <FeatureCard 
              icon={Cpu}
              title="Adaptive Engine"
              description="Content difficulty and format adjust dynamically as you progress, keeping you in the optimal learning zone."
              delay={0.2}
            />
          </Grid>
          <Grid item xs={12} sm={4} sx={{ display: 'flex' }}>
            <FeatureCard 
              icon={Target}
              title="Precision Analytics"
              description="Deep insights into your comprehension speed and mastery levels with actionable recommendations."
              delay={0.3}
            />
          </Grid>
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box sx={{ 
        py: 6, 
        background: 'linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%)',
        textAlign: 'center'
      }}>
        <Container maxWidth="md">
          <Typography variant="h2" sx={{ fontWeight: 900, mb: 4 }}>Ready to evolve?</Typography>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 6 }}>
            Join 10,000+ learners who have transformed their education with CogniLoop.
          </Typography>
          <Button 
            variant="contained" 
            size="large" 
            onClick={() => navigate('/login')}
            sx={{ px: 6, py: 2, borderRadius: 10, fontSize: '1.2rem' }}
          >
            Create Your Free Account
          </Button>
        </Container>
      </Box>

      {/* Footer */}
      <Box sx={{ py: 6, borderTop: '1px solid rgba(255, 255, 255, 0.05)', textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          © 2026 CogniLoop AI. All rights reserved. Built with passion for better learning.
        </Typography>
      </Box>
    </Box>
  );
};

export default Landing;
