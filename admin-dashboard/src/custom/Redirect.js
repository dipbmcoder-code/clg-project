'use client';

import { useRouter } from 'src/routes/hooks';

import { SplashScreen } from 'src/components/loading-screen';

export default function Redirect({ url }) {
  const router = useRouter();
  router.push(url);
  return <SplashScreen />;
}
