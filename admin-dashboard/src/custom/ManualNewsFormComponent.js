"use client";
import { useFormContext } from "react-hook-form";
import * as Yup from "yup";
import { useCallback, useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import LoadingButton from "@mui/lab/LoadingButton";
import {
  Grid,
  Stack,
  Button,
  MenuItem,
  Skeleton,
  TextField,
  Typography,
  FormControl,
  Card,
  CardContent,
  IconButton,
  Tooltip,
} from "@mui/material";
import { alpha } from '@mui/material/styles';

import { useRouter } from "src/routes/hooks";

import useCustomSnackbar from "src/hooks/use-custom-snackbar";

import { findUsers } from "src/utils/commonActions";

import {
  AutoCompleteBox,
  CustomLeagueAutocomplete,
  AutoSelectCountry,
  UsersAutoComplete,
  CustomAutoCompleteBox,
} from "src/custom";

import FormProvider, {
  RHFUpload,
  RHFSelect,
  RHFSwitch,
  RHFTextField,
  RHFDatePicker,
  RHFPasswordField,
  RHFContactField,
  RHFCustomLeagueAutocomplete,
  RHFDateTimePicker,
} from "src/components/hook-form";
import { Delete as DeleteIcon, Add as AddIcon } from "@mui/icons-material";
import { GlobalLoader } from "src/components/loading-screen";

const GoalscorersComponent = ({ control, name, homeTeam, awayTeam, disabled = false }) => {
  const { setValue, watch } = useFormContext();
  const goalscorersValue = watch(name) || [];
  const goalscorers = Array.isArray(goalscorersValue) ? goalscorersValue : [];

  const teamOptions = [
    { value: "HOME", label: homeTeam || "Home Team" },
    { value: "AWAY", label: awayTeam || "Away Team" },
  ];

  const handleGoalscorerChange = (index, field, fieldValue) => {
    if (disabled) return;

    const updatedGoalscorers = goalscorers.map((scorer, i) =>
      i === index ? { ...scorer, [field]: fieldValue } : scorer,
    );
    setValue(name, updatedGoalscorers, { shouldDirty: true });
  };

  const addGoalscorer = () => {
    if (disabled) return;

    const newGoalscorer = {
      player_name: "",
      team: "",
      minute: "",
    };
    const updatedGoalscorers = [...goalscorers, newGoalscorer];
    setValue(name, updatedGoalscorers, { shouldDirty: true });
  };

  const removeGoalscorer = (index) => {
    if (disabled) return;

    const updatedGoalscorers = goalscorers.filter((_, i) => i !== index);
    setValue(name, updatedGoalscorers, { shouldDirty: true });
  };

  return (
    <Card
      sx={{
        mt: 3,
        boxShadow: (theme) => theme.customShadows?.card || 2,
        borderRadius: 2,
        border: (theme) => `1px solid ${alpha(theme.palette.divider, 0.5)}`,
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Typography
          variant="h6"
          gutterBottom
          sx={{ fontWeight: 700, mb: 2 }}
        >
          Goalscorers
        </Typography>

        {goalscorers.map((scorer, index) => (
          <Grid container spacing={2} key={index} sx={{ mb: 2 }}>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Player Name"
                value={scorer.player_name || ""}
                onChange={(e) =>
                  handleGoalscorerChange(index, "player_name", e.target.value)
                }
                placeholder="Enter player name"
                disabled={disabled}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                  },
                }}
              />
            </Grid>
            <Grid item xs={12} sm={3}>
              <TextField
                select
                fullWidth
                label="Team"
                value={scorer.team || ""}
                onChange={(e) =>
                  handleGoalscorerChange(index, "team", e.target.value)
                }
                disabled={disabled}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                  },
                }}
              >
                <MenuItem value="">Select Team</MenuItem>
                {teamOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={3}>
              <TextField
                fullWidth
                label="Minute"
                value={scorer.minute || ""}
                onChange={(e) =>
                  handleGoalscorerChange(index, "minute", e.target.value)
                }
                placeholder="e.g., 45+2'"
                disabled={disabled}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                  },
                }}
              />
            </Grid>
            <Grid
              item
              xs={12}
              sm={2}
              sx={{ display: "flex", alignItems: "center" }}
            >
              <Tooltip title="Remove Goalscorer" arrow>
                <IconButton
                  onClick={() => removeGoalscorer(index)}
                  size="small"
                  disabled={disabled}
                  sx={{
                    color: 'error.main',
                    '&:hover': {
                      bgcolor: 'error.lighter',
                    },
                  }}
                >
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            </Grid>
          </Grid>
        ))}

        <Button
          startIcon={<AddIcon />}
          onClick={addGoalscorer}
          variant="outlined"
          disabled={disabled}
          sx={{
            mt: 1,
            fontWeight: 600,
            '&:hover': {
              bgcolor: 'primary.lighter',
            },
          }}
        >
          Add Goalscorer
        </Button>
      </CardContent>
    </Card>
  );
};

