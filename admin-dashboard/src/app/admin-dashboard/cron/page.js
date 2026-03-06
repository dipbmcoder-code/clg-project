import { getSingleType, getData, editData } from 'src/utils/commonActions';
import { ServerError } from 'src/custom';
import CronView from 'src/sections/admin/cron/view';
import { endpoints } from 'src/utils/axios';
import { fetchAPI } from 'src/utils/helper';
import { HOST_API } from 'src/config-global';

export const metadata = {
  title: 'Cron & Triggers | AI News Generator',
};

const collection = 'cron-settings';

export default async function Page() {
  try {
    const [cronRes, historyRes] = await Promise.all([
      getSingleType({ collection }),
      getHistoryAction({ sort: [{ field: 'log_time', sort: 'desc' }], pageSize: 20, page: 1 }),
    ]);

    if (cronRes?.error) {
      return <ServerError error={cronRes.error} />;
    }

    return (
      <CronView
        data={cronRes.data || {}}
        history={historyRes}
        onEdit={editDataAction}
        onTrigger={triggerAction}
        onRefreshSettings={refreshSettingsAction}
        onRefreshHistory={getHistoryAction}
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

async function triggerAction() {
  'use server';
  try {
    const url = `${HOST_API}${endpoints.cron.trigger}`;
    const res = await fetchAPI(url, { method: 'POST' });
    return res;
  } catch (err) {
    return { error: err?.message || 'Trigger failed' };
  }
}

async function refreshSettingsAction() {
  'use server';
  const res = await getSingleType({ collection });
  return res;
}

async function getHistoryAction(qryParams) {
  'use server';
  const res = await getData({ collection: 'news-log', fixParams: {}, qryParams });
  return res;
}
