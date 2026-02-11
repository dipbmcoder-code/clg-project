'use client';

import { useMemo } from 'react';
import { alpha } from '@mui/material/styles';
import { Box, Container, Typography, Button } from '@mui/material';
import { useSettingsContext } from 'src/components/settings';
import { useRouter } from 'src/routes/hooks';
import { BackButton, FormComponent } from 'src/custom';
/**
 * Renders a form for editing league information.
 * @param {Object} props - Component props.
 * @param {Object} props.data - Object containing the league's current information.
 * @param {Function} props.onEdit - Function to be called when the form is submitted.
 * @param {Function} props.onField - Function to handle changes in form fields.
 * @returns {JSX.Element} - Rendered component.
 */

function League({
  data,
  onEdit,
  onField,
  slug
}) {
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
      <Typography variant="h6" marginTop={2}>
        Leage Management
      </Typography>
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
export default League;
