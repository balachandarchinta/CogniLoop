import React from 'react';
import { Box, Grid, Typography, Paper, Card, CardContent, LinearProgress } from '@mui/material';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';
import { Brain, Zap, Clock, TrendingUp } from 'lucide-react';
import { useSelector, useDispatch } from 'react-redux';
import { cognitiveService } from '../services/cognitiveService';
import { adaptiveService } from '../services/adaptiveService';
import { setProfile, setRecommendations } from '../store/slices/cognitiveSlice';

const attentionData = [
  { time: '09:00', value: 80 },
  { time: '10:00', value: 65 },
  { time: '11:00', value: 90 },
  { time: '12:00', value: 45 },
  { time: '13:00', value: 70 },
];

const StatCard = ({ title, value, icon: Icon, color, trend }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Box sx={{ p: 1, borderRadius: 2, background: `${color}15`, color: color }}>
          <Icon size={24} />
        </Box>
        <Typography variant="caption" sx={{ color: 'success.main', display: 'flex', alignItems: 'center' }}>
          {trend} <TrendingUp size={14} style={{ marginLeft: 4 }} />
        </Typography>
      </Box>
      <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5 }}>{value}</Typography>
      <Typography variant="body2" color="text.secondary">{title}</Typography>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const dispatch = useDispatch();
  const { profile, recommendations } = useSelector((state) => state.cognitive);
  const { user } = useSelector((state) => state.auth);

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const profileData = await cognitiveService.getLatestProfile();
        dispatch(setProfile(profileData));
        
        const pathData = await adaptiveService.getPersonalizedPath();
        dispatch(setRecommendations(pathData));
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
      }
    };
    fetchData();
  }, [dispatch]);

  const styleData = profile?.learning_style_scores ? [
    { subject: 'Visual', A: profile.learning_style_scores.visual || 0, fullMark: 100 },
    { subject: 'Auditory', A: profile.learning_style_scores.auditory || 0, fullMark: 100 },
    { subject: 'Reading', A: profile.learning_style_scores.reading_writing || 0, fullMark: 100 },
    { subject: 'Kinesthetic', A: profile.learning_style_scores.kinesthetic || 0, fullMark: 100 },
  ] : [
    { subject: 'Visual', A: 85, fullMark: 100 },
    { subject: 'Auditory', A: 45, fullMark: 100 },
    { subject: 'Reading', A: 70, fullMark: 100 },
    { subject: 'Kinesthetic', A: 95, fullMark: 100 },
  ];

  return (
    <Box sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontFamily: 'Outfit', fontWeight: 800, mb: 1 }}>
          Welcome back, <span className="gradient-text">{user?.full_name || 'Learner'}!</span>
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {profile ? `Your ${profile.learning_style} learning style is driving ${profile.attention_span_minutes}m of focus.` : 'Your cognitive engagement is peaking. Ready to dive in?'}
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Attention Score" value={`${Math.round((profile?.attention_span_minutes / 60) * 100) || 88}%`} icon={Zap} color="#6366f1" trend="+5%" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Retention Rate" value={`${Math.round((profile?.retention_rate || 0.72) * 100)}%`} icon={Brain} color="#ec4899" trend="+3%" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Comprehension" value={profile?.comprehension_speed || 'Fast'} icon={Clock} color="#8b5cf6" trend="Optimal" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Mastery Level" value="Level 14" icon={TrendingUp} color="#10b981" trend="+2" />
        </Grid>

        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Learning Style Profile</Typography>
            <ResponsiveContainer width="100%" height="85%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={styleData}>
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <Radar
                  name="Learner"
                  dataKey="A"
                  stroke="#6366f1"
                  fill="#6366f1"
                  fillOpacity={0.4}
                />
              </RadarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Engagement Trends</Typography>
            <ResponsiveContainer width="100%" height="85%">
              <AreaChart data={attentionData}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="time" stroke="#475569" fontSize={10} />
                <YAxis hide />
                <Tooltip 
                  contentStyle={{ background: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                  itemStyle={{ color: '#f8fafc' }}
                />
                <Area type="monotone" dataKey="value" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorValue)" strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Recommended for You</Typography>
            <Grid container spacing={2}>
              {recommendations.length > 0 ? recommendations.map((item) => (
                <Grid item xs={12} sm={4} key={item.id}>
                  <Box sx={{ 
                    p: 2, 
                    borderRadius: 2, 
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid rgba(255,255,255,0.05)',
                    '&:hover': { background: 'rgba(255,255,255,0.05)', cursor: 'pointer' }
                  }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>{item.title}</Typography>
                    <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                      <Box sx={{ px: 1, py: 0.5, borderRadius: 1, background: '#6366f120', color: '#818cf8', fontSize: '0.7rem' }}>
                        {item.content_format}
                      </Box>
                      <Box sx={{ px: 1, py: 0.5, borderRadius: 1, background: '#10b98120', color: '#34d399', fontSize: '0.7rem' }}>
                        {item.difficulty_level}
                      </Box>
                    </Box>
                    <Typography variant="caption" color="text.secondary">Est. Time: {item.duration_minutes} mins</Typography>
                    <LinearProgress variant="determinate" value={0} sx={{ mt: 1, borderRadius: 1, height: 4 }} />
                  </Box>
                </Grid>
              )) : (
                <Typography variant="body2" color="text.secondary" sx={{ p: 2 }}>
                  Complete your initial assessment to see recommendations.
                </Typography>
              )}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
