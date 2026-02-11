'use client';

import PropTypes from 'prop-types';
import { Controller } from 'react-hook-form';
import { Chip, TextField, Autocomplete } from '@mui/material';

export default function CustomAutoCompleteBox({ control, field, helperText, options = [], disabled=false }) {
  return (
    <Controller
      render={({ field: { onChange, value }, fieldState: { error } }) => {
        // Handle the case where value is an array in single selection mode
        const normalizedValue = field.selectType === 'multiple' 
          ? value || [] 
          : Array.isArray(value) 
            ? value.length > 0 ? value[0] : null // Take first element if array, otherwise null
            : value;

        return (
          <Autocomplete
            fullWidth
            clearOnEscape
            filterSelectedOptions
            disabled={disabled}
            disableCloseOnSelect={field.selectType === 'multiple'}
            multiple={field.selectType === 'multiple'}
            options={options}
            value={normalizedValue}
            getOptionLabel={(option) => {
              if (!option) return '';
              if (typeof option === 'object') {
                return option.label || option.name || String(option.value) || '';
              }
              return String(option);
            }}
            isOptionEqualToValue={(option, value) => {
              // Handle null/undefined values
              if (!option || !value) return option === value;
              
              // Handle object comparison
              if (typeof option === 'object' && typeof value === 'object') {
                return option.value === value.value;
              }
              
              // Handle primitive comparison
              return option === value;
            }}
            onChange={(event, newValue) => {
              onChange(newValue);
            }}
            renderOption={(props, option) => (
              <li {...props} key={option.value}>
                {option.label || option.name || String(option.value)}
              </li>
            )}
            renderTags={(selectedOption, getTagProps) =>
              selectedOption.map((option, index) => (
                <Chip
                  {...getTagProps({ index })}
                  size="small"
                  variant="soft"
                  label={option.label || option.name || String(option.value)}
                  key={option.value || index}
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
        );
      }}
      name={field.name}
      control={control}
      defaultValue={field.selectType === 'multiple' ? [] : null}
    />
  );
}

CustomAutoCompleteBox.propTypes = {
  control: PropTypes.object.isRequired,
  field: PropTypes.object.isRequired,
  options: PropTypes.array,
  helperText: PropTypes.string,
};