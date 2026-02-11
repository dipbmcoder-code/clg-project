'use client';

import { alpha } from '@mui/material/styles';
import { Box, Container, Typography } from '@mui/material';

import { paths } from 'src/routes/paths';

import { BackButton, FormComponent } from 'src/custom';

import { useSettingsContext } from 'src/components/settings';
/**
 * Renders a form for editing Leagus information.
 * @param {Object} props - Component props.
 * @param {Object} props.data - Object containing the Leagues's current information.
 * @param {Function} props.onCreate - Function to be called when the form is submitted.
 * @param {Function} props.onField - Function to handle changes in form fields.
 * @returns {JSX.Element} - Rendered component.
 */
function LeaguesCreate({ onCreate, onField }) {
  const settings = useSettingsContext();

  const commonStyle = {
    xs: 12,
    sm: 6,
  };

  const fields = [
    { name: 'league_id', type: 'string', label: 'League ID', rules: { required: true } },
    { name: 'league_name', type: 'string', label: 'League Name', rules: { required: true } },
    { name: 'league_type', type: 'string', label: 'League Type' },
    { name: 'league_logo_url', type: 'string', label: 'League Logo Url' },
  ];
  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Typography variant="h4">Create League</Typography>

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
          redirect={`${paths.admin_dashboard.root}/leagues/`}
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
export default LeaguesCreate;
