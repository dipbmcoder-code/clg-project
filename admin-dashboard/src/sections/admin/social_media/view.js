'use client';

import { useState, useEffect, useCallback } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import Chip from '@mui/material/Chip';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import MenuItem from '@mui/material/MenuItem';
import CircularProgress from '@mui/material/CircularProgress';
import Snackbar from '@mui/material/Snackbar';
import Divider from '@mui/material/Divider';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';

import TwitterIcon from '@mui/icons-material/Twitter';
import RedditIcon from '@mui/icons-material/Reddit';

import { fetchAPI, editAction } from 'src/utils/helper';
import { endpoints } from 'src/utils/axios';

// ─── Social Media View ───────────────────────────────────────

export default function SocialMediaView() {
  const [websites, setWebsites] = useState([]);
  const [selectedWebsite, setSelectedWebsite] = useState('');
  const [config, setConfig] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [tab, setTab] = useState(0);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const fetchWebsites = useCallback(async () => {
    try {
      const res = await fetchAPI(endpoints.findMany('websites', { pageSize: 100 }));
      if (res.data) {
        setWebsites(res.data);
        if (res.data.length > 0) {
          setSelectedWebsite(res.data[0].id);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchWebsites();
  }, [fetchWebsites]);

  const fetchConfig = useCallback(async () => {
    if (!selectedWebsite) return;
    try {
      const res = await fetchAPI(endpoints.socialMedia.getConfig(selectedWebsite));
      if (res.data) setConfig(res.data);
    } catch (err) {
      console.error(err);
    }
  }, [selectedWebsite]);

  const fetchPosts = useCallback(async () => {
    if (!selectedWebsite) return;
    try {
      const res = await fetchAPI(endpoints.socialMedia.listByWebsite(selectedWebsite));
      if (res.data) setPosts(res.data);
    } catch (err) {
      console.error(err);
    }
  }, [selectedWebsite]);

  useEffect(() => {
    fetchConfig();
    fetchPosts();
  }, [fetchConfig, fetchPosts]);

  const handleConfigChange = (field) => (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setConfig((prev) => ({ ...prev, [field]: value }));
  };

  const handleSaveConfig = async () => {
    setSaving(true);
    try {
      const url = endpoints.socialMedia.updateConfig(selectedWebsite);
      const res = await editAction(url, JSON.stringify(config));
      if (res.data) {
        setSnackbar({ open: true, message: 'Social media config saved', severity: 'success' });
      }
    } catch (err) {
      setSnackbar({ open: true, message: 'Failed to save config', severity: 'error' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" py={10}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Social Media</Typography>
      </Stack>

      {/* Website selector */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <TextField
            select
            fullWidth
            label="Select Website"
            value={selectedWebsite}
            onChange={(e) => setSelectedWebsite(e.target.value)}
          >
            {websites.map((w) => (
              <MenuItem key={w.id} value={w.id}>
                {w.platformName} — {w.platformUrl}
              </MenuItem>
            ))}
          </TextField>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs value={tab} onChange={(e, v) => setTab(v)} sx={{ mb: 3 }}>
        <Tab label="Configuration" />
        <Tab label="Post History" />
      </Tabs>

      {/* Config Tab */}
      {tab === 0 && config && (
        <Grid container spacing={3}>
          {/* Twitter Config */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                avatar={<TwitterIcon color="primary" />}
                title="Twitter / X"
                subheader="Auto-post articles to Twitter"
                action={
                  <FormControlLabel
                    control={
                      <Switch
                        checked={config.twitterEnabled || false}
                        onChange={handleConfigChange('twitterEnabled')}
                      />
                    }
                    label=""
                  />
                }
              />
              <CardContent>
                <Stack spacing={2}>
                  <TextField
                    fullWidth
                    label="API Key"
                    type="password"
                    value={config.twitterApiKey || ''}
                    onChange={handleConfigChange('twitterApiKey')}
                    disabled={!config.twitterEnabled}
                  />
                  <TextField
                    fullWidth
                    label="API Secret"
                    type="password"
                    value={config.twitterApiSecret || ''}
                    onChange={handleConfigChange('twitterApiSecret')}
                    disabled={!config.twitterEnabled}
                  />
                  <TextField
                    fullWidth
                    label="Access Token"
                    type="password"
                    value={config.twitterAccessToken || ''}
                    onChange={handleConfigChange('twitterAccessToken')}
                    disabled={!config.twitterEnabled}
                  />
                  <TextField
                    fullWidth
                    label="Access Token Secret"
                    type="password"
                    value={config.twitterAccessSecret || ''}
                    onChange={handleConfigChange('twitterAccessSecret')}
                    disabled={!config.twitterEnabled}
                  />
                  {config._hasTwitterCreds && (
                    <Chip label="Credentials configured" color="success" variant="outlined" size="small" />
                  )}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Reddit Config */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                avatar={<RedditIcon sx={{ color: '#FF5700' }} />}
                title="Reddit"
                subheader="Auto-post articles to subreddits"
                action={
                  <FormControlLabel
                    control={
                      <Switch
                        checked={config.redditEnabled || false}
                        onChange={handleConfigChange('redditEnabled')}
                      />
                    }
                    label=""
                  />
                }
              />
              <CardContent>
                <Stack spacing={2}>
                  <TextField
                    fullWidth
                    label="Client ID"
                    value={config.redditClientId || ''}
                    onChange={handleConfigChange('redditClientId')}
                    disabled={!config.redditEnabled}
                  />
                  <TextField
                    fullWidth
                    label="Client Secret"
                    type="password"
                    value={config.redditClientSecret || ''}
                    onChange={handleConfigChange('redditClientSecret')}
                    disabled={!config.redditEnabled}
                  />
                  <TextField
                    fullWidth
                    label="Reddit Username"
                    value={config.redditUsername || ''}
                    onChange={handleConfigChange('redditUsername')}
                    disabled={!config.redditEnabled}
                  />
                  <TextField
                    fullWidth
                    label="Reddit Password"
                    type="password"
                    value={config.redditPassword || ''}
                    onChange={handleConfigChange('redditPassword')}
                    disabled={!config.redditEnabled}
                  />
                  <TextField
                    fullWidth
                    label="Subreddits (comma-separated)"
                    value={Array.isArray(config.redditSubreddits) ? config.redditSubreddits.join(', ') : ''}
                    onChange={(e) => {
                      const subs = e.target.value.split(',').map((s) => s.trim()).filter(Boolean);
                      setConfig((prev) => ({ ...prev, redditSubreddits: subs }));
                    }}
                    disabled={!config.redditEnabled}
                    placeholder="news, worldnews"
                    helperText="Enter subreddit names without r/"
                  />
                  {config._hasRedditCreds && (
                    <Chip label="Credentials configured" color="success" variant="outlined" size="small" />
                  )}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* General Settings */}
          <Grid item xs={12}>
            <Card>
              <CardHeader title="Posting Settings" />
              <CardContent>
                <Stack spacing={3}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={config.autoPostOnPublish || false}
                        onChange={handleConfigChange('autoPostOnPublish')}
                      />
                    }
                    label="Auto-post to social media when article is published to WordPress"
                  />
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    label="Post Template"
                    value={config.postTemplate || ''}
                    onChange={handleConfigChange('postTemplate')}
                    placeholder="📰 {title}&#10;&#10;Read more: {url}"
                    helperText="Use {title} and {url} as placeholders"
                  />
                  <Button variant="contained" onClick={handleSaveConfig} disabled={saving} sx={{ alignSelf: 'flex-end' }}>
                    {saving ? 'Saving...' : 'Save Configuration'}
                  </Button>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Post History Tab */}
      {tab === 1 && (
        <Card>
          <CardHeader title="Recent Social Media Posts" />
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Platform</TableCell>
                  <TableCell>Title</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Date</TableCell>
                  <TableCell>Link</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {posts.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      <Typography variant="body2" color="text.secondary" py={3}>
                        No social media posts yet
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  posts.map((post) => (
                    <TableRow key={post.id}>
                      <TableCell>
                        <Chip
                          icon={post.platform === 'twitter' ? <TwitterIcon /> : <RedditIcon />}
                          label={post.platform}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>{post.title}</TableCell>
                      <TableCell>
                        <Chip
                          label={post.status}
                          color={post.status === 'posted' ? 'success' : post.status === 'failed' ? 'error' : 'warning'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{new Date(post.createdAt).toLocaleString()}</TableCell>
                      <TableCell>
                        {post.postUrl && (
                          <Button href={post.postUrl} target="_blank" size="small">
                            View
                          </Button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </Card>
      )}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
      >
        <Alert severity={snackbar.severity} onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
