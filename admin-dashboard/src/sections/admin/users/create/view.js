'use client';

import { alpha } from '@mui/material/styles';
import { Box, Container, Typography, Stack } from '@mui/material';

import { paths } from 'src/routes/paths';

import { BackButton, FormComponent } from 'src/custom';

import { useSettingsContext } from 'src/components/settings';

/**
 * Create user form with all required fields including password and roles.
 */
function UserCreate({ onCreate, onField }) {
  const settings = useSettingsContext();

  const commonStyle = {
    xs: 12,
    sm: 6,
  };

  const fields = [
    { name: 'firstname', type: 'string', label: 'First Name', rules: { required: true } },
    { name: 'lastname', type: 'string', label: 'Last Name', rules: { required: true } },
    { name: 'email', type: 'email', label: 'Email', rules: { required: true } },
    {
      name: 'password',
      type: 'password',
      label: 'Password',
      rules: {
        required: true,
        regex: [
          { name: 'min8', value: /.{8,}/, message: 'Password requires min 8 characters' },
          { name: 'uppercase', value: /[A-Z]/, message: 'Must contain at least one uppercase letter' },
          { name: 'number', value: /\d/, message: 'Must contain at least one number' },
        ],
      },
    },
    {
      name: 'roles',
      type: 'select',
      label: 'Role',
      selectType: 'single',
      option: 'name',
      option_val: 'name',
      rules: { required: true },
    },
  ];

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Stack spacing={3}>
        <Typography variant="h4">Create User</Typography>

        <Box
          sx={{
            p: { xs: 2, sm: 3 },
            borderRadius: 2,
            bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
            border: (theme) => `dashed 1px ${theme.palette.divider}`,
          }}
        >
          <Box component="div" pb={2}>
            <BackButton />
          </Box>
          <FormComponent
            redirect={`${paths.admin_dashboard.root}/users/`}
            key={Date.now()}
            fields={fields}
            action={onCreate}
            onField={onField}
            commonStyle={commonStyle}
            component="page"
          />
        </Box>
      </Stack>
    </Container>
  );
}
export default UserCreate;
