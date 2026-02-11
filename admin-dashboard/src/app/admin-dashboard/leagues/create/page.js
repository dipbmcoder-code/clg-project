import { onField, createData } from 'src/utils/commonActions';

import LeaguesCreate from 'src/sections/admin/leagues/create/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Add League',
};

const collection = 'leagues-management';

export default async function Page() {
  return <LeaguesCreate onCreate={createDataAction} onField={onFieldAction} />;
}
 async function createDataAction(data, formData) {
    'use server';

    return await createData({ collection, data, formData });
  }
  async function onFieldAction(qryParams) {
    'use server';

    return await onField({ collection, qryParams });
  }