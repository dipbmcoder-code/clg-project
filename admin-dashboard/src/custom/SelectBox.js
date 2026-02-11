'use client';

import { debounce } from 'lodash';
import React, { useState, useEffect } from 'react';

import { Box, Chip, Select, styled, MenuItem, TextField, ListSubheader } from '@mui/material';

const CustomScrollbar = styled('div')({
  '&::-webkit-scrollbar': {
    width: '8px',
  },
  '&::-webkit-scrollbar-track': {
    background: '#f1f1f1',
  },
  '&::-webkit-scrollbar-thumb': {
    background: '#888',
    borderRadius: '4px',
  },
  '&::-webkit-scrollbar-thumb:hover': {
    background: '#555',
  },
});
export default function SelectBox({ id, options, field, onField, action, props }) {
  const [selectedOption, setSelectedOption] = useState(
    field.selectType === 'multiple'
      ? !options
        ? []
        : options.map((option) => option.value)
      : !options
        ? ''
        : options[0].value
  );
  const [allOptions, setAllOptions] = useState(!options ? [] : options);
  const [hasInteracted, setHasInteracted] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [fieldValues, setFieldValues] = useState(false);

  const handleMultiChange = debounce((fieldName, value) => {
    setFieldValues((prevFieldValues) => ({
      ...prevFieldValues,
      [fieldName]: value,
    }));
  }, 700);
  const fetchOptions = async () => {
    try {
      const params = {
        field: field.name,
        query: searchText,
        option: field.option,
        relation: field.relation,
      };
      if (fieldValues) {
        const filters = {
          $and: Object.entries(fieldValues).map(([key, value]) => {
            const keys = key.split('.');
            let nestedFilter = { $contains: value };

            for (let i = keys.length - 1; i >= 0; i--) {
              nestedFilter = { [keys[i]]: nestedFilter };
            }

            return nestedFilter;
          }),
        };

        params.filters = filters;
      }

      if (field.populate) {
        params.populate = field.populate;
      }
      const data = await onField(params);
      const newData = data.filter(
        (newOption) =>
          !(Array.isArray(selectedOption)
            ? selectedOption.includes(newOption.value)
            : selectedOption === newOption.value)
      );

      let prevOptions;
      if (Array.isArray(selectedOption)) {
        prevOptions = selectedOption.map((val) =>
          allOptions.find((option) => option.value === val)
        );
      } else {
        const option = allOptions.find((option) => option.value === selectedOption);
        if (option) {
          prevOptions = [option];
        } else {
          prevOptions = []; // or handle the case as appropriate
        }
      }
      setAllOptions([...prevOptions, ...newData]);
    } catch (error) {
      console.error('Failed to fetch options', error);
    }
  };

  useEffect(() => {
    if (!hasInteracted && !action) return;
    fetchOptions();
  }, [hasInteracted, searchText, fieldValues]);

  const handleChange = async (event) => {
    const { value } = event.target;
    if (field.selectType === 'multiple') {
      setSelectedOption(typeof value === 'string' ? value.split(',') : value);
    } else {
      setSelectedOption(selectedOption === value ? '' : value);
    }
    if (action) {
      await action(value);
    }
  };
  const handleSearch = debounce((e) => {
    setSearchText(e.target.value);
  }, 700);
  return (
    <Select
      {...props}
      multiple={field.selectType === 'multiple'}
      name={field.name}
      MenuProps={{
        autoFocus: false,
        PaperProps: {
          component: CustomScrollbar,
          sx: {
            maxHeight: 500,
          },
        },
      }}
      value={selectedOption}
      onChange={handleChange}
      onClose={() => setSearchText('')}
      onOpen={() => setHasInteracted(true)}
      renderValue={(selected) => {
        if (field.selectType === 'multiple') {
          return (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => {
                const optionLabel = allOptions.find((option) => option.value === value).label;
                return <Chip key={value} label={optionLabel} />;
              })}
            </Box>
          );
        }
        return allOptions.find((option) => option.value === selected).label;
      }}
    >
      <ListSubheader sx={{ display: 'flex', gap: 2, my: 2 }}>
        {Array.isArray(field.option) ? (
          <>
            {field.option.map((option, index) => (
              <TextField
                size="small"
                autoFocus
                placeholder={option.value}
                fullWidth
                InputProps={{ startAdornment: <></> }}
                onChange={(e) => handleMultiChange(option.key, e.target.value)}
                onKeyDown={(e) => {
                  if (e.key !== 'Escape') {
                    e.stopPropagation();
                  }
                }}
              />
            ))}
          </>
        ) : (
          <TextField
            size="small"
            autoFocus
            placeholder="Type to search..."
            fullWidth
            InputProps={{ startAdornment: <></> }}
            onChange={handleSearch}
            onKeyDown={(e) => {
              if (e.key !== 'Escape') {
                e.stopPropagation();
              }
            }}
          />
        )}
      </ListSubheader>
      {allOptions.map((option, i) => (
        <MenuItem key={i} value={option.value}>
          {option.label}
        </MenuItem>
      ))}
    </Select>
  );
}
