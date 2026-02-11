'use client';

import { debounce } from 'lodash';
import { useState, useEffect } from 'react';

import Box from '@mui/material/Box';
import {
  DataGrid,
  useGridApiRef,
  GridToolbarContainer,
  GridToolbarQuickFilter,
  GridToolbarColumnsButton,
  GridToolbarDensitySelector,
} from '@mui/x-data-grid';

import EmptyContent from 'src/custom/EmptyContent';

const HIDE_COLUMNS = {};

function DataGridTable({
  data,
  columns,
  autoSizeColumns,
  sorting,
  refresh,
  fetchData,
  pageSizeOptions,
  CustomPaginationComponent,
  hideFooter,
}) {
  const HIDE_COLUMNS_TOGGLABLE = ['edit', 'delete'];

  const [totalRowCount, setTotalRowCount] = useState(data.pagination.total);
  const [tableState, setTableState] = useState({
    page: data.pagination.page - 1,
    pageSize: data.pagination.pageSize,
    sort: sorting,
    _q: '',
  });
  const [isFirstRender, setIsFirstRender] = useState(true);
  const [results, setResults] = useState(data.results);
  const [loading, setLoading] = useState(false);
  const apiRef = useGridApiRef();

  const autosizeOptions = {
    columns: autoSizeColumns,
    includeOutliers: true,
    includeHeaders: true,
  };

  useEffect(() => {
    if (isFirstRender) {
      setIsFirstRender(false);
      return;
    }
    const load = async () => {
      setLoading(true);
      try {
        const res = await fetchData({ ...tableState, page: tableState.page + 1 });
        setResults(res.results);
        setTotalRowCount(res.pagination.total);
      } catch (error) {
        console.log(error);
      }
      setLoading(false);
    };
    load();
  }, [tableState, refresh]);
  useEffect(() => {
    if (isFirstRender) {
      setIsFirstRender(false);
      return;
    }
    apiRef.current.autosizeColumns(autosizeOptions);
  }, [results]);
  const updateTableState = (updates) => {
    setTableState((prev) => ({ ...prev, ...updates }));
  };
  const onFilterChange = debounce((data) => {
    updateTableState({
      _q: data.quickFilterValues.length > 0 ? data.quickFilterValues[0] : '',
      page: 0,
    });
  }, 1000);
  const [columnVisibilityModel, setColumnVisibilityModel] = useState(HIDE_COLUMNS);

  const getTogglableColumns = () =>
    columns
      .filter((column) => !HIDE_COLUMNS_TOGGLABLE.includes(column.field))
      .map((column) => column.field);
  return (
    <DataGrid
      apiRef={apiRef}
      autosizeOnMount={!!autoSizeColumns}
      autosizeOptions={autoSizeColumns && autosizeOptions}
      disableRowSelectionOnClick
      onCellClick={(e) => {
        e.stopPropagation;
      }}
      onRowClick={(e) => {
        e.stopPropagation;
      }}
      autoHeight
      autoWidth
      rows={results}
      columns={columns}
      sx={{
        '--DataGrid-overlayHeight': '300px',
        '&.MuiDataGrid-root .MuiDataGrid-cell:focus-within': {
          outline: 'none !important',
        },
      }}
      loading={loading}
      paginationMode="server"
      sortingMode="server"
      rowCount={totalRowCount}
      paginationModel={{
        page: tableState.page,
        pageSize: tableState.pageSize,
      }}
      hideFooterPagination={hideFooter}
      columnVisibilityModel={columnVisibilityModel}
      onColumnVisibilityModelChange={(newModel) => setColumnVisibilityModel(newModel)}
      disableColumnFilter
      filterMode="server"
      onFilterModelChange={onFilterChange}
      onPaginationModelChange={(model) => {
        const { page: newPage, pageSize: newPageSize } = model;
        const updates = {};
        if (newPage !== tableState.page) {
          updates.page = newPage;
        }
        if (newPageSize !== tableState.pageSize) {
          updates.pageSize = newPageSize;
        }
        updateTableState(updates);
      }}
      onSortModelChange={(model) => {
        updateTableState({ sort: model, page: 0 });
      }}
      sortModel={tableState.sort}
      slots={{
        toolbar: CustomToolbar,
        noRowsOverlay: (props) => <EmptyContent {...props} title="No Data" />,
        noResultsOverlay: (props) => <EmptyContent {...props} title="No results found" />,
        pagination: (props) => <CustomPaginationComponent {...props} pageSizes={pageSizeOptions} />,
      }}
      slotProps={{
        toolbar: {
          showQuickFilter: false,
        },
        columnsManagement: {
          getTogglableColumns,
        },
      }}
    />
  );
}
export default DataGridTable;
function CustomToolbar() {
  return (
    <GridToolbarContainer>
      <GridToolbarQuickFilter />
      <Box sx={{ flexGrow: 1 }} />
      <GridToolbarColumnsButton />
      {/* <GridToolbarFilterButton /> */}
      <GridToolbarDensitySelector />
      {/* <GridToolbarExport /> */}
    </GridToolbarContainer>
  );
}
