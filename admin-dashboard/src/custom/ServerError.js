'use client';

import { useState } from 'react';
import { m } from 'framer-motion';

import Button from '@mui/material/Button';
import SvgIcon from '@mui/material/SvgIcon';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';

import { useRouter } from 'src/routes/hooks';

import {
  ForbiddenIllustration,
  SeverErrorIllustration,
  PageNotFoundIllustration,
} from 'src/assets/illustrations';

import { varBounce, MotionContainer } from 'src/components/animate';

function HomeIcon(props) {
  return (
    <SvgIcon {...props}>
      <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
    </SvgIcon>
  );
}
export default function ServerError({ error = { status: 500 } }) {
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const handleSubmit = () => {
    router.back();
  };

  return (
    <Container component={MotionContainer} sx={{ textAlign: 'center' }}>
        <m.div variants={varBounce().in}>
          <Typography variant="h3" sx={{ mb: 2 }}>
            {(() => {
              switch (error.status) {
                case 403:
                  return 'Permission Denied';
                case 404:
                  return 'Not Found';
                default:
                  return 'Something Went Wrong..!';
              }
            })()}
          </Typography>
        </m.div>
        {error.status === 403 && (
          <m.div variants={varBounce().in}>
            <Typography sx={{ color: 'text.secondary' }}>
              You do not have permission to access this page
            </Typography>
          </m.div>
        )}

        <m.div variants={varBounce().in}>
          {(() => {
            switch (error.status) {
              case 403:
                return (
                  <ForbiddenIllustration
                    sx={{
                      height: 260,
                      my: { xs: 5, sm: 10 },
                    }}
                  />
                );
              case 404:
                return (
                  <PageNotFoundIllustration
                    sx={{
                      height: 260,
                      my: { xs: 5, sm: 10 },
                    }}
                  />
                );
              default:
                return (
                  <SeverErrorIllustration
                    sx={{
                      height: 260,
                      my: { xs: 5, sm: 10 },
                    }}
                  />
                );
            }
          })()}
        </m.div>
        <m.div variants={varBounce().in}>
          <Button
            variant="outlined"
            sx={{
              gap: 1,
            }}
            onClick={handleSubmit}
          >
            <Typography sx={{ color: 'text.primary' }}>GO BACK</Typography>
          </Button>
        </m.div>
      </Container>
  );
}
