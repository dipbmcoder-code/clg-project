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
  Card,
  CardContent,
  Tooltip,
} from '@mui/material';

import { usePathname } from 'src/routes/hooks';
import { RouterLink } from 'src/routes/components';

import { useBoolean } from 'src/hooks/use-boolean';

import { AddIcon, EditIcon, CheckIcon, DeleteIcon, ExclamationIcon } from 'src/utils/icons';

import { DataGridTable, CustomPagination, TransitionsDialog } from 'src/custom/index';

import Label from 'src/components/label';
import { useSettingsContext } from 'src/components/settings';

function Users({ data, pageSizeOptions, sorting, onPageChange, onDelete }) {
  const current_path = usePathname();
  const settings = useSettingsContext();
  const [refreshDataGrid, setRefreshDataGrid] = useState(false);

  const roleColors = {
    'Admin': 'success',
    'Super Admin': 'primary',
    'Editor': 'info',
  };

  const columns = [
    {
      field: 'firstname',
      headerName: 'First Name',
      minWidth: 160,
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        return (
          <Stack spacing={2} direction="row" alignItems="center" height="100%">
            <Avatar
              alt={value}
              sx={{
                width: 36,
                height: 36,
                bgcolor: 'primary.main',
                fontWeight: 700,
                fontSize: '0.9rem',
              }}
            >
              {value ? value.charAt(0).toUpperCase() : '?'}
            </Avatar>
            <Typography component="span" variant="body2" noWrap sx={{ fontWeight: 500 }}>
              {value}
            </Typography>
          </Stack>
        );
      },
    },
    {
      field: 'lastname',
      headerName: 'Last Name',
      minWidth: 140,
      filterable: false,
      renderCell: (params) => (
        <Typography component="span" variant="body2" noWrap>
          {params.value}
        </Typography>
      ),
    },
    {
      field: 'email',
      flex: 1,
      headerName: 'Email',
      minWidth: 200,
      filterable: false,
      renderCell: (params) => (
        <Typography component="span" variant="body2" noWrap sx={{ color: 'primary.main' }}>
          {params.value}
        </Typography>
      ),
    },
    {
      field: 'roles',
      headerName: 'Role',
      width: 130,
      align: 'center',
      headerAlign: 'center',
      filterable: false,
      sortable: false,
      renderCell: (params) => {
        const { value } = params;
        return (
          <Box sx={{ display: 'flex', height: '100%', gap: 1, justifyContent: 'center', alignItems: 'center' }}>
            {value && value.length > 0 ? (
              value.map((role, index) => (
                <Label key={index} color={roleColors[role.name] || 'default'} variant="soft">
                  {role.name}
                </Label>
              ))
            ) : (
              <Label>No Role</Label>
            )}
          </Box>
        );
      },
    },
    {
      field: 'isActive',
      headerName: 'Active',
      width: 100,
      align: 'center',
      headerAlign: 'center',
      sortable: false,
      filterable: false,
      renderCell: (params) => (
        <Stack direction="row" alignItems="center" justifyContent="center" height="100%">
          <Label color={params.value ? 'success' : 'warning'} variant="soft">
            {params.value ? 'Active' : 'Inactive'}
          </Label>
        </Stack>
      ),
    },
    {
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
        <Tooltip title="Edit User" arrow key="edit">
          <IconButton
            component={RouterLink}
            href={`${current_path}/${row.id}`}
            size="small"
            sx={{ color: 'primary.main', '&:hover': { bgcolor: 'primary.lighter' } }}
          >
            <EditIcon />
          </IconButton>
        </Tooltip>,
        <Tooltip title="Delete User" arrow key="delete">
          <IconButton
            size="small"
            onClick={(e) => {
              e.stopPropagation();
              deleteEntry(row.id);
            }}
            sx={{ color: 'error.main', '&:hover': { bgcolor: 'error.lighter' } }}
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
          '& .MuiDataGrid-cell': {
            py: 2,
            borderColor: (theme) => alpha(theme.palette.divider, 0.5),
          },
          '& .MuiDataGrid-columnHeaders': {
            bgcolor: (theme) => alpha(theme.palette.grey[500], 0.08),
            borderRadius: 0,
            borderBottom: (theme) => `2px solid ${theme.palette.divider}`,
          },
          '& .MuiDataGrid-columnHeader': {
            fontWeight: 700,
            fontSize: '0.875rem',
            color: 'text.primary',
          },
          '& .MuiDataGrid-row': {
            '&:hover': {
              bgcolor: (theme) => alpha(theme.palette.primary.main, 0.04),
            },
          },
          '& .MuiDataGrid-footerContainer': {
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
      <TransitionsDialog
        dialog={deleteDialog}
        refresh={handleRefreshDataGrid}
        action={onDelete}
        title="Delete User"
        content="Are you sure you want to delete this user?"
        buttonText="Delete"
        props={{
          variant: 'soft',
          startIcon: <DeleteIcon />,
          color: 'error',
        }}
      />
      <Container maxWidth={settings.themeStretch ? false : 'xl'}>
        <Stack spacing={3}>
          {/* Header */}
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
                Users
              </Typography>
              <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 500 }}>
                Manage team members and their access roles
              </Typography>
            </Box>
            <Link component={RouterLink} underline="none" href={`${current_path}/create`}>
              <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                sx={{ px: 3, py: 1.5, fontWeight: 600, boxShadow: (theme) => theme.customShadows.primary }}
              >
                Add User
              </Button>
            </Link>
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
export default Users;
