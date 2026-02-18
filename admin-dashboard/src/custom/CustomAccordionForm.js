'use client';

import PropTypes from 'prop-types';
import { useEffect, useState } from 'react';
import { Box, Tabs, Tab } from '@mui/material';
import CustomFormComponent from './CustomFormComponent';
import FormButtons from './FormButtons';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as Yup from 'yup';
import FormProvider from 'src/components/hook-form';
import useCustomSnackbar from 'src/hooks/use-custom-snackbar';
import { useRouter } from 'src/routes/hooks';
// ----------------------------------------------------------------------

export default function CustomAccordionForm({
  time,
  sections,
  dialog,
  refresh,
  action,
  onField,
  custom_data,
  ignoreDirty,
  type,
  commonStyle,
  deleteEntry,
  viewCategory,
  redirect
}) {
  const component = "page";
  const router = useRouter();
  const [currentTab, setCurrentTab] = useState(0);
  const handleChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const t = Number(new URLSearchParams(window.location.search).get('tab') || 0);
    if (!Number.isNaN(t)) setCurrentTab(t);
  }, []);

  const { customSnackbarAction } = useCustomSnackbar();

  const validationRules = sections.flatMap(section => section.fields).reduce(
    (acc, { rules, type, name, label, multiple, selectType }) => {
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
          case 'pre_select':
            acc[name] = Yup.mixed().test('required', `Please select ${label}`, function (value) {
              return Array.isArray(value) ? value.length > 0 : value !== '';
            });
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
                    return schema.test('regex', condition.message || validMessage, (value) => {
                      if (rules.required && (value == null || value === '')) {
                        return false;
                      }

                      if (condition.regex) {
                        return condition.regex.test(value);
                      }

                      return true;
                    });
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
    },
    {}
  );

  const validationSchema = Yup.object().shape(validationRules);

  const methods = useForm({
    resolver: yupResolver(validationSchema),
  });

  const { reset, handleSubmit, control, watch, formState: { isDirty, isSubmitting, dirtyFields, isLoading, defaultValues } } = methods;
  const values = watch();

  const fieldTypes = {
    ...sections.flatMap(section => section.fields).reduce((acc, field) => {
      acc[field.name] = field.type;
      return acc;
    }, {}),
  };

  useEffect(() => {
    const fetchDefaultValues = async () => {
      const defaultValuesPromises = sections.flatMap(section => section.fields).map(async (field) => {
        const sectionDialog = {
          ...(dialog || {}),
          value: {
            id: dialog?.id,
            [field.name]: dialog ? dialog[field.name] : undefined,
          },
        };
        const value = await getDefaultFieldValue(field, sectionDialog);
        return { [field.name]: value };
      });

      const resolvedValues = await Promise.all(defaultValuesPromises);
      const defaultValuesObj = resolvedValues.reduce((acc, curr) => ({ ...acc, ...curr }), {});

      reset(defaultValuesObj);
    };

    fetchDefaultValues();
  }, [dialog, reset, sections, JSON.stringify(dialog.value)]);

  async function getDefaultFieldValue(field, dialog) {
    switch (field.type) {
      case 'select':
      // case 'select_country':
      //   return processData(field);
      case 'pre_select':
        return processPreSelect(field, dialog);
      // case 'select_league':
      //   return await processLeagues(field);
      case 'file':
        if (field?.multiple) {
          return dialog && dialog.value && dialog.value[field.name] ? dialog.value[field.name] : [];
        }
        return dialog && dialog.value && dialog.value[field.name] ? dialog.value[field.name] : null;
      case 'string':
        return dialog &&
          dialog.value &&
          typeof dialog.value === 'object' &&
          field.name in dialog.value &&
          (dialog.value[field.name] == 0 || dialog.value[field.name])
          ? dialog.value[field.name].toString()
          : '';
      default:
        return dialog && dialog.value && dialog.value[field.name]
          ? dialog.value[field.name]
          : dialog &&
            dialog.value &&
            dialog.value[field.name] &&
            typeof dialog.value[field.name] === 'number' &&
            dialog.value[field.name] === 0
            ? '0'
            : '';
    }
  }

  const processPreSelect = (field, dlg) => {
    const { name, fieldValue, selectType } = field;
    if (fieldValue) {
      return fieldValue;
    }

    const value = dlg?.value?.[name] ?? '';
    if (selectType === 'multiple') {
      return fieldValue || (value ? value.split(',') : []);
    }
    return fieldValue || value;
  };

  const onSubmit = handleSubmit(async (formData) => {
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      const formDataToSend = new FormData();

      if (ignoreDirty || isDirty || custom_data) {
        const editFields = custom_data || ignoreDirty ? values : dirtyFields;
        const updatedData = new Object();
        if (dialog && dialog.documentId) {
          updatedData.id = dialog.documentId;
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
            } else if (fieldTypes[fieldName] === 'pre_select') {
              updatedData[fieldName] = Array.isArray(fieldValue)
                ? fieldValue.filter(Boolean).join(',')
                : fieldValue;
            } else if (Array.isArray(fieldValue) && Array.isArray(defaultValue)) {
              if (custom_data) {
                updatedData[fieldName] = fieldValue.map((obj) => obj.value).join(',');
              } else {
                updatedData[fieldName] = fieldValue;
              }
            } else if (fieldTypes[fieldName] === 'date_picker') {
              const date = new Date(fieldValue);
              const formattedDate = formatDate(date);
              updatedData[fieldName] = formattedDate;
            } else if (fieldTypes[fieldName] === 'boolean') {
              updatedData[fieldName] = !!fieldValue;
            } else {
              updatedData[fieldName] = fieldValue;
            }
          }
        }
        const encodedData = encodeURIComponent(JSON.stringify(updatedData));
        let res = await action(encodedData, formDataToSend);
        if (res.error) {
          if (res.error.status === 400 && res.error.message) {
            res.error.details.errors.forEach((error) => {
              if (error.path && error.path.length > 0) {
                const fieldName = error.path[0];
                methods.setError(fieldName, {
                  type: 'manual',
                  message: error.message,
                });
              }
            });
            customSnackbarAction(res.error.message, 'error');
          } else {
            customSnackbarAction('Something went wrong, Please check your credential', 'error');
          }
        } else {
          if (redirect) {
            const slug = res?.data?.id || res?.id;
            if (slug) {
              router.push(redirect + slug);
            }
          }
          // if (refresh) {
          //   // if (accordionSection) {
          //   //   refresh({ res, accordionSection });
          //   // } else {
          //     refresh({ res });
          //   // }
          // }


          customSnackbarAction('Data Saved Successfully', 'success');
          if (component == 'page') {
            if (typeof window !== 'undefined') {
              const params = new URLSearchParams(window.location.search);
              params.set('tab', String(currentTab));
              // update URL without navigating
              window.history.replaceState({}, '', `${window.location.pathname}?${params.toString()}`);
            }
            router.refresh();
          } else {
            if (!currentTab) {
              dialog.onFalse();
            }
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

  return (
    <FormProvider methods={methods} onSubmit={onSubmit}>
      <Box sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs
            value={currentTab}
            onChange={handleChange}
            variant="scrollable"
            scrollButtons="auto"
            allowScrollButtonsMobile
          >
            {sections.map((section, index) => (
              <Tab
                key={section.id}
                label={section.title}
                icon={section.icon}
                iconPosition="start"
                id={`tab-${section.id}`}
                aria-controls={`tabpanel-${section.id}`}
                sx={{
                  minHeight: 48,
                  typography: 'subtitle2',
                  '&.Mui-selected': {
                    color: 'primary.main',
                    fontWeight: 'bold',
                  }
                }}
              />
            ))}
          </Tabs>
        </Box>

        {sections.map((section, index) => {

          const filteredValues = {};
          let sectionFieldNames = null;
          let sectionDialog = null
          let values = dialog;


          // if (section.id !== 'dvdp' || section.id !== 'feeds') {

          sectionFieldNames = section.fields?.map((field) => field.name);

          Object.entries(dialog.default_images ? values : dialog).forEach(([key, value]) => {
            if (sectionFieldNames?.includes(key)) {
              filteredValues[key] = value;
            }
          });

          sectionDialog = {
            ...dialog,
            value: {
              id: dialog.id,
              ...filteredValues,
            },
          };
          // }


          return (
            <div
              key={section.id}
              role="tabpanel"
              hidden={currentTab !== index}
              id={`tabpanel-${section.id}`}
              aria-labelledby={`tab-${section.id}`}
            >
              {currentTab === index && (
                <Box>
                  {(() => {
                    switch (section.id) {
                      case 'dvdp':
                        return section.component;
                      case 'feeds':
                        return section.component;
                      case 'bannerset_uids':
                        return section.component;
                      default:
                        return <CustomFormComponent
                          methods={methods}
                          key={`${time}-${section.id}-${JSON.stringify(filteredValues)}`}
                          custom_data={!!custom_data}
                          ignoreDirty={!!ignoreDirty}
                          dialog={sectionDialog}
                          refresh={false}
                          fields={section.fields}
                          action={action}
                          onField={onField}
                          isLoading={isLoading}
                          control={control}
                          type={type}
                          commonStyle={commonStyle}
                          deleteEntry={deleteEntry}
                          accordionSection={section.id}
                          viewCategory={viewCategory}
                          component='page'
                          commonSX={section.id === "default_images" ? true : false}
                        />;
                    }
                  })()}
                </Box>
              )}
            </div>
          );
        })}
        <Box
          sx={{
            position: 'sticky',
            bottom: 0,
            zIndex: 1000,
            backgroundColor: 'background.paper',
            // boxShadow: 3,
            padding: 2,
          }}
        >
          <FormButtons
            deleteEntry={deleteEntry}
            dialog={dialog}
            handleClose={handleClose}
            isDirty={isDirty}
            isSubmitting={isSubmitting}
          />
        </Box>
      </Box>
    </FormProvider>
  );
}

CustomAccordionForm.propTypes = {
  sections: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      fields: PropTypes.arrayOf(
        PropTypes.shape({
          name: PropTypes.string.isRequired,
          type: PropTypes.string.isRequired,
          label: PropTypes.string.isRequired,
          rules: PropTypes.object,
        })
      ).isRequired,
    })
  ).isRequired,
  dialog: PropTypes.object.isRequired,
  refresh: PropTypes.func.isRequired,
  action: PropTypes.func.isRequired,
  onField: PropTypes.func,
  custom_data: PropTypes.bool,
  ignoreDirty: PropTypes.bool,
  type: PropTypes.string,
  commonStyle: PropTypes.object,
  deleteEntry: PropTypes.func,
  selectedOffers: PropTypes.array,
  excludeSections: PropTypes.array,
};