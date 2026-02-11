'use client';

import { m } from 'framer-motion';

import Box from '@mui/material/Box';
import { alpha } from '@mui/material/styles';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';

import { useAuthContext } from 'src/auth/hooks';

import { useSettingsContext } from 'src/components/settings';
import { varBounce, MotionContainer } from 'src/components/animate';
// ----------------------------------------------------------------------

export default function OneView() {
  const settings = useSettingsContext();
  const { user } = useAuthContext();

  return (
    <Container maxWidth={settings.themeStretch ? false : 'xl'}>
      <Typography variant="h4">Dashboard </Typography>

      <Box
        sx={{
          mt: 5,
          width: 1,
          height: 320,
          borderRadius: 2,

          bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
          border: (theme) => `dashed 1px ${theme.palette.divider}`,
        }}
      >
        <Container
          component={MotionContainer}
          sx={{
            textAlign: 'center',
            justifyContent: 'center',
            alignItems: 'center',
            display: 'flex',
            flexDirection: 'column',
            height: '100%',
          }}
        >
          <Typography variant="h3" sx={{ textAlign: 'center' }}>
            Welcome
          </Typography>
          <m.div variants={varBounce().in}>
            <Typography
              variant="h1"
              sx={{
                color: (theme) => theme.palette.primary.main,
                fontWeight: 'bold',
                lineHeight: 1.2,
              }}
            >
              {user?.firstname} {user?.lastname}
            </Typography>
          </m.div>
        </Container>
      </Box>
    </Container>
  );
}
