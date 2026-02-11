import { Stack, Button } from '@mui/material';
import LoadingButton from '@mui/lab/LoadingButton';
import { DeleteIcon } from 'src/utils/icons';

export default function FormButtons({ deleteEntry, dialog, handleClose, isDirty, isSubmitting }) {
  return (
    <Stack direction="row" alignItems="center" justifyContent="end" gap={2} mt={2}>
      {deleteEntry && (
        <Button
          color="error"
          onClick={() => {
            dialog.onFalse();
            deleteEntry(dialog.value.id);
          }}
          startIcon={<DeleteIcon />}
          variant="outlined"
        >
          Delete
        </Button>
      )}
      <Button onClick={handleClose} variant="contained" color="error">
        Cancel
      </Button>

      <LoadingButton
        disabled={!isDirty}
        loading={isSubmitting}
        type="submit"
        variant="contained"
        color="primary"
      >
        Save
      </LoadingButton>
    </Stack>
  );
}