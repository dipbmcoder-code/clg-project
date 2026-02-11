'use client';

import { useMemo, useState } from 'react';

import Button from '@mui/material/Button';
import { alpha } from '@mui/material/styles';
import { Box, Link, Stack, Avatar, Container, Typography, IconButton, Chip } from '@mui/material';

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

import Label from 'src/components/label/label';
import { useSettingsContext } from 'src/components/settings';

function Leagues({ data, pageSizeOptions, sorting, onPageChange, onDelete, onPublish, onCount }) {
  const current_path = usePathname();
  const { customSnackbarAction } = useCustomSnackbar();
  const settings = useSettingsContext();
  const [refreshDataGrid, setRefreshDataGrid] = useState(false);

  const [count, setCount] = useState(data.count);

  const handlePublish = async (val, id) => {
    const action = val ? 'publish' : 'unpublish';
    try {
      const res = await onPublish(id, action);
      if (!res.error) {
        handleRefreshDataGrid();
        customSnackbarAction(`League ${action}ed successfully`, 'success');
        const res = await onCount();
        setCount({
          total: res.total ?? 0,
          active: res.count,
          fallback: res.total - res.count,
        });
        return true;
      }

      customSnackbarAction(`Couldn't ${action} League `, 'error');
      return false;
    } catch (error) {
      console.log(error);
      customSnackbarAction(`Couldn't ${action} League `, 'error');
      return false;
    }
  };
  const columns = [
    {
      field: 'league_id',
      headerName: 'Leagues ID',
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
            <Typography component="span" variant="body2" noWrap>
              {value}
            </Typography>
          </Stack>
        );
      },
    },
    {
      flex: 1,
      field: 'league_name',
      headerName: 'League Name',
      sortable: false,
      renderCell: (params) => {
        return (
          <Stack
            direction="row"
            spacing={0.5}
            flexWrap="wrap"
            gap={0.5}
            sx={{ alignItems: 'center', height: '100%' }}
          >
            {params.value}
          </Stack>
        );
      },
    },
     {
      flex: 1,
      field: 'league_type',
      headerName: 'League Type',
      sortable: false,
      renderCell: (params) => {
        return (
          <Stack
            direction="row"
            spacing={0.5}
            flexWrap="wrap"
            gap={0.5}
            sx={{ alignItems: 'center', height: '100%' }}
          >
            {params.value}
          </Stack>
        );
      },
    },
    {
      type: 'actions',
      field: 'actions',
      headerName: 'Actions',
      maxWidth: 100,
      align: 'center',
      headerAlign: 'center',
      sortable: false,
      filterable: false,
      disableColumnMenu: true,
      getActions: ({ row }) => [
        <Link
          component={RouterLink}
          underline="none"
          display="flex"
          href={`${current_path}/${row.documentId}`}
        >
          <EditIcon />
        </Link>,
        <IconButton
          color="error"
          onClick={(e) => {
            e.stopPropagation();
            deleteEntry(row.documentId);
          }}
          label="Delete"
        >
          <DeleteIcon />
        </IconButton>,
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
    setCount({
      total: res.total ?? 0,
      active: res.count,
    });
  };
  const memoizedDataGridTable = useMemo(
    () => (
      <DataGridTable
        virtualizeColumnsWithAutoRowHeight
        getRowHeight={() => 'auto'}
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
        title="Delete League"
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
        <Typography variant="h4"> Leagues </Typography>

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
              justifyContent: 'space-between',
              px: 2,
            }}
          >
            <Box
              component="div"
              sx={{
                display: 'flex',
                flexDirection: {
                  xs: 'column',
                  sm: 'row',
                  alignItems: 'center',
                },
                gap: 2,
              }}
            >
            </Box>
            <Box
              component="div"
              sx={{
                display: 'flex',
                flexDirection: {
                  xs: 'column',
                  sm: 'row',
                  alignItems: 'center',
                },
                gap: 2,
              }}
            >

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
                    alignItems: 'center',
                  }}
                >
                  Add League
                </Button>
              </Link>
            </Box>
          </Box>
          {memoizedDataGridTable}
        </Box>
      </Container>
    </>
  );
}
export default Leagues;
