import { getData, deleteData } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import Users from 'src/sections/admin/users/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Users | AI News Generator',
};

const collection = 'users';
const pageSizeOptions = [10, 20, 50, 100];
const initParams = {
  sort: [{ field: 'id', sort: 'desc' }],
  pageSize: pageSizeOptions[0],
  page: 1,
};

export default async function Page() {
  try {
    const data = await getDataAction(initParams);

    if (!data?.error && data) {
      return (
        <Users
          data={data}
          pageSizeOptions={pageSizeOptions}
          sorting={initParams.sort}
          onPageChange={getDataAction}
          onDelete={deleteDataAction}
        />
      );
    }
    return <ServerError error={data.error} />;
  } catch (error) {
    console.error(error);
    return <ServerError />;
  }
}

async function getDataAction(qryParams) {
  'use server';
  const res = await getData({ collection, fixParams: {}, qryParams });
  return res;
}

async function deleteDataAction(id) {
  'use server';
  return await deleteData({ collection, id });
}