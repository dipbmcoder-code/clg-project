import qs from 'qs';
import axios from 'axios';

import { HOST_API } from 'src/config-global';

// ----------------------------------------------------------------------

const axiosInstance = axios.create();

axiosInstance.interceptors.response.use(
  (res) => res,
  (error) => Promise.reject((error.response && error.response.data) || 'Something went wrong')
);

export default axiosInstance;

// ─── API Route Map ───────────────────────────────────────────
// Maps old Strapi collection names to new clean REST endpoints
const COLLECTION_MAP = {
  'users-website': 'websites',
  'news-log': 'news-logs',
  'news-prompt': 'news-prompts',
  'manual-news': 'manual-news',
  'websites-news': 'website-news',
};

const resolveCollection = (collection) => COLLECTION_MAP[collection] || collection;

// ----------------------------------------------------------------------

export const endpoints = {
  auth: {
    me: '/api/auth/me',
    login: '/api/auth/login',
    register: '/api/auth/register',
    users: '/api/auth/users',
  },
  manualNews: {
    getManualNews: ({ id, qryParams } = {}) => {
      let url = `${HOST_API}/api/manual-news`;
      if (id) {
        url += `/${id}`;
      } else if (qryParams) {
        const params = {
          ...qryParams,
          sort: qryParams.sort ? qryParams.sort.map((o) => `${o.field}:${o.sort}`) : [],
        };
        url += `?${qs.stringify(params)}`;
      }
      return url;
    },
  },
  rapidapi: {
    getLeagues: () => `${HOST_API}/api/rapidapi/leagues`,
    getPlayers: (searchText) => `${HOST_API}/api/rapidapi/players/profiles?search=${searchText}`,
  },
  admin: {
    getUsers: ({ id, qryParams } = {}) => {
      let url = `${HOST_API}/api/auth/users`;
      if (id) url += `/${id}`;
      else if (qryParams) url += `?${qs.stringify(qryParams)}`;
      return url;
    },
  },
  assets: {
    upload: `${HOST_API}/api/upload`,
    location: `${HOST_API}/uploads`,
  },

  // AI Settings
  aiSettings: {
    get: () => `${HOST_API}/api/ai-settings`,
    update: () => `${HOST_API}/api/ai-settings`,
    test: (provider) => `${HOST_API}/api/ai-settings/test/${provider}`,
  },

  // Social Media
  socialMedia: {
    getConfig: (websiteId) => `${HOST_API}/api/social-media/config/${websiteId}`,
    updateConfig: (websiteId) => `${HOST_API}/api/social-media/config/${websiteId}`,
    post: () => `${HOST_API}/api/social-media/post`,
    listPosts: () => `${HOST_API}/api/social-media/posts`,
    listByWebsite: (websiteId) => `${HOST_API}/api/social-media/posts/${websiteId}`,
  },

  // WordPress
  wordpress: {
    categories: (websiteId) => `${HOST_API}/api/wordpress/${websiteId}/categories`,
    syncCategories: (websiteId) => `${HOST_API}/api/wordpress/${websiteId}/sync-categories`,
    health: (websiteId) => `${HOST_API}/api/wordpress/${websiteId}/health`,
    recentPosts: (websiteId) => `${HOST_API}/api/wordpress/${websiteId}/posts`,
  },

  // Clean REST endpoints — replaces Strapi content-manager pattern
  findMany: (collection, params = false) => {
    const resource = resolveCollection(collection);
    const paramsUrl = params ? `?${qs.stringify(params)}` : '';
    return `${HOST_API}/api/${resource}${paramsUrl}`;
  },

  findOne: (collection, id, params = false) => {
    const resource = resolveCollection(collection);
    return `${HOST_API}/api/${resource}/${id}${params ? `?${qs.stringify(params)}` : ''}`;
  },

  findAction: (collection, id, action) => {
    const resource = resolveCollection(collection);
    return `${HOST_API}/api/${resource}/${id}/${action}`;
  },

  findSingle: (collection) => {
    const resource = resolveCollection(collection);
    return `${HOST_API}/api/${resource}`;
  },
};
