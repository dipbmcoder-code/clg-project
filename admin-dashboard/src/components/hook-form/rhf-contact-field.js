import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import { Controller } from 'react-hook-form';
import { MuiTelInput } from 'mui-tel-input'


// ----------------------------------------------------------------------

export default function RHFContactField({ control, name, helperText, type, ...other }) {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <MuiTelInput
          {...field}
          name={field.name}
          label={field.label}
          defaultCountry="IN"
         
          error={!!error}
          helperText={error ? error?.message : helperText}
          {...other}
        />
      )}
    />
  );
}

RHFContactField.propTypes = {
  helperText: PropTypes.object,
  name: PropTypes.string,
  type: PropTypes.string,
};
