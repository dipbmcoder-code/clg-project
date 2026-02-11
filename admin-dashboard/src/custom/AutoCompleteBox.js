'use client';

import PropTypes from 'prop-types';
import isEqual from 'lodash/isEqual';
import debounce from 'lodash/debounce';
import { Controller } from 'react-hook-form';
import React, { useState, useEffect, useCallback } from 'react';

import { Chip, TextField, Autocomplete } from '@mui/material';

export default function AutoCompleteBox({ control, setValue, field, helperText, onField }) {
  const areEqual = (a, b) => isEqual(a, b);
  const [allOptions, setAllOptions] = useState(control._defaultValues[field.name]);
  const [hasInteracted, setHasInteracted] = useState(false);
  const [searchText, setSearchText] = useState('');

  const initialParent = field.parent?.fieldName ? control._getWatch(field.parent.fieldName) : false;

  const [parent, setParent] = useState(initialParent);

  useEffect(() => {
    if (!areEqual(initialParent, parent)) {
      setParent(initialParent);
      setValue(field.name, [], { shouldDirty: true });
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
        field: field.name,
        query: searchText,
        option: field.option,
        filters,
        relation: field.relation !== false,
      };
      if (field?.option_val) {
        params.option_val = field.option_val;
      }
      if (field?.populate) {
        params.populate = field.populate;
      }
      const data = await onField(params);
      setAllOptions(data);
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

  return (
    <Controller
      render={({ field: { onChange, value }, fieldState: { error } }) => (
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
      )}
      onChange={([event, data]) => data}
      name={field.name}
      control={control}
    />
  );
}
AutoCompleteBox.propTypes = {
  control: PropTypes.object.isRequired,
  setValue: PropTypes.func.isRequired,
  field: PropTypes.object.isRequired,
  onField: PropTypes.func.isRequired,
};
