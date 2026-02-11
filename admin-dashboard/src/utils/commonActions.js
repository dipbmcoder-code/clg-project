import { endpoints } from 'src/utils/axios';
import {
  upload,
  fetchAPI,
  editAction,
  createAction,
  deleteAction,
  deleteAssets,
} from 'src/utils/helper';
// Fetch data with given query parameters
export async function getData({ collection, fixParams, slug, parent, qryParams, filters = [] }) {
  const params = {
    ...qryParams,
    sort: qryParams.sort.map((option) => `${option.field}:${option.sort}`),
    filters: {
      $and: [...filters, ...(slug && parent ? [{ [parent]: { id: { $eq: slug } } }] : [])],
    },
  };

  const finalParams = { ...params, ...fixParams };
  const url = endpoints.findMany(collection, finalParams);
  const res = await fetchAPI(url);
  return res;
}

export async function getStatus({ collection, qryParamsData }) {
  const params = {
    ...qryParamsData,
    sort: qryParamsData.sort.map((option) => `${option.field}:${option.sort}`),
  };
  const finalParams = { ...params };
  const url = endpoints.findMany(collection, finalParams);
  const res = await fetchAPI(url);
  return res;
}

export async function editStatus({ collection, data }) {
  const decodedData = decodeURIComponent(data);
  let parsedData = JSON.parse(decodedData);
    const url = endpoints.findOne(collection, parsedData.id);
    const stringifyData = JSON.stringify(parsedData);
    const type = "PUT";
    const res = await editAction(url, stringifyData, type);
    return res;
}


export async function getActiveCount({ collection, slug, parent, id }) {
  const url = endpoints.findMany(collection);
  const res = await fetchAPI(url);
  if (!res.error) {
    return res;
  }
  return false;
}
export async function getEntry({ collection, slug, params }) {
  const url = endpoints.findOne(collection, slug, params);
  const res = await fetchAPI(url);
  return res;
}
// Generate parameters for field data requests
const generateFieldParams = (qryParams) => {
  const { query, id, populate, filters } = qryParams;
  return {
    entityId: id,
    populate,
    _q: query,
    pageSize: 50,
    page: 1,
    filters,
  };
};
// Fetch field data with specific parameters
export async function onField({ collection, qryParams }) {
  const { field, option, option_val, relation } = qryParams;
  const finalParams = generateFieldParams(qryParams);
  const url = endpoints.findMany(
    relation ? collection : field,
    finalParams,
    relation ? field : false
  );
  const options = {};
  try {
    const res = await fetchAPI(url, options);
    const fields = res.results.map((item) => ({
      label: Array.isArray(option)
        ? option
            .map((opt) => {
              if (opt.key.includes('.')) {
                const keys = opt.key.split('.');
                let value = item;
                keys.forEach((key) => {
                  if (value && value[key]) {
                    value = value[key];
                  } else {
                    value = null;
                  }
                });
                return value;
              }
              return item[opt.key] || null; // handle the case when key doesn't exist
            })
            .filter((value) => value !== null) // filter out null values
            .join(' - ')
        : item[option],
      value: item[option_val] || item.id,
    }));
    return fields;
  } catch (error) {
    console.log(error);
    return error;
  }
}
// Handle data edit actions
export async function editData({ collection, data, formData }) {
  const decodedData = decodeURIComponent(data);
  const parsedData = JSON.parse(decodedData);
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
          for (const value of formData.getAll(key)) {
            uploadData.append('files', value);
            isUpload = true;
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
      const url = endpoints.findOne(collection, parsedData.id);
      delete parsedData._files;
      delete parsedData.id;
      const stringifyData = JSON.stringify(parsedData);
      const res = await editAction(url, stringifyData);
      return res;
    } catch (error) {
      console.error('Error in editData:', error);
    }
  } else {
    const url = endpoints.findOne(collection, parsedData.id);
    delete parsedData.id;
    const stringifyData = JSON.stringify(parsedData);
    const res = await editAction(url, stringifyData);
    return res;
  }
}
// Handle data creation actions
export async function createData({ collection, slug, parent, data, formData }) {
  const decodedData = decodeURIComponent(data);

  try {
    const parsedData = JSON.parse(decodedData);
    if (parsedData._files) {
      try {
        await Promise.all(
          Object.keys(parsedData._files).map(async (key) => {
            let isUpload = false;
            const uploadData = new FormData();
            for (const value of formData.getAll(key)) {
              uploadData.append('files', value);
              isUpload = true;
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
        const url = endpoints.findMany(collection);
        delete parsedData._files;
        const stringifyData = JSON.stringify({
          ...parsedData,
          ...(slug && parent && { [parent]: { set: [slug] } }),
        });
        const res = await createAction(url, stringifyData);
        return res;
      } catch (error) {
        console.error('Error in editData:', error);
      }
    } else {
      const url = endpoints.findMany(collection);
      const stringifyData = JSON.stringify({
        ...parsedData,
        ...(slug && parent && { [parent]: { set: [slug] } }),
      });
      const res = await createAction(url, stringifyData);
      return res;
    }
  } catch (error) {
    return error;
  }
}
// Handle data deletion actions
export async function deleteData({ collection, id }) {
  try {
    const url = endpoints.findOne(collection, id);
    const res = await deleteAction(url);
    return res;
  } catch (error) {
    return error;
  }
}
export async function findUsers({ ids, query }) {
  try {
    const qryParams = {
      sort: [{ field: 'id', sort: 'asc' }],
    };

    if (ids && ids.length) {
      qryParams.filters = {
        $and: [{ id: { $in: ids } }],
      };
    } else if (query) {
      qryParams._q = query;
    } else {
      qryParams.pageSize = 30;
      qryParams.page = 1;
    }

    const url = endpoints.admin.getUsers({ qryParams });
    const res = await fetchAPI(url);

    if (res.data) {
      res.data.results = res.data.results.filter(
        (result) => !result.roles.some((role) => role.id === 1)
      );
      return res.data;
    }

    return res;
  } catch (error) {
    return error;
  }
}
