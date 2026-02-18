'use client';


import { useCallback, useState } from 'react';

import {
  Grid,
  MenuItem,
  Skeleton,
  IconButton,
  Typography,
  FormControl,
  Box,
} from '@mui/material';

import { useRouter } from 'src/routes/hooks';

import useCustomSnackbar from 'src/hooks/use-custom-snackbar';

import { AutoCompleteBox, AutoSelectCountry, FreeTextMultipleInput } from 'src/custom';

import { Edit as EditIcon } from '@mui/icons-material';
import { RHFContactField, RHFPasswordField, RHFPromptField, RHFSwitch, RHFTextField } from 'src/components/hook-form';

// const formatDate = (date) => {
//   const year = date.getFullYear();
//   const month = (date.getMonth() + 1).toString().padStart(2, '0');
//   const day = date.getDate().toString().padStart(2, '0');
//   return `${year}-${month}-${day}`;
// };

export default function CustomFormComponent({
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
  deleteEntry,
  type = 'page',
  saveAtTop = true,
  headerComponent,
  accordionSection = false,
  commonSX = false,
  viewCategory,
  methods,
  isLoading = false,
  control,
}) {
  const [hiddenItems, setHiddenItems] = useState({});
  const [values, setValue] = useState({});

  // Function to update visibility based on field's index
  const setVisibility = (index, shouldHide) => {
    setHiddenItems((prev) => ({ ...prev, [index]: shouldHide }));
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

      const newFiles = acceptedFiles
        .map((file) =>
          Object.assign(file, {
            preview: URL.createObjectURL(file),
          })
        )
        .sort((a, b) => a.name.localeCompare(b.name));

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

  const multiHandleReorder = useCallback(
    (sourceIndex, destinationIndex, field) => {
      const files = values[field.name] || [];
      const newFiles = Array.from(files);
      const [removed] = newFiles.splice(sourceIndex, 1);
      newFiles.splice(destinationIndex, 0, removed);

      setValue(field.name, newFiles, { shouldDirty: true });
    },
    [setValue, values]
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
            // setValue={setValue}
            disabled={field.hidden}
            helperText={field.helperText}
            {...(field.rules?.depend !== undefined && { depend: field.rules.depend })}
            multiline={!!field.multiline}
            control={control}
            fullWidth
            type={field.type === 'string' ? 'text' : field.type}
            variant="outlined"
            name={field.name}
            label={field.label}
            index={index}
            prefix={field.prefix}
            suffix={field.suffix}
          // onHide={setVisibility}
          />
        );
      case 'prompt':
        return (
          <RHFPromptField
            sx={{
              marginTop: 0,
            }}
            multiline
            rows={field.rows || 4}
            variables={field.variables || []}
            control={control}
            fullWidth
            name={field.name}
            label={field.label}
            helperText={field.helperText}
            rules={field.rules}
            {...(field.rules?.depend !== undefined && { depend: field.rules.depend })}
          />
        );
      case 'contact':
        return (
          <RHFContactField
            forceCallingCode
            disableDropdown
            onlyCountries={['US']}
            name={field.name}
            label={field.label}
            defaultCountry="US"
            control={control}
          />
        );
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
      case 'select_country':
        return (
          <AutoSelectCountry control={control} setValue={setValue} field={field} />
        );
      case 'free_text_multiple':
        return (
          <FreeTextMultipleInput
            control={control}
            name={field.name}
            label={field.label}
            helperText={field.helperText}
            placeholder={field.placeholder || "Enter values separated by comma or press Enter"}
            delimiter={field.delimiter || ','}
            options={field.options || []}
            field={field}
            limit={field.limit || 6}
          />
        );
      case 'pre_select':
        return field.selectType === 'multiple' ? (
          <RHFMultiSelect
            parentField={field.parentField ? field.parentField : null}
            checkbox={true}
            fullWidth={true}
            setValue={setValue}
            chip={true}
            control={control}
            name={field.name}
            label={field.label}
            options={field.options}
          />
        ) : (
          <RHFSelect fullWidth control={control} name={field.name} label={field.label}>
            {field.options.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </RHFSelect>
        );
      case 'boolean':
        if (
          (field.name === 'publish_now' || field.name === 'publish_on_create') &&
          dialog.value !== 'create'
        ) {
          return null;
        }
        return (
          <RHFSwitch color={field.color} control={control} label={field.label} name={field.name} />
        );

      case 'file':

        return (
          <Stack spacing={1}>
            {field.isEdit ?
              <>
                <Stack direction="row" alignItems="center" spacing={1}>
                  {!field.editLabel ? (
                    <>
                      <Typography variant="subtitle2">{field.label}</Typography>
                      <IconButton
                        onClick={() => {
                          field.editLabel = true;
                          setValue(`${field.name}_label`, field.label, { shouldDirty: true });
                        }}
                      >
                        <EditIcon />
                      </IconButton>
                    </>
                  ) : (
                    <RHFTextField
                      control={control}
                      name={`${field.name}_label`}
                      defaultValue={field.label}
                      label="Label"
                      onBlur={(e) => {
                        const updatedLabel = e.target.value;
                        field.label = updatedLabel;
                        const currentDefaults = values.default_images || {};
                        setValue(
                          `default_images`,
                          {
                            ...currentDefaults,
                            [`default_${index + 1}`]: {
                              title: updatedLabel,
                            },
                          },
                          { shouldDirty: true, shouldValidate: true }
                        );
                        field.editLabel = false;
                      }}
                    />
                  )}
                </Stack>
                <Stack direction="row" alignItems="center" spacing={1}>
                  {!field.editHelperText ? (
                    <>
                      <Typography variant="body2">{field.helperText}</Typography>
                      <IconButton
                        onClick={() => {
                          field.editHelperText = true;
                          setValue(`${field.name}_helperText`, field.helperText, { shouldDirty: true });
                        }}
                      >
                        <EditIcon />
                      </IconButton>
                    </>
                  ) : (
                    <RHFTextField
                      control={control}
                      name={`${field.name}_helperText`}
                      defaultValue={field.helperText}
                      label="Helper Text"
                      onBlur={(e) => {
                        const updatedHelperText = e.target.value;
                        field.helperText = updatedHelperText;
                        // setValue(`${field.name}_helperText`, updatedHelperText, { shouldDirty: true });
                        setValue(`default_images`, {
                          ...values.default_images,
                          [`default_${index + 1}`]: {
                            ...(values.default_images?.[`default_${index + 1}`] || {}),
                            size: field.helperText,
                          },
                        }, { shouldDirty: true });
                        field.editHelperText = false;
                      }}
                    />
                  )}
                </Stack></>
              : <Typography variant="subtitle2">{field.label}</Typography>}

            {field.multiple ? (
              <RHFUpload
                sx={{
                  '& .css-jpc0h9': {
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))',
                    gap: 2, // MUI spacing = 2 * 8px = 16px
                  },
                  '& img': {
                    width: '100%',
                    height: '100px',
                    objectFit: 'cover',
                    borderRadius: 1,
                  },
                }}
                multiple
                thumbnail
                control={control}
                name={field.name}
                key={index}
                helperText={!field.isEdit ? field.helperText : ''}
                aspectRatio={field.aspectRatio}
                maxSize={5 * 1024 * 1024}
                onDrop={(files) => {
                  const updatedFiles = files.map((file, idx) => ({
                    [`default_${idx + 1}`]: {
                      size: `${file.width}x${file.height}`,
                      title: file.name,
                    },
                  }));
                  setValue(field.name, updatedFiles, { shouldDirty: true });
                  multiHandleDrop(files, field);
                }}
                onRemove={(file) => multiHandleRemoveFile(file, field)}
                onRemoveAll={() => multiHandleRemoveAllFiles(field)}
                onReorder={(sourceIndex, destinationIndex) =>
                  multiHandleReorder(sourceIndex, destinationIndex, field)
                }
              />
            ) : (
              <RHFUpload
                helperText={field.helperText}
                control={control}
                key={index}
                name={field.name}
                maxSize={5 * 1024 * 1024}
                onDrop={(files) => {
                  const file = files[0];
                  const updatedFile = {
                    [`default_1`]: {
                      size: `${file.width}x${file.height}`,
                      title: file.name,
                    },
                  };
                  setValue(field.name, updatedFile, { shouldDirty: true });
                  handleDrop(files, field);
                }}
                onDelete={() => handleRemoveFile(field)}
              />
            )}
            {/* {field.isEdit ?
              <Stack direction="row" alignItems="center" spacing={1}>
                {!field.editHelperText ? (
                  <>
                    <Typography variant="body2">{field.helperText}</Typography>
                    <IconButton
                      onClick={() => {
                        field.editHelperText = true;
                        setValue(`${field.name}_helperText`, field.helperText, { shouldDirty: true });
                      }}
                    >
                      <EditIcon />
                    </IconButton>
                  </>
                ) : (
                  <RHFTextField
                    control={control}
                    name={`${field.name}_helperText`}
                    defaultValue={field.helperText}
                    label="Helper Text"
                    onBlur={(e) => {
                      const updatedHelperText = e.target.value;
                      field.helperText = updatedHelperText;
                      // setValue(`${field.name}_helperText`, updatedHelperText, { shouldDirty: true });
                      setValue(`default_images`, {
                        ...values.default_images,
                        [`default_${index + 1}`]: {
                          ...(values.default_images?.[`default_${index + 1}`] || {}),
                          size: field.helperText,
                        },
                      }, { shouldDirty: true });
                      field.editHelperText = false;
                    }}
                  />
                )}
              </Stack> : ''} */}
          </Stack>
        );
      case 'display':
        return (
          <RHFTextField
            disabled={true}
            fullWidth
            margin="dense"
            variant="filled"
            label={field.label}
            {...(field.name ? { name: field.name, control: control } : { value: field.value })}
          />
        );
      case 'date_picker':
        return (
          <RHFDatePicker
            fullWidth
            helperText={field.helperText}
            control={control}
            label={field.label}
            name={field.name}
          />
        );
      default:
        return null;
    }
  };
  const isPopup = type === 'popup';

  return (
    <Grid
      container
      rowSpacing={3}
      sx={{ mt: 1 }}
      columnSpacing={{ xs: 2, md: 3 }}
      alignItems="flex-start"
    >
      {fields.map((field, index) => {
        const shouldHide = hiddenItems[index] || field.hidden;

        return (
          <Grid
            item
            {...(field.props
              ? field.props
              : isPopup && field.multiline
                ? { xs: 12 }
                : commonStyle || { xs: 12 })}
            key={index}
            sx={{ ...(shouldHide && { display: 'none' }), ...(commonSX && { border: (theme) => `dashed 1px ${theme.palette.divider}`, pr: 3, pb: 3 }) }}
          >
            {isLoading ? (
              <Skeleton variant="rectangular" height={60} />
            ) : (
              <FormControl sx={{ width: '100%', ...(field.hidden && { display: 'none' }) }}>
                {renderField(field, index)}
              </FormControl>
            )}
          </Grid>
        );
      })}
    </Grid>
  );
}