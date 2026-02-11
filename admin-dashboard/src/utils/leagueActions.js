'use server';

import { endpoints } from 'src/utils/axios';
import {
  upload,
  fetchAPI,
  editAction,
  createAction,
  deleteAssets,
} from 'src/utils/helper';

export async function findLeagues() {
  try {
    const url = endpoints.rapidapi.getLeagues();
    const res = await fetchAPI(url);
    if (res.leagues) {
      return res.leagues
    }

    return res;
  } catch (error) {
    return error;
  }
}

export async function findPlayers(searchText) {
  try {
    const url = endpoints.rapidapi.getPlayers(searchText);
    const res = await fetchAPI(url);
    if (res.data) {
      return res.data
    }

    return res;
  } catch (error) {
    return error;
  }
}

export async function createUser(data, formData) {
  const url = endpoints.admin.getUsers({});
  const decodedData = decodeURIComponent(data);
  const parsedData = JSON.parse(decodedData);

  if (parsedData.roles && Array.isArray(parsedData.roles) && parsedData.roles.length > 0) {
    parsedData.roles = parsedData.roles.filter((role) => role !== 1);
  }
  const stringifyData = JSON.stringify(parsedData);
  const res = await createAction(url, stringifyData);

  return res;
}
export async function editUser(data, formData, id) {
  const url = endpoints.admin.getUsers({ id });
  const decodedData = decodeURIComponent(data);
  const parsedData = JSON.parse(decodedData);
  delete parsedData.id;
  delete parsedData.confirm_password;
  if (parsedData.roles && Array.isArray(parsedData.roles) && parsedData.roles.length > 0) {
    parsedData.roles = parsedData.roles.filter((role) => role !== 1);
  }

  if (parsedData._files) {
    try {
      const allRemovedFiles = Object.values(parsedData._files).flat();
      if (allRemovedFiles.length) {
        const data = JSON.stringify({ fileIds: allRemovedFiles });
        const delres = await deleteAssets(data);
      }

      await Promise.all(
        Object.keys(parsedData._files).map(async (key) => {
          let isUpload = false;
          const uploadData = new FormData();
          if (formData) {
            for (const value of formData.getAll(key)) {
              uploadData.append('files', value);
              isUpload = true;
            }
          }

          if (isUpload) {
            try {
              const uploadFile = await upload(uploadData);
              if (Array.isArray(parsedData[key]) && Array.isArray(uploadFile)) {
                parsedData[key] = [...parsedData[key], ...uploadFile];
              } else if (parsedData[key] === null && Array.isArray(uploadFile)) {
                parsedData[key] = uploadFile[0].id;
              }
            } catch (error) {
              console.error('Error in upload:', error);
            }
          }
        })
      );
      delete parsedData._files;
      const profileFields = ['profilePicture'];

      parsedData.profile = {};

      profileFields.forEach((field) => {
        if (parsedData.hasOwnProperty(field)) {
          parsedData.profile[field] = parsedData[field];
          delete parsedData[field];
        }
      });

      const stringifyData = JSON.stringify(parsedData);
      const res = await editAction(url, stringifyData);
      return res;
    } catch (error) {
      console.error('Error in editData:', error);
    }
  } else {
    const stringifyData = JSON.stringify(parsedData);
    const res = await editAction(url, stringifyData);
    return res;
  }
}
export async function getRoles(qryParams) {
  const { query, option, option_val } = qryParams;
  const url = endpoints.admin.getRoles({ query });
  const res = await fetchAPI(url);
  const fields = res.data
    .filter((item) => item[option_val] !== 'strapi-super-admin' && item.id !== 1)
    .map((item) => ({
      label: item[option],
      value: item[option_val] || item.id,
    }));
  return fields;
}