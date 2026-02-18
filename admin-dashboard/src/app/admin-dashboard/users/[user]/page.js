import { getEntry, editData, onField } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import User from 'src/sections/admin/users/user/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Edit User | AI News Generator',
};

const collection = 'users';

export default async function Page(props) {
  const params = await props.params;
  const parsedSlug = parseInt(params.user, 10);
  const slug = parsedSlug && parsedSlug.toString() === params.user ? parsedSlug : null;

  if (params.user && slug === null) {
    return <ServerError />;
  }

  if (slug) {
    try {
      const res = await getEntry({ collection, slug });
      if (res?.error) {
        return <ServerError error={res.error} />;
      }
      const { data } = res;
      return <User data={data} onEdit={editDataAction} onField={onFieldAction} slug={slug} />;
    } catch (error) {
      return <ServerError />;
    }
  } else {
    return <ServerError />;
  }
}

async function editDataAction(data, formData, slug) {
  'use server';
  const res = await editData({ collection, data, formData });
  return res;
}

async function onFieldAction(qryParams) {
  'use server';
  return await onField({ collection, qryParams });
}