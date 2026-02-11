"use client";

import { Autocomplete, Box, Button, Chip, FormControl, Grid, IconButton, InputLabel, MenuItem, OutlinedInput, Select, Stack, TextField, Typography, Tooltip } from '@mui/material';
import { alpha } from '@mui/material/styles';
import { Controller } from 'react-hook-form';
import debounce from 'lodash/debounce';
import { useCallback, useEffect, useState, useMemo } from 'react';
import isEqual from 'lodash/isEqual';
import PropTypes from 'prop-types';
import { DataGrid, useGridApiRef } from '@mui/x-data-grid';
import EmptyContent from './EmptyContent';
import { AddIcon, DeleteIcon, EditIcon } from 'src/utils/icons';
import { useBoolean } from 'src/hooks/use-boolean';
import { LeaguesCategoryPopup } from 'src/sections/admin/websites/website/leagues-category';
import { RHFSelect } from 'src/components/hook-form';
import { findLeagues } from 'src/utils/leagueActions';

export default function AutoSelectLeagues({ categoriesOptions, control, setValue, field, helperText, onField }) {
    AutoSelectLeagues.propTypes = {
        control: PropTypes.object.isRequired,
        setValue: PropTypes.func.isRequired,
        field: PropTypes.object.isRequired,
        onField: PropTypes.func.isRequired,
    };

    const apiRef = useGridApiRef();
    const [allOptions, setAllOptions] = useState([]);
    const viewCategory = useBoolean(false);
    const [selectedLeague, setSelectedLeague] = useState("");
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [inputValue, setInputValue] = useState(''); // ✅ Debounced input state
    const [filteredCategories, setFilteredCategories] = useState([]); // ✅ Filtered results
    const [hasInteracted, setHasInteracted] = useState(false);
    const val = control._getWatch(field.name);
    const [sortModel, setSortModel] = useState([{ field: 'country', sort: 'asc' }]);

    const fetchOptions = async () => {
        const leagues = await findLeagues();
        setAllOptions(leagues || []);
    };

    useEffect(() => {
        fetchOptions();
    }, []);

    // ✅ Proper debounced filter for Categories
    const debouncedFilterCategories = useMemo(() =>
        debounce((searchText) => {
            console.log('🔍 Debounced category search:', searchText);

            if (!searchText.trim()) {
                setFilteredCategories(categoriesOptions);
                return;
            }

            const lowerSearch = searchText.toLowerCase().trim();
            const filtered = categoriesOptions.filter(option => {
                // Skip already selected categories
                const isSelected = selectedCategories.some(
                    selected => selected?.id?.toString() === option?.id?.toString()
                );
                if (isSelected) return false;

                // Search in name and other fields
                const searchableText = `${option?.name || ''} ${option?.label || ''}`.toLowerCase();
                return searchableText.includes(lowerSearch);
            });
            console.log(filtered);
            setFilteredCategories(filtered);
        }, 300),
        [categoriesOptions, selectedCategories]);

    // ✅ Handle category input change
    const handleCategoryInputChange = useCallback((_, newInputValue) => {
        setInputValue(newInputValue);
        debouncedFilterCategories(newInputValue);
    }, [debouncedFilterCategories]);

    // ✅ Reset filtered categories when options change
    useEffect(() => {
        if (!inputValue.trim()) {
            setFilteredCategories(categoriesOptions || []);
        } else {
            // Re-run filter if options change while searching
            debouncedFilterCategories(inputValue);
        }
    }, [categoriesOptions, inputValue, debouncedFilterCategories]);

    // ✅ Cleanup debounce
    useEffect(() => {
        return () => {
            debouncedFilterCategories.cancel();
        };
    }, [debouncedFilterCategories]);

    const roleColors = {
        Admin: 'success',
    };
    const autoSizeColumns = ['name', 'country', 'categories', 'manage_catgeories'];
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
    }, [val, handleChange]);

    return (
        <Controller
            render={({ field: { onChange, value }, fieldState: { error } }) => (
                <>
                    <Grid container spacing={2} alignItems="center">
                        <Grid item xs={12} sm={5}>
                            <Autocomplete
                                options={allOptions.filter(option => !(value || []).some(row => row.id === option.id))}
                                getOptionLabel={(option) => `${option.country != 'World' ? option.country + ' - ' : ''}${option.name}`}
                                value={allOptions.find(opt => `${opt.country} ${opt.name}` === selectedLeague) || null}
                                onChange={(event, newValue) => {
                                    setSelectedLeague(newValue ? `${newValue.country} ${newValue.name}` : "");
                                }}
                                getOptionKey={(option) => option.id}
                                renderInput={(params) => (
                                    <TextField
                                        {...params}
                                        label="Select League"
                                        size="small"
                                        fullWidth
                                        sx={{
                                            '& .MuiOutlinedInput-root': {
                                                '&:hover fieldset': {
                                                    borderColor: 'primary.main',
                                                },
                                            },
                                        }}
                                    />
                                )}
                                filterSelectedOptions
                                isOptionEqualToValue={(option, value) => option.id === value?.id}
                                disableClearable={false}
                                clearOnEscape
                            />
                        </Grid>

                        <Grid item xs={12} sm={5}>
                            <FormControl fullWidth size='small'>
                                <Autocomplete
                                    multiple
                                    freeSolo={false}
                                    filterSelectedOptions={false} // ✅ Manual filtering
                                    filterOptions={(x) => x} // ✅ Use debounced results
                                    disabled={!selectedLeague}
                                    options={filteredCategories}
                                    value={selectedCategories || []}
                                    getOptionKey={(option) => option.id}
                                    inputValue={inputValue} // ✅ Controlled input
                                    onInputChange={handleCategoryInputChange} // ✅ Debounced input
                                    onChange={(event, newValue) => {
                                        setSelectedCategories(newValue);
                                    }}
                                    isOptionEqualToValue={(option, value) =>
                                        option?.id?.toString() === value?.id?.toString()
                                    }
                                    getOptionLabel={(option) => option?.name ?? ''}
                                    renderTags={(value, getTagProps) =>
                                        value.map((option, index) => (
                                            <Chip
                                                key={option?.id?.toString() ||
                                                    `${(option?.name || '').replace(/\s+/g, '-')}-${index}`}
                                                size='small'
                                                label={option?.name ?? ''}
                                                color="primary"
                                                variant="outlined"
                                                sx={{ fontWeight: 500 }}
                                                {...getTagProps({ index })}
                                            />
                                        ))
                                    }
                                    renderInput={(params) => (
                                        <TextField
                                            {...params}
                                            label="Select Categories"
                                            size='small'
                                            sx={{
                                                '& .MuiOutlinedInput-root': {
                                                    '&:hover fieldset': {
                                                        borderColor: 'primary.main',
                                                    },
                                                },
                                            }}
                                        />
                                    )}
                                    disableClearable={false}
                                    clearOnEscape
                                />
                            </FormControl>
                        </Grid>

                        <Grid item xs={12} sm={2}>
                            <Button
                                variant="contained"
                                color="primary"
                                startIcon={<AddIcon />}
                                disabled={!selectedLeague}
                                align="center"
                                sx={{
                                    height: '100%',
                                    fontWeight: 600,
                                    boxShadow: (theme) => theme.customShadows?.primary || 2,
                                    '&:hover': {
                                        boxShadow: (theme) => theme.customShadows?.primaryHover || 4,
                                    },
                                }}
                                onClick={() => {
                                    if (!selectedLeague) return;
                                    const league = allOptions.find((opt) => `${opt.country} ${opt.name}` === selectedLeague);

                                    if (!league) return;

                                    const newRow = {
                                        id: league.id,
                                        name: league.name,
                                        country: league.country,
                                        categories: selectedCategories,
                                    };

                                    const exists = (value || []).some((row) => row.id === league.id);
                                    if (exists) return;

                                    onChange([...(value || []), newRow]);

                                    setSelectedLeague("");
                                    setSelectedCategories([]);
                                    setInputValue(''); // ✅ Clear input
                                    setFilteredCategories(categoriesOptions); // ✅ Reset filtered
                                }}
                            >
                                Add
                            </Button>
                        </Grid>
                    </Grid>

                    {/* DataGrid remains unchanged */}
                    <DataGrid
                        apiRef={apiRef}
                        rows={value}
                        virtualizeColumnsWithAutoRowHeight
                        getRowHeight={() => 'auto'}
                        hideFooterPagination
                        autoSizeColumns={autoSizeColumns}
                        autosizeOptions={autosizeOptions}
                        sx={{
                            '--DataGrid-overlayHeight': '200px',
                            '&.MuiDataGrid-root .MuiDataGrid-cell:focus-within': {
                                outline: 'none !important',
                            },
                            pt: 4,
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
                                    cursor: 'pointer',
                                },
                                '&.Mui-selected': {
                                    bgcolor: (theme) => alpha(theme.palette.primary.main, 0.08),
                                    '&:hover': {
                                        bgcolor: (theme) => alpha(theme.palette.primary.main, 0.12),
                                    },
                                },
                            },
                            '& .MuiDataGrid-footerContainer': {
                                borderTop: (theme) => `2px solid ${theme.palette.divider}`,
                                bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
                            },
                        }}
                        sortModel={sortModel}
                        sortable
                        sortingMode="client"
                        onSortModelChange={(model) => {
                            setSortModel(model);
                            try {
                                const getModel = apiRef?.current?.getSortModel;
                                const current = getModel ? getModel() : undefined;
                                if (!isEqual(current, model) && apiRef?.current?.setSortModel) {
                                    apiRef.current.setSortModel(model);
                                }
                            } catch (e) { }
                        }}
                        slots={{
                            noRowsOverlay: (props) => <EmptyContent {...props} title="No Users Assigned" />,
                            noResultsOverlay: (props) => <EmptyContent {...props} title="No results found" />,
                        }}
                        columns={[
                            // ... your existing columns (unchanged)
                            {
                                field: 'country',
                                headerName: 'Country',
                                align: 'center',
                                headerAlign: 'center',
                                sortable: true,
                                renderCell: (params) => (
                                    <Stack spacing={2} direction="row" alignItems="center" justifyContent="center" sx={{ minWidth: 0, height: '100%', py: 1 }}>
                                        <Typography component="span" variant="body2" noWrap sx={{ fontWeight: 500, color: 'text.primary' }}>
                                            {params.value}
                                        </Typography>
                                    </Stack>
                                ),
                            },
                            {
                                field: 'name',
                                headerName: 'League',
                                align: 'center',
                                headerAlign: 'center',
                                minWidth: 250,
                                sortable: true,
                                renderCell: (params) => (
                                    <Stack spacing={2} direction="row" alignItems="center" justifyContent="center" sx={{ minWidth: 0, height: '100%', py: 1 }}>
                                        <Typography component="span" variant="body2" noWrap sx={{ fontWeight: 600, color: 'text.primary' }}>
                                            {params.value}
                                        </Typography>
                                    </Stack>
                                ),
                            },
                            {
                                field: 'categories',
                                headerName: 'Category',
                                align: 'center',
                                headerAlign: 'center',
                                filterable: false,
                                sortable: false,
                                flex: 1,
                                sortComparator: (v1 = [], v2 = []) => {
                                    const a = v1.map(c => c.name).join(', ');
                                    const b = v2.map(c => c.name).join(', ');
                                    return a.localeCompare(b);
                                },
                                renderCell: (params) => (
                                    <Stack spacing={2} direction="row" alignItems="center" flexWrap="wrap" gap={0.5} sx={{ minWidth: 0, height: '100%', py: 1 }}>
                                        {(params.value || []).map(C => (
                                            <Chip
                                                key={C.id}
                                                label={C.name}
                                                size="small"
                                                variant="outlined"
                                                color="primary"
                                                sx={{ fontWeight: 500 }}
                                            />
                                        ))}
                                    </Stack>
                                ),
                            },
                            {
                                type: 'actions',
                                field: 'manage_catgeories',
                                headerName: 'Manage',
                                align: 'center',
                                headerAlign: 'center',
                                sortable: false,
                                filterable: false,
                                disableColumnMenu: true,
                                getActions: ({ row }) => [
                                    <Tooltip title="Manage Categories" arrow>
                                        <Button
                                            aria-label="Manage Categories"
                                            variant="outlined"
                                            color="primary"
                                            startIcon={<AddIcon />}
                                            sx={{
                                                alignItems: 'center',
                                                fontWeight: 600,
                                                '&:hover': {
                                                    bgcolor: 'primary.lighter',
                                                },
                                            }}
                                            onClick={() => viewCategory?.setValue(row.id)}
                                        >
                                            Manage Categories
                                        </Button>
                                    </Tooltip>
                                ],
                            },
                            {
                                type: 'actions',
                                field: 'actions',
                                headerName: 'Actions',
                                align: 'center',
                                headerAlign: 'center',
                                sortable: false,
                                filterable: false,
                                disableColumnMenu: true,
                                getActions: ({ row }) => [
                                    <Tooltip title="Delete League" arrow>
                                        <IconButton
                                            size="small"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                const newValue = value.filter((item) => item.id !== row.id);
                                                onChange(newValue);
                                                handleChange();
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
                        ]}
                    />
                    <LeaguesCategoryPopup data={value} handle={viewCategory} categoriesOptions={categoriesOptions} action={onChange} handleChange={handleChange} />
                </>
            )}
            name={field.name}
            control={control}
        />
    );
}
