'use client';

import * as Yup from 'yup';
import { useCallback } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import LoadingButton from '@mui/lab/LoadingButton';
import {
  Grid,
  Stack,
  Button,
  MenuItem,
  Skeleton,
  TextField,
  Typography,
  FormControl,
} from '@mui/material';

import { useRouter } from 'src/routes/hooks';

import useCustomSnackbar from 'src/hooks/use-custom-snackbar';

import { findUsers } from 'src/utils/commonActions';

import { AutoCompleteBox, AutoSelectCountry, UsersAutoComplete } from 'src/custom';

import FormProvider, {
  RHFUpload,
  RHFSelect,
  RHFSwitch,
  RHFTextField,
  RHFDatePicker,
  RHFPasswordField,
  RHFContactField
} from 'src/components/hook-form';

export default function FormComponent({
  dialog,
  refresh,
  fields,
  action,
  onField,
  commonStyle,
  component,
  custom_data,
  redirect,
  ignoreDirty,
  slug
}) {
  const { customSnackbarAction } = useCustomSnackbar();

  const router = useRouter();
  const processData = (field) => {
    const { name, option, option_val, fieldValue } = field;
    if (fieldValue) {
      return fieldValue;
    }
    const value = dialog && dialog.value[name] ? dialog.value[name] : [];
    if (Array.isArray(value)) {
      return value.map((item) => ({
        label: item[option],
        value: item[option_val] || item.id,
      }));
    }
    if (typeof value === 'object' && value !== null) {
      return [
        {
          label: value[option],
          value: value[option_val] || value.id,
        },
      ];
    }
    return [];
  };
  const processUsers = async (field) => {
    const { name, option, option_val, fieldValue } = field;
    if (fieldValue) {
      return fieldValue;
    }
    const value = dialog && dialog.value[name] ? dialog.value[name] : null;

    if (Array.isArray(value) && value.length) {
      const ids = value.map((item) => item.id);
      const res = await findUsers({ ids });
      if (res.results) {
        return await res.results.map((item) => ({
          label: item[option],
          value: item[option_val] || item.id,
          ...item,
        }));
      }
    } else if (!Array.isArray(value) && typeof value === 'object' && value !== null) {
      const res = await findUsers({ ids: [value.id] });
      if (res.results) {
        return await res.results.map((item) => ({
          label: item[option],
          value: item[option_val] || item.id,
          ...item,
        }));
      }
    }
    return [];
  };
  const validationRules = fields.reduce((acc, { rules, type, name, label, multiple }) => {
    const requiredMessage = label ? `${label} is required` : 'This field is required';
    const validMessage = `Please enter valid ${label}`;

    if (rules && (rules.required || rules.regex || rules.depend)) {
      switch (type) {
        case 'email':
          acc[name] = Yup.string()
            .required(requiredMessage)
            .email('Email must be a valid email address');
          break;
        case 'select':
        case 'select_country':
          acc[name] = Yup.array()
            .min(1, `Please select ${label}`)
            .required(`Please select ${label}`);
          break;
        case 'file':
          if (multiple) {
            acc[name] =
              multiple && Number.isInteger(multiple)
                ? Yup.array()
                    .max(multiple, `Max ${multiple} ${label} is allowed`)
                    .min(1, requiredMessage)
                : Yup.array().min(1, requiredMessage);
          } else {
            acc[name] = Yup.mixed().nullable().required(requiredMessage);
          }
          break;
        default:
          if (rules && rules.depend) {
            const { fieldName, conditions, match } = rules.depend;
            if (match) {
              acc[name] = Yup.string().oneOf(
                [Yup.ref(fieldName)],
                match?.message || `${fieldName} do not match`
              );
            } else if (conditions) {
              acc[name] = Yup.string().when(fieldName, (value, schema) => {
                const condition = conditions.find((c) => c.value === value[0]);
                if (condition) {
                  return schema.test('regex', condition.message || validMessage, (value) =>
                    rules.required
                      ? condition.regex.test(value)
                      : value == null || value === '' || condition.regex.test(value)
                  );
                }
                return schema;
              });
            }
          } else {
            let schema = Yup.string();
            if (rules.regex && Array.isArray(rules.regex)) {
              rules.regex.forEach(({ name, value, message }) => {
                schema = schema.test(
                  name,
                  message,
                  (val) => val == null || val === '' || value.test(val)
                );
              });
            } else if (rules.regex) {
              schema = schema.test(
                rules.regex.name,
                rules.regex.message,
                (val) => val == null || val === '' || rules.regex.test(val)
              );
            }

            if (rules.required) {
              schema = schema.required(rules.required.message || requiredMessage);
            }

            acc[name] = schema;
          }

          break;
      }
    }

    return acc;
  }, {});

  const validationSchema = Yup.object().shape(validationRules);
  const fieldTypes = {
    ...fields.reduce((acc, field) => {
      acc[field.name] = field.type;
      return acc;
    }, {}),
  };
  async function getDefaultFieldValue(field, dialog) {
    switch (field.type) {
      case 'select':
        return processData(field);
      case 'select_user':
        return await processUsers(field);
      case 'file':
        if (field?.multiple) {
          return dialog && dialog.value[field.name] ? dialog.value[field.name] : [];
        }
        return dialog && dialog.value[field.name] ? dialog.value[field.name] : null;

      default:
        return dialog && dialog.value[field.name] ? dialog.value[field.name] : '';
    }
  }
  const methods = useForm(
    {
      resolver: yupResolver(validationSchema),
      defaultValues: async () => {
        const defaultValuesObj = await fields.reduce(async (accPromise, field) => {
          const acc = await accPromise; // Wait for the accumulator promise to resolve
          if (field.name) {
            acc[field.name] = await getDefaultFieldValue(field, dialog); // Wait for getDefaultFieldValue promise to resolve
          }
          return acc;
        }, Promise.resolve({}));

        return defaultValuesObj;
      },
    },
    []
  );

  const {
    control,
    setValue,
    watch,
    reset,
    handleSubmit,
    formState: { isLoading, isDirty, isSubmitting, dirtyFields, defaultValues, isSubmitSuccessful },
  } = methods;

  const values = watch();

  const onSubmit = handleSubmit(async (formData) => {
  
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));

      const formDataToSend = new FormData();

      if (ignoreDirty || isDirty || custom_data) {
        const editFields = custom_data || ignoreDirty ? values : dirtyFields;
        const updatedData = new Object();
        if (dialog && dialog.value.documentId) {
          updatedData.id = dialog.value.documentId;
        }
        for (const fieldName in editFields) {
          if (formData.hasOwnProperty(fieldName)) {
            const fieldValue = formData[fieldName];
            const defaultValue = defaultValues[fieldName];
            if (fieldTypes[fieldName] === 'file') {
              if (!updatedData._files) {
                updatedData._files = {};
              }
              if (Array.isArray(fieldValue) && Array.isArray(defaultValue)) {
                const newFiles = fieldValue.filter((item) => item.preview);
                const oldFiles = fieldValue.filter((item) => !item.preview);
                const removedFiles = defaultValue
                  .filter(
                    (defaultItem) =>
                      !fieldValue.some((fieldItem) => fieldItem.id === defaultItem.id)
                  )
                  .map((removedItem) => removedItem.id);

                updatedData[fieldName] = oldFiles;
                updatedData._files[fieldName] = removedFiles;
                newFiles.forEach((file) => formDataToSend.append(fieldName, file));
              } else {
                updatedData._files[fieldName] = defaultValue ? [defaultValue.id] : [];
                formDataToSend.append(fieldName, fieldValue);
                updatedData[fieldName] = null;
              }
            } else if (Array.isArray(fieldValue) && Array.isArray(defaultValue)) {
              if (custom_data) {
                updatedData[fieldName] = fieldValue.map((obj) => obj.value).join(',');
              } else if (fieldName === 'roles') {
                updatedData[fieldName] = fieldValue.map((obj) => obj.value);
              } else if (ignoreDirty) {
                const set = fieldValue.map((addedItem) => addedItem.value);
                updatedData[fieldName] = { set };
              } else {
                const disconnect = defaultValue
                  .filter(
                    (defaultItem) =>
                      !fieldValue.some((fieldItem) => fieldItem.value === defaultItem.value)
                  )
                  .map((removedItem) => ({ id: removedItem.value }));

                const connect = fieldValue
                  .filter(
                    (fieldItem) =>
                      !defaultValue.some((defaultItem) => defaultItem.value === fieldItem.value)
                  )
                  .map((addedItem) => ({ id: addedItem.value, position: { end: true } }));

                const changesObject = { disconnect, connect };
                updatedData[fieldName] = changesObject;
              }
            } else if (fieldTypes[fieldName] === 'date_picker') {
              updatedData[fieldName] = new Date(fieldValue).toISOString();
            } else {
              updatedData[fieldName] = fieldValue;
            }
          }
        }

        const encodedData = encodeURIComponent(JSON.stringify(updatedData));
        const res = await action(encodedData, formDataToSend, slug);
 
        if (res.error) {
          if (res.error.status === 400 && res.error.message) {
            customSnackbarAction(res.error.message, 'error');
          } else {
            customSnackbarAction('Something went wrong, Please check your credential', 'error');
          }
        } else {
          if (redirect) {
            const slug = res?.data?.documentId || res?.documentId;

            if (slug) {
              router.push(redirect + slug);
            }
          }
          if (refresh) {
            refresh();
          }
          customSnackbarAction('Data Saved Successfully', 'success');
          if (component == 'page') {
            router.refresh();
          } else {
            handleClose();
          }
        }
      }
    } catch (error) {
      console.log(error);
      customSnackbarAction('Something went wrong', 'error');
    }
  });

  const handleClose = () => {
    if (dialog?.onFalse) {
      dialog.onFalse();
    }
    reset();
  };

  const handleDrop = useCallback(
    (acceptedFiles, field) => {
      const file = acceptedFiles[0];

      const newFile = Object.assign(file, {
        preview: URL.createObjectURL(file),
      });

      if (file) {
        setValue(field.name, newFile, { shouldValidate: true, shouldDirty: true });
      }
    },
    [setValue]
  );

  const handleRemoveFile = useCallback(
    (field) => {
      setValue(field.name, null, { shouldDirty: true });
    },
    [setValue]
  );

  const multiHandleDrop = useCallback(
    (acceptedFiles, field) => {
      const files = values[field.name] || [];

      const newFiles = acceptedFiles.map((file) =>
        Object.assign(file, {
          preview: URL.createObjectURL(file),
        })
      );

      setValue(field.name, [...files, ...newFiles], { shouldValidate: true, shouldDirty: true });
    },
    [setValue, values]
  );

  const multiHandleRemoveFile = useCallback(
    (inputFile, field) => {
      const filtered =
        values[field.name] &&
        values[field.name]?.filter((file) =>
          inputFile?.hash && file?.hash ? inputFile?.hash !== file?.hash : file !== inputFile
        );
      setValue(field.name, filtered, { shouldDirty: true });
    },
    [setValue, values]
  );

  const multiHandleRemoveAllFiles = useCallback(
    (field) => {
      setValue(field.name, [], { shouldDirty: true });
    },
    [setValue]
  );

  const renderField = (field, index) => {
    switch (field.type) {
      case 'number':
      case 'string':
      case 'email':
        return (
          <RHFTextField
            sx={{
              marginTop: 0,
            }}
            helperText={field.helperText}
            {...(field.rules?.depend !== undefined && { depend: field.rules.depend })}
            multiline={!!field.multiline}
            control={control}
            fullWidth
            type={field.type === 'string' ? 'text' : field.type}
            margin="dense"
            variant="outlined"
            name={field.name}
            label={field.label}
          />
        );
      case 'contact':
        return <RHFContactField name={field.name} label={field.label} defaultCountry="IN" control={control} />
      case 'password':
        return (
          <RHFPasswordField
            sx={{
              marginTop: 0,
            }}
            helperText={field.helperText}
            {...(field.rules?.depend !== undefined && { depend: field.rules.depend })}
            control={control}
            fullWidth
            margin="dense"
            variant="outlined"
            name={field.name}
            label={field.label}
          />
        );
      case 'select':
        return (
          <AutoCompleteBox control={control} setValue={setValue} field={field} onField={onField} />
        );
      case 'select_user':
        return (
          <UsersAutoComplete
            control={control}
            setValue={setValue}
            field={field}
            onField={findUsers}
          />
        );
      case 'select_country':
        return (
          <AutoSelectCountry control={control} setValue={setValue} field={field} />
        );
      case 'pre_select':
        return (
          <RHFSelect fullWidth control={control} name={field.name} label={field.label}>
            <MenuItem key="none" value="">
              None
            </MenuItem>
            {field.options.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </RHFSelect>
        );
      case 'boolean':
        if (field.name === 'publish_now' && dialog.value !== 'create') {
          return null;
        }
        return <RHFSwitch control={control} label={field.label} name={field.name} />;

      case 'file':
        return (
          <Stack spacing={1}>
            <Typography variant="subtitle2">{field.label}</Typography>
            {field.multiple ? (
              <RHFUpload
                multiple
                thumbnail
                control={control}
                name={field.name}
                key={index}
                maxSize={5 * 1024 * 1024}
                onDrop={(files) => multiHandleDrop(files, field)}
                onRemove={(file) => multiHandleRemoveFile(file, field)}
                onRemoveAll={() => multiHandleRemoveAllFiles(field)}
              />
            ) : (
              <RHFUpload
                helperText={field.helperText}
                control={control}
                key={index}
                name={field.name}
                maxSize={5 * 1024 * 1024}
                onDrop={(files) => handleDrop(files, field)}
                onDelete={() => handleRemoveFile(field)}
              />
            )}
          </Stack>
        );
      case 'display':
        return (
          <TextField
            disable="true"
            fullWidth
            margin="dense"
            variant="filled"
            label={field.label}
            value={field.value}
          />
        );
      case 'date_picker':
        return <RHFDatePicker fullWidth control={control} label={field.label} name={field.name} />;
      default:
        return null;
    }
  };

  return (
    <FormProvider methods={methods} onSubmit={onSubmit}>
      <Grid container rowSpacing={3} columnSpacing={{ xs: 2, md: 3 }} alignItems="start">
        {fields.map((field, index) => (
          <Grid item {...(field.props ? field.props : commonStyle || { xs: 12 })} key={index}>
            {isLoading ? (
              <Skeleton variant="rectangular" height={60} />
            ) : (
              <FormControl sx={{ width: '100%' }}>{renderField(field, index)}</FormControl>
            )}
          </Grid>
        ))}
      </Grid>

      <Stack direction="row" alignItems="center" justifyContent="end" gap={2} mt={2}>
        <Button onClick={handleClose} variant="soft" color="error">
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
    </FormProvider>
  );
}
