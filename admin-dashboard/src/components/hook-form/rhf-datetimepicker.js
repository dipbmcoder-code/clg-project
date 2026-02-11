// import PropTypes from 'prop-types';
// import { Controller } from 'react-hook-form';
// import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
// import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
// import { LocalizationProvider as MuiLocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
// import { format, utcToZonedTime, zonedTimeToUtc } from 'date-fns-tz';

// // ----------------------------------------------------------------------

// export default function RHFDateTimePicker({ control, name, helperText, timezone = 'UTC', ...other }) {
//   return (
//     <Controller
//       name={name}
//       control={control}
//       render={({ field, fieldState: { error } }) => {
//         const fieldValue = field.value
//           ? utcToZonedTime(new Date(field.value), timezone) // Convert stored UTC → timezone
//           : null;

//         return (
//           <MuiLocalizationProvider dateAdapter={AdapterDateFns}>
//             <DateTimePicker
//               {...field}
//               value={fieldValue}
//               onChange={(newValue) => {
//                 // Convert selected timezone datetime → UTC before storing
//                 const utcDate = newValue ? zonedTimeToUtc(newValue, timezone) : null;
//                 field.onChange(utcDate ? utcDate.toISOString() : null);
//               }}
//               format="dd/MM/yyyy HH:mm"
//               slotProps={{
//                 textField: {
//                   fullWidth: true,
//                   error: !!error,
//                   helperText: error?.message || helperText,
//                 },
//               }}
//               {...other}
//             />
//           </MuiLocalizationProvider>
//         );
//       }}
//     />
//   );
// }

// RHFDateTimePicker.propTypes = {
//   control: PropTypes.object,
//   helperText: PropTypes.string,
//   name: PropTypes.string,
//   timezone: PropTypes.string, // e.g. "Asia/Kolkata", "America/New_York"
// };
import PropTypes from 'prop-types';
import { Controller } from 'react-hook-form';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider as MuiLocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

// ----------------------------------------------------------------------

export default function RHFDateTimePicker({ control, name, helperText, ...other }) {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => {
        const fieldValue = field.value ? new Date(field.value) : null;

        return (
          <MuiLocalizationProvider dateAdapter={AdapterDateFns}>
            <DateTimePicker
              {...field}
              value={fieldValue}
              // onChange={(newValue) => {
              //   // Always store in UTC ISO format
              //   // field.onChange(newValue ? newValue.toISOString() : null);
              //    if (newValue instanceof Date && !isNaN(newValue)) {
              //         // Valid date → store in UTC ISO format
              //         field.onChange(newValue.toISOString());
              //       } else {
              //         // Clear field if invalid
              //         field.onChange(null);
              //       }
              // }}
              format="dd/MM/yyyy HH:mm"
              slotProps={{
                textField: {
                  fullWidth: true,
                  error: !!error,
                  helperText: error?.message || helperText,
                },
              }}
              {...other}
            />
          </MuiLocalizationProvider>
        );
      }}
    />
  );
}

RHFDateTimePicker.propTypes = {
  control: PropTypes.object,
  helperText: PropTypes.string,
  name: PropTypes.string,
};
