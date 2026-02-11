import { endpoints } from 'src/utils/axios';
import { fetchAPI } from 'src/utils/helper';
import { onField, editData } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import Website from 'src/sections/admin/websites/website/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Edit Website',
};

const collection = 'users-website';

export default async function Page({ params }) {
  const slug = params?.website ? params?.website  : null;

  if (slug === null) {
    return <ServerError />;
  }

  if (slug) {
    const url = endpoints.findOne(collection, slug);
    
    try {
      const data = await fetchAPI(url);
      if (data?.error) {
        return <ServerError error={data.error} />;
      }
      
      return (
        <Website
          data={data.data}
          onEdit={editDataAction}
          onField={onFieldAction}
          time={new Date()}
          slug={slug}
        />
      );
    } catch (error) {
      console.log(error);
      return <ServerError />;
    }
  } else {
    return <ServerError />;
  }
}
  async function editDataAction(data, formData) {
    'use server';
    const res = await editData({ collection, data, formData });
    return res;
  }

  async function onFieldAction(qryParams) {
    'use server';

    return await onField({ collection, qryParams });
  }