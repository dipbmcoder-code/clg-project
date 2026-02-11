'use client';

import { useState, useCallback } from 'react';

import { alpha } from '@mui/material/styles';
import { Box, Container, Typography } from '@mui/material';

import { paths } from 'src/routes/paths';
import { useRouter } from 'src/routes/hooks';

import { useCopyToClipboard } from 'src/hooks/use-copy-to-clipboard';

import { BackButton, FormComponent } from 'src/custom';

import { useSnackbar } from 'src/components/snackbar';
import { useSettingsContext } from 'src/components/settings';
/**
 * Renders a form for editing user information.
 * @param {Object} props - Component props.
 * @param {Object} props.data - Object containing the user's current information.
 * @param {Function} props.onCreate - Function to be called when the form is submitted.
 * @param {Function} props.onField - Function to handle changes in form fields.
 * @returns {JSX.Element} - Rendered component.
 */
function UserCreate({ onCreate, onField }) {
  const settings = useSettingsContext();
  const { enqueueSnackbar } = useSnackbar();
  const { copy } = useCopyToClipboard();
  const router = useRouter();
  const [value, setValue] = useState('set password url');

  const commonStyle = {
    xs: 12,
    sm: 6,
  };
  const onCopy = useCallback(
    (text) => {
      if (text) {
        enqueueSnackbar('Copied!');
        copy(text);
      }
    },
    [copy, enqueueSnackbar]
  );

  const handleChange = useCallback((event) => {
    setValue(event.target.value);
  }, []);
  const fields = [
    { name: 'firstname', type: 'string', label: 'First Name', rules: { required: true } },
    { name: 'lastname', type: 'string', label: 'Last Name', rules: { required: true } },
    { name: 'email', type: 'email', label: 'Email', rules: { required: true } },
    {
      name: 'roles',
      type: 'select',
      label: 'Roles',
      selectType: 'single',
      option: 'name',
      rules: { required: true },
    },
  ];

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Box
        sx={{
          display: { sm: 'flex' },
          gap: 2,
          alignItems: 'center',
        }}
      >
        <Typography variant="h4"> Create User</Typography>
      </Box>

      <Box
        sx={{
          mt: 3,
          width: 1,
          p: 3,
          borderRadius: 2,
          bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
          border: (theme) => `dashed 1px ${theme.palette.divider}`,
        }}
      >
        <Box component="div" pb={2}>
          <BackButton />
        </Box>

        {/* <Box component="div" pb={4}>
            <TextField
              disable="true"
              fullWidth
              variant="filled"
              value={value}
              label="Share this url with user"
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <Tooltip title="Copy">
                      <IconButton onClick={() => onCopy(value)}>
                        <Iconify icon="eva:copy-fill" width={24} />
                      </IconButton>
                    </Tooltip>
                  </InputAdornment>
                ),
              }}
            />
          </Box> */}
        <FormComponent
          fields={fields}
          action={onCreate}
          onField={onField}
          commonStyle={commonStyle}
          component="page"
          redirect={`${paths.admin_dashboard.root}/users/`}
        />
      </Box>
    </Container>
  );
}
export default UserCreate;
