import ManualNewsCreate from 'src/sections/admin/manual_news/create/view';
import { onField, createData, getData } from 'src/utils/commonActions';
import { ServerError } from 'src/custom';
import { findLeagues } from 'src/utils/leagueActions';

export const metadata = {
  title: 'Create Manual News',
};
const collection = 'manual-news';

export default async function Page() {
  try {
    const websitesData = await fetchWebsites();
    const leaguesData = await fetchLeagues(); 
    return (
      <ManualNewsCreate 
        onCreate={createDataAction} 
        onField={onFieldAction} 
        leaguesData={leaguesData}
        websitesData={websitesData} // Pass websites data to component
      />
    );
  } catch (error) {
    console.log("Error fetching data:", error);
    return <ServerError />;
  }
}

async function fetchLeagues(){
  const leagues = await findLeagues();
  return leagues.map(l=>({
    ...l,
    label:l.name,
    value:l.id
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
        .filter(website => website.is_validated === true && website.active === true) // Ensure platform_name exists
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

async function createDataAction(data, formData) {
  'use server';

  // Parse the data from the form
  const parsedData = JSON.parse(decodeURIComponent(data));
    
  // Process website data if it exists
  if (parsedData.website) {
    if (Array.isArray(parsedData.website) && parsedData.website.length > 0) {
      parsedData.website = parsedData.website[0].id;
    } else if (typeof parsedData.website === 'object' && parsedData.website.id) {
      parsedData.website = parsedData.website.id;
    }
  }
  
  // Process goalscorers if they exist
  if (parsedData.goalscorers && Array.isArray(parsedData.goalscorers)) {
    // Remove any id fields that might be present from the UI
    parsedData.goalscorers = parsedData.goalscorers.map(scorer => {
      const { id, ...scorerWithoutId } = scorer;
      return scorerWithoutId;
    });
  }
  
  const processedData = encodeURIComponent(JSON.stringify(parsedData));
  
  return await createData({ collection, data: processedData, formData });
}

async function onFieldAction(qryParams) {
  'use server';
  return await onField({ collection, qryParams });
}