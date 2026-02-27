'use client';

import { useState, useCallback, useEffect, useRef, useTransition } from 'react';
import { alpha } from '@mui/material/styles';
import {
  Box, Container, Typography, Card, CardContent, Stack,
  Tooltip, IconButton, Alert, Snackbar, Switch, TextField,
  Button, Grid, Chip, LinearProgress, Divider, CircularProgress,
} from '@mui/material';

import HomeIcon from '@mui/icons-material/Home';
import ScheduleIcon from '@mui/icons-material/Schedule';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import RefreshIcon from '@mui/icons-material/Refresh';
import SpeedIcon from '@mui/icons-material/Speed';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import BarChartIcon from '@mui/icons-material/BarChart';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import TimerIcon from '@mui/icons-material/Timer';

import { useSettingsContext } from 'src/components/settings';
import { useRouter } from 'src/routes/hooks';
import Label from 'src/components/label';
import { fDate, fTime } from 'src/utils/format-time';

// ── Stat card component ──
function StatCard({ icon, title, value, color = 'primary', subtitle }) {
  return (
    <Card
      sx={{
        p: 2.5,
        height: '100%',
        border: (t) => `1px solid ${alpha(t.palette[color].main, 0.15)}`,
        bgcolor: (t) => alpha(t.palette[color].main, 0.04),
        transition: 'box-shadow 0.2s',
        '&:hover': { boxShadow: (t) => `0 4px 16px ${alpha(t.palette[color].main, 0.15)}` },
      }}
    >
      <Stack direction="row" alignItems="flex-start" spacing={2}>
        <Box
          sx={{
            p: 1.2,
            borderRadius: 1.5,
            bgcolor: (t) => alpha(t.palette[color].main, 0.12),
            color: `${color}.main`,
            display: 'flex',
          }}
        >
          {icon}
        </Box>
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.5 }}>
            {title}
          </Typography>
          <Typography variant="h5" sx={{ fontWeight: 700, mt: 0.5 }}>
            {value ?? '—'}
          </Typography>
          {subtitle && (
            <Typography variant="caption" sx={{ color: 'text.disabled', mt: 0.5 }}>
              {subtitle}
            </Typography>
          )}
        </Box>
      </Stack>
    </Card>
  );
}

