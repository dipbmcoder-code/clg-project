import { alpha } from '@mui/material/styles';

import { grey, primary } from '../palette';

// ----------------------------------------------------------------------

export function createPresets(preset) {
  const primaryColor = getPrimary(preset);

  const theme = {
    palette: {
      primary: primaryColor,
    },
    customShadows: {
      primary: `0 8px 16px 0 ${alpha(`${primaryColor?.main}`, 0.24)}`,
    },
  };

  return {
    ...theme,
  };
}

// ----------------------------------------------------------------------

const cyan = {
  lighter: '#CCF4FE',
  light: '#68CDF9',
  main: '#078DEE',
  dark: '#0351AB',
  darker: '#012972',
  contrastText: '#FFFFFF',
};

const purple = {
  lighter: '#EBD6FD',
  light: '#B985F4',
  main: '#7635dc',
  dark: '#431A9E',
  darker: '#200A69',
  contrastText: '#FFFFFF',
};

const blue = {
  lighter: '#D1E9FC',
  light: '#76B0F1',
  main: '#2065D1',
  dark: '#103996',
  darker: '#061B64',
  contrastText: '#FFFFFF',
};

const green = {
  lighter: '#C8FAD6',
  light: '#5BE49B',
  main: '#00A76F',
  dark: '#007867',
  darker: '#004B50',
  contrastText: '#FFFFFF',
};

const red = {
  lighter: '#FFE3D5',
  light: '#FFC1AC',
  main: '#FF3030',
  dark: '#B71833',
  darker: '#7A0930',
  contrastText: '#FFFFFF',
};
const spring = {
  lighter: '#a6b718',
  light: '#9aa712',
  main: '#96a600',
  dark: '#859100',
  darker: '#768000',
  contrastText: grey[800], // Assuming you have defined grey somewhere
};

export const presetOptions = [
  { name: 'default', value: primary.main },
  { name: 'spring', value: spring.main },
  { name: 'cyan', value: cyan.main },
  { name: 'purple', value: purple.main },
  { name: 'blue', value: blue.main },
  { name: 'green', value: green.main },
  { name: 'red', value: red.main },
];

export function getPrimary(preset) {
  return {
    default: primary,
    spring,
    cyan,
    purple,
    blue,
    green,
    red,
  }[preset];
}
