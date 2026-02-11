'use client';

import { Autocomplete, Box, Button, Dialog, DialogContent, DialogTitle, IconButton, List, ListItem, ListItemText, TextField, Chip, Tooltip, Typography, Divider } from "@mui/material";
import { alpha } from '@mui/material/styles';
import { GridCloseIcon } from "@mui/x-data-grid";
import { useEffect, useState } from "react";
import { DeleteIcon } from "src/utils/icons";

export const LeaguesCategoryPopup = ({ handle, data, action, categoriesOptions, handleChange }) => {
    const [category, setCategory] = useState([]);
    const [categories, setCategories] = useState([]);
    const [editIndex, setEditIndex] = useState(false);
    const [filteredOptions, setFilteredOptions] = useState([]);

    useEffect(() => {
        if (handle.value) {
            setFilteredOptions(categoriesOptions);
            const initialCategories = data?.find(league => league.id === handle.value)?.categories || [];
            setCategories(initialCategories);
        }
    }, [handle.value]);

    const addOrUpdateCategory = () => {
        setCategories([...categories, ...category]);
        data.map(league => {
            if (league.id === handle.value) {
                league.categories = [...categories, ...category];
            }
        });
        action(data);
        handleChange();
        setCategory([]);
        setEditIndex(false);
    };

    const deleteCategory = (index) => {
        setCategories(categories.filter((_, i) => i !== index));
        data.map(league => {
            if (league.id === handle.value) {
                league.categories = categories.filter((_, i) => i !== index);
            }
        });
        action(data);
        handleChange();
        if (editIndex === index) {
            setCategory('');
            setEditIndex(null);
        }
    };

    return (
        <Dialog
            open={handle.value}
            onClose={handle.onFalse}
            maxWidth="sm"
            fullWidth
            PaperProps={{
                sx: {
                    borderRadius: 2,
                    boxShadow: (theme) => theme.customShadows?.dialog || 24,
                }
            }}
        >
            <DialogTitle
                sx={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    px: 3,
                    pt: 2.5,
                    pb: 2,
                    borderBottom: (theme) => `1px solid ${alpha(theme.palette.divider, 0.5)}`,
                }}
            >
                <Typography
                    variant="h5"
                    sx={{
                        fontWeight: 700,
                        background: (theme) => `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                    }}
                >
                    Manage League Categories
                </Typography>
                <Tooltip title="Close" arrow>
                    <IconButton
                        aria-label="close"
                        onClick={handle.onFalse}
                        sx={{
                            color: (theme) => theme.palette.grey[500],
                            '&:hover': {
                                bgcolor: (theme) => alpha(theme.palette.grey[500], 0.08),
                            },
                        }}
                    >
                        <GridCloseIcon />
                    </IconButton>
                </Tooltip>
            </DialogTitle>
            <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 0, p: 3 }}>
                <Box display="flex" gap={1.5} my={2.5}>
                    <Autocomplete
                        //freeSolo // allows typing anything
                        options={filteredOptions}
                        openOnFocus
                        multiple
                        clearOnEscape
                        disableCloseOnSelect0
                        filterSelectedOptions
                        value={category}
                        getOptionLabel={(option) => option.name ?? option}
                        onChange={(e, newInputValue) => {
                            setCategory(newInputValue)
                        }}
                        sx={{ flexGrow: 1 }}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                fullWidth
                                size="small"
                                variant="outlined"
                                placeholder="Add new category..."
                                sx={{
                                    '& .MuiOutlinedInput-root': {
                                        '&:hover fieldset': {
                                            borderColor: 'primary.main',
                                        },
                                    },
                                }}
                            />
                        )}
                    />

                    <Button
                        variant="contained"
                        color="primary"
                        onClick={addOrUpdateCategory}
                        sx={{
                            px: 3,
                            fontWeight: 600,
                            boxShadow: (theme) => theme.customShadows?.primary || 2,
                            '&:hover': {
                                boxShadow: (theme) => theme.customShadows?.primaryHover || 4,
                            },
                        }}
                    >
                        {editIndex !== false ? 'Update' : 'Add'}
                    </Button>
                </Box>
                <Box sx={{ maxHeight: 320, overflowY: 'auto', mt: 0.5 }}>
                    {categories.length > 0 ? (
                        <List sx={{ p: 0, m: 0 }}>
                            {categories.map((t, i) => (
                                <ListItem
                                    key={i}
                                    sx={{
                                        backgroundColor: (theme) => alpha(theme.palette.primary.main, 0.08),
                                        mb: 1.5,
                                        py: 1.5,
                                        px: 2,
                                        borderRadius: 1.5,
                                        border: (theme) => `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                                        transition: 'all 0.2s ease-in-out',
                                        '&:hover': {
                                            backgroundColor: (theme) => alpha(theme.palette.primary.main, 0.12),
                                            // transform: 'translateX(4px)',
                                            boxShadow: (theme) => `0 2px 8px ${alpha(theme.palette.primary.main, 0.2)}`,
                                        },
                                        '&:last-child': {
                                            mb: 0,
                                        },
                                    }}
                                    secondaryAction={
                                        <Tooltip title="Delete Category" arrow>
                                            <IconButton
                                                edge="end"
                                                aria-label="delete"
                                                size="small"
                                                onClick={() => deleteCategory(i)}
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
                                    }
                                >
                                    <Chip
                                        label={t.name}
                                        size="small"
                                        color="primary"
                                        variant="outlined"
                                        sx={{
                                            fontWeight: 600,
                                            fontSize: '0.875rem',
                                        }}
                                    />
                                </ListItem>
                            ))}
                        </List>
                    ) : (
                        <Box
                            sx={{
                                textAlign: 'center',
                                py: 6,
                                px: 2,
                                color: 'text.secondary',
                            }}
                        >
                            <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                No categories added yet
                            </Typography>
                        </Box>
                    )}
                </Box>
            </DialogContent>
        </Dialog>
    );
};