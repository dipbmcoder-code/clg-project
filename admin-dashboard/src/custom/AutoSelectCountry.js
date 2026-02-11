"use client";

import { Autocomplete, Box, Chip, TextField } from '@mui/material';
import { Controller } from 'react-hook-form';
import debounce from 'lodash/debounce';
import { useCallback, useEffect, useState } from 'react';

const { countries } = require('countries-list');
const countries2to3 = require('countries-list/minimal/countries.2to3.min.json');

export default function AutoSelectCountry({ control, helperText, field }) {
    const allOptions = Object.keys(countries).map(key => { return { code: key, name: countries[key].name, code3: countries2to3[key] } });
    const [hasInteracted, setHasInteracted] = useState(false);
    const [searchText, setSearchText] = useState('');
    const [showAll, setShowAll] = useState(false);

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

    return (
        <Controller
            render={({ field: { onChange, value }, fieldState: { error } }) => (
                <Autocomplete
                    options={allOptions}
                    multiple
                    clearOnEscape
                    filterSelectedOptions
                    value={value || []}
                    getOptionLabel={(option) => option.name ?? option}
                    onInputChange={(_, val) => debouncedSearchText(val)}
                    onOpen={() => setHasInteracted(true)}
                    isOptionEqualToValue={(option, value) => option.code === value.code}
                    onChange={(_, newInputValue) => {
                        onChange(newInputValue);
                    }}
                    renderOption={(props, option) => (
                        <li {...props} key={option.name}>
                            {option.name}
                        </li>
                    )}
                    renderTags={(tagValue, getTagProps) => {
                        const reversed = [...tagValue].reverse();
                        const visible = showAll ? reversed : reversed.slice(0, 6);
                        const hiddenCount = reversed.length - visible.length;

                        return (
                        <Box sx={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 0.5 }}>
                            {visible.map(option => {
                            const originalIndex = tagValue.indexOf(option);
                            return (
                                
                            <Chip
                                key={option.code || option.name}
                                label={option.name ?? option}
                                {...getTagProps({ index: originalIndex })}
                            />
                            )})}

                            {!showAll && hiddenCount > 0 && (
                            <Chip
                                label={`+${hiddenCount} more`}
                                onClick={() => setShowAll(true)}
                                color='primary'
                                sx={{ cursor: "pointer" }}
                            />
                            )}

                            {showAll && tagValue.length > 6 && (
                            <Chip
                                label="Read less"
                                color='primary'
                                onClick={() => setShowAll(false)}
                                sx={{ cursor: "pointer" }}
                            />
                            )}
                        </Box>
                        );
                    }}
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            label={field.label}
                            error={!!error}
                            helperText={error ? error?.message : helperText}
                        />
                    )}
                />
            )}
            onChange={([event, data]) => data}
            name={field.name}
            control={control}
        />
    )
}