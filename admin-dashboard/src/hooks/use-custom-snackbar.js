import Button from '@mui/material/Button';

import { useSnackbar } from 'src/components/snackbar';

const useCustomSnackbar = () => {
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  const getOptions = (variant) => ({
    variant: variant || 'info',
    anchorOrigin: { vertical: 'top', horizontal: 'right' },
  });
  const showSnackbar = (message, options) => {
    enqueueSnackbar(message, options);
  };

  const closeCustomSnackbar = (key) => {
    closeSnackbar(key);
  };

  const customSnackbarAction = (message, variant) => {
    const options = getOptions(variant);
    showSnackbar(message, {
      ...options,
      action: (key) => (
        <Button size="small" color="inherit" onClick={() => closeCustomSnackbar(key)}>
          Dismiss
        </Button>
      ),
    });
  };

  return { showSnackbar, closeCustomSnackbar, customSnackbarAction };
};

export default useCustomSnackbar;
