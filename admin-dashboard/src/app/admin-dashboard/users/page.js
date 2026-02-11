import { endpoints } from 'src/utils/axios';
import { fetchAPI, deleteAction } from 'src/utils/helper';

import { ServerError } from 'src/custom';

import Users from 'src/sections/admin/users/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Users',
};

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
    console.log(error);
    return <ServerError />;
  }
}
async function getDataAction(qryParams) {
    'use server';

    const url = endpoints.admin.getUsers({ qryParams });
    const res = await fetchAPI(url);

    if (res.data) {
      res.data.results = res.data.results.filter(
        (result) => !result.roles.some((role) => role.id === 1)
      );
      return res.data;
    }

    return res;
  }

  async function deleteDataAction(id) {
    'use server';

    const url = endpoints.admin.getUsers({ id });
    return await deleteAction(url);
  }