const PlayersToWatchComponent = ({ control, name, homeTeam, awayTeam, disabled = false }) => {
  const { setValue, watch } = useFormContext();
  const playersValue = watch(name) || [];
  const players = Array.isArray(playersValue) ? playersValue : [];

  const teamOptions = [
    { value: "HOME", label: homeTeam || "Home Team" },
    { value: "AWAY", label: awayTeam || "Away Team" },
  ];

  const handlePlayerChange = (index, field, fieldValue) => {
    if (disabled) return;

    const updatedPlayers = players.map((player, i) =>
      i === index ? { ...player, [field]: fieldValue } : player,
    );
    setValue(name, updatedPlayers, { shouldDirty: true });
  };

  const addPlayer = () => {
    if (disabled) return;

    const newPlayer = {
      player_name: "",
      team: "",
      session_goals: "",
    };
    const updatedPlayers = [...players, newPlayer];
    setValue(name, updatedPlayers, { shouldDirty: true });
  };

  const removePlayer = (index) => {
    if (disabled) return;

    const updatedPlayers = players.filter((_, i) => i !== index);
    setValue(name, updatedPlayers, { shouldDirty: true });
  };

  return (
    <Card
      sx={{
        mt: 3,
        boxShadow: (theme) => theme.customShadows?.card || 2,
        borderRadius: 2,
        border: (theme) => `1px solid ${alpha(theme.palette.divider, 0.5)}`,
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Typography
          variant="h6"
          gutterBottom
          sx={{ fontWeight: 700, mb: 2 }}
        >
          Players to Watch
        </Typography>

        {players.map((player, index) => (
          <Grid container spacing={2} key={index} sx={{ mb: 2 }}>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Player Name"
                value={player.player_name || ""}
                onChange={(e) =>
                  handlePlayerChange(index, "player_name", e.target.value)
                }
                placeholder="Enter player name"
                disabled={disabled}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                  },
                }}
              />
            </Grid>
            <Grid item xs={12} sm={3}>
              <TextField
                select
                fullWidth
                label="Team"
                value={player.team || ""}
                onChange={(e) =>
                  handlePlayerChange(index, "team", e.target.value)
                }
                disabled={disabled}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                  },
                }}
              >
                <MenuItem value="">Select Team</MenuItem>
                {teamOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={3}>
              <TextField
                fullWidth
                label="Session Goals"
                value={player.session_goals || ""}
                onChange={(e) =>
                  handlePlayerChange(index, "session_goals", e.target.value)
                }
                placeholder="e.g., 2"
                disabled={disabled}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                  },
                }}
              />
            </Grid>
            <Grid
              item
              xs={12}
              sm={2}
              sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}
            >
              <Tooltip title="Remove Player" arrow>
                <IconButton
                  onClick={() => removePlayer(index)}
                  size="small"
                  disabled={disabled}
                  sx={{
                    color: 'error.main',
                    '&:hover': {
                      bgcolor: 'error.lighter',
                    },
                  }}
                >
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            </Grid>
          </Grid>
        ))}

        <Button
          startIcon={<AddIcon />}
          onClick={addPlayer}
          variant="outlined"
          disabled={disabled}
          sx={{
            mt: 1,
            fontWeight: 600,
            '&:hover': {
              bgcolor: 'primary.lighter',
            },
          }}
        >
          Add Player to Watch
        </Button>
      </CardContent>
    </Card>
  );
};

