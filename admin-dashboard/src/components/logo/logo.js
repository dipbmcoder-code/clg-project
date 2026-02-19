import PropTypes from 'prop-types';
import { forwardRef } from 'react';

import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import { useTheme } from '@mui/material/styles';

import { RouterLink } from 'src/routes/components';

// ----------------------------------------------------------------------

const Logo = forwardRef(({ disabledLink = false, isSmall = false, sx, ...other }, ref) => {
  const theme = useTheme();

  const PRIMARY_MAIN = theme.palette.primary.main;
  const PRIMARY_DARK = theme.palette.primary.dark;

  const logo = (
    <Box
      ref={ref}
      component="div"
      sx={{
        height: isSmall ? 40 : 48,
        display: 'inline-flex',
        alignItems: 'center',
        ...sx,
      }}
      {...other}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 240 48"
        width={isSmall ? 160 : 220}
        height={isSmall ? 36 : 48}
      >
        {/* AI icon */}
        <rect x="2" y="8" width="32" height="32" rx="8" fill={PRIMARY_MAIN} />
        <text x="18" y="30" textAnchor="middle" fill="white" fontSize="18" fontWeight="bold" fontFamily="Arial, sans-serif">AI</text>

        {/* Brand text */}
        <text y="32" fontSize="20" fontWeight="bold" fontFamily="Arial, sans-serif">
          <tspan x="40" fill={PRIMARY_DARK}>News</tspan>
          <tspan fill={PRIMARY_MAIN}> Gen</tspan>
        </text>
      </svg>
    </Box>
  );

  if (disabledLink) {
    return logo;
  }

  return (
    <Link component={RouterLink} href="/" sx={{ display: 'contents' }}>
      {logo}
    </Link>
  );
});

Logo.propTypes = {
  disabledLink: PropTypes.bool,
  isSmall: PropTypes.bool,
  sx: PropTypes.object,
};

export default Logo;
