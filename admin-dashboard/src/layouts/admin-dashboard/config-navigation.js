import { useMemo } from 'react';

import DashboardIcon from '@mui/icons-material/Dashboard';
import LanguageIcon from '@mui/icons-material/Language';
import ShareIcon from '@mui/icons-material/Share';
import TerminalIcon from '@mui/icons-material/Terminal';
import EventNoteIcon from '@mui/icons-material/EventNote';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import { paths } from 'src/routes/paths';
// ----------------------------------------------------------------------

export function useNavData() {
  const data = useMemo(
    () => [
      {
        subheader: 'AI News Generator',
        items: [
          { title: 'dashboard', path: paths.admin_dashboard.root, icon: <DashboardIcon /> },
          { title: 'websites', path: paths.admin_dashboard.websites, icon: <LanguageIcon /> },
          { title: 'social posts', path: paths.admin_dashboard.social_posts, icon: <ShareIcon /> },
          { title: 'AI prompts', path: paths.admin_dashboard.news_prompts, icon: <TerminalIcon /> },
          { title: 'news logs', path: paths.admin_dashboard.logs, icon: <EventNoteIcon /> },
          { title: 'users', path: paths.admin_dashboard.users, icon: <SupervisorAccountIcon /> },
        ],
      },
    ],
    []
  );

  return data;
}
