'use client';

import PropTypes from 'prop-types';
import isEqual from 'lodash/isEqual';
import debounce from 'lodash/debounce';
import { Controller } from 'react-hook-form';
import React, { useState, useEffect, useCallback } from 'react';

import { Chip, TextField, Autocomplete } from '@mui/material';

export default function AutoCompleteBox({ control, setValue, field, helperText, onField }) {
  const areEqual = (a, b) => isEqual(a, b);
  const safeDefault = Array.isArray(control?._defaultValues?.[field.name]) ? control._defaultValues[field.name] : [];
  const [allOptions, setAllOptions] = useState(safeDefault);
  const [hasInteracted, setHasInteracted] = useState(false);
  const [searchText, setSearchText] = useState('');

  const initialParent = field.parent?.fieldName && typeof control._getWatch === 'function' ? control._getWatch(field.parent.fieldName) : false;

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
      // onField may return either an array or an object like { results: [] }
      const opts = Array.isArray(data) ? data : data?.results ?? [];
      // normalize options to { label, value } shape to avoid MUI errors
      setAllOptions(Array.isArray(opts) ? opts.map(normalizeOption) : []);
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
      render={({ field: { onChange, value }, fieldState: { error } }) => {
        const normalizedValue = field.selectType === 'multiple'
          ? (Array.isArray(value) ? value.map(normalizeOption) : [])
          : (value ? normalizeOption(value) : null);

        return (
          <Autocomplete
          fullWidth
          clearOnEscape
          filterSelectedOptions
          multiple={field.selectType === 'multiple'}
          options={allOptions}
          value={normalizedValue}
          getOptionLabel={(option) => {
            if (Array.isArray(option)) return option.map(o => o.label ?? String(o)).join(', ');
            if (option == null) return '';
            return String(option.label ?? option.value ?? option.name ?? option);
          }}
          isOptionEqualToValue={(option, val) => {
            const optVal = option?.value ?? option?.code ?? option?.name ?? option;
            const valVal = val?.value ?? val?.code ?? val?.name ?? val;
            return String(optVal) === String(valVal);
          }}
          onChange={(event, d) => {
            let newValue;
            if (field.selectType === 'multiple') {
              newValue = Array.isArray(d) ? d.map(normalizeOption) : [];
            } else {
              const first = Array.isArray(d) ? d[0] ?? null : d ?? null;
              newValue = first ? normalizeOption(first) : null;
            }
            onChange(newValue);
          }}
          renderOption={(props, option) => (
            <li {...props} key={option.value ?? option.label}>
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
                key={option.value ?? option.label ?? index}
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

function normalizeOption(item) {
  if (item == null) return { label: '', value: '' };
  if (typeof item === 'string' || typeof item === 'number') {
    return { label: String(item), value: String(item) };
  }
  if (typeof item === 'object') {
    const label = item.label ?? item.name ?? item.label ?? String(item);
    const value = item.value ?? item.code ?? item.id ?? item.name ?? JSON.stringify(item);
    return { label: String(label), value: String(value) };
  }
  return { label: String(item), value: String(item) };
}
