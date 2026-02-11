import PropTypes from 'prop-types';
import { Controller } from 'react-hook-form';

import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider as MuiLocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
// ----------------------------------------------------------------------

export default function RHFDatePicker({ control, name, helperText, ...other }) {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <MuiLocalizationProvider dateAdapter={AdapterDateFns}>
          <DatePicker
            {...field}
            format="dd/MM/yyyy"
            value={field.value && new Date(field.value) ? new Date(field.value) : ''}
            slotProps={{
              textField: {
                fullWidth: true,
                error: !!error,
                helperText: error?.message,
              },
            }}
            {...other}
          />
        </MuiLocalizationProvider>
      )}
    />
  );
}

RHFDatePicker.propTypes = {
  control: PropTypes.object,
  helperText: PropTypes.string,
  name: PropTypes.string,
};
