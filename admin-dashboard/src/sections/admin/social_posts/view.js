'use client';

import { useMemo, useState } from 'react';

import {
  Box,
  Chip,
  Card,
  Stack,
  Tooltip,
  Container,
  Typography,
  IconButton,
  CardContent,
} from '@mui/material';
import { alpha } from '@mui/material/styles';
import { gridClasses } from '@mui/x-data-grid';


import Label from 'src/components/label';
import { useSettingsContext } from 'src/components/settings';
import { DataGridTable, CustomPagination } from 'src/custom/index';
import { fDate, fTime } from 'src/utils/format-time';

// Icons
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import RedditIcon from '@mui/icons-material/Reddit';
import TwitterIcon from '@mui/icons-material/Twitter';

function SocialPosts({ data, pageSizeOptions, sorting, onPageChange }) {
  const settings = useSettingsContext();
  const [refreshDataGrid, setRefreshDataGrid] = useState(false);

  const columns = [
    {
      field: 'source',
      headerName: 'Source',
      width: 120,
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        const isReddit = value?.toLowerCase() === 'reddit';
        return (
          <Chip
            icon={isReddit ? <RedditIcon sx={{ fontSize: 16 }} /> : <TwitterIcon sx={{ fontSize: 16 }} />}
            label={value ? value.charAt(0).toUpperCase() + value.slice(1) : 'Unknown'}
            color={isReddit ? 'warning' : 'info'}
            size="small"
            variant="outlined"
            sx={{ fontWeight: 600, fontSize: '0.75rem' }}
          />
        );
      },
    },
    {
      field: 'post_title',
      headerName: 'Title',
      flex: 1,
      minWidth: 250,
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        return (
          <Typography
            variant="body2"
            sx={{
              whiteSpace: 'normal',
              wordWrap: 'break-word',
              fontWeight: 500,
              color: 'text.primary',
            }}
          >
            {value || 'N/A'}
          </Typography>
        );
      },
    },
    {
      field: 'tweet_text',
      headerName: 'Content',
      flex: 1.5,
      minWidth: 300,
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        const truncated = value && value.length > 150 ? `${value.substring(0, 150)}...` : value;
        return (
          <Typography
            variant="body2"
            sx={{
              whiteSpace: 'normal',
              wordWrap: 'break-word',
              py: 1,
              color: 'text.secondary',
            }}
          >
            {truncated || 'No content'}
          </Typography>
        );
      },
    },
    {
      field: 'score',
      headerName: 'Score',
      width: 90,
      align: 'center',
      headerAlign: 'center',
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        return (
          <Typography variant="body2" sx={{ fontWeight: 600 }}>
            {value ?? '—'}
          </Typography>
        );
      },
    },
    {
      field: 'is_posted',
      headerName: 'Published',
      width: 110,
      align: 'center',
      headerAlign: 'center',
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        return (
          <Label color={value ? 'success' : 'default'} sx={{ fontWeight: 600 }}>
            {value ? 'Yes' : 'No'}
          </Label>
        );
      },
    },
    {
      field: 'scraped_time',
      headerName: 'Scraped At',
      width: 170,
      headerAlign: 'center',
      align: 'center',
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        if (!value) return <Typography variant="body2" color="text.secondary">—</Typography>;
        return (
          <Stack sx={{ textAlign: 'center', justifyContent: 'center', gap: 0.5 }}>
            <Box component="span" sx={{ fontWeight: 600, fontSize: '0.875rem', color: 'text.primary' }}>
              {fDate(new Date(value))}
            </Box>
            <Box component="span" sx={{ color: 'text.secondary', typography: 'caption', fontSize: '0.75rem' }}>
              {fTime(new Date(value))}
            </Box>
          </Stack>
        );
      },
    },
    {
      field: 'permalink',
      headerName: 'Link',
      width: 70,
      align: 'center',
      headerAlign: 'center',
      filterable: false,
      sortable: false,
      renderCell: (params) => {
        const { value } = params;
        if (!value) return null;
        return (
          <Tooltip title="Open original post" arrow>
            <IconButton
              size="small"
              component="a"
              href={value}
              target="_blank"
              rel="noopener noreferrer"
              sx={{ color: 'primary.main' }}
            >
              <OpenInNewIcon sx={{ fontSize: 18 }} />
            </IconButton>
          </Tooltip>
        );
      },
    },
  ];

  const memoizedDataGridTable = useMemo(
    () => (
      <DataGridTable
        data={data}
        columns={columns}
        refresh={refreshDataGrid}
        sorting={sorting}
        fetchData={onPageChange}
        pageSizeOptions={pageSizeOptions}
        CustomPaginationComponent={CustomPagination}
        sx={{
          border: 'none',
          [`& .${gridClasses.cell}`]: {
            py: 2,
            borderColor: (theme) => alpha(theme.palette.divider, 0.5),
          },
          [`& .${gridClasses.columnHeaders}`]: {
            bgcolor: (theme) => alpha(theme.palette.grey[500], 0.08),
            borderRadius: 0,
            borderBottom: (theme) => `2px solid ${theme.palette.divider}`,
          },
          [`& .${gridClasses.columnHeader}`]: {
            fontWeight: 700,
            fontSize: '0.875rem',
            color: 'text.primary',
          },
          [`& .${gridClasses.row}`]: {
            '&:hover': {
              bgcolor: (theme) => alpha(theme.palette.primary.main, 0.04),
            },
          },
          [`& .${gridClasses.footerContainer}`]: {
            borderTop: (theme) => `2px solid ${theme.palette.divider}`,
            bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
          },
        }}
      />
    ),
    [data, sorting, onPageChange, refreshDataGrid]
  );

  return (
    <>
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
            <Box>
              <Typography
                variant="h4"
                sx={{
                  fontWeight: 700,
                  background: (theme) => `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  mb: 0.5,
                }}
              >
                Social Posts
              </Typography>
              <Typography
                variant="body2"
                sx={{ color: 'text.secondary', fontWeight: 500 }}
              >
                Scraped posts from Reddit & X (Twitter) ready for AI processing
              </Typography>
            </Box>
          </Box>

          {/* Data Grid */}
          <Card
            sx={{
              boxShadow: (theme) => theme.customShadows.card,
              borderRadius: 2,
              overflow: 'hidden',
            }}
          >
            <CardContent sx={{ p: 0 }}>
              {memoizedDataGridTable}
            </CardContent>
          </Card>
        </Stack>
      </Container>
    </>
  );
}

export default SocialPosts;
