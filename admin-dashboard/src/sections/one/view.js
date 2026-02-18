'use client';

import { useState, useEffect, useCallback } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import { alpha } from '@mui/material/styles';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import CardContent from '@mui/material/CardContent';
import LinearProgress from '@mui/material/LinearProgress';
import Chip from '@mui/material/Chip';
import Divider from '@mui/material/Divider';
import Skeleton from '@mui/material/Skeleton';

// Icons
import LanguageIcon from '@mui/icons-material/Language';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import TodayIcon from '@mui/icons-material/Today';
import PublishIcon from '@mui/icons-material/Publish';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import RedditIcon from '@mui/icons-material/Reddit';
import TwitterIcon from '@mui/icons-material/Twitter';
import AccessTimeIcon from '@mui/icons-material/AccessTime';

import axiosInstance, { endpoints } from 'src/utils/axios';
import { useAuthContext } from 'src/auth/hooks';
import { useSettingsContext } from 'src/components/settings';

// ─── Stat Card ───
function StatCard({ title, value, icon, color, subtitle, loading }) {
  return (
    <Card
      sx={{
        height: '100%',
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          width: 4,
          height: '100%',
          bgcolor: `${color}.main`,
          borderRadius: '4px 0 0 4px',
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" alignItems="flex-start" justifyContent="space-between">
          <Stack spacing={0.5}>
            <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.5 }}>
              {title}
            </Typography>
            {loading ? (
              <Skeleton width={60} height={40} />
            ) : (
              <Typography variant="h3" sx={{ fontWeight: 700 }}>
                {value ?? 0}
              </Typography>
            )}
            {subtitle && (
              <Typography variant="caption" color="text.secondary">
                {subtitle}
              </Typography>
            )}
          </Stack>
          <Box
            sx={{
              p: 1.5,
              borderRadius: 2,
              bgcolor: (theme) => alpha(theme.palette[color].main, 0.12),
              color: `${color}.main`,
              display: 'flex',
            }}
          >
            {icon}
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
}

// ─── Source Bar ───
function SourceBar({ label, count, total, color }) {
  const pct = total > 0 ? (count / total) * 100 : 0;
  return (
    <Stack spacing={0.5}>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography variant="body2" sx={{ fontWeight: 600 }}>{label}</Typography>
        <Typography variant="body2" color="text.secondary">{count}</Typography>
      </Stack>
      <LinearProgress
        variant="determinate"
        value={pct}
        sx={{
          height: 8,
          borderRadius: 4,
          bgcolor: (theme) => alpha(theme.palette[color].main, 0.12),
          '& .MuiLinearProgress-bar': {
            borderRadius: 4,
            bgcolor: `${color}.main`,
          },
        }}
      />
    </Stack>
  );
}

// ─── Activity Item ───
function ActivityItem({ item }) {
  const getStatusColor = (status) => {
    const s = (status || '').toLowerCase();
    if (s === 'published' || s === 'success') return 'success';
    if (s === 'failed' || s === 'error') return 'error';
    if (s === 'pending' || s === 'processing') return 'warning';
    return 'info';
  };

  return (
    <Stack direction="row" alignItems="center" spacing={2} sx={{ py: 1.5 }}>
      <Box
        sx={{
          width: 8,
          height: 8,
          borderRadius: '50%',
          flexShrink: 0,
          bgcolor: (theme) => theme.palette[getStatusColor(item.news_status)].main,
        }}
      />
      <Stack spacing={0} sx={{ flex: 1, minWidth: 0 }}>
        <Typography variant="body2" noWrap sx={{ fontWeight: 500 }}>
          {item.title || 'Untitled'}
        </Typography>
        <Stack direction="row" spacing={1} alignItems="center">
          <Typography variant="caption" color="text.secondary">
            {item.news_type}
          </Typography>
          {item.website_name && (
            <>
              <Typography variant="caption" color="text.secondary">•</Typography>
              <Typography variant="caption" color="text.secondary">
                {item.website_name}
              </Typography>
            </>
          )}
        </Stack>
      </Stack>
      <Chip
        label={item.news_status || 'Unknown'}
        size="small"
        color={getStatusColor(item.news_status)}
        sx={{ fontWeight: 600, fontSize: '0.7rem' }}
      />
    </Stack>
  );
}

// ─── Main View ───
export default function OneView() {
  const settings = useSettingsContext();
  const { user } = useAuthContext();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true);
      const { data } = await axiosInstance.get(endpoints.dashboard.stats);
      setStats(data.data);
    } catch (err) {
      console.error('Failed to fetch dashboard stats:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  const sourceIcons = {
    reddit: <RedditIcon sx={{ fontSize: 16 }} />,
    twitter: <TwitterIcon sx={{ fontSize: 16 }} />,
  };

  const sourceColors = {
    reddit: 'warning',
    twitter: 'info',
  };

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Stack spacing={3}>
        {/* Greeting */}
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Welcome back, {user?.firstname || 'Admin'} 👋
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            Here&apos;s what&apos;s happening with your AI news pipeline.
          </Typography>
        </Box>

        {/* Stat Cards */}
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Total Websites"
              value={stats?.total_websites}
              icon={<LanguageIcon />}
              color="primary"
              subtitle="Configured platforms"
              loading={loading}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Active Scrapers"
              value={stats?.active_scrapers}
              icon={<SmartToyIcon />}
              color="success"
              subtitle="Currently running"
              loading={loading}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Posts Today"
              value={stats?.posts_today}
              icon={<TodayIcon />}
              color="info"
              subtitle="Scraped today"
              loading={loading}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Published Today"
              value={stats?.published_today}
              icon={<PublishIcon />}
              color="warning"
              subtitle="Sent to websites"
              loading={loading}
            />
          </Grid>
        </Grid>

        {/* Second Row */}
        <Grid container spacing={3}>
          {/* Posts by Source */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent sx={{ p: 3 }}>
                <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 3 }}>
                  <TrendingUpIcon color="primary" sx={{ fontSize: 20 }} />
                  <Typography variant="h6" sx={{ fontWeight: 700 }}>
                    Posts by Source
                  </Typography>
                </Stack>

                <Stack spacing={2.5}>
                  {loading ? (
                    <>
                      <Skeleton height={40} />
                      <Skeleton height={40} />
                    </>
                  ) : stats?.posts_by_source && stats.posts_by_source.length > 0 ? (
                    stats.posts_by_source.map((s) => (
                      <SourceBar
                        key={s.source}
                        label={s.source}
                        count={parseInt(s.count, 10)}
                        total={stats.total_posts || 1}
                        color={sourceColors[s.source] || 'primary'}
                      />
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
                      No posts data yet
                    </Typography>
                  )}

                  <Divider sx={{ my: 1 }} />

                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                      Total Posts
                    </Typography>
                    <Typography variant="h6" sx={{ fontWeight: 700 }}>
                      {stats?.total_posts ?? 0}
                    </Typography>
                  </Stack>
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Failures Today */}
          <Grid item xs={12} md={2}>
            <Card
              sx={{
                height: '100%',
                bgcolor: (theme) =>
                  stats?.failures_today > 0
                    ? alpha(theme.palette.error.main, 0.05)
                    : alpha(theme.palette.success.main, 0.05),
                border: (theme) =>
                  `1px solid ${alpha(
                    stats?.failures_today > 0
                      ? theme.palette.error.main
                      : theme.palette.success.main,
                    0.2
                  )}`,
              }}
            >
              <CardContent sx={{ p: 3, textAlign: 'center' }}>
                <ErrorOutlineIcon
                  sx={{
                    fontSize: 40,
                    color: stats?.failures_today > 0 ? 'error.main' : 'success.main',
                    mb: 1,
                  }}
                />
                <Typography variant="h3" sx={{ fontWeight: 700 }}>
                  {loading ? <Skeleton width={40} sx={{ mx: 'auto' }} /> : (stats?.failures_today ?? 0)}
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                  Failures Today
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Recent Activity */}
          <Grid item xs={12} md={6}>
            <Card sx={{ height: '100%' }}>
              <CardContent sx={{ p: 3 }}>
                <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                  <AccessTimeIcon color="primary" sx={{ fontSize: 20 }} />
                  <Typography variant="h6" sx={{ fontWeight: 700 }}>
                    Recent Activity
                  </Typography>
                </Stack>

                {loading ? (
                  <Stack spacing={2}>
                    {[1, 2, 3, 4, 5].map((i) => (
                      <Skeleton key={i} height={50} />
                    ))}
                  </Stack>
                ) : stats?.recent_activity && stats.recent_activity.length > 0 ? (
                  <Stack divider={<Divider sx={{ borderStyle: 'dashed' }} />}>
                    {stats.recent_activity.map((item, idx) => (
                      <ActivityItem key={item.id || idx} item={item} />
                    ))}
                  </Stack>
                ) : (
                  <Box
                    sx={{
                      py: 6,
                      textAlign: 'center',
                      borderRadius: 1,
                      bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
                      border: (theme) => `dashed 1px ${theme.palette.divider}`,
                    }}
                  >
                    <Typography variant="body2" color="text.secondary">
                      No recent activity
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Stack>
    </Container>
  );
}
