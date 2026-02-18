import { getData } from 'src/utils/commonActions';

import SocialPosts from 'src/sections/admin/social_posts/view';

// ----------------------------------------------------------------------

export const metadata = {
  title: 'Social Posts | AI News Generator',
};

const collection = 'social-posts';

const pageSizeOptions = [10, 25, 50, 100];

const sorting = [{ field: 'scraped_time', sort: 'desc' }];

export default async function Page(props) {
  const searchParams = await props.searchParams;
  const page = searchParams?.page ?? 1;
  const pageSize = searchParams?.pageSize ?? pageSizeOptions[0];

  const qryParams = {
    page,
    pageSize,
    sort: sorting,
  };

  try {
    const data = await getData({ collection, qryParams });

    return (
      <SocialPosts
        data={data}
        pageSizeOptions={pageSizeOptions}
        sorting={sorting}
        onPageChange={async (p) => {
          'use server';

          const params = {
            page: p.page ?? 1,
            pageSize: p.pageSize ?? pageSizeOptions[0],
            sort: p.sort ?? sorting,
            _q: p._q,
            source: p.source,
            is_posted: p.is_posted,
          };

          return getData({ collection, qryParams: params });
        }}
      />
    );
  } catch (error) {
    console.error('Error fetching social posts:', error);
    return (
      <SocialPosts
        data={{ results: [], pagination: { page: 1, pageSize: 10, total: 0, pageCount: 0 } }}
        pageSizeOptions={pageSizeOptions}
        sorting={sorting}
        onPageChange={async () => {
          'use server';
          return { results: [], pagination: { page: 1, pageSize: 10, total: 0, pageCount: 0 } };
        }}
      />
    );
  }
}
