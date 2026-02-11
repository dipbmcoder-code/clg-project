"use client";

import { useMemo, useState } from "react";

import Button from "@mui/material/Button";
import { alpha } from "@mui/material/styles";
import {
  Box,
  Link,
  Stack,
  Container,
  Typography,
  IconButton,
  Avatar,
  Card,
  CardContent,
  Chip,
  Tooltip,
} from "@mui/material";

import { usePathname } from "src/routes/hooks";
import { RouterLink } from "src/routes/components";

import { useBoolean } from "src/hooks/use-boolean";

import { AddIcon, EditIcon, DeleteIcon } from "src/utils/icons";

import {
  DataGridTable,
  CustomPagination,
  TransitionsDialog,
} from "src/custom/index";

import Label from "src/components/label";
import { useSettingsContext } from "src/components/settings";

function ManualNewsList({
  data,
  pageSizeOptions,
  sorting,
  onPageChange,
  onDelete,
  onCount,
}) {
  const current_path = usePathname();
  const settings = useSettingsContext();
  const [refreshDataGrid, setRefreshDataGrid] = useState(false);
  const [count, setCount] = useState(data.count);
  const typeColors = {
    match_reviews: "success",
    match_previews: "info",
  };

  const columns = [
    {
      field: "league",
      flex: 1,
      headerName: "League",
      filterable: false,
      align: "center",
      headerAlign: "center",
      renderCell: (params) => {
        const leagues = params.value; // an array
        const leagueName =
          Array.isArray(leagues) && leagues.length > 0 ? leagues[0].name : "-";
        return (
          <Stack
            spacing={2}
            direction="row"
            alignItems="center"
            sx={{ minWidth: 0, height: '100%', py: 1 }}
          >
            <Avatar alt={leagueName} sx={{ width: 36, height: 36 }} color="primary">
              {leagueName.charAt(0).toUpperCase()}
            </Avatar>
            <Typography component="span" variant="body2" noWrap>
              {leagueName}
            </Typography>
          </Stack>
        );
      },
    },
    {
      field: "home_team",
      flex: 1,
      headerName: "Match",
      align: "center",
      headerAlign: "center",
      filterable: false,
      renderCell: (params) => {
        const { row } = params;
        return (
          <Typography component="span" variant="body2" noWrap>
            {row.home_team} v/s {row.away_team}
          </Typography>
        );
      },
    },
    {
      field: "news_type",
      flex: 1,
      headerName: "Type",
      align: "center",
      headerAlign: "center",
      filterable: false,
      renderCell: (params) => {
        const { value } = params;
        const formattedValue = value
          ?.replace("_", " ")
          ?.replace(/\b\w/g, (l) => l.toUpperCase());
        return (
          <Chip
            label={formattedValue}
            color={typeColors[value] || "default"}
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
      field: "published",
      flex: 1,
      headerName: "Status",
      align: "center",
      headerAlign: "center",
      filterable: false,
      renderCell: (params) => {
        const { value } = params; // boolean value

        const isPublished = Boolean(value);
        const label = isPublished ? "Published" : "Unpublished";
        const color = isPublished ? "success" : "error";

        return (
          <Label
            color={color}
            variant="soft"
            sx={{
              fontWeight: 600,
              fontSize: '0.75rem',
              px: 1.5,
            }}
          >
            {label}
          </Label>
        );
      },
    },
    {
      field: "createdAt",
      flex: 1,
      headerName: "Created At",
      filterable: false,
      align: "center",
      headerAlign: "center",
      renderCell: (params) => {
        const { value } = params;
        return (
          <Typography component="span" variant="body2" noWrap>
            {/* {new Date(value).toLocaleDateString()} */}
            {new Date(value).toLocaleString()}
          </Typography>
        );
      },
    },
    {
      type: "actions",
      field: "actions",
      flex: 1,
      headerName: "Actions",
      maxWidth: 100,
      align: "center",
      headerAlign: "center",
      sortable: false,
      filterable: false,
      disableColumnMenu: true,
      getActions: ({ row }) => [
        <Tooltip title="Edit News" arrow>
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
        <Tooltip title={row.published ? "Cannot delete published news" : "Delete News"} arrow>
          <IconButton
            size="small"
            disabled={row.published}
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

  const autoSizeColumns = ["home_team", "league", "news_type"];
  const deleteDialog = useBoolean();

  const deleteEntry = (id) => {
    deleteDialog.setValue(id);
  };

  const deleteCallback = async () => {
    const res = await onCount();
    const totalCount = res?.results?.length || 0;
    const activeCount = res.results?.filter((item) => item.published).length || 0;
    const fallbackCount = totalCount - activeCount;

    setCount({
      total: totalCount,
      publish: activeCount,
      fallback: fallbackCount,
    });
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
    [data, sorting, onPageChange, refreshDataGrid],
  );

  return (
    <>
      <TransitionsDialog
        dialog={deleteDialog}
        refresh={handleRefreshDataGrid}
        action={onDelete}
        callback={deleteCallback}
        title="Delete News"
        content="Are you sure you want to delete this news item?"
        buttonText="Delete"
        props={{
          variant: "soft",
          startIcon: <DeleteIcon />,
          color: "error",
        }}
      />
      <Container maxWidth={settings.themeStretch ? false : "xl"}>
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
                Manual News
              </Typography>
              <Typography
                variant="body2"
                sx={{
                  color: 'text.secondary',
                  fontWeight: 500,
                }}
              >
                Manage and publish manual news articles
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
                Add News
              </Button>
            </Link>
          </Box>

          {/* Statistics Cards */}
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={2}
            sx={{ width: '100%' }}
          >
            {/* Total News Card */}
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
                    Total News
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

            {/* Published News Card */}
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
                    Published News
                  </Typography>
                  <Typography
                    variant="h4"
                    sx={{
                      color: 'primary.main',
                      fontWeight: 700,
                    }}
                  >
                    {count.publish}
                  </Typography>
                </Stack>
              </CardContent>
            </Card>

            {/* Unpublished Card */}
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
                    Unpublished
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

export default ManualNewsList;
