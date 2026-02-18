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
    websites: `${ROOTS.ADMIN_DASHBOARD}/websites`,
    social_posts: `${ROOTS.ADMIN_DASHBOARD}/social_posts`,
    news_prompts: `${ROOTS.ADMIN_DASHBOARD}/news_prompts`,
    logs: `${ROOTS.ADMIN_DASHBOARD}/news_logs`,
    users: `${ROOTS.ADMIN_DASHBOARD}/users`,
  },
  agent_dashboard: {
    root: ROOTS.AGENT_DASHBOARD,
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
