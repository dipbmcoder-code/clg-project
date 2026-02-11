'use client';

import { useMemo, useState } from 'react';

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import Chip from '@mui/material/Chip';
import { alpha } from '@mui/material/styles';
import { Box, Stack, Container, Typography } from '@mui/material';
import { BackButton } from 'src/custom';

import { DataGridTable } from 'src/custom/index';
import { gridClasses } from '@mui/x-data-grid';

import Label from 'src/components/label';
import { useSettingsContext } from 'src/components/settings';
import { fDate, fTime } from 'src/utils/format-time';

// Icons
import ArticleIcon from '@mui/icons-material/Article';
import LanguageIcon from '@mui/icons-material/Language';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import InfoIcon from '@mui/icons-material/Info';

function NewsLog({ data }) {
    const settings = useSettingsContext();
    const [refreshDataGrid, setRefreshDataGrid] = useState(false);

    // Parse log messages if they're in JSON format
    const logMessages = useMemo(() => {
        if (!data?.log_message?.messages) return [];

        try {
            // If log_messages is a string, parse it
            if (typeof data.log_message?.messages === 'string') {
                return JSON.parse(data.log_message?.messages);
            }
            // If it's already an array, return it
            if (Array.isArray(data.log_message?.messages)) {
                return data.log_message?.messages;
            }
            return [];
        } catch (error) {
            console.error('Error parsing log messages:', error);
            return [];
        }
    }, [data?.log_message?.messages]);
    // Define columns for log messages grid
    const messageColumns = [
        {
            field: 'id',
            headerName: '#',
            width: 50,
            filterable: false,
            renderCell: (params) => {
                return (
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {params.api.getAllRowIds().indexOf(params.id) + 1}
                    </Typography>
                );
            },
        },
        {
            field: 'message',
            headerName: 'Message',
            flex: 1,
            minWidth: 300,
            filterable: false,
            renderCell: (params) => {
                const { value } = params;
                return (
                    <Typography
                        variant="body2"
                        sx={{
                            whiteSpace: 'normal',
                            wordWrap: 'break-word',
                            py: 1,
                        }}
                    >
                        {value || 'N/A'}
                    </Typography>
                );
            },
        },
        {
            field: 'error',
            headerName: 'Error Details',
            flex: 1,
            minWidth: 300,
            filterable: false,
            renderCell: (params) => {
                const { value } = params;
                return (
                    <Typography
                        variant="body2"
                        sx={{
                            whiteSpace: 'normal',
                            wordWrap: 'break-word',
                            py: 1,
                        }}
                    >
                        {value}
                    </Typography>
                );
            },
        },
        {
            field: 'status',
            headerName: 'Message Status',
            width: 150,
            filterable: false,
            renderCell: (params) => {
                const { value } = params;
                const statusLower = value?.toLowerCase() || '';

                let color = 'default';
                if (statusLower === 'success' || statusLower === 'completed' || statusLower === 'published') {
                    color = 'success';
                } else if (statusLower === 'error' || statusLower === 'failed') {
                    color = 'error';
                } else if (statusLower === 'warning' || statusLower === 'pending') {
                    color = 'warning';
                } else if (statusLower === 'info' || statusLower === 'processing') {
                    color = 'info';
                }

                return value ? (
                    <Label color={color}>
                        {value}
                    </Label>
                ) : (
                    <Typography variant="body2" color="text.secondary">
                        N/A
                    </Typography>
                );
            },
        },
    ];

    // Prepare data for the grid
    const messagesData = useMemo(() => {
        return {
            results: logMessages?.map((msg, index) => ({
                id: index,
                message: msg.message || msg.msg || msg.text || '',
                status: msg.status || msg.state || '',
                error: msg.error_details || '',
            })),
            pagination: {
                page: 1,
                pageSize: logMessages?.length,
                pageCount: 1,
                total: logMessages?.length,
            },
        };
    }, [logMessages]);
    const memoizedMessagesGrid = useMemo(
        () => (
            <DataGridTable
                data={messagesData}
                columns={messageColumns}
                refresh={refreshDataGrid}
                hideFooter={true}
                disableColumnMenu={true}
                sx={{
                    [`& .${gridClasses.cell}`]: {
                        py: 1.5,
                    },
                    minHeight: 300,
                }}
            />
        ),
        [messagesData, refreshDataGrid]
    );

    // Get status color
    const getStatusColor = (status) => {
        const statusLower = status?.toLowerCase() || '';
        if (statusLower === 'published' || statusLower === 'success') return 'success';
        if (statusLower === 'failed' || statusLower === 'error') return 'error';
        if (statusLower === 'pending' || statusLower === 'processing') return 'warning';
        return 'info';
    };

    return (
        <>
            <Container maxWidth={settings.themeStretch ? false : 'xl'}>
                <Box
                    sx={{
                        display: 'flex',
                        gap: 2,
                        alignItems: 'center',
                        mb: 3,
                    }}
                >
                    <BackButton />
                    <Typography variant="h4">News Log Details</Typography>
                </Box>

                {/* Log Information Card */}
                <Card
                    sx={{
                        mb: 3,
                        boxShadow: (theme) => theme.customShadows.card,
                    }}
                >
                    <CardContent sx={{ p: 3 }}>
                        <Grid container spacing={3}>
                            {/* Log Type */}
                            <Grid item xs={12} sm={6} md={3}>
                                <Stack spacing={1}>
                                    <Stack direction="row" spacing={1} alignItems="center">
                                        <ArticleIcon sx={{ color: 'text.secondary', fontSize: 20 }} />
                                        <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                            Log Type
                                        </Typography>
                                    </Stack>
                                    <Chip
                                        label={data?.news_type?.toUpperCase() || 'N/A'}
                                        color="primary"
                                        variant="outlined"
                                        size="small"
                                        sx={{ width: 'fit-content', fontWeight: 600 }}
                                    />
                                </Stack>
                            </Grid>

                            {/* Website Name */}
                            <Grid item xs={12} sm={6} md={3}>
                                <Stack spacing={1}>
                                    <Stack direction="row" spacing={1} alignItems="center">
                                        <LanguageIcon sx={{ color: 'text.secondary', fontSize: 20 }} />
                                        <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                            Website
                                        </Typography>
                                    </Stack>
                                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                        {data?.website_name || 'N/A'}
                                    </Typography>
                                </Stack>
                            </Grid>

                            {/* Log Time */}
                            <Grid item xs={12} sm={6} md={3}>
                                <Stack spacing={1}>
                                    <Stack direction="row" spacing={1} alignItems="center">
                                        <AccessTimeIcon sx={{ color: 'text.secondary', fontSize: 20 }} />
                                        <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                            Log Time
                                        </Typography>
                                    </Stack>
                                    <Stack>
                                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                            {data?.log_time ? fDate(new Date(data.log_time)) : 'N/A'}
                                        </Typography>
                                        <Typography variant="caption" color="text.secondary">
                                            {data?.log_time ? fTime(new Date(data.log_time)) : ''}
                                        </Typography>
                                    </Stack>
                                </Stack>
                            </Grid>

                            {/* News Status */}
                            <Grid item xs={12} sm={6} md={3}>
                                <Stack spacing={1}>
                                    <Stack direction="row" spacing={1} alignItems="center">
                                        <InfoIcon sx={{ color: 'text.secondary', fontSize: 20 }} />
                                        <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                            News Status
                                        </Typography>
                                    </Stack>
                                    {data?.news_status ? (
                                        <Label color={getStatusColor(data.news_status)} sx={{ width: 'fit-content' }}>
                                            {data.news_status}
                                        </Label>
                                    ) : (
                                        <Typography variant="body2" color="text.secondary">
                                            N/A
                                        </Typography>
                                    )}
                                </Stack>
                            </Grid>

                            {/* Log Title - Full Width */}
                            <Grid item xs={12}>
                                <Divider sx={{ my: 1 }} />
                                <Stack spacing={1} sx={{ mt: 2 }}>
                                    <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                        Log Title
                                    </Typography>
                                    <Typography variant="h6" sx={{ fontWeight: 500 }}>
                                        {data?.title || 'No title available'}
                                    </Typography>
                                </Stack>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>

                {/* Log Messages Grid */}
                <Card
                    sx={{
                        boxShadow: (theme) => theme.customShadows.card,
                    }}
                >
                    <CardContent sx={{ p: 3 }}>
                        <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                            Log Messages
                        </Typography>
                        <Divider sx={{ mb: 3 }} />

                        {logMessages.length > 0 ? (
                            <Box
                                sx={{
                                    width: 1,
                                    borderRadius: 1,
                                    bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
                                    border: (theme) => `solid 1px ${theme.palette.divider}`,
                                }}
                            >
                                {memoizedMessagesGrid}
                            </Box>
                        ) : (
                            <Box
                                sx={{
                                    py: 8,
                                    textAlign: 'center',
                                    borderRadius: 1,
                                    bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
                                    border: (theme) => `dashed 1px ${theme.palette.divider}`,
                                }}
                            >
                                <Typography variant="body1" color="text.secondary">
                                    No log messages available
                                </Typography>
                            </Box>
                        )}
                    </CardContent>
                </Card>
            </Container>
        </>
    );
}
export default NewsLog;
