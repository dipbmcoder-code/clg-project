'use client';

import { useMemo, useState } from 'react';

import Button from '@mui/material/Button';
import { alpha } from '@mui/material/styles';
import { Box, Link, Stack, Avatar, Container, Typography, IconButton } from '@mui/material';

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
    Admin: 'success',
  };
  const columns = [
    {
      field: 'firstname',
      // flex: 1,
      headerName: 'First Name',

      filterable: false,
      renderCell: (params) => {
        const { value, row } = params;
        const { thumbnail } = row;
        const thumb_url = thumbnail?.formats?.thumbnail?.url
          ? thumbnail?.formats?.thumbnail?.url
          : thumbnail?.url;
        return (
          <Stack spacing={2} direction="row" alignItems="center" height="100%">
            <Avatar alt={value} sx={{ width: 36, height: 36 }} src={thumbnail && thumb_url}>
              {!thumbnail && value.charAt(0).toUpperCase()}
            </Avatar>
            <Typography component="span" variant="body2" noWrap>
              {value}
            </Typography>
          </Stack>
        );
      },
    },
    {
      field: 'lastname',
      // flex: 1,
      headerName: 'Last Name',

      filterable: false,

      renderCell: (params) => {
        const { value } = params;
        return (
          <Typography component="span" variant="body2" noWrap>
            {value}
          </Typography>
        );
      },
    },
    {
      field: 'email',
      flex: 1,
      headerName: 'Email',
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        return (
          <Typography component="span" variant="body2" noWrap>
            {value}
          </Typography>
        );
      },
    },
    {
      field: 'roles',
      // flex: 1,
      headerName: 'Roles',
      align: 'center',
      headerAlign: 'center',
      filterable: false,
      sortable: false,
      renderCell: (params) => {
        const { value } = params;
        return (
          <Box
            sx={{
              display: 'flex',
              height: '100%',
              gap: 1,
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            {value && value.length > 0 ? (
              value.map((role, index) => (
                <Label key={index} color={roleColors[role.name] || 'default'} variant="soft">
                  {role.name}
                </Label>
              ))
            ) : (
              <Label>No Roles</Label>
            )}
          </Box>
        );
      },
    },
    {
      field: 'blocked',
      // flex: 1,
      headerName: 'Blocked',
      align: 'center',
      headerAlign: 'center',
      filterable: false,
      sortable: false,

      renderCell: (params) => (
        <Stack direction="row" alignItems="center" justifyContent="center" height="100%">
          {params.value ? (
            <CheckIcon sx={{ color: 'primary.main' }} />
          ) : (
            <ExclamationIcon sx={{ color: 'warning.main' }} />
          )}
        </Stack>
      ),
    },
    {
      field: 'isActive',
      flex: 1,
      headerName: 'Active',
      align: 'center',
      headerAlign: 'center',
      sortable: false,
      sortable: false,

      renderCell: (params) => (
        <Stack direction="row" alignItems="center" justifyContent="center" height="100%">
          {params.value ? (
            <CheckIcon sx={{ color: 'primary.main' }} />
          ) : (
            <ExclamationIcon sx={{ color: 'warning.main' }} />
          )}
        </Stack>
      ),
    },
    {
      type: 'actions',
      field: 'actions',
      flex: 1,
      headerName: 'Actions',
      maxWidth: 100,
      align: 'center',
      headerAlign: 'center',
      sortable: false,
      filterable: false,
      disableColumnMenu: true,
      getActions: ({ row }) => [
        <Link component={RouterLink} underline="none" href={`${current_path}/${row.id}`}>
          <EditIcon />
        </Link>,
        <IconButton
          color="error"
          onClick={(e) => {
            e.stopPropagation();
            deleteEntry(row.id);
          }}
          label="Delete"
        >
          <DeleteIcon />
        </IconButton>,
      ],
    },
  ];
  const autoSizeColumns = ['firstname', 'lastname', 'roles'];
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
        autoSizeColumns={autoSizeColumns}
        data={data}
        columns={columns}
        refresh={refreshDataGrid}
        sorting={sorting}
        fetchData={onPageChange}
        pageSizeOptions={pageSizeOptions}
        CustomPaginationComponent={CustomPagination}
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
        content="Are you sure you want to delete?"
        buttonText="Delete"
        props={{
          variant: 'soft',
          startIcon: <DeleteIcon />,
          color: 'error',
        }}
      />
      <Container maxWidth={settings.themeStretch ? false : 'xl'}>
        <Typography variant="h4"> Users </Typography>
        <Box
          sx={{
            mt: 5,
            width: 1,
            borderRadius: 2,
            bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
            border: (theme) => `dashed 1px ${theme.palette.divider}`,
          }}
        >
          <Box
            component="div"
            sx={{
              mt: 2,
              display: 'flex',
              gap: 2,
              justifyContent: 'end',
              px: 2,
            }}
          >
            <Link component={RouterLink} underline="none" href={`${current_path}/create`}>
              <Button
                aria-label="Create"
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                sx={{
                  alignItems: 'center',
                }}
              >
                Add User
              </Button>
            </Link>
          </Box>
          {memoizedDataGridTable}
        </Box>
      </Container>
    </>
  );
}
export default Users;
