import { useMemo } from 'react';

import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import ArticleIcon from '@mui/icons-material/Article';
import { paths } from 'src/routes/paths';
import LanguageIcon from '@mui/icons-material/Language';
import EventNoteIcon from '@mui/icons-material/EventNote';
import TerminalIcon from '@mui/icons-material/Terminal';
import ShareIcon from '@mui/icons-material/Share';
import CategoryIcon from '@mui/icons-material/Category';
import SmartToyIcon from '@mui/icons-material/SmartToy';

// ----------------------------------------------------------------------

export function useNavData() {
  const data = useMemo(
    () => [
      {
        subheader: 'Content',
        items: [
          { title: 'Websites', path: paths.admin_dashboard.websites, icon: <LanguageIcon /> },
          // { title: 'Manual News', path: paths.admin_dashboard.manual_news, icon: <ArticleIcon /> },
          { title: 'News Prompts', path: paths.admin_dashboard.news_prompts, icon: <TerminalIcon /> },
          { title: 'News Logs', path: paths.admin_dashboard.logs, icon: <EventNoteIcon /> },
        ],
      },
      {
        subheader: 'Social & Publishing',
        items: [
          { title: 'Social Media', path: paths.admin_dashboard.social_media, icon: <ShareIcon /> },
          { title: 'WP Categories', path: paths.admin_dashboard.wp_categories, icon: <CategoryIcon /> },
        ],
      },
      {
        subheader: 'Settings',
        items: [
          { title: 'AI Settings', path: paths.admin_dashboard.ai_settings, icon: <SmartToyIcon /> },
          { title: 'Users', path: paths.admin_dashboard.users, icon: <SupervisorAccountIcon /> },
        ],
      },
    ],
    []
  );

  return data;
}
