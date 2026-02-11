"use client";
// src/custom/FreeTextMultipleInput.js
import { Controller } from 'react-hook-form';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import Chip from '@mui/material/Chip';
import FormControl from '@mui/material/FormControl';
import { Box } from '@mui/material';
import { useCallback, useEffect, useState } from 'react';
import debounce from 'lodash/debounce';

// const { countries } = require('countries-list');
const world_countries = require('world-countries');
// const countries2to3 = require('countries-list/minimal/countries.2to3.min.json');

export default function FreeTextMultipleInput({ 
  control, 
  name, 
  label,
  options = [],
  helperText,
  field,
  limit = 6,
  placeholder = "Enter values separated by comma or press Enter",
  delimiter = ',' // Can be changed to space or other delimiter
}) {
  const [hasInteracted, setHasInteracted] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [showAll, setShowAll] = useState(false);
  // const allOptions = Object.keys(countries).map(key => { return { code: key, name: countries[key].name, code3: countries2to3[key] } });
  const allOptions = world_countries.default.map(key => { return { code: key.cca2, name: key.name.official, shortName: key.name.common, code3: key.cca3 } });
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
      name={name}
      control={control}
      render={({ field: { onChange, value }, fieldState: { error } }) => (
        <FormControl fullWidth>
          <Autocomplete
            multiple
            freeSolo
            options={field?.option_val == 'code' ? allOptions : options}
            filterSelectedOptions
            value={value || []}
            onOpen={() => setHasInteracted(true)}
            onChange={(_, newValue) => {
              const currentValue = field.selectType == 'single' ? Array.from(newValue).slice(-1) : newValue;
              onChange(currentValue);
            }}
            getOptionKey={(option) => option.id || option.code || option}
            getOptionLabel={(option) => option.name ?? option}
            onInputChange={(_, val) => debouncedSearchText(val)}
            isOptionEqualToValue={(option, value) => option.name === value.name}
            renderTags={(tagValue, getTagProps) => {
              const reversed = [...tagValue].reverse();
              const visible = showAll ? reversed : reversed.slice(0, limit);
              const hiddenCount = reversed.length - visible.length;

              return (
                <Box sx={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 0.5 }}>
                  {visible.map(option => {
                    const originalIndex = tagValue.indexOf(option);
                    const tagProps = getTagProps({ index: originalIndex });
                    const { key, ...chipProps } = tagProps;
                    return (
                      <Chip
                        key={key}
                        label={option.name ?? option}
                        {...chipProps}
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

                  {showAll && value.length > limit && (
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
                label={label}
                helperText={error ? error.message : helperText}
                error={!!error}
              />
            )}
          />
        </FormControl>
      )}
    />
  );
}