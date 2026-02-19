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
import MenuItem from '@mui/material/MenuItem';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import Chip from '@mui/material/Chip';
import CircularProgress from '@mui/material/CircularProgress';
import Divider from '@mui/material/Divider';
import Snackbar from '@mui/material/Snackbar';

import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';

import { fetchAPI, editAction } from 'src/utils/helper';
import { endpoints } from 'src/utils/axios';

// ─── AI Settings View ────────────────────────────────────────

export default function AiSettingsView() {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [testResults, setTestResults] = useState({});
  const [showKeys, setShowKeys] = useState({});
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const fetchSettings = useCallback(async () => {
    try {
      const res = await fetchAPI(endpoints.aiSettings.get());
      if (res.data) setSettings(res.data);
    } catch (err) {
      console.error('Failed to load AI settings:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const handleChange = (field) => (e) => {
    setSettings((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const url = endpoints.aiSettings.update();
      const res = await editAction(url, JSON.stringify(settings));
      if (res.data) {
        setSnackbar({ open: true, message: 'Settings saved successfully', severity: 'success' });
      } else {
        setSnackbar({ open: true, message: 'Failed to save settings', severity: 'error' });
      }
    } catch (err) {
      setSnackbar({ open: true, message: 'Error saving settings', severity: 'error' });
    } finally {
      setSaving(false);
    }
  };

  const handleTest = async (provider) => {
    setTestResults((prev) => ({ ...prev, [provider]: { loading: true } }));
    try {
      const res = await fetchAPI(endpoints.aiSettings.test(provider), { method: 'POST' });
      setTestResults((prev) => ({
        ...prev,
        [provider]: { loading: false, success: res.data?.success, message: res.data?.message },
      }));
    } catch (err) {
      setTestResults((prev) => ({
        ...prev,
        [provider]: { loading: false, success: false, message: err.message },
      }));
    }
  };

  const toggleShowKey = (field) => {
    setShowKeys((prev) => ({ ...prev, [field]: !prev[field] }));
  };

  const renderKeyField = (label, field, provider) => (
    <Stack direction="row" spacing={1} alignItems="flex-start">
      <TextField
        fullWidth
        label={label}
        value={settings?.[field] || ''}
        onChange={handleChange(field)}
        type={showKeys[field] ? 'text' : 'password'}
        placeholder="Enter API key..."
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton onClick={() => toggleShowKey(field)} edge="end" size="small">
                {showKeys[field] ? <VisibilityOffIcon /> : <VisibilityIcon />}
              </IconButton>
            </InputAdornment>
          ),
        }}
        helperText={
          settings?.[`_has${field.charAt(0).toUpperCase() + field.slice(1).replace('ApiKey', 'Key').replace('Api', '')}`]
            ? '✓ Key is set'
            : 'No key configured'
        }
      />
      {provider && (
        <Button
          variant="outlined"
          onClick={() => handleTest(provider)}
          disabled={testResults[provider]?.loading}
          sx={{ minWidth: 100, mt: 0.5 }}
        >
          {testResults[provider]?.loading ? <CircularProgress size={20} /> : 'Test'}
        </Button>
      )}
    </Stack>
  );

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
        <Typography variant="h4">AI Settings</Typography>
        <Button variant="contained" onClick={handleSave} disabled={saving} size="large">
          {saving ? 'Saving...' : 'Save Settings'}
        </Button>
      </Stack>

      <Grid container spacing={3}>
        {/* Content Generation */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Content Generation"
              subheader="Configure which AI service generates article text"
            />
            <CardContent>
              <Stack spacing={3}>
                <TextField
                  select
                  fullWidth
                  label="Content Service"
                  value={settings?.contentService || 'openai'}
                  onChange={handleChange('contentService')}
                >
                  <MenuItem value="openai">OpenAI (GPT)</MenuItem>
                  <MenuItem value="openrouter">OpenRouter</MenuItem>
                </TextField>

                <Divider />
                <Typography variant="subtitle2" color="text.secondary">
                  OpenAI
                </Typography>
                {renderKeyField('OpenAI API Key', 'openaiApiKey', 'openai')}
                {testResults.openai && !testResults.openai.loading && (
                  <Chip
                    icon={testResults.openai.success ? <CheckCircleIcon /> : <ErrorIcon />}
                    label={testResults.openai.message}
                    color={testResults.openai.success ? 'success' : 'error'}
                    variant="outlined"
                    size="small"
                  />
                )}
                <TextField
                  fullWidth
                  label="OpenAI Model"
                  value={settings?.openaiModel || ''}
                  onChange={handleChange('openaiModel')}
                  placeholder="gpt-4"
                />

                <Divider />
                <Typography variant="subtitle2" color="text.secondary">
                  OpenRouter
                </Typography>
                {renderKeyField('OpenRouter API Key', 'openrouterApiKey', 'openrouter')}
                {testResults.openrouter && !testResults.openrouter.loading && (
                  <Chip
                    icon={testResults.openrouter.success ? <CheckCircleIcon /> : <ErrorIcon />}
                    label={testResults.openrouter.message}
                    color={testResults.openrouter.success ? 'success' : 'error'}
                    variant="outlined"
                    size="small"
                  />
                )}
                <TextField
                  fullWidth
                  label="OpenRouter Model"
                  value={settings?.openrouterModel || ''}
                  onChange={handleChange('openrouterModel')}
                  placeholder="meta-llama/llama-3-70b"
                />
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Image Generation */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Image Generation"
              subheader="Configure which AI service generates news images"
            />
            <CardContent>
              <Stack spacing={3}>
                <TextField
                  select
                  fullWidth
                  label="Image Service"
                  value={settings?.imageService || 'gemini'}
                  onChange={handleChange('imageService')}
                >
                  <MenuItem value="gemini">Google Gemini</MenuItem>
                  <MenuItem value="openrouter">OpenRouter</MenuItem>
                  <MenuItem value="imagen">Google Imagen</MenuItem>
                  <MenuItem value="gemini-flash-image">Gemini Flash Image</MenuItem>
                </TextField>

                <Divider />
                <Typography variant="subtitle2" color="text.secondary">
                  Google Gemini
                </Typography>
                {renderKeyField('Gemini API Key', 'geminiApiKey', 'gemini')}
                {testResults.gemini && !testResults.gemini.loading && (
                  <Chip
                    icon={testResults.gemini.success ? <CheckCircleIcon /> : <ErrorIcon />}
                    label={testResults.gemini.message}
                    color={testResults.gemini.success ? 'success' : 'error'}
                    variant="outlined"
                    size="small"
                  />
                )}
                <TextField
                  fullWidth
                  label="Gemini Model"
                  value={settings?.geminiModel || ''}
                  onChange={handleChange('geminiModel')}
                  placeholder="gemini-pro"
                />
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* External Services */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="External Services"
              subheader="RapidAPI for sports data, SendGrid for alerts"
            />
            <CardContent>
              <Stack spacing={3}>
                {renderKeyField('RapidAPI Key', 'rapidapiKey')}
                <Divider />
                {renderKeyField('SendGrid API Key', 'sendgridApiKey')}
                <TextField
                  fullWidth
                  label="Alert Email"
                  value={settings?.alertEmail || ''}
                  onChange={handleChange('alertEmail')}
                  placeholder="admin@example.com"
                  type="email"
                />
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* AWS S3 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="AWS S3 Storage"
              subheader="Cloud storage for generated images"
            />
            <CardContent>
              <Stack spacing={3}>
                {renderKeyField('AWS Access Key', 'awsAccessKey')}
                {renderKeyField('AWS Secret Key', 'awsSecretKey')}
                <TextField
                  fullWidth
                  label="S3 Bucket"
                  value={settings?.awsS3Bucket || ''}
                  onChange={handleChange('awsS3Bucket')}
                  placeholder="my-bucket"
                />
                <TextField
                  fullWidth
                  label="AWS Region"
                  value={settings?.awsRegion || ''}
                  onChange={handleChange('awsRegion')}
                  placeholder="us-east-1"
                />
              </Stack>
            </CardContent>
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
