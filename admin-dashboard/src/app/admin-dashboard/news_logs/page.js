import { getData } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import NewsLogs from 'src/sections/admin/news_log/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'News Logs | AI News Generator',
};

const collection = 'news-log';
const pageSizeOptions = [10, 20, 50, 100];
const initParams = {
  sort: [{ field: 'log_time', sort: 'desc' }],
  pageSize: pageSizeOptions[3],
  page: 1,
};

export default async function Page() {
  try {
    const data = await getDataAction(initParams);
    if (!data?.error && data) {
      return (
        <NewsLogs
          data={data}
          pageSizeOptions={pageSizeOptions}
          sorting={initParams.sort}
          onPageChange={getDataAction}
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
