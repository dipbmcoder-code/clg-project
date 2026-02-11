'use client';

import PropTypes from 'prop-types';
import isEqual from 'lodash/isEqual';
import debounce from 'lodash/debounce';
import { Controller } from 'react-hook-form';
import React, { useState, useEffect, useCallback } from 'react';

import { DataGrid, useGridApiRef } from '@mui/x-data-grid';
import {
  Box,
  Chip,
  Link,
  Stack,
  Avatar,
  TextField,
  Typography,
  IconButton,
  Autocomplete,
  Button,
} from '@mui/material';

import { RouterLink } from 'src/routes/components';

import { EditIcon, CheckIcon, DeleteIcon, ExclamationIcon, AddIcon } from 'src/utils/icons';

import EmptyContent from 'src/custom/EmptyContent';

import Label from 'src/components/label';

export default function UsersAutoComplete({ control, setValue, field, helperText, onField,viewCategory }) {
  UsersAutoComplete.propTypes = {
    control: PropTypes.object.isRequired,
    setValue: PropTypes.func.isRequired,
    field: PropTypes.object.isRequired,
    onField: PropTypes.func.isRequired,
  };
  const areEqual = (a, b) => isEqual(a, b);
  const apiRef = useGridApiRef();
  const [allOptions, setAllOptions] = useState(control._defaultValues[field.name]);
  const [hasInteracted, setHasInteracted] = useState(false);
  const [searchText, setSearchText] = useState('');

  const initialParent = field.parent?.fieldName ? control._getWatch(field.parent.fieldName) : false;
  const val = control._getWatch(field.name);

  const [parent, setParent] = useState(initialParent);

  useEffect(() => {
    if (!areEqual(initialParent, parent)) {
      setParent(initialParent);
      setValue(field.name, []);
      setAllOptions([]);
    }
  }, [initialParent]);

  const fetchOptions = async () => {
    let filters = {};

    if (parent) {
      filters = {
        $and: [
          {
            [field.parent.relation || field.parent.fieldName]: {
              id: {
                $eq: parent[0]?.value || null,
              },
            },
          },
        ],
      };
    } else if (field.parent?.default) {
      filters = {
        $and: [
          {
            [field.parent.relation]: {
              id: {
                $eq: field.parent.default,
              },
            },
          },
        ],
      };
    }

    if (!hasInteracted) {
      return;
    }

    try {
      const params = {
        query: searchText,
      };

      const { option, option_val } = field;
      const data = await onField(params);

      if (data.results) {
        const options = data.results.map((item) => ({
          label: item[option],
          value: item[option_val] || item.id,
          ...item,
        }));
        setAllOptions(options);
      }
    } catch (error) {
      console.error('Failed to fetch options', error);
    }
  };

  useEffect(() => {
    fetchOptions();
  }, [parent, hasInteracted]);

  const debouncedSearchText = useCallback(
    debounce((text) => {
      setSearchText(text);
    }, 700),
    []
  );

  useEffect(() => {
    if (!hasInteracted) return;
    debouncedSearchText(searchText);
  }, [searchText, debouncedSearchText]);

  const roleColors = {
    Admin: 'success',
  };
  const autoSizeColumns = ['league_name', 'league_type', 'league_logo_url','category','manage_catgeories'];
  const autosizeOptions = {
    columns: autoSizeColumns,
    includeOutliers: true,
    includeHeaders: true,
  };
  const handleChange = useCallback(() => {
    apiRef.current.autosizeColumns(autosizeOptions);
  }, []);
  useEffect(() => {
    handleChange();
  }, [val]);
  return (
    <Controller
      render={({ field: { onChange, value }, fieldState: { error } }) => (
        <>
          <Autocomplete
            fullWidth
            clearOnEscape
            filterSelectedOptions
            multiple
            options={allOptions}
            value={value}
            getOptionLabel={(option) => option.label ?? option}
            isOptionEqualToValue={(option, val) => option.value === val.value}
            onChange={(event, d) => {
              const newValue = field.selectType == 'multiple' ? d : Array.from(d).slice(-1);
              onChange(newValue);
              handleChange();
            }}
            renderOption={(props, option) => (
              <li {...props} key={option.label}>
                {option.label}
              </li>
            )}
            onInputChange={(event, val) => debouncedSearchText(val)}
            onOpen={() => setHasInteracted(true)}
            renderTags={(selectedOption, getTagProps) =>
              selectedOption.map((option, index) => (
                <Chip
                  {...getTagProps({ index })}
                  size="small"
                  variant="soft"
                  label={option.label}
                  key={option.label}
                />
              ))
            }
            renderInput={(params) => (
              <TextField
                {...params}
                label={field.label}
                error={!!error}
                helperText={error ? error?.message : helperText}
              />
            )}
          />

          <DataGrid
            apiRef={apiRef}
            rows={value}
            hideFooterPagination
            autosizeOnMount
            autoSizeColumns={autoSizeColumns}
            autosizeOptions={autoSizeColumns && autosizeOptions}
            autoHeight
            autoWidth
            sx={{
              '--DataGrid-overlayHeight': '200px',
              '&.MuiDataGrid-root .MuiDataGrid-cell:focus-within': {
                outline: 'none !important',
              },
              pt: 4,
            }}
            slots={{
              noRowsOverlay: (props) => <EmptyContent {...props} title="No Users Assigned" />,
              noResultsOverlay: (props) => <EmptyContent {...props} title="No results found" />,
            }}
            columns={[
              {
                field: 'league_logo_url',
                headerName: 'League Logo',
                sortable: false,
                filterable: false,
                renderCell: (params) => {
                  const { value, row } = params;
                  const { league_logo_url } = row;
                  return (
                    <Stack spacing={2} direction="row" alignItems="center" height="100%">
                      <Box
                        component="img"
                        alt={row.league_name}
                        src={league_logo_url}
                        sx={{
                          width: 'auto',
                          height: 40,
                          objectFit: 'contain',
                        }}
                      />
                    </Stack>
                  );
                },
              },
              {
                field: 'league_id',
                headerName: 'League Id',
                filterable: false,
                sortable: false,
                flex: 1,
                renderCell: (params) => (
                  <Typography component="span" variant="body2" noWrap>
                    {params.value}
                  </Typography>
                ),
              },
              {
                field: 'league_name',
                headerName: 'League',
                align: 'center',
                headerAlign: 'center',
                filterable: false,
                sortable: false,
                renderCell: (params) => (
                  <Typography component="span" variant="body2" noWrap>
                    {params.value}
                  </Typography>
                ),
              },
              {
                field: 'league_type',
                headerName: 'League Type',
                align: 'center',
                headerAlign: 'center',
                filterable: false,
                sortable: false,
                renderCell: (params) => (
                  <Typography component="span" variant="body2" noWrap>
                    {params.value}
                  </Typography>
                ),
              },
              {
                field: 'category',
                headerName: 'Category',
                align: 'center',
                headerAlign: 'center',
                filterable: false,
                sortable: false,
                renderCell: (params) => (
                  <Typography component="span" variant="body2" noWrap>
                    {params.value}
                  </Typography>
                ),
              },
              {
                type: 'actions',
                field: 'manage_catgeories',
                flex: 1,
                headerName:'Manage',
                align: 'center',
                headerAlign: 'center',
                sortable: false,
                filterable: false,
                disableColumnMenu: true,
                getActions: ({ row }) => [
                  <Button
                  aria-label="Manage Categories"
                  variant="outlined"
                  color="primary"
                  startIcon={<AddIcon />}
                  sx={{
                    alignItems: 'center',
                  }}
                  onClick={() => viewCategory?.setValue(row.documentId)}
                >
                  Manage Categories
                </Button>
                ],
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
                  <Link
                    component={RouterLink}
                    underline="none"
                    href={`/admin-dashboard/leagues/${row.documentId}`}
                  >
                    <IconButton color="success" label="Edit">
                      <EditIcon />
                    </IconButton>
                  </Link>,
                  <IconButton
                    color="error"
                    onClick={(e) => {
                      e.stopPropagation();
                      const newValue = value.filter((item) => item.value !== row.value);
                      onChange(newValue);
                      handleChange();
                    }}
                    label="Delete"
                  >
                    <DeleteIcon />
                  </IconButton>,
                ],
              },
            ]}
          />
        </>
      )}
      onChange={([event, data]) => data}
      name={field.name}
      control={control}
    />
  );
}
