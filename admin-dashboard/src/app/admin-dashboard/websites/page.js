import { fetchAPI } from 'src/utils/helper';
import { endpoints } from 'src/utils/axios';
import { getData, deleteData, getActiveCount, editData } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import Websites from 'src/sections/admin/websites/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Users Website',
};
const fixParams = {};

const collection = 'users-website';
const pageSizeOptions = [10, 20, 50, 100];
const initParams = {
  sort: [{ field: 'platform_name', sort: 'asc' }],
  pageSize: pageSizeOptions[3],
  page: 1,
};
export default async function Page() {
  try {
    const data = await getDataAction(initParams);
    const totalCount = data?.results?.length || 0;
    const activeCount = data.results?.filter((item) => item.active).length || 0;
    const fallbackCount = totalCount - activeCount;
    data.count = {
      total: totalCount,
      active: activeCount,
      fallback: fallbackCount,
    };
    if (!data?.error && data) {
      return (
        <Websites
          data={data}
          pageSizeOptions={pageSizeOptions}
          sorting={initParams.sort}
          onCount={getCount}
          onPageChange={getDataAction}
          onDelete={deleteDataAction}
          onPublish={onPublish}
          onActive={onActive}
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

async function onActive(data, formData) {
  'use server';
  const res = await editData({ collection, data, formData });
  return res;
}
