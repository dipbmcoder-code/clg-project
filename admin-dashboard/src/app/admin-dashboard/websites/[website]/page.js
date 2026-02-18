import { getEntry, onField, editData } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import Website from 'src/sections/admin/websites/website/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Edit Website | AI News Generator',
};

const collection = 'users-website';

export default async function Page(props) {
  const params = await props.params;
  const slug = params?.website ? params?.website : null;

  if (slug === null) {
    return <ServerError />;
  }

  try {
    const data = await getEntry({ collection, slug });
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
    console.error(error);
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
