'use client';

import { useMemo, useState } from 'react';

import { alpha } from '@mui/material/styles';
import {
  Box,
  Stack,
  Container,
  Typography,
  IconButton,
  Card,
  CardContent,
  Chip,
  Tooltip,
} from '@mui/material';
import { usePathname } from 'src/routes/hooks';
import { RouterLink } from 'src/routes/components';

import { EditIcon } from 'src/utils/icons';

import { DataGridTable, CustomPagination } from 'src/custom/index';
import { gridClasses } from '@mui/x-data-grid';

import Label from 'src/components/label';
import { useSettingsContext } from 'src/components/settings';
import { fDate, fTime } from 'src/utils/format-time';

function NewsLogs({ data, pageSizeOptions, sorting, onPageChange }) {
  const current_path = usePathname();
  const settings = useSettingsContext();
  const [refreshDataGrid, setRefreshDataGrid] = useState(false);
  const columns = [
    {
      field: 'news_type',
      headerName: 'News Type',
      width: 130,
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        const typeColors = {
          social_media: 'primary',
          reddit: 'warning',
          twitter: 'info',
          scraping: 'secondary',
          publishing: 'success',
        };
        return (
          <Chip
            label={value.toUpperCase()}
            color={typeColors[value] || 'default'}
            size="small"
            sx={{
              fontWeight: 600,
              fontSize: '0.75rem',
            }}
          />
        );
      },
    },
    {
      field: 'title',
      flex: 1,
      headerName: 'Title',
      height: '100%',
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
            {value}
          </Typography>
        );
      },
    },
    {
      field: 'website_name',
      headerName: 'Website',
      height: '100%',
      width: 150,
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        return (
          <Chip
            label={value}
            variant="outlined"
            size="small"
            sx={{
              fontWeight: 500,
            }}
          />
        );
      },
    },
    {
      field: 'log_time',
      width: 170,
      height: '100%',
      headerAlign: 'center',
      align: 'center',
      headerName: 'Publish Time',
      filterable: false,
      renderCell: (params) => {
        return (
          <Stack
            sx={{
              textAlign: 'center',
              height: '100%',
              lineHeight: 'inherit',
              justifyContent: 'center',
              gap: 0.5,
            }}
          >
            <Box
              component="span"
              sx={{
                lineHeight: 'normal',
                fontWeight: 600,
                fontSize: '0.875rem',
                color: 'text.primary',
              }}
            >
              {fDate(new Date(params.value))}
            </Box>
            <Box
              component="span"
              sx={{
                color: 'text.secondary',
                typography: 'caption',
                fontSize: '0.75rem',
              }}
            >
              {fTime(new Date(params.value))}
            </Box>
          </Stack>
        );
      },
    },
    {
      field: 'news_status',
      headerName: 'Status',
      width: 130,
      height: '100%',
      align: 'center',
      headerAlign: 'center',
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        const statusConfig = {
          'Published': { color: 'success', icon: '✓' },
          'Failed': { color: 'error', icon: '✕' },
          'Partial': { color: 'warning', icon: '⟳' },
          'Pending': { color: 'info', icon: '⋯' },
        };
        const config = statusConfig[value] || { color: 'default', icon: '•' };
        return (value &&
          <Label
            color={config.color}
            sx={{
              fontWeight: 600,
              fontSize: '0.75rem',
              px: 1.5,
            }}
          >
            {config.icon} {value}
          </Label>
        );
      },
    },
    {
      type: "actions",
      field: 'actions',
      headerName: 'Actions',
      height: '100%',
      width: 80,
      filterable: false,
      align: "center",
      headerAlign: "center",
      sortable: false,
      filterable: false,
      disableColumnMenu: true,
      getActions: ({ row }) => [
        <Tooltip title="View Details" arrow>
          <IconButton
            component={RouterLink}
            href={`${current_path}/${row.documentId}`}
            size="small"
            sx={{
              color: 'primary.main',
              '&:hover': {
                bgcolor: 'primary.lighter',
              },
            }}
          >
            <EditIcon />
          </IconButton>
        </Tooltip>
      ]
    },
  ];

  const memoizedDataGridTable = useMemo(
    () => (
      <DataGridTable
        // autoSizeColumns={autoSizeColumns}
        data={data}
        // virtualizeColumnsWithAutoRowHeight
        // getRowHeight={() => 'auto'}
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
              cursor: 'pointer',
            },
            '&.Mui-selected': {
              bgcolor: (theme) => alpha(theme.palette.primary.main, 0.08),
              '&:hover': {
                bgcolor: (theme) => alpha(theme.palette.primary.main, 0.12),
              },
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
          {/* Header Section */}
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: 2,
              p: 3,
              borderRadius: 2,
              // background: (theme) => `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.08)} 0%, ${alpha(theme.palette.primary.dark, 0.12)} 100%)`,
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
                News Logs
              </Typography>
              <Typography
                variant="body2"
                sx={{
                  color: 'text.secondary',
                  fontWeight: 500,
                }}
              >
                Track and monitor all news publication activities
              </Typography>
            </Box>
          </Box>

          {/* Data Grid Card */}
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
export default NewsLogs;
