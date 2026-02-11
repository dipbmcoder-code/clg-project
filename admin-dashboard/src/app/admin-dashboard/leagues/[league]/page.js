import { endpoints } from 'src/utils/axios';
import { fetchAPI} from 'src/utils/helper';
import { onField, editData } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import League from 'src/sections/admin/leagues/league/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Edit League',
};

const collection = 'leagues-management';
const fixParams = {
};

export default async function Page({ params }) {
  const slug = params?.league ? params?.league  : null;

  if (slug === null) {
    return <ServerError />;
  }

  if (slug) {
    let initialParams = JSON.parse(JSON.stringify(fixParams));
    const url = endpoints.findOne(collection, slug, initialParams);
    
    try {
      const data = await fetchAPI(url);
      if (data?.error) {
        return <ServerError error={data.error} />;
      }

      return (
        <League
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
    console.log(data);
    console.log(collection);
    const res = await editData({ collection, data, formData });
    return res;
  }

  async function onFieldAction(qryParams) {
    'use server';

    return await onField({ collection, qryParams });
  }