'use client';

import { useForm } from 'react-hook-form';
import { useState, useEffect } from 'react';

import LoadingButton from '@mui/lab/LoadingButton';
import {
  Alert,
  Button,
  Dialog,
  Switch,
  InputLabel,
  DialogTitle,
  FormControl,
  DialogActions,
  DialogContent,
  FormControlLabel,
} from '@mui/material';

import { SelectBox } from 'src/custom';

import FormProvider, { RHFTextField } from 'src/components/hook-form';
// ----------------------------------------------------------------------
export default function FormDialog({ dialog, fields, title, action, onField }) {
  const [errorMsg, setErrorMsg] = useState('');

  const methods = useForm({
    reValidateMode: 'onSubmit',
  });
  const fieldValues = fields.reduce((acc, field) => {
    if (field.type !== 'select') {
      acc[field.name] = dialog.value[field.name];
    }
    return acc;
  }, {});
  const {
    control,
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;
  useEffect(() => {
    reset({ ...fieldValues });
  }, [dialog]);

  const onSubmit = handleSubmit(async (formData) => {
    try {
      const res = await action(formData);
    } catch (error) {
      reset();
      setErrorMsg(error.message);
    }
  });
  const handleClose = () => {
    // reset();
    setErrorMsg('');
    dialog.onFalse();
  };
  const processData = (field) => {
    const { name, option } = field;
    const value = fieldValues[name];
    if (Array.isArray(value)) {
      return value.map((item) => ({
        label: item[option],
        value: item.id,
      }));
    } if (typeof value === 'object' && value !== null) {
      return [
        {
          label: value.make,
          value: value.id,
        },
      ];
    } 
      return false;
    
  };
  const renderForm = (
    <>
      <DialogContent>
        {fields.map((field, index) => {
          switch (field.type) {
            case 'number':
            case 'string':
              return (
                <FormControl key={index} sx={field.sx ? field.sx : { width: '100%' }}>
                  <RHFTextField
                    autoFocus={index === 0}
                    fullWidth
                    type={field.type === 'string' ? 'text' : 'number'}
                    margin="dense"
                    variant="outlined"
                    name={field.name}
                    label={field.label}
                  />
                </FormControl>
              );
            case 'select':
              return (
                <FormControl key={index} sx={field.sx ? field.sx : { width: '100%', my: 2 }}>
                  <InputLabel htmlFor={field.name}>{field.label}</InputLabel>
                  <SelectBox
                    id={fieldValues.id}
                    options={processData(field)}
                    field={field}
                    onField={onField}
                  />
                </FormControl>
              );
            case 'boolean':
              return (
                <FormControl key={index} sx={field.sx ? field.sx : { width: '50%' }}>
                  <FormControlLabel
                    control={
                      <Switch checked={data && data[field.name] ? data[field.name] : false} />
                    }
                    label={field.label}
                    sx={{ mt: 1 }}
                  />
                </FormControl>
              );
            default:
              return null;
          }
        })}
      </DialogContent>

      <DialogActions>
        <Button onClick={handleClose} variant="outlined" color="inherit">
          Cancel
        </Button>
        <LoadingButton loading={isSubmitting} type="submit" variant="contained" color="primary">
          Save
        </LoadingButton>
      </DialogActions>
    </>
  );
  return (
    <div>
      <Dialog open={!!dialog.value} onClose={handleClose}>
        <DialogTitle>{title}</DialogTitle>
        <FormProvider methods={methods} onSubmit={onSubmit}>
          {renderForm}
        </FormProvider>
        {!!errorMsg && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {errorMsg}
          </Alert>
        )}
      </Dialog>
    </div>
  );
}
