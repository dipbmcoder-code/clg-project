// ----------------------------------------------------------------------

const ROOTS = {
  AUTH: '/auth',
  ADMIN_DASHBOARD: '/admin-dashboard',
  AGENT_DASHBOARD: '/agent-dashboard',
};

// ----------------------------------------------------------------------

export const paths = {
  // AUTH
  auth: {
    login: `${ROOTS.AUTH}/login`,
  },
  // DASHBOARD
  admin_dashboard: {
    root: ROOTS.ADMIN_DASHBOARD,
    orders: `${ROOTS.ADMIN_DASHBOARD}/orders`,
    customers: `${ROOTS.ADMIN_DASHBOARD}/customers`,

    users: `${ROOTS.ADMIN_DASHBOARD}/users`,
    leagues: `${ROOTS.ADMIN_DASHBOARD}/leagues`,
    websites: `${ROOTS.ADMIN_DASHBOARD}/websites`,
    news_prompts: `${ROOTS.ADMIN_DASHBOARD}/news_prompts`,
    manual_news: `${ROOTS.ADMIN_DASHBOARD}/manual_news`,
    logs: `${ROOTS.ADMIN_DASHBOARD}/news_logs`,
  },
  agent_dashboard: {
    root: ROOTS.AGENT_DASHBOARD,
    orders: `${ROOTS.AGENT_DASHBOARD}/orders`,
  },

};

export const getRootPath = (roles) => {
  if (roles?.length) {
    const currentRoles = roles?.map((role) => role.name) || [];
    switch (currentRoles[0]) {
      case 'Admin':
        return paths.admin_dashboard.root;
      case 'Super Admin':
        return paths.admin_dashboard.root;
      case 'Agent':
        return paths.agent_dashboard.root;

      default:
        return '/';

    }
  } else {
    return paths.auth.login;
  }
};
