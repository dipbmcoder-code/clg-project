import axios from 'axios';
import { HOST_API } from 'src/config-global';

// ─── Axios Instance ───
const axiosInstance = axios.create({
  baseURL: HOST_API,
});

axiosInstance.interceptors.response.use(
  (res) => res,
  (error) => Promise.reject((error.response && error.response.data) || 'Something went wrong')
);

export default axiosInstance;

// ─── API Endpoints (Node.js Express backend) ───
export const endpoints = {
  auth: {
    me: '/api/auth/me',
    login: '/api/auth/login',
  },
  websites: {
    list: '/api/websites',
    get: (id) => `/api/websites/${id}`,
    create: '/api/websites',
    update: (id) => `/api/websites/${id}`,
    delete: (id) => `/api/websites/${id}`,
  },
  prompts: {
    get: '/api/news-prompts',
    update: '/api/news-prompts',
  },
  logs: {
    list: '/api/news-logs',
    get: (id) => `/api/news-logs/${id}`,
  },
  posts: {
    list: '/api/social-posts',
  },
  dashboard: {
    stats: '/api/dashboard/stats',
  },
  users: {
    list: '/api/users',
    get: (id) => `/api/users/${id}`,
    create: '/api/users',
    update: (id) => `/api/users/${id}`,
    delete: (id) => `/api/users/${id}`,
    roles: '/api/users/roles/list',
  },
  wordpress: {
    validate: '/api/wordpress/validate',
    categories: (websiteId) => `/api/wordpress/categories?website_id=${websiteId}`,
    authors: (websiteId) => `/api/wordpress/authors?website_id=${websiteId}`,
    publish: '/api/wordpress/publish',
  },
};
