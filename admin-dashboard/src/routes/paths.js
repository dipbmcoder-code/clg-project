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

    // New pages
    ai_settings: `${ROOTS.ADMIN_DASHBOARD}/ai_settings`,
    social_media: `${ROOTS.ADMIN_DASHBOARD}/social_media`,
    wp_categories: `${ROOTS.ADMIN_DASHBOARD}/wp_categories`,
  },
  agent_dashboard: {
    root: ROOTS.AGENT_DASHBOARD,
    orders: `${ROOTS.AGENT_DASHBOARD}/orders`,
  },
};

export const getRootPath = (roles) => {
  if (roles?.length) {
    const currentRoles = roles?.map((role) => role.name || role) || [];
    const firstRole = currentRoles[0];
    switch (firstRole) {
      case 'Admin':
      case 'ADMIN':
        return paths.admin_dashboard.root;
      case 'Super Admin':
      case 'SUPER_ADMIN':
        return paths.admin_dashboard.root;
      case 'Agent':
      case 'AGENT':
        return paths.agent_dashboard.root;
      default:
        return '/';
    }
  } else {
    return paths.auth.login;
  }
};
