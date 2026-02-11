'use client';

import * as React from 'react';
import { Autocomplete, TextField } from '@mui/material';
import { useFormContext, Controller } from 'react-hook-form';
import { createFilterOptions } from '@mui/material/Autocomplete';

const filter = createFilterOptions();

const RHFCustomLeagueAutocomplete = ({
  name,
  options = [],
  label = "Select League",
  size = "medium",
  fullWidth = true,
  ...props
}) => {
  const { control, watch } = useFormContext();
  const value = watch(name);
  const getOptionFromValue = (val) => {
    if (!val) return null;

    // Handle array values - take the first item if it's an array
    if (Array.isArray(val)) {
      if (val.length === 0) return null;
      val = val[0]; // Take the first item from the array
    }

    // If value is already in the options format
    if (typeof val === 'object' && val !== null) {
      // Try to find matching option from the list using id (convert string id to number if needed)
      const foundOption = options.find(option =>
        option.id?.toString() === val.id?.toString() ||
        option.value?.toString() === val.value?.toString()
      );
      return foundOption || val;
    }

    // If value is a string (from free text input)
    if (typeof val === 'string') {
      return {
        id: 0,
        value: "0",
        name: val,
        label: val,
        isNew: true
      };
    }

    return null;
  };

  const selectedOption = getOptionFromValue(value);
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <Autocomplete
          value={selectedOption}
          freeSolo
          options={options}
          getOptionKey={(option) => option.id}
          filterOptions={(options, params) => {
            const filtered = filter(options, params);
            return filtered;
          }}
          getOptionLabel={(option) => {
            if (typeof option === 'string') {
              return option;
            }
            if (option.inputValue) {

              return option.inputValue;
            }
            return `${option.country !== 'World' ? option.country + ' - ' : ''}${option.label || option.name || option.title || ''}`;
          }}
          onChange={(event, newValue) => {
            if (typeof newValue === 'string') {
              field.onChange({
                id: 0,
                value: "0",
                name: newValue,
                label: newValue,
                isNew: true
              });
            } else if (newValue && newValue.inputValue) {
              field.onChange({
                id: 0,
                value: "0",
                name: newValue.inputValue,
                label: newValue.inputValue,
                isNew: true
              });
            } else {
              field.onChange(newValue);
            }
          }}
          renderOption={(props, option) => {
            const { key, ...optionProps } = props;
            return (
              <li key={key} {...optionProps}>
                {option.country !== 'World' ? option.country + ' - ' : ''}{option.title || option.label || option.name}
              </li>
            );
          }}
          renderInput={(params) => (
            <TextField
              {...params}
              label={label}
              size={size}
              fullWidth={fullWidth}
              error={!!error}
              helperText={error?.message}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                }
              }}
            />
          )}
          isOptionEqualToValue={(option, value) => {
            if (!option || !value) return false;
            if (typeof option === 'string' || typeof value === 'string') {
              return option === value;
            }
            // Compare using both id and value properties
            return option.id?.toString() === value.id?.toString() ||
              option.value?.toString() === value.value?.toString();
          }}
          selectOnFocus
          clearOnBlur
          handleHomeEndKeys
          {...props}
        />
      )}
    />
  );
};

export default RHFCustomLeagueAutocomplete;