// ── Main view ──
function CronView({ data, history, onEdit, onTrigger, onRefreshSettings, onRefreshHistory, time }) {
  const settings = useSettingsContext();
  const router = useRouter();

  const [cronEnabled, setCronEnabled] = useState(data?.cron_enabled ?? false);
  const [intervalMinutes, setIntervalMinutes] = useState(data?.cron_interval_minutes ?? 60);
  const [isRunning, setIsRunning] = useState(data?.is_running ?? false);
  const [localData, setLocalData] = useState(data);
  const [logData, setLogData] = useState(history);
  const [saving, setSaving] = useState(false);
  const [triggering, setTriggering] = useState(false);
  const [isPending, startTransition] = useTransition();
  const pollRef = useRef(null);

  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const showMsg = (message, severity = 'success') => setSnackbar({ open: true, message, severity });

  // Sync with server data when it changes
  useEffect(() => {
    setLocalData(data);
    setCronEnabled(data?.cron_enabled ?? false);
    setIntervalMinutes(data?.cron_interval_minutes ?? 60);
    setIsRunning(data?.is_running ?? false);
  }, [data]);

  // Polling while pipeline is running
  useEffect(() => {
    if (isRunning) {
      pollRef.current = setInterval(async () => {
        try {
          const fresh = await onRefreshSettings();
          if (fresh?.data) {
            setLocalData(fresh.data);
            setIsRunning(fresh.data.is_running ?? false);
            if (!fresh.data.is_running) {
              showMsg('Pipeline run completed!', fresh.data.last_run_status === 'success' ? 'success' : 'warning');
              // Also refresh history
              const hist = await onRefreshHistory({ sort: [{ field: 'log_time', sort: 'desc' }], pageSize: 20, page: 1 });
              if (hist && !hist.error) setLogData(hist);
            }
          }
        } catch (_) { /* ignore polling errors */ }
      }, 5000);
    }
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, [isRunning, onRefreshSettings, onRefreshHistory]);

  // ── Save settings ──
  const handleSave = useCallback(async () => {
    setSaving(true);
    try {
      const payload = JSON.stringify({ cron_enabled: cronEnabled, cron_interval_minutes: Number(intervalMinutes) });
      const res = await onEdit(payload);
      if (res?.error) {
        showMsg('Failed to save cron settings', 'error');
      } else {
        showMsg('Cron settings saved!');
        const fresh = await onRefreshSettings();
        if (fresh?.data) setLocalData(fresh.data);
      }
    } catch (err) {
      showMsg('Error saving settings', 'error');
    }
    setSaving(false);
  }, [cronEnabled, intervalMinutes, onEdit, onRefreshSettings]);

  // ── Manual trigger ──
  const handleTrigger = useCallback(async () => {
    setTriggering(true);
    try {
      const res = await onTrigger();
      if (res?.error) {
        showMsg(res.error, 'error');
      } else {
        showMsg(res.message || 'Pipeline triggered!');
        setIsRunning(true);
      }
    } catch (err) {
      showMsg('Failed to trigger pipeline', 'error');
    }
    setTriggering(false);
  }, [onTrigger]);

  // ── Refresh ──
  const handleRefresh = useCallback(async () => {
    startTransition(async () => {
      try {
        const [freshSettings, freshHistory] = await Promise.all([
          onRefreshSettings(),
          onRefreshHistory({ sort: [{ field: 'log_time', sort: 'desc' }], pageSize: 20, page: 1 }),
        ]);
        if (freshSettings?.data) {
          setLocalData(freshSettings.data);
          setCronEnabled(freshSettings.data.cron_enabled ?? false);
          setIntervalMinutes(freshSettings.data.cron_interval_minutes ?? 60);
          setIsRunning(freshSettings.data.is_running ?? false);
        }
        if (freshHistory && !freshHistory.error) setLogData(freshHistory);
        showMsg('Refreshed!');
      } catch (_) {
        showMsg('Refresh failed', 'error');
      }
    });
  }, [onRefreshSettings, onRefreshHistory]);

  const formatDuration = (sec) => {
    if (!sec && sec !== 0) return '—';
    if (sec < 60) return `${sec}s`;
    return `${Math.floor(sec / 60)}m ${sec % 60}s`;
  };

  const formatDate = (d) => {
    if (!d) return '—';
    try { return `${fDate(d)} ${fTime(d)}`; } catch { return String(d); }
  };

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Stack spacing={3}>
        {/* ── Header ── */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: 2,
            p: 3,
            borderRadius: 2,
            border: (t) => `1px solid ${alpha(t.palette.primary.main, 0.2)}`,
          }}
        >
          <Stack direction="row" alignItems="center" spacing={1.5}>
            <Tooltip title="Go to Dashboard" arrow>
              <IconButton size="small" onClick={() => router.push('/admin-dashboard')} sx={{ color: 'primary.main' }}>
                <HomeIcon />
              </IconButton>
            </Tooltip>
            <Typography variant="h4" sx={{ fontWeight: 700, color: 'text.secondary' }}>/</Typography>
            <ScheduleIcon sx={{ color: 'primary.main', fontSize: 28 }} />
            <Typography variant="h4" sx={{ fontWeight: 700 }}>Cron & Triggers</Typography>
          </Stack>

          <Stack direction="row" spacing={1}>
            <Tooltip title="Refresh data">
              <IconButton onClick={handleRefresh} disabled={isPending}>
                <RefreshIcon sx={{ animation: isPending ? 'spin 1s linear infinite' : 'none', '@keyframes spin': { '0%': { transform: 'rotate(0deg)' }, '100%': { transform: 'rotate(360deg)' } } }} />
              </IconButton>
            </Tooltip>
          </Stack>
        </Box>

        {/* ── Running banner ── */}
        {isRunning && (
          <Alert severity="info" icon={<CircularProgress size={20} />} sx={{ borderRadius: 2, fontWeight: 600 }}>
            Pipeline is running… This page will auto-refresh when the run finishes.
          </Alert>
        )}

        {/* ── Stat cards ── */}
        <Grid container spacing={2.5}>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              icon={<SpeedIcon fontSize="small" />}
              title="Status"
              value={isRunning ? 'Running' : (cronEnabled ? 'Active' : 'Paused')}
              color={isRunning ? 'warning' : (cronEnabled ? 'success' : 'error')}
              subtitle={isRunning ? 'Pipeline in progress' : (cronEnabled ? `Every ${localData?.cron_interval_minutes ?? 60} min` : 'Cron disabled')}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              icon={<TrendingUpIcon fontSize="small" />}
              title="Total Runs"
              value={localData?.total_runs ?? 0}
              color="info"
              subtitle={`${localData?.total_success ?? 0} success / ${localData?.total_failures ?? 0} failed`}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              icon={<AccessTimeIcon fontSize="small" />}
              title="Last Run"
              value={localData?.last_run_status ? (
                <Chip
                  label={localData.last_run_status}
                  size="small"
                  color={localData.last_run_status === 'success' ? 'success' : 'error'}
                  sx={{ fontWeight: 700, fontSize: '0.8rem' }}
                />
              ) : '—'}
              color="primary"
              subtitle={formatDate(localData?.last_run_at)}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              icon={<TimerIcon fontSize="small" />}
              title="Duration"
              value={formatDuration(localData?.last_run_duration_sec)}
              color="secondary"
              subtitle={localData?.next_run_at ? `Next: ${formatDate(localData.next_run_at)}` : 'No schedule'}
            />
          </Grid>
        </Grid>

        {/* ── Settings card ── */}
        <Card sx={{ borderRadius: 2, border: (t) => `1px solid ${t.palette.divider}` }}>
          <CardContent sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>Cron Configuration</Typography>
            <Grid container spacing={3} alignItems="center">
              <Grid item xs={12} sm={4}>
                <Stack direction="row" alignItems="center" spacing={1.5}>
                  <Switch
                    checked={cronEnabled}
                    onChange={(e) => setCronEnabled(e.target.checked)}
                    color="success"
                  />
                  <Box>
                    <Typography variant="subtitle2">Enable Cron</Typography>
                    <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                      {cronEnabled ? 'Auto-scraping is ON' : 'Auto-scraping is OFF'}
                    </Typography>
                  </Box>
                </Stack>
              </Grid>
              <Grid item xs={12} sm={4}>
                <TextField
                  label="Interval (minutes)"
                  type="number"
                  value={intervalMinutes}
                  onChange={(e) => setIntervalMinutes(Math.max(1, Number(e.target.value)))}
                  inputProps={{ min: 1, max: 1440 }}
                  size="small"
                  fullWidth
                  helperText="1 – 1440 minutes (24 hrs)"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <Stack direction="row" spacing={1.5}>
                  <Button
                    variant="contained"
                    onClick={handleSave}
                    disabled={saving}
                    startIcon={saving ? <CircularProgress size={16} color="inherit" /> : <CheckCircleIcon />}
                    sx={{ textTransform: 'none', fontWeight: 600 }}
                  >
                    {saving ? 'Saving…' : 'Save Settings'}
                  </Button>
                  <Button
                    variant="outlined"
                    color="warning"
                    onClick={handleTrigger}
                    disabled={triggering || isRunning}
                    startIcon={triggering ? <CircularProgress size={16} color="inherit" /> : <PlayArrowIcon />}
                    sx={{ textTransform: 'none', fontWeight: 600 }}
                  >
                    {triggering ? 'Starting…' : (isRunning ? 'Running…' : 'Run Now')}
                  </Button>
                </Stack>
              </Grid>
            </Grid>

            {localData?.last_run_message && (
              <>
                <Divider sx={{ my: 2 }} />
                <Alert
                  severity={localData.last_run_status === 'success' ? 'success' : 'error'}
                  icon={localData.last_run_status === 'success' ? <CheckCircleIcon /> : <ErrorIcon />}
                  sx={{ borderRadius: 1.5 }}
                >
                  <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>Last Run Message</Typography>
                  <Typography variant="body2" sx={{ mt: 0.5, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                    {localData.last_run_message}
                  </Typography>
                </Alert>
              </>
            )}
          </CardContent>
        </Card>

        {/* ── Recent activity log ── */}
        <Card sx={{ borderRadius: 2, border: (t) => `1px solid ${t.palette.divider}` }}>
          <CardContent sx={{ p: 3 }}>
            <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
              <Stack direction="row" alignItems="center" spacing={1}>
                <BarChartIcon sx={{ color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 700 }}>Recent Activity</Typography>
              </Stack>
              <Chip label={`${logData?.results?.length ?? 0} logs`} size="small" variant="outlined" />
            </Stack>

            {logData?.results?.length > 0 ? (
              <Box sx={{ overflowX: 'auto' }}>
                <Box component="table" sx={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                  <Box component="thead">
                    <Box component="tr" sx={{ borderBottom: (t) => `2px solid ${t.palette.divider}` }}>
                      {['Time', 'Type', 'Title', 'Website', 'Status'].map((h) => (
                        <Box component="th" key={h} sx={{ p: 1.5, textAlign: 'left', fontWeight: 700, color: 'text.secondary', whiteSpace: 'nowrap' }}>
                          {h}
                        </Box>
                      ))}
                    </Box>
                  </Box>
                  <Box component="tbody">
                    {logData.results.map((row, i) => (
                      <Box
                        component="tr"
                        key={row.id || i}
                        sx={{
                          borderBottom: (t) => `1px solid ${t.palette.divider}`,
                          '&:hover': { bgcolor: (t) => alpha(t.palette.primary.main, 0.04) },
                        }}
                      >
                        <Box component="td" sx={{ p: 1.5, whiteSpace: 'nowrap', color: 'text.secondary' }}>
                          {formatDate(row.log_time)}
                        </Box>
                        <Box component="td" sx={{ p: 1.5 }}>
                          <Chip label={row.news_type || '—'} size="small" variant="outlined" sx={{ fontSize: '0.75rem' }} />
                        </Box>
                        <Box component="td" sx={{ p: 1.5, maxWidth: 280, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {row.title || '—'}
                        </Box>
                        <Box component="td" sx={{ p: 1.5, color: 'text.secondary' }}>
                          {row.website_name || '—'}
                        </Box>
                        <Box component="td" sx={{ p: 1.5 }}>
                          <Label
                            color={
                              row.news_status === 'success' ? 'success' :
                              row.news_status === 'error' ? 'error' :
                              row.news_status === 'skipped' ? 'warning' :
                              'default'
                            }
                          >
                            {row.news_status || '—'}
                          </Label>
                        </Box>
                      </Box>
                    ))}
                  </Box>
                </Box>
              </Box>
            ) : (
              <Box sx={{ py: 6, textAlign: 'center' }}>
                <WarningAmberIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 1 }} />
                <Typography variant="body1" sx={{ color: 'text.secondary' }}>No recent activity logs</Typography>
                <Typography variant="caption" sx={{ color: 'text.disabled' }}>
                  Logs will appear here after the pipeline runs
                </Typography>
              </Box>
            )}
          </CardContent>
        </Card>
      </Stack>

      {/* ── Snackbar ── */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar((s) => ({ ...s, open: false }))}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={() => setSnackbar((s) => ({ ...s, open: false }))}
          severity={snackbar.severity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default CronView;
