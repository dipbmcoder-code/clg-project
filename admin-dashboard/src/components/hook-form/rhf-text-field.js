import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import { Controller } from 'react-hook-form';

import TextField from '@mui/material/TextField';

// ----------------------------------------------------------------------

export default function RHFTextField({ depend, control, name, helperText, type, ...other }) {
  const [adornment, setAdornment] = useState({
    prefix: false,
    suffix: false,
  });

  if (depend) {
    const dependField = control._getWatch(depend.fieldName);

    useEffect(() => {
      const conditionMatch = depend.conditions.find((condition) => condition.value === dependField);
      setAdornment({
        prefix: conditionMatch?.prefix || false,
        suffix: conditionMatch?.suffix || false,
      });
    }, [dependField]);
  }
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <TextField
          {...field}
          fullWidth
          type={type}
          value={field.value === null || field.value === undefined ? '' : (type == 'number' && !field.value?0:field.value)}
          error={!!error}
          helperText={error ? error?.message : helperText}
          InputProps={{
            startAdornment: <>{!!adornment.prefix && adornment.prefix}</>,
            endAdornment: <>{!!adornment.suffix && adornment.suffix}</>,
          }}
          {...other}
        />
      )}
    />
  );
}

RHFTextField.propTypes = {
  helperText: PropTypes.object,
  name: PropTypes.string,
  type: PropTypes.string,
};
