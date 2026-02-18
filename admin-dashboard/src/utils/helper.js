'use server';

import { cookies } from 'next/headers';
import { HOST_API } from 'src/config-global';

/**
 * Get auth token from cookies.
 */
async function getAuthToken() {
  const cookieStore = await cookies();
  const token = await cookieStore.get('accessToken');
  if (!token || !token.value) return false;
  return token.value;
}

/**
 * Make an authenticated API request to the Node.js backend.
 */
export async function fetchAPI(url, options = {}) {
  const token = await getAuthToken();
  if (!token) return { error: 'Unauthorized' };

  try {
    const fullUrl = url.startsWith('http') ? url : `${HOST_API}${url}`;
    const mergedOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      cache: 'no-store',
      ...options,
    };

    const response = await fetch(fullUrl, mergedOptions);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('fetchAPI error:', error);
    return { error: 'Request failed' };
  }
}

/**
 * PUT request helper.
 */
export async function editAction(url, data) {
  return fetchAPI(url, { method: 'PUT', body: data });
}

/**
 * POST request helper.
 */
export async function createAction(url, data) {
  return fetchAPI(url, { method: 'POST', body: data });
}

/**
 * DELETE request helper.
 */
export async function deleteAction(url) {
  return fetchAPI(url, { method: 'DELETE' });
}
