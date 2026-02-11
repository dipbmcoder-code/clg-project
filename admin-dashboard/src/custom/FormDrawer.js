'use client';

import { Stack, Drawer, Typography } from '@mui/material';

import Scrollbar from 'src/components/scrollbar';

import FormComponent from './FormComponent';

export default function FormDrawer({
  dialog,
  refresh,
  fields,
  title,
  action,
  onField,
  custom_data,
  ignoreDirty,
}) {
  if (!dialog.value) {
    return null;
  }

  return (
    <div>
      <Drawer
        open
        onClose={() => dialog.onFalse()}
        slotProps={{
          backdrop: { invisible: false },
        }}
        anchor="right"
        PaperProps={{
          sx: {
            width: 320,
          },
        }}
      >
        <Scrollbar sx={{ height: 1 }}>
          <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ p: 2.5 }}>
            <Typography variant="h6"> {title} </Typography>
          </Stack>
          <Stack
            spacing={2.5}
            justifyContent="center"
            sx={{
              p: 2.5,
              bgcolor: 'background.neutral',
            }}
          >
            <FormComponent
              custom_data={!!custom_data}
              ignoreDirty={!!ignoreDirty}
              dialog={dialog}
              refresh={refresh}
              fields={fields}
              action={action}
              onField={onField}
            />
          </Stack>
        </Scrollbar>
      </Drawer>
    </div>
  );
}
