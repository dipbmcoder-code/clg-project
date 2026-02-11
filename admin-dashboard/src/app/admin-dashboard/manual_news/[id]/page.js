import { endpoints } from 'src/utils/axios';
import { fetchAPI, editAction } from 'src/utils/helper';
import { onField, editData, getData } from 'src/utils/commonActions';

import { ServerError } from 'src/custom';
import ManualNewsEdit from 'src/sections/admin/manual_news/edit/view';
import { findLeagues } from 'src/utils/leagueActions';
// ----------------------------------------------------------------------

export const metadata = {
  title: 'Edit Manual News',
};
const collection = 'manual-news';
const fixParams = {
  populate: ['*'],
  websites_news: ['*'],
};

export default async function Page({ params }) {
  const slug = params?.id ? params?.id : null;

  if (slug === null) {
    return <ServerError />;
  }

  if (slug) {
    // const url = endpoints.manualNews.getManualNews({ id: slug });
    const url = endpoints.findOne(collection, slug, fixParams);
    try {
      const res = await fetchAPI(url);
      // console.log('manual news data', res.data);
      if (res?.error) {
        return <ServerError error={res.error} />;
      }
      const { data } = res;
      // Transform users_websites into the Autocomplete-friendly format
      const formattedWebsites = (data.users_websites || []).map(site => ({
        label: site.platform_name,
        value: site.documentId,
        name: site.platform_name,
        id: site.documentId, // use documentId as unique key
      }));

      // Replace users_websites in data
      const transformedData = {
        ...data,
        users_websites: formattedWebsites,
        // league: formattedleages,
      };
      const websitesData = await fetchWebsites();
      const leaguesData = await fetchLeagues();
      return <ManualNewsEdit
        data={transformedData}
        onEdit={editDataAction}
        onField={onFieldAction}
        slug={slug}
        leaguesData={leaguesData}
        websitesData={websitesData}
        // onPublish={publishWebsiteNewsAction}
        onPublishAll={publishAllWebsiteNewsAction}
        onRegenerate={regenerateWebsiteNewsAction} />;
    } catch (error) {
      return <ServerError />;
    }
  } else {
    return <ServerError />;
  }
}

async function fetchLeagues() {
  const leagues = await findLeagues();
  return leagues.map(l => ({
    ...l,
    label: l.name,
    value: l.id
  }));
}

async function fetchWebsites() {
  try {
    const fixParams = {};
    // const qryParams = {};
    const qryParams = {
      sort: [{ field: 'id', sort: 'asc' }],
      // pageSize: 100, 
      // page: 1 
    };
    const websiteCollection = 'users-website';
    const res = await getData({ collection: websiteCollection, fixParams, qryParams });


    // Process websites data to extract name and other fields
    if (res && res.results && Array.isArray(res.results)) {
      return res.results
        .filter(website => website.is_validated === true && website.active === true)
        .map(website => ({
        label: website.platform_name || 'Unnamed Website',
        value: website.documentId,
        name: website.platform_name || 'Unnamed Website',
        id: website.documentId,
      }));
    }
    return [];
    // return res;
  } catch (error) {
    console.error("Error fetching websites:", error);
    return [];
  }
}

async function publishWebsiteNewsAction(websiteNewsId, publishStatus) {
  'use server';

  try {
    const url = endpoints.findOne('websites-news', websiteNewsId);
    // console.log('url',url);
    const data = JSON.stringify({ published: publishStatus });
    // const data = encodeURIComponent(JSON.stringify({ published: publishStatus }));
    const res = await editAction(url, data);
    //  console.log(res);
    return res;
  } catch (error) {
    console.error("Error publishing website news:", error);
    return { error: error.message };
  }
}

async function publishAllWebsiteNewsAction(publishStatus, manualnewsid) {
  'use server';

  try {
    // console.log("Publish all action called with status:", publishStatus);
    const collection = 'manual-news';
    // Here you would call your manual-news endpoint to publish all
    // For example, if you have an endpoint to update the main manual news item
    const url = endpoints.findOne(collection, manualnewsid);
    // console.log('Publish all URL:', url);

    const data = JSON.stringify({
      published: publishStatus,
      // You might need additional fields depending on your API
    });

    const res = await editAction(url, data);

    return res;
  } catch (error) {
    console.error("Error publishing all website news:", error);
    return { error: error.message };
  }
}

async function regenerateWebsiteNewsAction(websiteNewsId) {
  'use server';

  try {
    const url = endpoints.findOne('websites-news', websiteNewsId);

    // Only set regenerated to true without changing publish status
    const data = JSON.stringify({
      regenerated: true
    });

    const res = await editAction(url, data);
    // console.log('Regeneration result:', res);
    return res;
  } catch (error) {
    console.error("Error regenerating website news:", error);
    return { error: error.message };
  }
}

async function editDataAction(data, formData) {
  'use server';
  const res = await editData({ collection, data, formData });
  return res;
}

async function onFieldAction(qryParams) {
  'use server';
  return await onField({ collection: 'manual-news', qryParams });
}