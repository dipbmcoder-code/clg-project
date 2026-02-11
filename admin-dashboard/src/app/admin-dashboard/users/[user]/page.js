import { endpoints } from 'src/utils/axios';
import { fetchAPI, editAction } from 'src/utils/helper';

import { ServerError } from 'src/custom';

import User from 'src/sections/admin/users/user/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Edit User',
};

export default async function Page(props) {
  const params = await props.params;
  const parsedSlug = parseInt(params.user, 10);
  const slug = parsedSlug && parsedSlug.toString() === params.user ? parsedSlug : null;

  if (params.user && slug === null) {
    return <ServerError />;
  }

  if (slug) {
    const url = endpoints.admin.getUsers({ id: slug });
    try {
      const res = await fetchAPI(url);
      if (res?.error) {
        return <ServerError error={res.error} />;
      }
      const { data } = res;
      if (data.roles.some((role) => role.id === 1)) {
        return <ServerError error={{ status: 404 }} />;
      }
      return <User data={data} onEdit={editDataAction} onField={onFieldAction} slug={slug} />;
    } catch (error) {
      return <ServerError />;
    }
  } else {
    return <ServerError />;
  }
}


  async function editDataAction(data,formData,slug) {
    'use server';
    const url = endpoints.admin.getUsers({ id: slug });
    const decodedData = decodeURIComponent(data);
    const parsedData = JSON.parse(decodedData);
    delete parsedData.id;
    delete parsedData.confirm_password;
    if (parsedData.roles && Array.isArray(parsedData.roles) && parsedData.roles.length > 0) {
      parsedData.roles = parsedData.roles.filter((role) => role !== 1);
    }
    const stringifyData = JSON.stringify(parsedData);
    const res = await editAction(url, stringifyData);

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