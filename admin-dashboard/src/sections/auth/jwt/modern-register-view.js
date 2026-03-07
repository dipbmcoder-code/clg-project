'use client';

import * as Yup from 'yup';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import Alert from '@mui/material/Alert';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import LoadingButton from '@mui/lab/LoadingButton';
import InputAdornment from '@mui/material/InputAdornment';

import { paths } from 'src/routes/paths';
import { RouterLink } from 'src/routes/components';

import { useBoolean } from 'src/hooks/use-boolean';

import { useAuthContext } from 'src/auth/hooks';

import Iconify from 'src/components/iconify';
import FormProvider, { RHFTextField } from 'src/components/hook-form';

// ----------------------------------------------------------------------

export default function ModernRegisterView() {
    const password = useBoolean();
    const { register } = useAuthContext();
    const [errorMsg, setErrorMsg] = useState('');

    const RegisterSchema = Yup.object().shape({
        firstname: Yup.string().required('First name is required').min(1, 'First name is required'),
        lastname: Yup.string().required('Last name is required').min(1, 'Last name is required'),
        email: Yup.string().required('Email is required').email('Email must be a valid email address'),
        password: Yup.string()
            .required('Password is required')
            .min(6, 'Password must be at least 6 characters'),
    });

    const defaultValues = {
        firstname: '',
        lastname: '',
        email: '',
        password: '',
    };

    const methods = useForm({
        resolver: yupResolver(RegisterSchema),
        defaultValues,
    });

    const {
        reset,
        handleSubmit,
        formState: { isSubmitting },
    } = methods;

    const onSubmit = handleSubmit(async (data) => {
        try {
            await register?.(data.firstname, data.lastname, data.email, data.password);
        } catch (error) {
            reset();

            // Handle various error shapes from axios interceptor
            if (typeof error === 'string') {
                setErrorMsg(error);
            } else if (error?.error?.message) {
                setErrorMsg(error.error.message);
            } else if (error?.message) {
                setErrorMsg(error.message);
            } else {
                setErrorMsg('Something went wrong. Please try again later.');
            }
        }
    });

    const renderHead = (
        <Stack spacing={2} sx={{ mb: 5 }}>
            <Typography variant="h4">Create your account</Typography>

            <Stack direction="row" spacing={0.5}>
                <Typography variant="body2">Already have an account?</Typography>

                <Link
                    component={RouterLink}
                    href={paths.auth.login}
                    variant="subtitle2"
                    sx={{ color: 'primary.main' }}
                >
                    Sign in
                </Link>
            </Stack>
        </Stack>
    );

    const renderForm = (
        <Stack spacing={2.5}>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                <RHFTextField name="firstname" label="First name" />
                <RHFTextField name="lastname" label="Last name" />
            </Stack>

            <RHFTextField name="email" label="Email address" />

            <RHFTextField
                name="password"
                label="Password"
                type={password.value ? 'text' : 'password'}
                InputProps={{
                    endAdornment: (
                        <InputAdornment position="end">
                            <IconButton onClick={password.onToggle} edge="end">
                                <Iconify icon={password.value ? 'solar:eye-bold' : 'solar:eye-closed-bold'} />
                            </IconButton>
                        </InputAdornment>
                    ),
                }}
            />

            <LoadingButton
                fullWidth
                color="inherit"
                size="large"
                type="submit"
                variant="contained"
                loading={isSubmitting}
                endIcon={<Iconify icon="eva:arrow-ios-forward-fill" />}
                sx={{ justifyContent: 'space-between', pl: 2, pr: 1.5 }}
            >
                Create Account
            </LoadingButton>
        </Stack>
    );

    return (
        <>
            {!!errorMsg && (
                <Alert severity="error" sx={{ mb: 3 }}>
                    {errorMsg}
                </Alert>
            )}
            <FormProvider methods={methods} onSubmit={onSubmit}>
                {renderHead}

                {renderForm}
            </FormProvider>
        </>
    );
}
