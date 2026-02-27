'use client';

import { useMemo, useState, useCallback } from 'react';
import { alpha } from '@mui/material/styles';
import {
  Box, Container, Typography, Card, CardContent, Stack,
  Tooltip, IconButton, Alert, Snackbar,
} from '@mui/material';

import HomeIcon from '@mui/icons-material/Home';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import KeyIcon from '@mui/icons-material/Key';
import ImageIcon from '@mui/icons-material/Image';
import CloudIcon from '@mui/icons-material/Cloud';
import EmailIcon from '@mui/icons-material/Email';

import { useSettingsContext } from 'src/components/settings';
import { useRouter } from 'src/routes/hooks';
import { CustomAccordionForm } from 'src/custom/index';
import { useBoolean } from 'src/hooks/use-boolean';

function AiSettingsView({ data, onEdit, time }) {
  const settings = useSettingsContext();
  const router = useRouter();
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const commonStyle = { xs: 12, sm: 6 };

  const editDataAction = useCallback(async (formDataStr, formData) => {
    try {
      const response = await onEdit(formDataStr, formData);
      if (response?.error) {
        setSnackbar({ open: true, message: 'Failed to save settings', severity: 'error' });
      } else {
        setSnackbar({ open: true, message: 'AI settings saved successfully!', severity: 'success' });
      }
      return response;
    } catch (err) {
      setSnackbar({ open: true, message: 'Error saving settings', severity: 'error' });
      return { error: err.message };
    }
  }, [onEdit]);

  const viewCategory = useBoolean(false);

  const memoizedData = useMemo(() => ({ ...data }), [data]);

  const sections = [
    {
      id: 'content_ai',
      title: 'Content Generation (AI)',
      icon: <SmartToyIcon sx={{ fontSize: 20 }} />,
      defaultExpanded: true,
      fields: [
        {
          name: 'content_provider',
          type: 'pre_select',
          label: 'Content Provider',
          props: { xs: 12, sm: 6 },
          options: [
            { label: 'OpenAI', value: 'openai' },
            { label: 'OpenRouter', value: 'openrouter' },
          ],
        },
        {
          name: 'content_model',
          type: 'string',
          label: 'Model Name',
          helperText: 'e.g. gpt-4o-mini, gpt-4o, deepseek/deepseek-chat',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'content_api_key',
          type: 'password',
          label: 'Content API Key',
          helperText: 'OpenAI or OpenRouter API key',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'content_base_url',
          type: 'string',
          label: 'Base URL (optional)',
          helperText: 'Custom API base URL (leave empty for default)',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'content_temperature',
          type: 'number',
          label: 'Temperature',
          helperText: '0.0 = deterministic, 1.0 = creative (default: 0.7)',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'content_max_tokens',
          type: 'number',
          label: 'Max Tokens',
          helperText: 'Maximum tokens per API call (default: 2000)',
          props: { xs: 12, sm: 6 },
        },
      ],
    },
    {
      id: 'image_ai',
      title: 'Image Generation',
      icon: <ImageIcon sx={{ fontSize: 20 }} />,
      fields: [
        {
          name: 'image_provider',
          type: 'pre_select',
          label: 'Image Provider',
          props: { xs: 12, sm: 6 },
          options: [
            { label: 'Gemini Flash Image', value: 'gemini-flash-image' },
            { label: 'Google Imagen', value: 'imagen' },
            { label: 'OpenRouter', value: 'openrouter' },
          ],
        },
        {
          name: 'image_api_key',
          type: 'password',
          label: 'Image API Key',
          helperText: 'Gemini or OpenRouter image API key',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'image_model',
          type: 'string',
          label: 'Image Model (optional)',
          helperText: 'e.g. gemini-2.5-flash-preview-image, openrouter/dall-e-3',
          props: { xs: 12 },
        },
      ],
    },
    {
      id: 'aws',
      title: 'AWS S3 Storage',
      icon: <CloudIcon sx={{ fontSize: 20 }} />,
      fields: [
        {
          name: 'aws_access_key_id',
          type: 'password',
          label: 'AWS Access Key ID',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'aws_secret_access_key',
          type: 'password',
          label: 'AWS Secret Access Key',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'aws_s3_bucket',
          type: 'string',
          label: 'S3 Bucket Name',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'aws_region',
          type: 'string',
          label: 'AWS Region',
          helperText: 'e.g. us-east-1, eu-central-1',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'aws_url',
          type: 'string',
          label: 'S3 Public URL',
          helperText: 'Full S3 bucket URL for public access',
          props: { xs: 12 },
        },
      ],
    },
    {
      id: 'email',
      title: 'Email Alerts (SendGrid)',
      icon: <EmailIcon sx={{ fontSize: 20 }} />,
      fields: [
        {
          name: 'sendgrid_api_key',
          type: 'password',
          label: 'SendGrid API Key',
          props: { xs: 12, sm: 6 },
        },
        {
          name: 'sender_email',
          type: 'string',
          label: 'Sender Email Address',
          helperText: 'From address for alert emails',
          props: { xs: 12, sm: 6 },
        },
      ],
    },
  ];

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Stack spacing={3}>
        {/* Header */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: 2,
            p: 3,
            borderRadius: 2,
            border: (theme) => `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
          }}
        >
          <Stack direction="row" alignItems="center" spacing={1.5}>
            <Box>
              <Stack direction="row" alignItems="center" spacing={1}>
                <Tooltip title="Go to Dashboard" arrow>
                  <IconButton
                    size="small"
                    onClick={() => router.push('/admin-dashboard')}
                    sx={{ color: 'primary.main', '&:hover': { bgcolor: 'primary.lighter' } }}
                  >
                    <HomeIcon />
                  </IconButton>
                </Tooltip>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'text.secondary' }}>/</Typography>
                <KeyIcon sx={{ color: 'primary.main', fontSize: 28 }} />
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'text.primary' }}>
                  AI Settings
                </Typography>
              </Stack>
              <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 500, mt: 0.5 }}>
                Configure AI providers, API keys, cloud storage, and email alerts.
              </Typography>
            </Box>
          </Stack>
        </Box>

        <Alert severity="info" sx={{ borderRadius: 2 }}>
          API keys are encrypted and masked after saving. To update a key, enter the new value and save.
        </Alert>

        {/* Settings Form */}
        <Card
          sx={{
            boxShadow: (theme) =>
              `0 0 2px 0 ${alpha(theme.palette.grey[500], 0.08)}, 0 12px 24px -4px ${alpha(theme.palette.grey[500], 0.08)}`,
            borderRadius: 2,
            border: (theme) => `1px solid ${theme.palette.divider}`,
            overflow: 'hidden',
          }}
        >
          <CardContent sx={{ p: { xs: 2, md: 3 } }}>
            <CustomAccordionForm
              time={time}
              selectedOffers={['content_ai']}
              sections={sections}
              dialog={memoizedData}
              refresh={true}
              action={editDataAction}
              viewCategory={viewCategory}
              type="page"
              commonStyle={commonStyle}
            />
          </CardContent>
        </Card>
      </Stack>

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

export default AiSettingsView;
