import { HOST_API } from 'src/config-global';
import { endpoints } from 'src/utils/axios';
import { fetchAPI, editAction, createAction, deleteAction } from 'src/utils/helper';

/**
 * Build a URL with query parameters for list endpoints.
 */
function buildListUrl(baseUrl, qryParams) {
  const params = new URLSearchParams();

  if (qryParams.page) params.set('page', qryParams.page);
  if (qryParams.pageSize) params.set('pageSize', qryParams.pageSize);
  if (qryParams._q) params.set('_q', qryParams._q);

  // Convert sort array to single string "field:dir"
  if (qryParams.sort && qryParams.sort.length > 0) {
    const s = qryParams.sort[0];
    params.set('sort', `${s.field}:${s.sort}`);
  }

  // Additional filters
  if (qryParams.news_type) params.set('news_type', qryParams.news_type);
  if (qryParams.news_status) params.set('news_status', qryParams.news_status);
  if (qryParams.source) params.set('source', qryParams.source);
  if (qryParams.is_posted !== undefined) params.set('is_posted', qryParams.is_posted);
  if (qryParams.active !== undefined) params.set('active', qryParams.active);

  const qs = params.toString();
  return `${HOST_API}${baseUrl}${qs ? `?${qs}` : ''}`;
}

// ─── URL Maps ───
const LIST_URLS = {
  'users-website': endpoints.websites.list,
  'news-log': endpoints.logs.list,
  'social-posts': endpoints.posts.list,
  'users': endpoints.users.list,
};

const EDIT_URLS = {
  'users-website': (id) => `${HOST_API}${endpoints.websites.update(id)}`,
  'news-prompt': () => `${HOST_API}${endpoints.prompts.update}`,
  'ai-settings': () => `${HOST_API}${endpoints.aiSettings.update}`,
  'cron-settings': () => `${HOST_API}${endpoints.cron.settings}`,
  'users': (id) => `${HOST_API}${endpoints.users.update(id)}`,
};

const CREATE_URLS = {
  'users-website': `${HOST_API}${endpoints.websites.create}`,
  'users': `${HOST_API}${endpoints.users.create}`,
};

const DELETE_URLS = {
  'users-website': (id) => `${HOST_API}${endpoints.websites.delete(id)}`,
  'users': (id) => `${HOST_API}${endpoints.users.delete(id)}`,
};

const ENTRY_URLS = {
  'users-website': (id) => `${HOST_API}${endpoints.websites.get(id)}`,
  'news-log': (id) => `${HOST_API}${endpoints.logs.get(id)}`,
  'users': (id) => `${HOST_API}${endpoints.users.get(id)}`,
};

const SINGLE_TYPE_URLS = {
  'news-prompt': `${HOST_API}${endpoints.prompts.get}`,
  'ai-settings': `${HOST_API}${endpoints.aiSettings.get}`,
  'cron-settings': `${HOST_API}${endpoints.cron.settings}`,
};

/**
 * Fetch paginated list data for a collection.
 */
export async function getData({ collection, fixParams, qryParams }) {
  const baseUrl = LIST_URLS[collection];
  if (!baseUrl) {
    console.error(`Unknown collection: ${collection}`);
    return { error: 'Unknown collection' };
  }
  const url = buildListUrl(baseUrl, qryParams);
  return await fetchAPI(url);
}

/**
 * Get all websites (for counting active/inactive).
 */
export async function getActiveCount({ collection }) {
  const url = `${HOST_API}${endpoints.websites.list}?pageSize=100`;
  return await fetchAPI(url);
}

/**
 * Edit (PUT) a record.
 */
export async function editData({ collection, data, formData }) {
  const decodedData = decodeURIComponent(data);
  const parsedData = JSON.parse(decodedData);

  const urlBuilder = EDIT_URLS[collection];
  if (!urlBuilder) {
    console.error(`Unknown collection for edit: ${collection}`);
    return { error: 'Unknown collection' };
  }

  const url = urlBuilder(parsedData.id);

  // Clean internal fields before sending
  delete parsedData.id;
  delete parsedData._files;
  delete parsedData.documentId;
  delete parsedData.created_at;
  delete parsedData.updated_at;

  return await editAction(url, JSON.stringify(parsedData));
}

/**
 * Create (POST) a new record.
 */
export async function createData({ collection, data, formData }) {
  const decodedData = decodeURIComponent(data);
  const parsedData = JSON.parse(decodedData);

  const url = CREATE_URLS[collection];
  if (!url) {
    console.error(`Unknown collection for create: ${collection}`);
    return { error: 'Unknown collection' };
  }

  delete parsedData._files;
  return await createAction(url, JSON.stringify(parsedData));
}

/**
 * Delete a record.
 */
export async function deleteData({ collection, id }) {
  const urlBuilder = DELETE_URLS[collection];
  if (!urlBuilder) {
    console.error(`Unknown collection for delete: ${collection}`);
    return { error: 'Unknown collection' };
  }
  return await deleteAction(urlBuilder(id));
}

/**
 * Fetch a single record by ID.
 */
export async function getEntry({ collection, slug }) {
  const urlBuilder = ENTRY_URLS[collection];
  if (!urlBuilder) {
    console.error(`Unknown collection for getEntry: ${collection}`);
    return { error: 'Unknown collection' };
  }
  return await fetchAPI(urlBuilder(slug));
}

/**
 * Fetch single-type data (e.g., news prompts).
 */
export async function getSingleType({ collection }) {
  const url = SINGLE_TYPE_URLS[collection];
  if (!url) {
    console.error(`Unknown single type: ${collection}`);
    return { error: 'Unknown collection' };
  }
  return await fetchAPI(url);
}

/**
 * Field options — dynamic lookups for select fields.
 */
export async function onField({ collection, qryParams }) {
  if (collection === 'users' && qryParams?.field === 'roles') {
    const url = `${HOST_API}${endpoints.users.roles}`;
    const res = await fetchAPI(url);
    if (res?.data) {
      const { option, option_val } = qryParams;
      return res.data.map((item) => ({
        label: item[option] || item.name,
        value: item[option_val] || item.id,
      }));
    }
    return [];
  }
  return [];
}

/**
 * Find users — for autocomplete and user-select fields.
 * Accepts { ids, query } and returns { results: [...] }.
 */
export async function findUsers({ ids, query } = {}) {
  const params = new URLSearchParams();
  params.set('pageSize', '50');

  if (query) {
    params.set('_q', query);
  }

  const qs = params.toString();
  const url = `${HOST_API}${endpoints.users.list}${qs ? `?${qs}` : ''}`;
  const res = await fetchAPI(url);

  if (res?.error) return { results: [] };

  // If filtering by IDs, filter the results client-side
  if (ids && ids.length > 0) {
    const filtered = (res.results || []).filter((u) => ids.includes(u.id) || ids.includes(u.documentId));
    return { results: filtered };
  }

  return res;
}
