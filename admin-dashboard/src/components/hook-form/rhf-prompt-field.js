import PropTypes from 'prop-types';
import { Controller } from 'react-hook-form';
import { useRef, useState, useEffect, useCallback } from 'react';

import { alpha } from '@mui/material/styles';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import {
    Box,
    Menu,
    Stack,
    Button,
    Divider,
    Tooltip,
    MenuItem,
    TextField,
    Typography,
    IconButton,
} from '@mui/material';

import useCustomSnackbar from 'src/hooks/use-custom-snackbar';

import { CopyClipboard } from 'src/utils/icons';

// ----------------------------------------------------------------------

export default function RHFPromptField({ depend, name, control, helperText, rows = 4, variables = [], rules, ...other }) {
    const { customSnackbarAction } = useCustomSnackbar();

    const [adornment, setAdornment] = useState({
        prefix: false,
        suffix: false,
    });

    const [anchorEl, setAnchorEl] = useState(null);

    const inputRef = useRef(null);

    const handleOpenVariables = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleCloseVariables = () => {
        setAnchorEl(null);
    };

    const handleCopyVariable = (variable) => {
        const textToCopy = `{ ${variable} }`;
        navigator.clipboard.writeText(textToCopy).then(() => {
            customSnackbarAction(`Copied: ${textToCopy}`, 'success');
        }).catch((err) => {
            console.error('Could not copy text: ', err);
            customSnackbarAction('Failed to copy variable', 'error');
        });
    };

    const dependField = control?._getWatch(depend?.fieldName);

    useEffect(() => {
        if (depend) {
            const conditionMatch = depend.conditions.find((condition) => condition.value === dependField);
            setAdornment({
                prefix: conditionMatch?.prefix || false,
                suffix: conditionMatch?.suffix || false,
            });
        }
    }, [depend, dependField]);

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.stopPropagation();
        }
    };

    const handleVariableClick = (variable, field) => {
        const input = inputRef.current;
        if (!input) return;

        const start = input.selectionStart;
        const end = input.selectionEnd;
        const value = field.value || '';
        const newValue = `${value.substring(0, start)}{ ${variable} }${value.substring(end)}`;

        field.onChange(newValue);

        setTimeout(() => {
            input.focus();
            const newPos = start + variable.length + 4;
            input.setSelectionRange(newPos, newPos);
        }, 0);
    };

    const validateVariables = useCallback((value) => {
        if (!value || variables.length === 0) return true;
        const regex = /\{(.*?)\}/g;
        let match = regex.exec(value);
        while (match !== null) {
            const varName = match[1].trim();
            if (!variables.includes(varName)) {
                return `Invalid variable: { ${varName} }. Allowed variables are: ${variables.join(', ')}`;
            }
            match = regex.exec(value);
        }
        return true;
    }, [variables]);

    return (
        <Controller
            name={name}
            control={control}
            rules={{
                ...rules,
                validate: {
                    validVariables: validateVariables,
                    ...rules?.validate,
                },
            }}
            render={({ field, fieldState: { error } }) => (
                <Box>
                    <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 1.5 }}>
                        <Typography variant="subtitle2" sx={{ color: 'text.secondary', fontWeight: 700, mr: 2, flexGrow: 1 }}>
                            {other.label}
                        </Typography>

                        {variables.length > 0 && (
                            <>
                                <Button
                                    size="small"
                                    color="primary"
                                    onClick={handleOpenVariables}
                                    endIcon={<ArrowDropDownIcon />}
                                    sx={{
                                        fontSize: '0.75rem',
                                        fontWeight: 700,
                                        py: 0.5,
                                        px: 1.5,
                                        borderRadius: 0.75,
                                        bgcolor: (theme) => alpha(theme.palette.primary.main, 0.1),
                                        '&:hover': {
                                            bgcolor: (theme) => alpha(theme.palette.primary.main, 0.2),
                                        },
                                    }}
                                >
                                    Variables
                                </Button>

                                <Menu
                                    anchorEl={anchorEl}
                                    open={Boolean(anchorEl)}
                                    onClose={handleCloseVariables}
                                    anchorOrigin={{
                                        vertical: 'bottom',
                                        horizontal: 'right',
                                    }}
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    PaperProps={{
                                        sx: {
                                            minWidth: 200,
                                            maxWidth: 320,
                                            maxHeight: 400,
                                            mt: 0.5,
                                        }
                                    }}
                                >
                                    <Box sx={{ px: 2, py: 1 }}>
                                        <Typography variant="subtitle2" sx={{ color: 'text.secondary' }}>
                                            Variables
                                        </Typography>
                                    </Box>
                                    <Divider sx={{ borderStyle: 'dashed' }} />
                                    {variables.map((variable) => (
                                        <MenuItem
                                            key={variable}
                                            sx={{
                                                justifyContent: 'space-between',
                                                '&:hover .copy-button': {
                                                    opacity: 1,
                                                }
                                            }}
                                            onClick={() => {
                                                handleVariableClick(variable, field);
                                                handleCloseVariables();
                                            }}
                                        >
                                            <Typography variant="body2" sx={{ fontWeight: 500, mr: 2 }}>
                                                {`{ ${variable} }`}
                                            </Typography>

                                            <Tooltip title="Copy Variable" placement="left">
                                                <IconButton
                                                    className="copy-button"
                                                    size="small"
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        handleCopyVariable(variable);
                                                    }}
                                                    sx={{
                                                        opacity: 0,
                                                        transition: (theme) => theme.transitions.create('opacity'),
                                                        color: 'primary.main',
                                                        '&:hover': {
                                                            bgcolor: (theme) => alpha(theme.palette.primary.main, 0.08),
                                                        }
                                                    }}
                                                >
                                                    <CopyClipboard sx={{ width: 16, height: 16 }} />
                                                </IconButton>
                                            </Tooltip>
                                        </MenuItem>
                                    ))}
                                </Menu>
                            </>
                        )}
                    </Stack>

                    <TextField
                        {...field}
                        fullWidth
                        multiline
                        rows={rows}
                        value={field.value === null || field.value === undefined ? '' : field.value}
                        error={!!error}
                        helperText={error ? error?.message : helperText}
                        onKeyDown={handleKeyDown}
                        inputRef={inputRef}
                        InputProps={{
                            startAdornment: <>{!!adornment.prefix && adornment.prefix}</>,
                            endAdornment: <>{!!adornment.suffix && adornment.suffix}</>,
                            sx: {
                                '& textarea': {
                                    color: (theme) => theme.palette.text.primary,
                                },
                            }
                        }}
                        {...other}
                        label={null}
                    />
                </Box>
            )}
        />
    );
}

RHFPromptField.propTypes = {
    control: PropTypes.oneOfType([PropTypes.object, PropTypes.any]),
    helperText: PropTypes.string,
    name: PropTypes.string,
    rows: PropTypes.number,
    depend: PropTypes.oneOfType([PropTypes.object, PropTypes.any]),
    variables: PropTypes.oneOfType([PropTypes.array, PropTypes.any]),
    rules: PropTypes.oneOfType([PropTypes.object, PropTypes.any]),
};
