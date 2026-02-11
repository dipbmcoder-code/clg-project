import PropTypes from 'prop-types';
import { useEffect, useCallback } from 'react';

import { getRootPath } from 'src/routes/paths';
import { useRouter, useSearchParams } from 'src/routes/hooks';

import { SplashScreen } from 'src/components/loading-screen';

import { useAuthContext } from '../hooks';

// ----------------------------------------------------------------------

export default function GuestGuard({ children }) {
  return <Container> {children}</Container>;
}

GuestGuard.propTypes = {
  children: PropTypes.node,
};

// ----------------------------------------------------------------------

function Container({ children }) {
  const router = useRouter();
  const { authenticated, user, loading } = useAuthContext();
  const searchParams = useSearchParams();
  const returnTo = searchParams.get('returnTo');

  const check = useCallback(async () => {
    if (authenticated && user) {
      if (returnTo) {
        router.replace(returnTo);
      } else {
        router.replace(getRootPath(user?.roles));
      }
    }
  }, [authenticated, user, router]);

  useEffect(() => {
    const performCheck = async () => {
      await check();
    };

    performCheck();
  }, [check]);
  return <>{loading || authenticated ? <SplashScreen /> : <>{children}</>}</>;
}

Container.propTypes = {
  children: PropTypes.node,
};
