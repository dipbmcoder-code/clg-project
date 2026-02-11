import { useMemo } from 'react';


import LocationOnIcon from '@mui/icons-material/LocationOn';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import SportsSoccerIcon from '@mui/icons-material/SportsSoccer';
import ArticleIcon from '@mui/icons-material/Article';
import { paths } from 'src/routes/paths';
import LanguageIcon from '@mui/icons-material/Language';
import EventNoteIcon from '@mui/icons-material/EventNote';
import SvgColor from 'src/components/svg-color';

import TerminalIcon from '@mui/icons-material/Terminal';
// ----------------------------------------------------------------------

const icon = (name) => (
  <SvgColor src={`/assets/icons/navbar/${name}.svg`} sx={{ width: 1, height: 1 }} />
  // OR
  // <Iconify icon="fluent:mail-24-filled" />
  // https://icon-sets.iconify.design/solar/
  // https://www.streamlinehq.com/icons
);

const ICONS = {
  job: icon('ic_job'),
  blog: icon('ic_blog'),
  chat: icon('ic_chat'),
  mail: icon('ic_mail'),
  user: icon('ic_user'),
  file: icon('ic_file'),
  lock: icon('ic_lock'),
  tour: icon('ic_tour'),
  order: icon('ic_order'),
  label: icon('ic_label'),
  blank: icon('ic_blank'),
  kanban: icon('ic_kanban'),
  folder: icon('ic_folder'),
  banking: icon('ic_banking'),
  booking: icon('ic_booking'),
  invoice: icon('ic_invoice'),
  product: icon('ic_product'),
  calendar: icon('ic_calendar'),
  disabled: icon('ic_disabled'),
  external: icon('ic_external'),
  menuItem: icon('ic_menu_item'),
  ecommerce: icon('ic_ecommerce'),
  analytics: icon('ic_analytics'),
  dashboard: icon('ic_dashboard'),
};

// ----------------------------------------------------------------------

export function useNavData() {
  const data = useMemo(
    () => [
      // OVERVIEW
      // ----------------------------------------------------------------------
      {
        subheader: 'Admin',
        items: [
          // { title: 'leagues', path: paths.admin_dashboard.leagues, icon: <SportsSoccerIcon /> },
          { title: 'websites', path: paths.admin_dashboard.websites, icon: <LanguageIcon /> },
          { title: 'manual news', path: paths.admin_dashboard.manual_news, icon: <ArticleIcon /> },
          { title: 'news prompts', path: paths.admin_dashboard.news_prompts, icon: <TerminalIcon /> },
          { title: 'news logs', path: paths.admin_dashboard.logs, icon: <EventNoteIcon /> },
          { title: 'users', path: paths.admin_dashboard.users, icon: <SupervisorAccountIcon /> },
        ],
      },
    ],
    []
  );

  return data;
}
