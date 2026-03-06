import { useMemo } from 'react';

import DashboardIcon from '@mui/icons-material/Dashboard';
import LanguageIcon from '@mui/icons-material/Language';
import ShareIcon from '@mui/icons-material/Share';
import TerminalIcon from '@mui/icons-material/Terminal';
import EventNoteIcon from '@mui/icons-material/EventNote';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import SettingsIcon from '@mui/icons-material/Settings';
import ScheduleIcon from '@mui/icons-material/Schedule';
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
          { title: 'AI settings', path: paths.admin_dashboard.ai_settings, icon: <SettingsIcon /> },
          { title: 'cron & triggers', path: paths.admin_dashboard.cron, icon: <ScheduleIcon /> },
          { title: 'news logs', path: paths.admin_dashboard.logs, icon: <EventNoteIcon /> },
          { title: 'users', path: paths.admin_dashboard.users, icon: <SupervisorAccountIcon /> },
        ],
      },
    ],
    []
  );

  return data;
}
