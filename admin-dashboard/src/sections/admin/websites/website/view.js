'use client';

import { useMemo } from 'react';
import { alpha } from '@mui/material/styles';
import { Box, Container, Typography, Card, CardContent, Stack, Tooltip, IconButton, Link } from '@mui/material';

// Icons
import TvIcon from '@mui/icons-material/Tv';
import ShareIcon from '@mui/icons-material/Share';
import PublicIcon from '@mui/icons-material/Public';
import SettingsIcon from '@mui/icons-material/Settings';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';
import FactCheckIcon from '@mui/icons-material/FactCheck';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import HomeIcon from '@mui/icons-material/Home';

import { useSettingsContext } from 'src/components/settings';
import { useRouter, usePathname } from 'src/routes/hooks';
import { RouterLink } from 'src/routes/components';

import {
  CustomAccordionForm,
} from 'src/custom/index';
import { useBoolean } from 'src/hooks/use-boolean';

/**
 * Renders a form for editing dealer information.
 * @param {Object} props - Component props.
 * @param {Object} props.data - Object containing the dealer's current information.
 * @param {Function} props.onEdit - Function to be called when the form is submitted.
 * @param {Function} props.onField - Function to handle changes in form fields.
 * @returns {JSX.Element} - Rendered component.
 */

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
  const { name, account_number, oem, id, url, offer_page_url_format, banner_setting } = data;

  const settings = useSettingsContext();

  const commonStyle = {
    xs: 12,
    sm: 6,
  };

  const editDataAction = async (data, formData) => {
    const response = await onEdit(data, formData);
    return response;
  }

  const viewCategory = useBoolean(false);

  data = useMemo(() => {
    return {
      ...data,
    };
  }, [data]);
  const sections = [
    {
      id: 'general',
      title: 'General Settings',
      icon: <SettingsIcon sx={{ fontSize: 20 }} />,
      fields: [
        { name: 'platform_name', type: 'string', label: 'Website Name', rules: { required: true } },
        { name: 'platform_url', type: 'string', label: 'Website Url', rules: { required: true } },
        { name: 'platform_user', type: 'string', label: 'Admin User', rules: { required: true } },
        { name: 'platform_password', type: 'password', label: 'Admin Password', rules: { required: true }, helperText: data?.is_validated ? '✅ Validated' : "❌ Wrong credentials" },
        {
          name: 'website_author',
          type: 'free_text_multiple',
          selectType: 'single',
          label: 'Author',
          options: data.authorsOptions || []
        },
        { name: 'active', type: 'boolean', label: 'Active/Deactive Website : ', },
      ],
    },
    {
      id: 'website_leagues',
      title: 'Leagues',
      icon: <EmojiEventsIcon sx={{ fontSize: 20 }} />,
      fields: [
        {
          name: 'website_leagues',
          type: 'select_league',
          label: 'Leagues',
          selectType: 'multiple',
          option: 'league_name',
          options: data.leagues || [],
          props: {
            xs: 12,
          },
        },
      ],
    },
    {
      id: 'previews_reviews',
      title: 'Previews & Reviews',
      icon: <FactCheckIcon sx={{ fontSize: 20 }} />,
      fields: [
        { name: 'enable_match_previews', type: 'boolean', label: 'Enable Match Previews' },
        { name: 'match_previews_time', type: 'number', label: 'Match Preview Time (in hours)' },
        { name: 'enable_match_reviews', type: 'boolean', label: 'Enable Match Reviews' },
        { name: 'match_reviews_time', type: 'number', label: 'Match Review Time After Kickoff (in minutes)' },
        {
          name: 'manual_preview_categories',
          limit: 2,
          type: 'free_text_multiple', // New type we'll handle
          label: 'Manual previews categories',
          options: data.categoriesOptions || [],
        },
        {
          name: 'manual_review_categories',
          limit: 2,
          type: 'free_text_multiple', // New type we'll handle
          label: 'Manual review categories',
          options: data.categoriesOptions || [],
        },
      ],
    },
    {
      id: 'social_media',
      title: 'Social Media',
      icon: <ShareIcon sx={{ fontSize: 20 }} />,
      fields: [
        {
          name: "enable_social_media",
          type: 'boolean',
          label: 'Enable Social Media',
          props: {
            xs: 12,
          },
        },
        {
          name: 'twitter_handles',
          limit: 2,
          type: 'free_text_multiple', // New type we'll handle
          label: 'X (Twitter) Handles',
          props: {
            xs: 6,
          },
        },
        {
          name: 'social_media_categories',
          limit: 2,
          type: 'free_text_multiple', // New type we'll handle
          label: 'Social Media Categories',
          options: data.categoriesOptions || [],
          props: {
            xs: 6,
          },
        },
      ],
    },
    {
      id: 'player_abroad',
      title: 'Player Abroad',
      icon: <PublicIcon sx={{ fontSize: 20 }} />,
      fields: [
        { name: 'enabled_player_abroad', type: 'boolean', label: 'Enable Player Abroad', props: { xs: 12 } },
        { name: 'player_abroad_prompt', type: 'string', label: 'Player Abroad Prompt', multiline: true },
        {
          name: 'player_abroad_categories',
          limit: 2,
          type: 'free_text_multiple', // New type we'll handle
          label: 'Player Abroad Categories',
          options: data.categoriesOptions || [],
          props: {
            xs: 6,
          },
        },
        {
          name: 'player_abroad_countries',
          type: 'free_text_multiple',
          label: 'Countries',
          selectType: 'multiple',
          option: 'name',
          option_val: 'code',
          props: { xs: 12 },
        },
      ]
    },
    {
      id: 'player_profiles',
      title: 'Player Profiles',
      icon: <AccountCircleIcon sx={{ fontSize: 20 }} />,
      fields: [
        { name: 'enable_player_profiles', type: 'boolean', label: 'Enable Player Profiles', },
        {
          name: 'player_profiles_categories',
          limit: 2,
          type: 'free_text_multiple', // New type we'll handle
          label: 'Categories',
          options: data.categoriesOptions || [],
          props: {
            xs: 6,
          },
        },
        {
          name: 'player_profiles',
          type: 'select_profiles',
          label: 'Leagues',
          selectType: 'multiple',
          option: 'league_name',
          options: data.leagues || [],
          fields: [
            { name: 'league', type: 'select', label: 'Select League', options: data.leagues || [] },
            { name: 'player', type: 'select', label: 'Select Players' },
            { name: 'datetime', type: 'datetime', label: 'Select Date & Time' },
          ],
          props: {
            xs: 12,
          },
        },
      ]
    },
    {
      id: 'transfer_rumors',
      title: 'Transfer & Rumors',
      icon: <SwapHorizIcon sx={{ fontSize: 20 }} />,
      fields: [
        { name: 'enable_transfer_rumors', type: 'boolean', label: 'Enable Transfer & Rumors', props: { xs: 12 } },
        {
          name: 'transfer_categories',
          limit: 2,
          type: 'free_text_multiple', // New type we'll handle
          label: 'Transfer Categories',
          options: data.categoriesOptions || [],
          props: {
            xs: 6,
          },
        },
        {
          name: 'rumors_categories',
          limit: 2,
          type: 'free_text_multiple', // New type we'll handle
          label: 'Rumors Categories',
          options: data.categoriesOptions || [],
          props: {
            xs: 6,
          },
        },
        {
          name: 'transfer_rumour_countries',
          type: 'free_text_multiple',
          label: 'Countries',
          selectType: 'multiple',
          option: 'name',
          option_val: 'code',
          props: { xs: 12 },
        },
      ]
    },
    {
      id: 'where_to_watch',
      title: 'Where To Watch',
      icon: <TvIcon sx={{ fontSize: 20 }} />,
      fields: [
        { name: 'enabled_where_to_watch', type: 'boolean', label: 'Enable Where to Watch', props: { xs: 12 } },
        { name: 'where_to_watch_days', type: 'number', label: 'News Publish Time (Days Before League Start)' },
        {
          name: 'where_to_watch_categories',
          limit: 2,
          type: 'free_text_multiple', // New type we'll handle
          label: 'Where to Watch Categories',
          options: data.categoriesOptions || [],
        },
        {
          name: 'where_to_watch_countries',
          type: 'free_text_multiple',
          label: 'Countries',
          selectType: 'multiple',
          option: 'name',
          option_val: 'code',
          props: { xs: 12 },
        },
      ]
    }
  ];

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Stack spacing={3}>
        {/* Header Section */}
        {data.platform_name && (
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


              {/* Breadcrumb Navigation */}
              <Box>
                <Stack direction="row" alignItems="center" spacing={1}>
                  {/* Home Icon */}
                  <Tooltip title="Go to Dashboard" arrow>
                    <IconButton
                      size="small"
                      onClick={() => router.push('/admin-dashboard')}
                      sx={{
                        color: 'primary.main',
                        '&:hover': {
                          bgcolor: 'primary.lighter',
                        },
                      }}
                    >
                      <HomeIcon />
                    </IconButton>
                  </Tooltip>
                  <Typography
                    variant="h4"
                    sx={{
                      fontWeight: 700,
                      color: 'text.secondary',
                    }}
                  >
                    /
                  </Typography>
                  <Link
                    component={RouterLink}
                    href="/admin-dashboard/websites"
                    underline="hover"
                    sx={{
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                    }}
                  >
                    <Typography
                      variant="h4"
                      sx={{
                        fontWeight: 700,
                        background: (theme) => `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        '&:hover': {
                          opacity: 0.8,
                        },
                      }}
                    >
                      Websites
                    </Typography>
                  </Link>
                  <Typography
                    variant="h4"
                    sx={{
                      fontWeight: 700,
                      color: 'text.secondary',
                    }}
                  >
                    /
                  </Typography>
                  <Typography
                    variant="h4"
                    sx={{
                      fontWeight: 700,
                      color: 'text.primary',
                    }}
                  >
                    {data.platform_name}
                  </Typography>
                </Stack>
                <Typography
                  variant="body2"
                  sx={{
                    color: 'text.secondary',
                    fontWeight: 500,
                    mt: 0.5,
                  }}
                >
                  Configure website settings and integrations
                </Typography>
              </Box>
            </Stack>
          </Box>
        )}


        {/* Settings Form Card */}
        <Card
          sx={{
            boxShadow: (theme) => theme.customShadows.card,
            borderRadius: 2,
            overflow: 'hidden',
          }}
        >
          <CardContent sx={{ p: 3 }}>
            <CustomAccordionForm
              time={time}
              // excludeSections={excludeSections}
              selectedOffers={['general', 'leagues']}
              sections={sections}
              // custom_data={!!custom_data}
              // ignoreDirty={!!ignoreDirty}
              dialog={data}
              refresh={true}
              action={editDataAction}
              viewCategory={viewCategory}
              onField={onField}
              type={"page"}
              commonStyle={commonStyle}
            // deleteEntry={deleteEntry}
            />
          </CardContent>
        </Card>
        {/* <LeaguesCategoryPopup data={data} handle={viewCategory} action={editDataAction} /> */}
      </Stack>
    </Container>
  );
}
export default Website;