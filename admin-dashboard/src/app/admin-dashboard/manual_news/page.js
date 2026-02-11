import { ServerError } from 'src/custom';
import ManualNewsList from 'src/sections/admin/manual_news/view';
import { getData, deleteData } from 'src/utils/commonActions';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Manual News',
};
const fixParams = {};

const collection = 'manual-news';
const pageSizeOptions = [10, 20, 50, 100];
const initParams = {
  sort: [{ field: 'createdAt', sort: 'desc' }],
  pageSize: pageSizeOptions[3],
  page: 1,
};

export default async function Page() {
 
  try {
    // Use searchParams for initial data if needed, or use initParams
    const data = await getDataAction(initParams);
    if (!data?.error && data) {
      const totalCount = data?.results?.length || 0;
      const activeCount = data.results?.filter((item) => item.published).length || 0;
      const fallbackCount = totalCount - activeCount;
      data.count = {
        total: totalCount,
        publish: activeCount,
        fallback: fallbackCount,
      };
      return (
        <ManualNewsList
          data={data}
          pageSizeOptions={pageSizeOptions}
          sorting={initParams.sort}
          onCount={getCount}
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
async function getCount() {
  'use server';

  const res = await getActiveCount({ collection });
  return res;
}
async function getDataAction(qryParams) {
  // return res;
  'use server';
  const res = await getData({ collection, fixParams, qryParams });
  return res;
}

async function deleteDataAction(id) {
  'use server';

  return await deleteData({ collection, id });
}