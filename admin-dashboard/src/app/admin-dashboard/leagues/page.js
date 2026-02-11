import { fetchAPI } from 'src/utils/helper';
import { endpoints } from 'src/utils/axios';
import { getData, deleteData, getActiveCount } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import Leagues from 'src/sections/admin/leagues/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Leagues',
};
const fixParams = {
  populate: {
    region: '*',
    oem: '*',
  },
};

const collection = 'leagues-management';
const pageSizeOptions = [10, 20, 50, 100];
const initParams = {
  sort: [{ field: 'league_id', sort: 'asc' }],
  pageSize: pageSizeOptions[3],
  page: 1,
};
export default async function Page() {
  try {
    const data = await getDataAction(initParams);

    if (!data?.error && data) {
      const { count, total } = await getCount();
      data.count = {
        total: total,
        active: count,
        fallback: total - count,
      };
      return (
        <Leagues
          data={data}
          pageSizeOptions={pageSizeOptions}
          sorting={initParams.sort}
          onCount={getCount}
          onPageChange={getDataAction}
          onDelete={deleteDataAction}
          onPublish={onPublish}
        />
      );
    }
    return <ServerError error={data.error} />;
  } catch (error) {
    console.log(error);
    return <ServerError />;
  }
}
 async function getCount() {
    'use server';

    const res = await getActiveCount({ collection });
    return res;
  }

  async function getDataAction(qryParams) {
    'use server';

    const res = await getData({ collection, fixParams, qryParams });
    return res;
  }

  async function deleteDataAction(id) {
    'use server';

    return await deleteData({ collection, id });
  }
async function onPublish(itemId, action) {
  'use server';

  const url = endpoints.findAction(collection, itemId, action);
  try {
    const fixOptions = {
      method: 'POST',
    };

    const postResponse = await fetchAPI(url, fixOptions);
    return postResponse;
  } catch (error) {
    return error;
  }
}
