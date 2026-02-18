'use client';

import { useMemo, useState, useEffect, useCallback } from 'react';
import { alpha } from '@mui/material/styles';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Stack,
  Tooltip,
  IconButton,
  Link,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';

// Icons
import ShareIcon from '@mui/icons-material/Share';
import SettingsIcon from '@mui/icons-material/Settings';
import RedditIcon from '@mui/icons-material/Reddit';
import HomeIcon from '@mui/icons-material/Home';
import VerifiedIcon from '@mui/icons-material/Verified';
import SyncIcon from '@mui/icons-material/Sync';

import { useSettingsContext } from 'src/components/settings';
import { useRouter, usePathname } from 'src/routes/hooks';
import { RouterLink } from 'src/routes/components';

import {
  CustomAccordionForm,
} from 'src/custom/index';
import { useBoolean } from 'src/hooks/use-boolean';
import axiosInstance, { endpoints } from 'src/utils/axios';

function Website({
  data,
  onEdit,
  onField,
  time,
  componentData,
  defaultImagedata
}) {
  const mergedObject = { ...componentData };
  if (defaultImagedata) {
    for (const key in mergedObject.schema) {
      if (defaultImagedata.schema.hasOwnProperty(key)) {
        mergedObject.schema[key] = defaultImagedata.schema[key];
      }
    }
    for (const key in defaultImagedata) {
      if (/^default_\d+$/.test(key)) {
        mergedObject[key] = defaultImagedata[key];
      }
    }
  }

  const router = useRouter();
  const pathname = usePathname();
  const settings = useSettingsContext();

  // WordPress integration state
  const [wpCategories, setWpCategories] = useState([]);
  const [wpAuthors, setWpAuthors] = useState([]);
  const [wpLoading, setWpLoading] = useState(false);
  const [wpValidating, setWpValidating] = useState(false);
  const [wpError, setWpError] = useState('');
  const [isValidated, setIsValidated] = useState(data?.is_validated || false);

  const commonStyle = {
    xs: 12,
    sm: 6,
  };

  const editDataAction = async (data, formData) => {
    const response = await onEdit(data, formData);
    return response;
  };

  const viewCategory = useBoolean(false);

  // Fetch WP categories & authors if credentials are validated
  const fetchWPData = useCallback(async () => {
    if (!data?.id || !data?.is_validated) return;

    setWpLoading(true);
    setWpError('');
    try {
      const [catRes, authRes] = await Promise.all([
        axiosInstance.get(endpoints.wordpress.categories(data.id)),
        axiosInstance.get(endpoints.wordpress.authors(data.id)),
      ]);
      setWpCategories(
        (catRes.data?.data || []).map((c) => ({ label: c.name, value: c.id }))
      );
      setWpAuthors(
        (authRes.data?.data || []).map((a) => ({ label: a.name, value: a.id }))
      );
    } catch (err) {
      console.error('Failed to fetch WP data:', err);
      setWpError('Failed to load WordPress categories/authors');
    } finally {
      setWpLoading(false);
    }
  }, [data?.id, data?.is_validated]);

  useEffect(() => {
    fetchWPData();
  }, [fetchWPData]);

  // Validate WP credentials
  const handleValidate = async () => {
    setWpValidating(true);
    setWpError('');
    try {
      const res = await axiosInstance.post(endpoints.wordpress.validate, {
        website_id: data.id,
      });
      if (res.data?.data?.validated) {
        setIsValidated(true);
        // Refetch categories & authors after successful validation
        setTimeout(() => fetchWPData(), 500);
      }
    } catch (err) {
      setIsValidated(false);
      const msg = err?.error?.message || err?.message || 'Validation failed';
      setWpError(msg);
    } finally {
      setWpValidating(false);
    }
  };

  const memoizedData = useMemo(() => ({ ...data }), [data]);

  const sections = [
    {
      id: 'general',
      title: 'General Settings',
      icon: <SettingsIcon sx={{ fontSize: 20 }} />,
      fields: [
        { name: 'platform_name', type: 'string', label: 'Website Name', rules: { required: true } },
        { name: 'platform_url', type: 'string', label: 'WordPress URL', rules: { required: true }, helperText: 'e.g. https://yoursite.com' },
        { name: 'platform_user', type: 'string', label: 'WP Username', rules: { required: true }, helperText: 'WordPress admin username' },
        {
          name: 'platform_password',
          type: 'password',
          label: 'WP Application Password',
          rules: { required: true },
          helperText: isValidated
            ? '✅ Credentials validated — connected to WordPress'
            : '❌ Not validated — enter an Application Password from WP → Users → Application Passwords',
        },
        {
          name: 'website_author',
          type: 'free_text_multiple',
          selectType: 'single',
          label: 'Default Author',
          options: wpAuthors.length > 0 ? wpAuthors : (data.authorsOptions || []),
        },
        { name: 'topic_niche', type: 'string', label: 'Topic / Niche', helperText: 'e.g. Technology, Finance, Sports, Health' },
        {
          name: 'post_status',
          type: 'select',
          label: 'Default Post Status',
          options: [
            { label: 'Draft', value: 'draft' },
            { label: 'Publish', value: 'publish' },
            { label: 'Pending Review', value: 'pending' },
          ],
          props: { xs: 6 },
        },
        { name: 'active', type: 'boolean', label: 'Active / Deactivate Website' },
      ],
    },
    {
      id: 'social_media',
      title: 'Social Media Scraping',
      icon: <ShareIcon sx={{ fontSize: 20 }} />,
      fields: [
        {
          name: 'enable_social_media',
          type: 'boolean',
          label: 'Enable Social Media Scraping',
          props: { xs: 12 },
        },
        {
          name: 'twitter_handles',
          limit: 10,
          type: 'free_text_multiple',
          label: 'X (Twitter) Handles',
          props: { xs: 6 },
        },
        {
          name: 'social_media_categories',
          limit: 5,
          type: 'free_text_multiple',
          label: 'WordPress Categories',
          options: wpCategories.length > 0 ? wpCategories : (data.categoriesOptions || []),
          props: { xs: 6 },
          helperText: wpCategories.length > 0 ? `${wpCategories.length} categories loaded from WordPress` : 'Validate credentials to load categories',
        },
      ],
    },
    {
      id: 'reddit',
      title: 'Reddit Scraping',
      icon: <RedditIcon sx={{ fontSize: 20 }} />,
      fields: [
        {
          name: 'enable_reddit',
          type: 'boolean',
          label: 'Enable Reddit Scraping',
          props: { xs: 12 },
        },
        {
          name: 'reddit_subreddits',
          limit: 10,
          type: 'free_text_multiple',
          label: 'Subreddits (without r/)',
          helperText: 'e.g. technology, worldnews, science',
          props: { xs: 6 },
        },
        {
          name: 'reddit_mode',
          type: 'select',
          label: 'Sort Mode',
          options: [
            { label: 'Hot', value: 'hot' },
            { label: 'New', value: 'new' },
            { label: 'Top', value: 'top' },
            { label: 'Rising', value: 'rising' },
          ],
          props: { xs: 6 },
        },
        {
          name: 'reddit_categories',
          limit: 5,
          type: 'free_text_multiple',
          label: 'WordPress Categories',
          options: wpCategories.length > 0 ? wpCategories : (data.categoriesOptions || []),
          props: { xs: 6 },
          helperText: wpCategories.length > 0 ? `${wpCategories.length} categories loaded` : 'Validate credentials first',
        },
        {
          name: 'reddit_min_score',
          type: 'number',
          label: 'Minimum Score',
          helperText: 'Only scrape posts with this minimum upvote score',
          props: { xs: 6 },
        },
      ],
    },
  ];

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Stack spacing={3}>
        {/* Header Section */}
        {data.platform_name && (
          <Box
            sx={{
              display: 'flex',
              alignItems: { xs: 'flex-start', sm: 'center' },
              justifyContent: 'space-between',
              flexDirection: { xs: 'column', sm: 'row' },
              gap: 2,
              p: 3,
              borderRadius: 2,
              border: (theme) => `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
            }}
          >
            <Stack direction="row" alignItems="center" spacing={1.5} sx={{ flexWrap: 'wrap' }}>
              <Box>
                <Stack direction="row" alignItems="center" spacing={1} sx={{ flexWrap: 'wrap' }}>
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
                  <Link
                    component={RouterLink}
                    href="/admin-dashboard/websites"
                    underline="hover"
                    sx={{ cursor: 'pointer', transition: 'all 0.2s' }}
                  >
                    <Typography
                      variant="h4"
                      sx={{
                        fontWeight: 700,
                        background: (theme) => `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        '&:hover': { opacity: 0.8 },
                      }}
                    >
                      Websites
                    </Typography>
                  </Link>
                  <Typography variant="h4" sx={{ fontWeight: 700, color: 'text.secondary' }}>/</Typography>
                  <Typography variant="h4" sx={{ fontWeight: 700, color: 'text.primary' }}>
                    {data.platform_name}
                  </Typography>
                </Stack>
                <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 500, mt: 0.5 }}>
                  Configure website settings, WordPress integration, and scraping
                </Typography>
              </Box>
            </Stack>

            {/* Validate Button */}
            <Button
              variant={isValidated ? 'outlined' : 'contained'}
              color={isValidated ? 'success' : 'primary'}
              startIcon={wpValidating ? <CircularProgress size={18} color="inherit" /> : (isValidated ? <VerifiedIcon /> : <SyncIcon />)}
              onClick={handleValidate}
              disabled={wpValidating}
              sx={{
                minWidth: 180,
                fontWeight: 600,
                flexShrink: 0,
              }}
            >
              {wpValidating ? 'Validating...' : isValidated ? 'Re-validate WP' : 'Validate Credentials'}
            </Button>
          </Box>
        )}

        {/* WordPress Status Alert */}
        {wpError && (
          <Alert severity="error" onClose={() => setWpError('')} sx={{ borderRadius: 2 }}>
            {wpError}
          </Alert>
        )}

        {wpLoading && (
          <Alert severity="info" icon={<CircularProgress size={18} />} sx={{ borderRadius: 2 }}>
            Loading WordPress categories and authors...
          </Alert>
        )}

        {isValidated && wpCategories.length > 0 && !wpLoading && (
          <Alert severity="success" sx={{ borderRadius: 2 }}>
            Connected to WordPress — {wpCategories.length} categories and {wpAuthors.length} authors loaded
          </Alert>
        )}

        {/* Settings Form Card */}
        <Card
          sx={{
            boxShadow: (theme) => theme.customShadows.card,
            borderRadius: 2,
            overflow: 'hidden',
          }}
        >
          <CardContent sx={{ p: { xs: 2, md: 3 } }}>
            <CustomAccordionForm
              time={time}
              selectedOffers={['general']}
              sections={sections}
              dialog={memoizedData}
              refresh={true}
              action={editDataAction}
              viewCategory={viewCategory}
              onField={onField}
              type="page"
              commonStyle={commonStyle}
            />
          </CardContent>
        </Card>
      </Stack>
    </Container>
  );
}

export default Website;
