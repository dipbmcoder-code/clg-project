'use client';

import { Box, Stack, Select, MenuItem, Pagination } from '@mui/material';
import {
  useGridSelector,
  gridPageSelector,
  useGridApiContext,
  gridPageCountSelector,
  gridPaginationSelector,
} from '@mui/x-data-grid';

export default function CustomPagination(props) {
  const apiRef = useGridApiContext();
  const page = useGridSelector(apiRef, gridPageSelector);
  const pageCount = useGridSelector(apiRef, gridPageCountSelector);
  const paginationState = useGridSelector(apiRef, gridPaginationSelector);
  const {pageSize} = paginationState.paginationModel;
  const handlePageSizeChange = (event) => {
    apiRef.current.setPageSize(Number(event.target.value));
  };

  return (
    <Stack direction="row" spacing={2} alignItems="center" py={2} flexWrap="wrap">
      {props.pageSizes.length > 0 && (
        <Select
          value={pageSize}
          onChange={handlePageSizeChange}
          displayEmpty
          inputProps={{ 'aria-label': 'Select page size' }}
        >
          {props.pageSizes.map((size) => (
            <MenuItem key={size} value={size}>
              {size}
            </MenuItem>
          ))}
        </Select>
      )}
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        {pageSize * page + 1} - {Math.min(pageSize * page + pageSize, paginationState.rowCount)} of{' '}
        {paginationState.rowCount}
      </Box>
      <Pagination
        sx={{
          width: { xs: '100%', sm: 'auto' },
        }}
        color="primary"
        count={pageCount}
        page={page + 1}
        size="small"
        showFirstButton
        showLastButton
        onChange={(event, value) => apiRef.current.setPage(value - 1)}
      />
    </Stack>
  );
}
