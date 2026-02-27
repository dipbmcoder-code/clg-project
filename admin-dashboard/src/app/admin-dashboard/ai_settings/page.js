import { getSingleType, editData } from 'src/utils/commonActions';
import { ServerError } from 'src/custom';
import AiSettingsView from 'src/sections/admin/ai_settings/view';

export const metadata = {
  title: 'AI Settings | AI News Generator',
};

const collection = 'ai-settings';

export default async function Page() {
  try {
    const data = await getSingleType({ collection });
    if (data?.error) {
      return <ServerError error={data.error} />;
    }

    return (
      <AiSettingsView
        data={data.data || {}}
        onEdit={editDataAction}
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
