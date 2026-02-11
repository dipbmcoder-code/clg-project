import qs from 'qs';
import axios from 'axios';

import { HOST_API, ASSETS_API } from 'src/config-global';

// ----------------------------------------------------------------------

const axiosInstance = axios.create();
axiosInstance.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

axiosInstance.interceptors.response.use(
  (res) => res,
  (error) => Promise.reject((error.response && error.response.data) || 'Something went wrong')
);

export default axiosInstance;
// ----------------------------------------------------------------------

export const endpoints = {
  auth: {
    me: '/admin/users/me',
    login: '/admin/login',
  },
  feeds: {
    getUrls: (id) => `${HOST_API}/custom-actions/auto/feed-urls/${id}`,
  },
  manualNews: {
    getManualNews: ({ id, qryParams, fixParams } = {}) => {
      const params = {
        ...qryParams,
        sort: qryParams ? qryParams.sort.map((option) => `${option.field}:${option.sort}`) : [],
      };
      let url = `${HOST_API}/manual-news`;
      if (id) {
        url += `/${id}`;
      } else if (params) {
        url += `?${qs.stringify({ ...params, ...fixParams })}`;
      }
      return url;
    },
  },
  rapidapi: {
    getLeagues: () => `${HOST_API}/api/rapidapi/leagues`,
    getPlayers: (searchText) => `${HOST_API}/api/rapidapi/players/profiles/?search=${searchText}`,
  },
  admin: {
    getUsers: ({ id, qryParams, fixParams }) => {
      const params = {
        ...qryParams,
        sort: qryParams ? qryParams.sort.map((option) => `${option.field}:${option.sort}`) : [],
      };

      let url = `${HOST_API}/admin/users`;
      if (id) {
        url += `/${id}`;
      } else if (params) {
        url += `?${qs.stringify({ ...params, ...fixParams })}`;
      }
      return url;
    },
    getRoles: ({ query }) => {
      let url = `${HOST_API}/admin/roles`;
      if (query) {
        url += `?_q=${query}`;
      }
      return url;
    },
  },
  assets: {
    upload: `${ASSETS_API}/upload`,
    location: `${ASSETS_API}/uploads`,
    actions: {
      bulkDelete: `${ASSETS_API}/upload/actions/bulk-delete`,
    },
  },

  /**
   * Generates the URL for finding multiple items in the API
   * @param {string} collection - The name of the collection
   * @param {object|null} params - The parameters for the query
   * @param {string|null} relation - The relation to the parent collection
   * @returns {string} The URL for the API request
   */
  findMany: (collection, params = false, relation = false) => {
    const baseUrl = `${HOST_API}/content-manager/${!relation ? 'collection-types' : 'relations'
      }/${collection.startsWith("plugin::") ? collection : `api::${collection}.${collection}`
      }`;
    const relationUrl = relation ? `/${relation}` : '';
    const paramsUrl = params ? `?${qs.stringify(params)}` : '';
    return `${baseUrl}${relationUrl}${paramsUrl}`;
  },
  findOne: (collection, id, params = false) =>
    `${HOST_API}/content-manager/collection-types/${collection.startsWith("plugin::") ? collection : `api::${collection}.${collection}`
    }/${id}${params ? `?${qs.stringify(params)}` : ''
    } `,
  findAction: (collection, id, action) =>
    `${HOST_API}/content-manager/collection-types/${collection.startsWith("plugin::") ? collection : `api::${collection}.${collection}`
    }/${id}/actions/${action}`,
  findSingle: (collection) =>
    `${HOST_API}/content-manager/single-types/${collection.startsWith("plugin::") ? collection : `api::${collection}.${collection}`
    }`,
};
