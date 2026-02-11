'use client';

import React, { useState } from 'react';
import { Autocomplete, TextField } from '@mui/material';

const CustomLeagueAutocomplete = ({
  options = [],
  value = null,
  onChange,
  onInputChange,
  label = "Select League",
  size = "small",
  fullWidth = true,
  maxOptions = 50,
  disableClearable = false,
  filterSelected = false,
  selectedValues = [],
  ...props
}) => {
  const [searchText, setSearchText] = useState('');
  const [hasInteracted, setHasInteracted] = useState(false);

  // Filter options based on search text and exclude already selected values if filterSelected is true
  const filteredOptions = options
    .filter(option => 
      filterSelected 
        ? !selectedValues.some(row => row.id === option.id)
        : true
    )
    .filter(option =>
      searchText
        ? option.name.toLowerCase().includes(searchText.toLowerCase())
        : true
    )
    .slice(0, maxOptions);

  const handleChange = (event, newValue) => {
    if (onChange) {
      onChange(newValue);
    }
    setHasInteracted(true);
  };

  const handleInputChange = (event, newInputValue) => {
    setSearchText(newInputValue);
    setHasInteracted(true);
    if (onInputChange) {
      onInputChange(newInputValue);
    }
  };

  return (
    <Autocomplete
      options={filteredOptions}
      getOptionLabel={(option) => option.name || ''}
      value={value}
      onChange={handleChange}
      onInputChange={handleInputChange}
      renderInput={(params) => (
        <TextField
          {...params}
          label={label}
          size={size}
          fullWidth={fullWidth}
        />
      )}
      isOptionEqualToValue={(option, value) => option.id === value?.id}
      disableClearable={disableClearable}
      clearOnEscape
      {...props}
    />
  );
};

export default CustomLeagueAutocomplete;