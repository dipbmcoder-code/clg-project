import { endpoints } from 'src/utils/axios';
import { fetchAPI } from 'src/utils/helper';
import { onField, editData } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';

import NewsLog from 'src/sections/admin/news_log/edit/view';
// ----------------------------------------------------------------------

export const metadata = {
    title: 'News Log',
};

const collection = 'news-log';

export default async function Page({ params }) {
    const slug = params?.log_id ? params?.log_id : null;

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
                <NewsLog
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