'use client';

import { useMemo, useState } from 'react';

import Button from '@mui/material/Button';
import { alpha } from '@mui/material/styles';
import {
  Box,
  Link,
  Stack,
  Avatar,
  Container,
  Typography,
  IconButton,
  Chip,
  Card,
  CardContent,
  Tooltip
} from '@mui/material';

import { usePathname } from 'src/routes/hooks';
import { RouterLink } from 'src/routes/components';

import { useBoolean } from 'src/hooks/use-boolean';
import useCustomSnackbar from 'src/hooks/use-custom-snackbar';

import {
  AddIcon,
  EditIcon,
  CheckIcon,
  DeleteIcon,
  ExclamationIcon,
} from 'src/utils/icons';

import { ActionSwitch, DataGridTable, CustomPagination, TransitionsDialog } from 'src/custom/index';

import { useSettingsContext } from 'src/components/settings';

function Websites({ data, pageSizeOptions, sorting, onPageChange, onDelete, onCount, onActive }) {
  const current_path = usePathname();
  const { customSnackbarAction } = useCustomSnackbar();
  const settings = useSettingsContext();
  const [refreshDataGrid, setRefreshDataGrid] = useState(false);

  const [count, setCount] = useState(data.count);

  const columns = [
    {
      field: 'platform_name',
      headerName: 'Website Name',
      minWidth: 250,
      renderCell: (params) => {
        const { value, row } = params;
        return (
          <Stack
            spacing={2}
            direction="row"
            alignItems="center"
            sx={{ minWidth: 0, height: '100%', py: 1 }}
          >
            <Avatar
              alt={value}
              sx={{
                width: 40,
                height: 40,
                bgcolor: 'primary.main',
                fontWeight: 700,
                fontSize: '1rem',
                color: 'primary.contrastText',
              }}
            >
              {value.charAt(0).toUpperCase()}
            </Avatar>
            <Typography
              component="span"
              variant="body2"
              noWrap
              sx={{
                fontWeight: 600,
                color: 'text.primary',
              }}
            >
              {value}
            </Typography>
          </Stack>
        );
      },
    },
    {
      flex: 1,
      field: 'platform_url',
      headerName: 'Website Url',
      sortable: false,
      //minWidth: 350,
      renderCell: (params) => {
        return (
          <Stack
            spacing={2}
            direction="row"
            alignItems="center"
            sx={{ minWidth: 0, height: '100%', py: 1 }}
          >
            <Typography
              component="span"
              variant="body2"
              noWrap
              sx={{
                color: 'primary.main',
                fontWeight: 500,
              }}
            >
              {params.value}
            </Typography>
          </Stack>
        );
      },
    },
    /*{
      flex: 1,
      field: 'platform_countries',
      headerName: 'Countries',
      sortable: false,
      //minWidth: 150,
      renderCell: (params) => {
        return (
          <Stack
            spacing={2}
            direction="row"
            alignItems="center"
            flexWrap="wrap"
            gap={0.5}
            sx={{ minWidth: 0, height: '100%', py: 1 }}
          >
            {params.value?.map((C) => (
              <Chip key={C.code} label={C.name} size="small" variant="soft" />
            ))}
          </Stack>
        );
      },
    },*/
    {
      flex: 1,
      field: 'is_validated',
      headerName: 'Status',
      sortable: false,
      align: 'center',
      headerAlign: 'center',
      width: 120,
      renderCell: (params) => {
        return (
          <Tooltip title={params.value ? 'Validated' : 'Not Validated'} arrow>
            <Stack
              direction="row"
              spacing={0.5}
              flexWrap="wrap"
              gap={0.5}
              sx={{ alignItems: 'center', justifyContent: 'center', height: '100%' }}
            >
              {params.value ? (
                <Chip
                  icon={<CheckIcon sx={{ fontSize: '1rem' }} />}
                  label="Validated"
                  color="success"
                  size="small"
                  sx={{ fontWeight: 600, fontSize: '0.75rem' }}
                />
              ) : (
                <Chip
                  icon={<ExclamationIcon sx={{ fontSize: '1rem' }} />}
                  label="Pending"
                  color="warning"
                  size="small"
                  sx={{ fontWeight: 600, fontSize: '0.75rem' }}
                />
              )}
            </Stack>
          </Tooltip>
        );
      },
    },
    {
      flex: 1,
      type: 'boolean',
      field: 'active',
      headerName: 'Active',
      align: 'center',
      headerAlign: 'center',
      minWidth: 100,
      sortable: true,
      filterable: false,
      renderCell: (params) => (
        <ActionSwitch
          color="warning"
          defaultVal={params.value === null ? false : !!params.value}
          action={(val) => handleActive(val, params.row.documentId)}
        />
      ),
    },
    {
      flex: 1,
      type: 'actions',
      field: 'actions',
      headerName: 'Actions',
      width: 120,
      align: 'center',
      headerAlign: 'center',
      sortable: false,
      filterable: false,
      disableColumnMenu: true,
      getActions: ({ row }) => [
        <Tooltip title="Edit Website" arrow>
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
        </Tooltip>,
        <Tooltip title="Delete Website" arrow>
          <IconButton
            size="small"
            onClick={(e) => {
              e.stopPropagation();
              deleteEntry(row.documentId);
            }}
            sx={{
              color: 'error.main',
              '&:hover': {
                bgcolor: 'error.lighter',
              },
            }}
          >
            <DeleteIcon />
          </IconButton>
        </Tooltip>,
      ],
    },
  ];

  const deleteDialog = useBoolean();

  const deleteEntry = (id) => {
    deleteDialog.setValue(id);
  };
  const handleRefreshDataGrid = () => {
    setRefreshDataGrid((prev) => !prev);
  };
  const deleteCallback = async () => {
    const res = await onCount();
    const totalCount = res?.results?.length || 0;
    const activeCount = res.results?.filter((item) => item.active).length || 0;
    const fallbackCount = totalCount - activeCount;

    setCount({
      total: totalCount,
      active: activeCount,
      fallback: fallbackCount,
    });
  };
  const autoSizeColumns = ['platform_name', 'platform_url'];
  const memoizedDataGridTable = useMemo(
    () => (
      <DataGridTable
        autoSizeColumns={autoSizeColumns}
        data={data}
        columns={columns}
        refresh={refreshDataGrid}
        sorting={sorting}
        fetchData={onPageChange}
        pageSizeOptions={pageSizeOptions}
        CustomPaginationComponent={CustomPagination}
        sx={{
          border: 'none',
          [`& .MuiDataGrid-cell`]: {
            py: 2,
            borderColor: (theme) => alpha(theme.palette.divider, 0.5),
          },
          [`& .MuiDataGrid-columnHeaders`]: {
            bgcolor: (theme) => alpha(theme.palette.grey[500], 0.08),
            borderRadius: 0,
            borderBottom: (theme) => `2px solid ${theme.palette.divider}`,
          },
          [`& .MuiDataGrid-columnHeader`]: {
            fontWeight: 700,
            fontSize: '0.875rem',
            color: 'text.primary',
          },
          [`& .MuiDataGrid-row`]: {
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
          [`& .MuiDataGrid-footerContainer`]: {
            borderTop: (theme) => `2px solid ${theme.palette.divider}`,
            bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
          },
        }}
      />
    ),
    [data, sorting, onPageChange, refreshDataGrid]
  );

  const handleActive = async (val, id) => {
    const updatedData = { 'active': val, 'id': id }
    const encodedData = encodeURIComponent(JSON.stringify(updatedData));
    const formData = new FormData();
    const res = await onActive(encodedData, formData);
    if (res.error) {
      handleRefreshDataGrid()
      if (res.error.message) {
        customSnackbarAction(res.error.message, 'error');
      } else {
        customSnackbarAction('Something went wrong', 'error');
      }
      return false;
    } else {
      customSnackbarAction(val ? 'Activated Successfully' : 'Deactivated Successfully', 'success');
      setCount({
        total: count.total,
        active: val ? count.active + 1 : count.active - 1,
        fallback: val ? count.fallback - 1 : count.fallback + 1,
      });
      return true;
    }
  }

  return (
    <>
      <TransitionsDialog
        dialog={deleteDialog}
        refresh={handleRefreshDataGrid}
        action={onDelete}
        title="Delete Website"
        content="Are you sure you want to delete?"
        buttonText="Delete"
        callback={deleteCallback}
        props={{
          variant: 'soft',
          startIcon: <DeleteIcon />,
          color: 'error',
        }}
      />
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
                Websites
              </Typography>
              <Typography
                variant="body2"
                sx={{
                  color: 'text.secondary',
                  fontWeight: 500,
                }}
              >
                Manage and monitor all website platforms
              </Typography>
            </Box>
            <Link
              component={RouterLink}
              underline="none"
              display="flex"
              href={`${current_path}/create`}
            >
              <Button
                aria-label="Create"
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                sx={{
                  px: 3,
                  py: 1.5,
                  fontWeight: 600,
                  boxShadow: (theme) => theme.customShadows.primary,
                }}
              >
                Add New Website
              </Button>
            </Link>
          </Box>

          {/* Statistics Cards */}
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={2}
            sx={{ width: '100%' }}
          >
            {/* Total Websites Card */}
            <Card
              sx={{
                flex: 1,
                borderRadius: 2,
                border: (theme) => `1px solid ${alpha(theme.palette.success.main, 0.4)}`,
                bgcolor: (theme) => alpha(theme.palette.success.main, 0.08),
              }}
            >
              <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                <Stack direction="row" alignItems="center" justifyContent="space-between">
                  <Typography
                    variant="body2"
                    sx={{
                      color: 'success.dark',
                      fontWeight: 600,
                      fontSize: '0.875rem',
                    }}
                  >
                    Total Websites
                  </Typography>
                  <Typography
                    variant="h4"
                    sx={{
                      color: 'success.main',
                      fontWeight: 700,
                    }}
                  >
                    {count.total}
                  </Typography>
                </Stack>
              </CardContent>
            </Card>

            {/* Active Websites Card */}
            <Card
              sx={{
                flex: 1,
                borderRadius: 2,
                border: (theme) => `1px solid ${alpha(theme.palette.primary.main, 0.4)}`,
                bgcolor: (theme) => alpha(theme.palette.primary.main, 0.08),
              }}
            >
              <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                <Stack direction="row" alignItems="center" justifyContent="space-between">
                  <Typography
                    variant="body2"
                    sx={{
                      color: 'primary.dark',
                      fontWeight: 600,
                      fontSize: '0.875rem',
                    }}
                  >
                    Active Websites
                  </Typography>
                  <Typography
                    variant="h4"
                    sx={{
                      color: 'primary.main',
                      fontWeight: 700,
                    }}
                  >
                    {count.active}
                  </Typography>
                </Stack>
              </CardContent>
            </Card>

            {/* On Fallback Card */}
            <Card
              sx={{
                flex: 1,
                borderRadius: 2,
                border: (theme) => `1px solid ${alpha(theme.palette.error.main, 0.4)}`,
                bgcolor: (theme) => alpha(theme.palette.error.main, 0.08),
              }}
            >
              <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                <Stack direction="row" alignItems="center" justifyContent="space-between">
                  <Typography
                    variant="body2"
                    sx={{
                      color: 'error.dark',
                      fontWeight: 600,
                      fontSize: '0.875rem',
                    }}
                  >
                    On Fallback
                  </Typography>
                  <Typography
                    variant="h4"
                    sx={{
                      color: 'error.main',
                      fontWeight: 700,
                    }}
                  >
                    {count.fallback}
                  </Typography>
                </Stack>
              </CardContent>
            </Card>
          </Stack>



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
export default Websites;
