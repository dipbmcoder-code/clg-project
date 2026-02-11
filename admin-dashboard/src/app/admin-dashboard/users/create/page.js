import { endpoints } from 'src/utils/axios';
import { fetchAPI, createAction } from 'src/utils/helper';

import UserCreate from 'src/sections/admin/users/create/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Create User',
};

export default async function Page() {
  return <UserCreate onCreate={createDataAction} onField={onFieldAction} />;
}

async function createDataAction(data, formData) {
    'use server';

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
  async function onFieldAction(qryParams) {
    'use server';

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