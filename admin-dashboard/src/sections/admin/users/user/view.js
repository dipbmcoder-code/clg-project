'use client';

import { alpha } from '@mui/material/styles';
import { Box, Container, Typography, Stack } from '@mui/material';

import { BackButton, FormComponent } from 'src/custom';

import { useSettingsContext } from 'src/components/settings';

/**
 * Edit user form with all fields including password change and role selection.
 */
function User({ data, onEdit, onField, slug }) {
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
      label: 'New Password',
      helperText: 'Leave blank to keep current password',
      rules: {
        regex: [
          { name: 'min8', value: /.{8,}/, message: 'Password requires min 8 characters' },
          { name: 'uppercase', value: /[A-Z]/, message: 'Must contain at least one uppercase letter' },
          { name: 'number', value: /\d/, message: 'Must contain at least one number' },
        ],
      },
    },
    {
      name: 'confirm_password',
      type: 'password',
      label: 'Confirm Password',
      rules: {
        depend: {
          fieldName: 'password',
          match: { message: 'Passwords do not match' },
        },
      },
    },
    { name: 'isActive', type: 'boolean', label: 'Active' },
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

  const { firstname, lastname } = data;

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Stack spacing={3}>
        {firstname && lastname && (
          <Typography variant="h4">
            User / {firstname} {lastname}
          </Typography>
        )}

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
            key={Date.now()}
            dialog={{ value: data }}
            refresh={false}
            fields={fields}
            action={onEdit}
            onField={onField}
            commonStyle={commonStyle}
            component="page"
            slug={slug}
          />
        </Box>
      </Stack>
    </Container>
  );
}
export default User;
