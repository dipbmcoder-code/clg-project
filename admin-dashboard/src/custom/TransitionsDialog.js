'use client';

import { useState, forwardRef } from 'react';

import Alert from '@mui/lab/Alert';
import Slide from '@mui/material/Slide';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import LoadingButton from '@mui/lab/LoadingButton';
import DialogTitle from '@mui/material/DialogTitle';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';

// ----------------------------------------------------------------------

const Transition = forwardRef((props, ref) => <Slide direction="up" ref={ref} {...props} />);

export default function TransitionsDialog({
  dialog,
  title,
  content,
  action,
  refresh,
  callback,
  buttonText,
  props,
}) {
  const [errorMsg, setErrorMsg] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const res = await action(dialog.value);
      if (!res.error) {
        refresh();
        if (callback) {
          callback();
        }
        handleClose();
      } else {
        setErrorMsg('Something went wrong');
      }
      handleClose();
    } catch (error) {
      setErrorMsg('Something went wrong');
      console.log(error);
    }
    setIsSubmitting(false);
  };
  const handleClose = async () => {
    setIsSubmitting(false);
    setErrorMsg('');
    dialog.onFalse();
  };
  return (
    <div>
      <Dialog
        keepMounted
        open={!!dialog.value}
        TransitionComponent={Transition}
        onClose={handleClose}
      >
        <DialogTitle>{title}</DialogTitle>

        <DialogContent sx={{ color: 'text.secondary' }}>{content}</DialogContent>

        <DialogActions>
          <Button variant="outlined" onClick={handleClose}>
            Cancel
          </Button>
          <LoadingButton
            loading={isSubmitting}
            onClick={handleSubmit}
            type="submit"
            variant="soft"
            color="primary"
            {...props}
          >
            {buttonText}
          </LoadingButton>
        </DialogActions>
        {!!errorMsg && (
          <Alert
            auto
            severity="error"
            onClose={() => {
              setErrorMsg('');
            }}
          >
            {errorMsg}
          </Alert>
        )}
      </Dialog>
    </div>
  );
}
