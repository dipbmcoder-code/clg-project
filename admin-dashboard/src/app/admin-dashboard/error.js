'use client';

import { ServerError } from 'src/custom';

export default function ErrorBoundry({ error }) {
  return <ServerError />;
}
