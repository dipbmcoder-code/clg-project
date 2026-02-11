"use client";

import { Autocomplete, Box, Button, Chip, FormControl, Grid, IconButton, InputLabel, MenuItem, OutlinedInput, Select, TextField, Typography } from '@mui/material';
import { Controller } from 'react-hook-form';
import debounce from 'lodash/debounce';
import { useCallback, useEffect, useState } from 'react';
import isEqual from 'lodash/isEqual';
import PropTypes from 'prop-types';
import { DataGrid, useGridApiRef } from '@mui/x-data-grid';
import EmptyContent from './EmptyContent';
import { AddIcon, DeleteIcon, EditIcon } from 'src/utils/icons';
import { useBoolean } from 'src/hooks/use-boolean';
import { LeaguesCategoryPopup } from 'src/sections/admin/websites/website/leagues-category';
import { RHFDateTimePicker, RHFSelect } from 'src/components/hook-form';
import { findLeagues, findPlayers } from 'src/utils/leagueActions';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider as MuiLocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

export default function AutoSelectProfiles({ control, setValue, field, helperText, onField }) {
    AutoSelectProfiles.propTypes = {
        control: PropTypes.object.isRequired,
        setValue: PropTypes.func.isRequired,
        field: PropTypes.object.isRequired,
        onField: PropTypes.func.isRequired,
    };
    const areEqual = (a, b) => isEqual(a, b);
    const apiRef = useGridApiRef();
    const [allOptions, setAllOptions] = useState([]);
    const [playerOptions, setPlayerOptions] = useState([]);
    const viewCategory = useBoolean(false);
    const [selectedLeague, setSelectedLeague] = useState("");
    const [selectedPlayers, setSelectedPlayers] = useState(null);
    const [hasInteracted, setHasInteracted] = useState(false);
    const [hasPlayerInteracted, setHasPlayerInteracted] = useState(false);
    const [searchText, setSearchText] = useState('');
    const [searchPlayer, setSearchPlayer] = useState('');
    const [dateTime, setDateTime] = useState(null);
    const val = control._getWatch(field.name);

    const fetchPlayerOptions = async (searchText = "") => {
        try {
            console.log("search", searchText)
            const res = await findPlayers(searchText);
            console.log("players res",res);
            if (res.players) {
                setPlayerOptions(res.players);
            } else {
                setPlayerOptions([]);
            }
        } catch (error) {
            console.log(error);
            setPlayerOptions([]);
        }
    }

    useEffect(() => {
        console.log("fetching leagues");
        fetchPlayerOptions();
    }, [hasInteracted]);

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


    const autoSizeColumns = ['name', 'datetime', 'actions'];
    const autosizeOptions = {
        columns: autoSizeColumns,
        includeOutliers: true,
        includeHeaders: true,
    };


    const options = {
        year: "numeric",
        month: "short", // 👈 gives short month name
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    };

    const handleDateTimeChange = (newValue) => {
        const date = new Date(newValue);
        return date.toLocaleString("en-US", options);
    }

    return (
        <Controller
            render={({ field: { onChange, value }, fieldState: { error } }) => (
                <>
                    <Grid container spacing={2} alignItems="center">
                       { /* <Grid item xs={12} sm={6}>
                            <Autocomplete
                                options={allOptions
                                    .filter(option =>
                                        searchText
                                            ? option.name.toLowerCase().includes(searchText.toLowerCase())
                                            : true
                                    )
                                    .slice(0, 50)
                                }
                                getOptionLabel={(option) => option.name}
                                value={allOptions.find(opt => opt.id === selectedLeague?.id) || null}
                                onChange={(event, newValue) => {
                                    setSelectedLeague(newValue);
                                    fetchPlayerOptions(newValue?.id, searchPlayer);
                                }}
                                onInputChange={(event, newInputValue) => {
                                    setSearchText(newInputValue);
                                    setHasInteracted(true);
                                }}
                                renderInput={(params) => (
                                    <TextField
                                        {...params}
                                        label="Select League"
                                        size="small"
                                        fullWidth
                                    />
                                )}
                                isOptionEqualToValue={(option, value) => option.id === value.id}
                                disableClearable={false}
                                clearOnEscape
                            />
                        </Grid> */}
                                
                        <Grid item xs={12} sm={5}>
                            <Autocomplete
                                options={playerOptions}
                                getOptionLabel={(option) => `${option.name} - ${option.position}`}
                                value={selectedPlayers || null}
                                onChange={(event, newValue) => {   
                                    setSelectedPlayers(newValue); 
                                }}
                                onInputChange={(event, newInputValue) => {
                                    console.log("new input value",newInputValue);
                                    if (newInputValue) {
                                        if (newInputValue.trim().length >= 3)
                                            fetchPlayerOptions(newInputValue);
                                        else fetchPlayerOptions();
                                    }
                                    
                                }}
                                renderInput={(params) => (
                                    <TextField
                                        {...params}
                                        label="Select Player"
                                        size="small"
                                        fullWidth
                                    />
                                )}
                                isOptionEqualToValue={(option, value) => option.id === value.id}
                                disableClearable={false}
                                clearOnEscape
                            />
                            {/* <FormControl fullWidth size='small'>
                                <InputLabel id="category-label">Select Player</InputLabel>
                                <Select
                                    labelId="category-label"
                                    disabled={!selectedLeague}
                                    value={selectedPlayers}
                                    onChange={(e) => setSelectedPlayers(e.target.value)}
                                    input={<OutlinedInput label="Select Player" />}
                                >
                                    {playerOptions.map((cat) => (
                                        <MenuItem key={cat.id} value={cat}>
                                            {cat.name}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl> */}
                        </Grid>
                        <Grid item xs={12} sm={5}>
                            <MuiLocalizationProvider dateAdapter={AdapterDateFns}>
                                <DateTimePicker
                                    label="Select Date & Time"
                                    value={dateTime}
                                    onChange={(newValue) => {
                                    if (newValue) {
                                        setDateTime(newValue);
                                    }
                                    }}
                                    slotProps={{
                                    textField: {
                                        fullWidth: true,
                                        error: !!error,
                                        helperText: error?.message || helperText,
                                        size: "small",
                                    },
                                    }}
                                />
                            </MuiLocalizationProvider>
                        </Grid>

                        <Grid item xs={12} sm={2}>
                            <Button
                                variant="contained"
                                color="primary"
                                startIcon={<AddIcon />}
                                disabled={!selectedPlayers || !dateTime}
                                align="center"
                                sx={{ height: '100%' }}
                                onClick={() => {
                                    if (!selectedPlayers) return;
                                    if (!dateTime) return;

                                    const newRow = {
                                        id: selectedPlayers?.id,
                                        name: selectedPlayers?.name,
                                        position: selectedPlayers?.position,
                                        datetime: dateTime,
                                    };

                                    onChange([...(value || []), newRow]);
                                    setSearchText('');
                                    setDateTime(null);
                                }}
                            >
                                Add
                            </Button>
                        </Grid>
                    </Grid>

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
                                field: 'name',
                                headerName: 'Player',
                                align: 'center',
                                headerAlign: 'center',
                                filterable: false,
                                sortable: false,
                                minWidth: 250,
                                renderCell: (params) => (
                                    <Typography component="span" variant="body2" noWrap>
                                        {params.value}
                                    </Typography>

                                ),
                            },
                            {
                                field: 'position',
                                headerName: 'Player Position',
                                align: 'center',
                                headerAlign: 'center',
                                filterable: false,
                                sortable: false,
                                minWidth: 250,
                                renderCell: (params) => (
                                    <Typography component="span" variant="body2" noWrap>
                                        {params.value}
                                    </Typography>

                                ),
                            },
                            {
                                field: 'datetime',
                                headerName: 'Date & Time',
                                filterable: false,
                                sortable: false,
                                flex: 1,
                                renderCell: (params) => (
                                    <Typography component="span" variant="body2" noWrap>
                                        { handleDateTimeChange(params.value)}
                                    </Typography>
                                ),
                            },
                            {
                                type: 'actions',
                                field: 'actions',
                                flex: 1,
                                headerName: 'Actions',
                                align: 'center',
                                headerAlign: 'center',
                                sortable: false,
                                filterable: false,
                                disableColumnMenu: true,
                                getActions: ({ row }) => [

                                    <IconButton
                                        color="error"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            const newValue = value.filter((item) => item.id !== row.id);
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
            name={field?.name}
            control={control}
        />
    )
}