'use client';

import { alpha } from '@mui/material/styles';
import { Box, Container, Typography } from '@mui/material';

import { paths } from 'src/routes/paths';

import { BackButton, FormComponent } from 'src/custom';

import { useSettingsContext } from 'src/components/settings';
/**
 * Renders a form for editing Leagus information.
 * @param {Object} props - Component props.
 * @param {Object} props.data - Object containing the Website's current information.
 * @param {Function} props.onCreate - Function to be called when the form is submitted.
 * @param {Function} props.onField - Function to handle changes in form fields.
 * @returns {JSX.Element} - Rendered component.
 */
function WebsitesCreate({ onCreate, onField }) {
  const settings = useSettingsContext();

  const commonStyle = {
    xs: 12,
    sm: 6,
  };
  const fields = [
    { name: 'platform_name', type: 'string', label: 'Website Name', rules: { required: true } },
    { name: 'platform_url', type: 'string', label: 'Website Url', rules: { required: true } },
    { name: 'platform_user', type: 'string', label: 'Admin User', rules: { required: true } },
    { name: 'platform_password', type: 'password', label: 'Admin Password', rules: { required: true } },
    // {
    //       name: 'platform_countries',
    //       type: 'select_country',
    //       label: 'Countries',
    //       selectType: 'multiple',
    //       option: 'name',
    //       rules: { required: true },
    //     },
    // { name: 'openai_prompt', type: 'string', multiline: true, label: 'OpenAI Prompt' },
  ];
  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Typography variant="h4">Create Website</Typography>

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
        <FormComponent
          redirect={`${paths.admin_dashboard.root}/websites/`}
          key={Date.now()}
          fields={fields}
          action={onCreate}
          onField={onField}
          commonStyle={commonStyle}
          component="page"
          saveAtTop={true}
          headerComponent={<BackButton />}
        />
      </Box>
    </Container>
  );
}
export default WebsitesCreate;
