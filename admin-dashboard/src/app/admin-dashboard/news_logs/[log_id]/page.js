import { getEntry } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import NewsLog from 'src/sections/admin/news_log/edit/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'News Log Detail | AI News Generator',
};

const collection = 'news-log';

export default async function Page(props) {
  const params = await props.params;
  const slug = params?.log_id ? params?.log_id : null;

  if (slug === null) {
    return <ServerError />;
  }

  try {
    const data = await getEntry({ collection, slug });
    if (data?.error) {
      return <ServerError error={data.error} />;
    }

    return (
      <NewsLog
        data={data.data}
        time={new Date()}
        slug={slug}
      />
    );
  } catch (error) {
    console.error(error);
    return <ServerError />;
  }
}
