import { useState } from 'react';
import PropTypes from 'prop-types';
import { Controller } from 'react-hook-form';

import { TextField, IconButton, InputAdornment } from '@mui/material';

import Iconify from 'src/components/iconify';

// ----------------------------------------------------------------------

export default function RHFPasswordField({ control, name, helperText, ...other }) {
  const [showPassword, setShowPassword] = useState(false);

  const handleTogglePassword = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <TextField
          {...field}
          fullWidth
          type={showPassword ? 'text' : 'password'}
          value={field.value ?? ''}
          onChange={(event) => field.onChange(event.target.value)}
          error={!!error}
          helperText={error ? error.message : helperText}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={handleTogglePassword} edge="end">
                  <Iconify icon={showPassword ? 'solar:eye-bold' : 'solar:eye-closed-bold'} />
                </IconButton>
              </InputAdornment>
            ),
          }}
          {...other}
        />
      )}
    />
  );
}

RHFPasswordField.propTypes = {
  control: PropTypes.object.isRequired,
  name: PropTypes.string.isRequired,
  helperText: PropTypes.string,
};
