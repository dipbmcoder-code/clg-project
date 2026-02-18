'use client';

import { useMemo } from 'react';
import { alpha } from '@mui/material/styles';
import { Box, Container, Typography, Card, CardContent, Stack, Tooltip, IconButton } from '@mui/material';

// Icons
import ShareIcon from '@mui/icons-material/Share';
import HomeIcon from '@mui/icons-material/Home';
import SmartToyIcon from '@mui/icons-material/SmartToy';

import { useSettingsContext } from 'src/components/settings';
import { useRouter } from 'src/routes/hooks';

import {
  CustomAccordionForm,
} from 'src/custom/index';
import { useBoolean } from 'src/hooks/use-boolean';

function NewsPrompts({
  data,
  onEdit,
  onField,
  time,
  componentData,
  defaultImagedata
}) {
  const settings = useSettingsContext();
  const router = useRouter();

  const commonStyle = {
    xs: 12,
    sm: 6,
  };

  const editDataAction = async (data, formData) => {
    const response = await onEdit(data, formData);
    return response;
  };

  const viewCategory = useBoolean(false);

  data = useMemo(() => {
    return {
      ...data,
    };
  }, [data]);

  const sections = [
    {
      id: 'social_media',
      title: 'Social Media Prompts',
      icon: <ShareIcon sx={{ fontSize: 20 }} />,
      fields: [
        {
          name: 'social_media_news_title_prompt',
          type: 'prompt',
          label: 'News Title Prompt',
          rows: 6,
          props: { xs: 12 },
          variables: ['post_text', 'source', 'post_title', 'score'],
        },
        {
          name: 'social_media_news_image_prompt',
          type: 'prompt',
          label: 'News Image Prompt',
          rows: 8,
          props: { xs: 12 },
          variables: ['post_text', 'source', 'post_title'],
        },
        {
          name: 'social_media_news_content_prompt',
          type: 'prompt',
          label: 'News Content Prompt',
          rows: 8,
          props: { xs: 12 },
          variables: ['post_text', 'source', 'post_title', 'score', 'permalink'],
        },
      ],
    },
    {
      id: 'general',
      title: 'General AI Settings',
      icon: <SmartToyIcon sx={{ fontSize: 20 }} />,
      fields: [
        {
          name: 'ai_tone',
          type: 'prompt',
          label: 'AI Writing Tone / Style Prompt',
          rows: 4,
          props: { xs: 12 },
          helperText: 'Describe the tone & style AI should use when generating content',
        },
        {
          name: 'ai_language',
          type: 'string',
          label: 'Output Language',
          helperText: 'e.g. English, Spanish, Arabic',
          props: { xs: 6 },
        },
        {
          name: 'ai_max_words',
          type: 'number',
          label: 'Max Words per Article',
          helperText: 'Approximate word count for generated articles',
          props: { xs: 6 },
        },
      ],
    },
  ];

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Stack spacing={3}>
        {/* Header Section */}
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
                    sx={{
                      color: 'primary.main',
                      '&:hover': { bgcolor: 'primary.lighter' },
                    }}
                  >
                    <HomeIcon />
                  </IconButton>
                </Tooltip>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'text.secondary' }}>
                  /
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'text.primary' }}>
                  AI Prompts
                </Typography>
              </Stack>
              <Typography
                variant="body2"
                sx={{ color: 'text.secondary', fontWeight: 500, mt: 0.5 }}
              >
                Manage and customize AI generation prompts for content creation.
              </Typography>
            </Box>
          </Stack>
        </Box>

        {/* Settings Form Card */}
        <Card
          sx={{
            boxShadow: (theme) => `0 0 2px 0 ${alpha(theme.palette.grey[500], 0.08)}, 0 12px 24px -4px ${alpha(theme.palette.grey[500], 0.08)}`,
            borderRadius: 2,
            border: (theme) => `1px solid ${theme.palette.divider}`,
            overflow: 'hidden',
            position: 'relative',
          }}
        >
          <CardContent sx={{ p: { xs: 2, md: 3 } }}>
            <CustomAccordionForm
              time={time}
              selectedOffers={['social_media']}
              sections={sections}
              dialog={data}
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

export default NewsPrompts;