export default function ManualNewsFormComponent({
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
  slug,
  // goalscorers,
  // onGoalscorersChange,
  currentTab,
  disabled
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
    if (typeof value === "object" && value !== null) {
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
    } else if (
      !Array.isArray(value) &&
      typeof value === "object" &&
      value !== null
    ) {
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

  const validationRules = fields.reduce(
    (acc, { rules, type, name, label, multiple }) => {
      const requiredMessage = label
        ? `${label} is required`
        : "This field is required";
      const validMessage = `Please enter valid ${label}`;

      if (rules && (rules.required || rules.regex || rules.depend)) {
        switch (type) {
          case "email":
            acc[name] = Yup.string()
              .required(requiredMessage)
              .email("Email must be a valid email address");
            break;
          case "select":
          case "select_country":
            acc[name] = Yup.array()
              .min(1, `Please select ${label}`)
              .required(`Please select ${label}`);
            break;
          case "file":
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
                  match?.message || `${fieldName} do not match`,
                );
              } else if (conditions) {
                acc[name] = Yup.string().when(fieldName, (value, schema) => {
                  const condition = conditions.find(
                    (c) => c.value === value[0],
                  );
                  if (condition) {
                    return schema.test(
                      "regex",
                      condition.message || validMessage,
                      (value) =>
                        rules.required
                          ? condition.regex.test(value)
                          : value == null ||
                          value === "" ||
                          condition.regex.test(value),
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
                    (val) => val == null || val === "" || value.test(val),
                  );
                });
              } else if (rules.regex) {
                schema = schema.test(
                  rules.regex.name,
                  rules.regex.message,
                  (val) => val == null || val === "" || rules.regex.test(val),
                );
              }

              if (rules.required) {
                schema = schema.required(
                  rules.required.message || requiredMessage,
                );
              }

              acc[name] = schema;
            }

            break;
        }
      }

      return acc;
    },
    {},
  );

  const validationSchema = Yup.object().shape(validationRules);
  const fieldTypes = {
    ...fields.reduce((acc, field) => {
      acc[field.name] = field.type;
      return acc;
    }, {}),
  };

  async function getDefaultFieldValue(field, dialog) {
    switch (field.type) {
      case "select":
        return processData(field);

      case "select_user":
        return await processUsers(field);
      case "file":
        if (field?.multiple) {
          return dialog && dialog.value[field.name]
            ? dialog.value[field.name]
            : [];
        }
        return dialog && dialog.value[field.name]
          ? dialog.value[field.name]
          : null;

      default:
        return dialog && dialog.value[field.name]
          ? dialog.value[field.name]
          : dialog &&
            dialog.value[field.name] &&
            typeof dialog.value[field.name] === 'number' &&
            dialog.value[field.name] === 0
            ? '0'
            : '';
    }
  }

  const methods = useForm(
    {
      resolver: yupResolver(validationSchema),
      defaultValues: async () => {
        const defaultValuesObj = await fields.reduce(
          async (accPromise, field) => {
            const acc = await accPromise;
            if (field.name) {
              acc[field.name] = await getDefaultFieldValue(field, dialog);
            }
            return acc;
          },
          Promise.resolve({}),
        );

        return defaultValuesObj;
      },
    },
    [],
  );

  const {
    control,
    setValue,
    watch,
    reset,
    handleSubmit,
    formState: {
      isLoading,
      isDirty,
      isSubmitting,
      dirtyFields,
      defaultValues,
      isSubmitSuccessful,
    },
  } = methods;

  const values = watch();
  const goalscorersValue = watch("goalscorers") || [];
  const playersValue = watch("players_to_watch") || [];

  const onSubmit = handleSubmit(async (formData) => {
    // console.log("Submitting form with data:", formData);
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));

      const formDataToSend = new FormData();

      // Check if there are any changes (form dirty OR goalscorers have data OR custom_data provided)
      const hasGoalscorersChanges =
        goalscorersValue.length > 0 &&
        goalscorersValue.some(
          (scorer) => scorer.player_name || scorer.team || scorer.minute,
        );

      const hasPlayersToWatchChanges =
        values.players_to_watch &&
        values.players_to_watch.length > 0 &&
        values.players_to_watch.some(
          (player) => player.player_name || player.team || player.session_goals,
        );

      const hasChanges =
        isDirty ||
        hasGoalscorersChanges ||
        hasPlayersToWatchChanges ||
        custom_data ||
        ignoreDirty;

      if (hasChanges) {
        const editFields = custom_data || ignoreDirty ? values : dirtyFields;
        const updatedData = new Object();

        if (dialog && dialog.value.documentId) {
          updatedData.id = dialog.value.documentId;
        }

        updatedData.news_type =
          currentTab === "match_reviews" ? "match_reviews" : "match_previews";

        if (hasGoalscorersChanges) {
          const validGoalscorers = goalscorersValue.filter(
            (scorer) => scorer.player_name && scorer.team && scorer.minute,
          );

          if (validGoalscorers.length > 0) {
            updatedData.goalscorers = validGoalscorers;
          }
        }
        if (hasPlayersToWatchChanges) {
          const validPlayers = values.players_to_watch.filter(
            (player) => player.player_name && player.team && player.session_goals,
          );

          if (validPlayers.length > 0) {
            updatedData.players_to_watch = validPlayers;
          }
        }

        for (const fieldName in editFields) {
          if (formData.hasOwnProperty(fieldName)) {
            const fieldValue = formData[fieldName];
            const defaultValue = defaultValues[fieldName];

            if (fieldTypes[fieldName] === "file") {
              if (!updatedData._files) {
                updatedData._files = {};
              }
              if (Array.isArray(fieldValue) && Array.isArray(defaultValue)) {
                const newFiles = fieldValue.filter((item) => item.preview);
                const oldFiles = fieldValue.filter((item) => !item.preview);
                const removedFiles = defaultValue
                  .filter(
                    (defaultItem) =>
                      !fieldValue.some(
                        (fieldItem) => fieldItem.id === defaultItem.id,
                      ),
                  )
                  .map((removedItem) => removedItem.id);

                updatedData[fieldName] = oldFiles;
                updatedData._files[fieldName] = removedFiles;
                newFiles.forEach((file) =>
                  formDataToSend.append(fieldName, file),
                );
              } else {
                updatedData._files[fieldName] = defaultValue
                  ? [defaultValue.id]
                  : [];
                formDataToSend.append(fieldName, fieldValue);
                updatedData[fieldName] = null;
              }
            } else if (
              Array.isArray(fieldValue) &&
              Array.isArray(defaultValue)
            ) {
              if (custom_data) {
                updatedData[fieldName] = fieldValue
                  .map((obj) => obj.value)
                  .join(",");
              } else if (fieldName === "roles") {
                updatedData[fieldName] = fieldValue.map((obj) => obj.value);
              } else if (ignoreDirty) {
                const set = fieldValue.map((addedItem) => addedItem.value);
                updatedData[fieldName] = { set };
              } else if (fieldName === "goalscorers" && fieldValue.length > 0) {
                continue;
              } else if (fieldName === "players_to_watch" && fieldValue.length > 0) {
                continue;
              } else if (fieldName === "users_websites" && fieldValue.length > 0) {
                updatedData[fieldName] = fieldValue
                  .map((obj) => {
                    // Return the value property if it exists, otherwise return id
                    if (obj && typeof obj === "object") {
                      return obj.value || obj.id;
                    }
                    return null;
                  })
                  .filter((value) => value !== null && value !== undefined);
              } else {
                const disconnect = defaultValue
                  .filter(
                    (defaultItem) =>
                      !fieldValue.some(
                        (fieldItem) => fieldItem.value === defaultItem.value,
                      ),
                  )
                  .map((removedItem) => ({ id: removedItem.value }));

                const connect = fieldValue
                  .filter(
                    (fieldItem) =>
                      !defaultValue.some(
                        (defaultItem) => defaultItem.value === fieldItem.value,
                      ),
                  )
                  .map((addedItem) => ({
                    id: addedItem.value,
                    position: { end: true },
                  }));

                const changesObject = { disconnect, connect };
                updatedData[fieldName] = changesObject;
              }
            } else if (fieldTypes[fieldName] === "date_picker") {
              updatedData[fieldName] = new Date(fieldValue).toISOString();
            } else if (fieldTypes[fieldName] === "date_time_picker") {
              updatedData[fieldName] = new Date(fieldValue).toISOString();
            } else {
              if (fieldName === "league" && fieldValue) {
                // For league, always send as array of objects (even if single object)

                if (Array.isArray(fieldValue)) {
                  updatedData[fieldName] = fieldValue.map((item) => ({
                    label: item.name || item.label || "",
                    value: item.id || item.label || "0",
                    name: item.name || item.label || "",
                    id: item.id || item.value || "0",
                  }));
                } else if (
                  typeof fieldValue === "object" &&
                  fieldValue !== null
                ) {
                  // Convert single object to array
                  updatedData[fieldName] = [
                    {
                      label: fieldValue.name || fieldValue.label || "",
                      value: fieldValue.id || fieldValue.value || "0",
                      name: fieldValue.name || fieldValue.label || "",
                      id: fieldValue.id || fieldValue.value || "0",
                    },
                  ];
                } else {
                  updatedData[fieldName] = fieldValue;
                }
              } else {
                updatedData[fieldName] = fieldValue;
              }
            }
          }
        }
        if (dialog?.mode === "edit") {
          updatedData.reganrate_slug = true;
        }
        // Always regenerate slug on every update
        // console.log("Encoded data to be updatedData:", updatedData);
        const encodedData = encodeURIComponent(JSON.stringify(updatedData));
        // console.log("Encoded data to be formDataToSend:", formDataToSend);
        // console.log("Encoded data to be sent:", encodedData);
        const res = await action(encodedData, formDataToSend, slug);

        if (res.error) {
          if (res.error.status === 400 && res.error.message) {
            customSnackbarAction(res.error.message, "error");
          } else {
            customSnackbarAction("Something went wrong", "error");
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
          customSnackbarAction("News Generated Successfully", "success");
          if (component == "page") {
            router.refresh();
          } else {
            handleClose();
          }

          // // Reset goalscorers after successful submission
          // if (onGoalscorersChange) {
          //   onGoalscorersChange([]);
          // }
          // setLocalGoalscorers([]);
        }
      }
    } catch (error) {
      console.log(error);
      customSnackbarAction("Something went wrong", "error");
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
        setValue(field.name, newFile, {
          shouldValidate: true,
          shouldDirty: true,
        });
      }
    },
    [setValue],
  );

  const handleRemoveFile = useCallback(
    (field) => {
      setValue(field.name, null, { shouldDirty: true });
    },
    [setValue],
  );

  const multiHandleDrop = useCallback(
    (acceptedFiles, field) => {
      const files = values[field.name] || [];
      const newFiles = acceptedFiles.map((file) =>
        Object.assign(file, {
          preview: URL.createObjectURL(file),
        }),
      );

      setValue(field.name, [...files, ...newFiles], {
        shouldValidate: true,
        shouldDirty: true,
      });
    },
    [setValue, values],
  );

  const multiHandleRemoveFile = useCallback(
    (inputFile, field) => {
      const filtered =
        values[field.name] &&
        values[field.name]?.filter((file) =>
          inputFile?.hash && file?.hash
            ? inputFile?.hash !== file?.hash
            : file !== inputFile,
        );
      setValue(field.name, filtered, { shouldDirty: true });
    },
    [setValue, values],
  );

  const multiHandleRemoveAllFiles = useCallback(
    (field) => {
      setValue(field.name, [], { shouldDirty: true });
    },
    [setValue],
  );

  const renderField = (field, index) => {
    switch (field.type) {
      case "number":
      case "string":
      case "email":
        return (
          <RHFTextField
            sx={{ marginTop: 0 }}
            helperText={field.helperText}
            {...(field.rules?.depend !== undefined && {
              depend: field.rules.depend,
            })}
            multiline={!!field.multiline}
            control={control}
            fullWidth
            type={field.type === "string" ? "text" : field.type}
            margin="dense"
            variant="outlined"
            name={field.name}
            label={field.label}
            disabled={field.disabled}
          />
        );
      case "contact":
        return (
          <RHFContactField
            name={field.name}
            label={field.label}
            defaultCountry="IN"
            control={control}
          />
        );
      case "password":
        return (
          <RHFPasswordField
            sx={{ marginTop: 0 }}
            helperText={field.helperText}
            {...(field.rules?.depend !== undefined && {
              depend: field.rules.depend,
            })}
            control={control}
            fullWidth
            margin="dense"
            variant="outlined"
            name={field.name}
            label={field.label}
          />
        );
      case "select":
        return (
          // <AutoCompleteBox control={control} setValue={setValue} field={field} onField={onField} />
          <CustomAutoCompleteBox
            control={control}
            field={field}
            options={field.options || []}
            helperText={field.helperText}
            disabled={field.disabled}
          />
        );
      case "league_autocomplete":
        return (
          <RHFCustomLeagueAutocomplete
            key={field.name}
            name={field.name}
            label={field.label}
            options={field.options || []}
            control={control}
            fullWidth
            disabled={field.disabled}
          />
          //  <RHFCustomLeagueAutocomplete
          //     control={control}
          //     field={field}
          //     options={field.options}
          // />
          //  <AutoSelectCountry control={control} setValue={setValue} field={field} />
        );
      case "select_user":
        return (
          <UsersAutoComplete
            control={control}
            setValue={setValue}
            field={field}
            onField={findUsers}
            disabled={field.disabled}
          />
        );
      case "select_country":
        return (
          <AutoSelectCountry
            control={control}
            setValue={setValue}
            field={field}
            disabled={field.disabled}
          />
        );
      case "pre_select":
        return (
          <RHFSelect
            fullWidth
            control={control}
            name={field.name}
            label={field.label}
            disabled={field.disabled}
          >
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
      case "boolean":
        if (field.name === "publish_now" && dialog.value !== "create") {
          return null;
        }
        return (
          <RHFSwitch control={control} label={field.label} name={field.name} disabled={field.disabled} />
        );

      case "file":
        return (
          <Stack spacing={1.5}>
            <Typography
              variant="subtitle2"
              sx={{
                fontWeight: 600,
                color: 'text.primary',
              }}
            >
              {field.label}
            </Typography>
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
                sx={{
                  border: (theme) => `2px dashed ${alpha(theme.palette.primary.main, 0.3)}`,
                  borderRadius: 2,
                  '&:hover': {
                    borderColor: 'primary.main',
                    bgcolor: (theme) => alpha(theme.palette.primary.main, 0.04),
                  },
                }}
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
                sx={{
                  border: (theme) => `2px dashed ${alpha(theme.palette.primary.main, 0.3)}`,
                  borderRadius: 2,
                  '&:hover': {
                    borderColor: 'primary.main',
                    bgcolor: (theme) => alpha(theme.palette.primary.main, 0.04),
                  },
                }}
              />
            )}
          </Stack>
        );
      case "display":
        return (
          <TextField
            disable="true"
            fullWidth
            margin="dense"
            variant="filled"
            label={field.label}
            value={field.value}
            disabled={field.disabled}
          />
        );
      case "date_picker":
        return (
          <RHFDatePicker
            fullWidth
            control={control}
            label={field.label}
            name={field.name}
            disabled={field.disabled}
          />
        );
      case "date_time_picker":
        return (
          <RHFDateTimePicker
            fullWidth
            helperText={field.helperText}
            control={control}
            label={field.label}
            name={field.name}
            disabled={field.disabled}
          />
        );
      case "goalscorers":
        return <GoalscorersComponent control={control} name={field.name} disabled={field.disabled} />;
      case "players_to_watch":
        return <PlayersToWatchComponent control={control} name={field.name} disabled={field.disabled} />;
      default:
        return null;
    }
  };

  return (
    <FormProvider methods={methods} onSubmit={onSubmit}>
      <Grid
        container
        rowSpacing={3}
        columnSpacing={{ xs: 2, md: 3 }}
        alignItems="start"
        sx={{
          '& .MuiTextField-root': {
            '& .MuiOutlinedInput-root': {
              '&:hover fieldset': {
                borderColor: 'primary.main',
              },
            },
          },
        }}
      >
        {fields.map((field, index) => (index === 0 ? null : (
          <Grid
            item
            {...(field.props ? field.props : commonStyle || { xs: 12 })}
            key={index}
          >
            {isLoading ? (
              <Skeleton
                variant="rectangular"
                height={60}
                sx={{ borderRadius: 1 }}
              />
            ) : (
              <FormControl sx={{ width: "100%" }}>
                {renderField(field, index)}
              </FormControl>
            )}
          </Grid>
        )))}
      </Grid>

      <Stack
        direction="row"
        alignItems="center"
        justifyContent="end"
        gap={2}
        mt={4}
        sx={{
          display: disabled ? "none" : "flex",
          pt: 2,
          borderTop: (theme) => `1px solid ${alpha(theme.palette.divider, 0.5)}`,
        }}
      >
        <Button
          onClick={handleClose}
          variant="outlined"
          color="inherit"
          sx={{
            px: 3,
            fontWeight: 600,
            color: 'text.secondary',
            borderColor: 'divider',
            '&:hover': {
              borderColor: 'text.secondary',
              bgcolor: (theme) => alpha(theme.palette.grey[500], 0.08),
            },
          }}
        >
          Cancel
        </Button>
        <LoadingButton
          disabled={!isDirty}
          loading={isSubmitting}
          type="submit"
          variant="contained"
          color="primary"
          sx={{
            px: 4,
            py: 1.5,
            fontWeight: 600,
            boxShadow: (theme) => theme.customShadows?.primary || 2,
            '&:hover': {
              boxShadow: (theme) => theme.customShadows?.primaryHover || 4,
            },
            '&.Mui-disabled': {
              bgcolor: (theme) => alpha(theme.palette.primary.main, 0.3),
              color: (theme) => alpha(theme.palette.primary.contrastText, 0.6),
            },
          }}
        >
          Generate
          {/* {dialog?.mode === "edit" ? "Save" : "Generate"} */}
        </LoadingButton>
      </Stack>
      <GlobalLoader open={isSubmitting} />
    </FormProvider>
  );
}
