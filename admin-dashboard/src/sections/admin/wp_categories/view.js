'use client';

import { useState, useEffect, useCallback } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import Chip from '@mui/material/Chip';
import CircularProgress from '@mui/material/CircularProgress';
import Snackbar from '@mui/material/Snackbar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Divider from '@mui/material/Divider';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

import FolderIcon from '@mui/icons-material/Folder';
import SyncIcon from '@mui/icons-material/Sync';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import ArticleIcon from '@mui/icons-material/Article';

import { fetchAPI } from 'src/utils/helper';
import { endpoints } from 'src/utils/axios';

// ─── WordPress Categories View ───────────────────────────────

export default function WpCategoriesView() {
  const [websites, setWebsites] = useState([]);
  const [selectedWebsite, setSelectedWebsite] = useState('');
  const [categories, setCategories] = useState([]);
  const [tree, setTree] = useState([]);
  const [health, setHealth] = useState(null);
  const [recentPosts, setRecentPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [expanded, setExpanded] = useState({});
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const fetchWebsites = useCallback(async () => {
    try {
      const res = await fetchAPI(endpoints.findMany('websites', { pageSize: 100 }));
      if (res.data) {
        setWebsites(res.data);
        if (res.data.length > 0) setSelectedWebsite(res.data[0].id);
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

  const fetchCategories = useCallback(async () => {
    if (!selectedWebsite) return;
    try {
      const res = await fetchAPI(endpoints.wordpress.categories(selectedWebsite));
      if (res.data) {
        setCategories(res.data.categories || []);
        setTree(res.data.tree || []);
      }
    } catch (err) {
      console.error(err);
    }
  }, [selectedWebsite]);

  const fetchHealth = useCallback(async () => {
    if (!selectedWebsite) return;
    try {
      const res = await fetchAPI(endpoints.wordpress.health(selectedWebsite));
      if (res.data) setHealth(res.data);
    } catch (err) {
      setHealth({ healthy: false, error: 'Failed to check' });
    }
  }, [selectedWebsite]);

  const fetchRecentPosts = useCallback(async () => {
    if (!selectedWebsite) return;
    try {
      const res = await fetchAPI(endpoints.wordpress.recentPosts(selectedWebsite));
      if (res.data) setRecentPosts(res.data.posts || []);
    } catch (err) {
      console.error(err);
    }
  }, [selectedWebsite]);

  useEffect(() => {
    fetchCategories();
    fetchHealth();
    fetchRecentPosts();
  }, [fetchCategories, fetchHealth, fetchRecentPosts]);

  const handleSync = async () => {
    setSyncing(true);
    try {
      const res = await fetchAPI(endpoints.wordpress.syncCategories(selectedWebsite), { method: 'POST' });
      if (res.data) {
        setSnackbar({ open: true, message: res.data.message || 'Categories synced!', severity: 'success' });
        fetchCategories();
      }
    } catch (err) {
      setSnackbar({ open: true, message: 'Sync failed', severity: 'error' });
    } finally {
      setSyncing(false);
    }
  };

  const toggleExpand = (id) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const renderCategoryTree = (nodes, level = 0) =>
    nodes.map((node) => (
      <Box key={node.wpId}>
        <ListItem sx={{ pl: 2 + level * 3 }}>
          <ListItemIcon sx={{ minWidth: 36 }}>
            <FolderIcon color="primary" fontSize="small" />
          </ListItemIcon>
          <ListItemText
            primary={node.name}
            secondary={`Slug: ${node.slug} · ${node.count} posts · WP ID: ${node.wpId}`}
          />
          {node.children?.length > 0 && (
            <IconButton size="small" onClick={() => toggleExpand(node.wpId)}>
              {expanded[node.wpId] ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            </IconButton>
          )}
        </ListItem>
        {node.children?.length > 0 && (
          <Collapse in={expanded[node.wpId] || false}>
            {renderCategoryTree(node.children, level + 1)}
          </Collapse>
        )}
      </Box>
    ));

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
        <Typography variant="h4">WordPress Categories</Typography>
      </Stack>

      {/* Website Selector + Health */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stack direction="row" spacing={2} alignItems="center">
            <TextField
              select
              fullWidth
              label="Select Website"
              value={selectedWebsite}
              onChange={(e) => setSelectedWebsite(e.target.value)}
            >
              {websites.map((w) => (
                <MenuItem key={w.id} value={w.id}>
                  {w.platformName}
                </MenuItem>
              ))}
            </TextField>

            {health && (
              <Chip
                icon={health.healthy ? <CheckCircleIcon /> : <ErrorIcon />}
                label={health.healthy ? `Connected (${health.latency})` : 'Disconnected'}
                color={health.healthy ? 'success' : 'error'}
                variant="outlined"
              />
            )}

            <Button
              variant="contained"
              startIcon={syncing ? <CircularProgress size={16} color="inherit" /> : <SyncIcon />}
              onClick={handleSync}
              disabled={syncing}
              sx={{ minWidth: 180 }}
            >
              {syncing ? 'Syncing...' : 'Sync Categories'}
            </Button>
          </Stack>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Category Tree */}
        <Grid item xs={12} md={7}>
          <Card>
            <CardHeader
              title={`Categories (${categories.length})`}
              subheader="Synced from WordPress"
            />
            <CardContent sx={{ maxHeight: 600, overflow: 'auto' }}>
              {categories.length === 0 ? (
                <Typography color="text.secondary" textAlign="center" py={4}>
                  No categories synced yet. Click &quot;Sync Categories&quot; to fetch from WordPress.
                </Typography>
              ) : (
                <List dense>{renderCategoryTree(tree)}</List>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Posts */}
        <Grid item xs={12} md={5}>
          <Card>
            <CardHeader
              title="Recent WordPress Posts"
              subheader="Latest articles published to this site"
              avatar={<ArticleIcon color="primary" />}
            />
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Title</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Date</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {recentPosts.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={3} align="center">
                        <Typography variant="body2" color="text.secondary" py={2}>
                          No posts found
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    recentPosts.map((post) => (
                      <TableRow key={post.wpId}>
                        <TableCell>
                          <Button
                            href={post.link}
                            target="_blank"
                            size="small"
                            sx={{ textTransform: 'none', textAlign: 'left', justifyContent: 'flex-start' }}
                          >
                            {post.title}
                          </Button>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={post.status}
                            size="small"
                            color={post.status === 'publish' ? 'success' : 'default'}
                          />
                        </TableCell>
                        <TableCell>{new Date(post.date).toLocaleDateString()}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Card>
        </Grid>
      </Grid>

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
