import { createData, onField } from 'src/utils/commonActions';

import UserCreate from 'src/sections/admin/users/create/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Create User | AI News Generator',
};

const collection = 'users';

export default async function Page() {
  return <UserCreate onCreate={createDataAction} onField={onFieldAction} />;
}

async function createDataAction(data, formData) {
  'use server';
  const res = await createData({ collection, data, formData });
  return res;
}

async function onFieldAction(qryParams) {
  'use server';
  return await onField({ collection, qryParams });
}