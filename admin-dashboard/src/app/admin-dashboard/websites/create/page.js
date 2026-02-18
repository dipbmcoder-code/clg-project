import { onField, createData } from 'src/utils/commonActions';

import WebsitesCreate from 'src/sections/admin/websites/create/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Add New Website | AI News Generator',
};

const collection = 'users-website';

export default async function Page() {
  return <WebsitesCreate onCreate={createDataAction} onField={onFieldAction} />;
}

async function createDataAction(data, formData) {
  'use server';
  return await createData({ collection, data, formData });
}

async function onFieldAction(qryParams) {
  'use server';
  return await onField({ collection, qryParams });
}
