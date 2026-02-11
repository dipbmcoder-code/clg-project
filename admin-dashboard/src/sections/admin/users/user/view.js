'use client';

import { alpha } from '@mui/material/styles';
import { Box, Container, Typography } from '@mui/material';

import { useRouter } from 'src/routes/hooks';

import { BackButton, FormComponent } from 'src/custom';

import { useSettingsContext } from 'src/components/settings';
/**
 * Renders a form for editing league information.
 * @param {Object} props - Component props.
 * @param {Object} props.data - Object containing the league's current information.
 * @param {Function} props.onEdit - Function to be called when the form is submitted.
 * @param {Function} props.onField - Function to handle changes in form fields.
 * @returns {JSX.Element} - Rendered component.
 */
function User({ data, onEdit, onField, slug }) {
  const settings = useSettingsContext();
  const router = useRouter();

  const commonStyle = {
    xs: 12,
    sm: 6,
  };

  const fields = [
    { name: 'firstname', type: 'string', label: 'First Name', rules: { required: true } },
    { name: 'lastname', type: 'string', label: 'Last Name', rules: { required: true } },
    { name: 'email', type: 'email', label: 'Email', rules: { required: true } },
    { name: 'username', type: 'string', label: 'Username' },
    {
      name: 'password',
      type: 'password',
      label: 'Password',
      helperText: 'asdas',
      rules: {
        regex: [
          { name: 'min8', value: /.{8,}/, message: 'Password requires min 8 letters' },
          {
            name: 'uppercase',
            value: /[A-Z]/,
            message: 'Password must contain at least one uppercase letter',
          },
          {
            name: 'number',
            value: /\d/,
            message: 'Password must contain at least one number',
          },
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
          match: {
            message: 'Passwords do not match',
          },
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
      rules: { required: true },
    },
  ];

  const { firstname, lastname, email } = data;
  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      {firstname && lastname && (
        <Box
          sx={{
            display: { sm: 'flex' },
            gap: 2,
            alignItems: 'center',
          }}
        >
          <Typography variant="h4">
            User / {firstname} {lastname}
          </Typography>
        </Box>
      )}

      <Box
        sx={{
          mt: 3,
          width: 1,
          p: { xs: 1, sm: 3 },
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
    </Container>
  );
}
export default User;
