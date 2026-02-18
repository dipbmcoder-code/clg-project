import { getSingleType, onField, editData } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import NewsPrompts from 'src/sections/admin/news_prompts/view';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'AI Prompts | AI News Generator',
};

const collection = 'news-prompt';

export default async function Page() {
  try {
    const data = await getSingleType({ collection });
    if (data?.error) {
      return <ServerError error={data.error} />;
    }

    return (
      <NewsPrompts
        data={data.data || {}}
        onEdit={editDataAction}
        onField={onFieldAction}
        time={new Date()}
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
