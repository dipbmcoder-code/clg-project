'use client';

import { useEffect } from 'react';

import { useRouter } from 'src/routes/hooks';
import { getRootPath } from 'src/routes/paths';

import { useAuthContext } from 'src/auth/hooks';

import { SplashScreen } from 'src/components/loading-screen';
// ----------------------------------------------------------------------

export default function HomePage() {
  const router = useRouter();
  const { user, loading } = useAuthContext();
  useEffect(() => {
    if (!loading) {
      const returnTo = getRootPath(user?.roles);
      router.push(returnTo);
    }
  }, [loading]);

  return loading ? <SplashScreen /> : null;
}
