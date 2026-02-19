'use server';

import { cookies } from 'next/headers';

import { endpoints } from './axios';

async function authoraizeRequest() {
  const cookieStore = await cookies();
  const token = await cookieStore.get('accessToken');
  if (!token || !token.value) {
    return false;
  }
  return token.value;
}
export async function upload(data) {
  const isValid = await authoraizeRequest();
  if (!isValid) {
    return {
      error: 'Unauthorized',
    };
  }
  const mergedOptions = {
    headers: {
      Authorization: `Bearer ${isValid}`,
    },
    method: 'POST',
    body: data,
  };
  //
  try {
    const response = await fetch(endpoints.assets.upload, mergedOptions);
    const res = await response.json();
    return res;
  } catch (error) {
    return error;
  }
}

export async function fetchAPI(url, options = {}) {
  const isValid = await authoraizeRequest();
  if (!isValid) {
    return {
      error: 'Unauthorized',
    };
  }
  try {
    const mergedOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${isValid}`,
      },
      ...options,
    };

    // Trigger API call
    const response = await fetch(url, mergedOptions);
    const data = await response.json();

    return data;
  } catch (error) {
    return error;
  }
}
export async function editAction(url, data) {
  const isValid = await authoraizeRequest();
  if (!isValid) {
    return {
      error: 'Unauthorized',
    };
  }
  try {
    const putOptions = {
      method: 'PUT',
      body: data,
    };

    // Make a PUT request using fetchAPI function
    const putResponse = await fetchAPI(url, putOptions);
    return putResponse;
  } catch (error) {
    return error;
  }
}
export async function createAction(url, data) {
  try {
    const postOptions = {
      method: 'POST',
      body: data,
    };

    const postResponse = await fetchAPI(url, postOptions);

    return postResponse;
  } catch (error) {
    return error;
  }
}
export async function deleteAction(url) {
  try {
    const fixOptions = {
      method: 'DELETE',
    };
    const putResponse = await fetchAPI(url, fixOptions);
    return putResponse;
  } catch (error) {
    return error;
  }
}
export async function deleteAssets(data) {
  try {
    const fixOptions = {
      method: 'POST',
      body: data,
    };
    // Bulk delete assets via backend
    const response = await fetchAPI(`${HOST_API}/api/upload/bulk-delete`, fixOptions);
    return response;
  } catch (error) {
    return error;
  }
}
