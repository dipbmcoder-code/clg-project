'use client';

import { useState, useEffect } from 'react';
import { alpha } from '@mui/material/styles';
import { 
  Box, 
  Container, 
  Typography, 
  Card,
  CardContent,
  Tabs,
  Tab,
  Grid,
  IconButton,
  Button,
  TextField,
  MenuItem
} from '@mui/material';
import { useSettingsContext } from 'src/components/settings';
import { BackButton, ManualNewsFormComponent } from 'src/custom';
import { Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import { paths } from 'src/routes/paths';

export default function ManualNewsCreate({ onCreate, onField, leaguesData = [] ,websitesData = []}) {
  const settings = useSettingsContext();
  const [currentTab, setCurrentTab] = useState(0);
  const [leagues, setLeagues] = useState(leaguesData);
  const [websites, setwebsites] = useState(websitesData);

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  // Define the sections for each tab
  const matchReviewFields = [
    {
      name: "news_type",
      type: "hidden",
      value: "match_reviews",
      props: {
        style: { display: 'none' }
      }
    },
    {
      name: "league",
      type: "league_autocomplete",
      selectType:"single",
      label: "League",
      options: leagues,
      option: "name",
      option_val: "id",
      props: { xs: 12 }
    },
    {
      name: "home_team",
      type: "string",
      label: "Home Team",
      rules: { required: "Home team is required" },
      props: { xs: 12, sm: 6 }
    },
    {
      name: "home_score",
      type: "number",
      label: "Home Score",
      inputProps: { min: 0 },
      rules: {
        required: "Home score is required",
        min: { value: 0, message: "Score cannot be negative" },
      },
      props: { xs: 12, sm: 6 }
    },
    {
      name: "away_team",
      type: "string",
      label: "Away Team",
      rules: { required: "Away team is required" },
      props: { xs: 12, sm: 6 }
    },
    {
      name: "away_score",
      type: "number",
      label: "Away Score",
      inputProps: { min: 0 },
      rules: {
        required: "Away score is required",
        min: { value: 0, message: "Score cannot be negative" },
      },
      props: { xs: 12, sm: 6 }
    },
    {
      name: "venue",
      type: "string",
      multiline: true,
      rows: 4,
      label: "Match Venue",
      inputProps: { min: 0 },
      props: { xs: 6 },
      rules: { required: "Match Venue is required" },
    },
    {
      name: "match_date",
      type: "date_time_picker",
      label: "Match Date & Time",
      rules: { required: "Match date and time is required" },
      props: { xs: 6 }
    },
    {
      name: "summary",
      type: "string",
      multiline: true,
      rows: 4,
      label: "Match Summary",
      props: { xs: 6 }
    },
    {
      name: "users_websites",
      type: "select",
      label: "websites",
      selectType:"multiple",
      options: websites,
      option: "name",
      option_val: "id",
      rules: { required: "websites is required" },
      props: { xs: 6}
    },
    
    {
      name: 'goalscorers',
      type: 'goalscorers',
      label: 'Goalscorers',
      props: { xs: 12 }
    }

  ];

  const matchPreviewFields = [
    {
      name: "news_type",
      type: "hidden",
      value: "match_previews",
      props: {
        style: { display: 'none' }
      }
    },
    {
      name: "league",
      type: "league_autocomplete",
      selectType:"single",
      label: "League",
      options: leagues,
      option: "name",
      option_val: "id",
      props: { xs: 12 }
    },
    {
      name: "home_team",
      type: "string",
      label: "Home Team",
      rules: { required: "Home team is required" },
      props: { xs: 12, sm: 6 }
    },
    {
      name: "home_team_position",
      type: "string",
      multiline: true,
      rows: 4,
      label: "Home Team Position",
      inputProps: { min: 0 },
      props: { xs: 12, sm: 6 },
      rules: { required: "Home Team Position is required" },
    },
    {
      name: "away_team",
      type: "string",
      label: "Away Team",
      rules: { required: "Away team is required" },
      props: { xs: 12, sm: 6 }
    },
    {
      name: "away_team_position",
      type: "string",
      multiline: true,
      rows: 4,
      label: "Away Team Position",
      rules: { required: "Away Team Position is required" },
      inputProps: { min: 0 },
      props: { xs: 12, sm: 6 }
    },
    {
      name: "venue",
      type: "string",
      multiline: true,
      rows: 4,
      label: "Match Venue",
      rules: { required: "Match Venue is required" },
      inputProps: { min: 0 },
      props: { xs: 6 }
    },
    {
      name: "match_date",
      type: "date_time_picker",
      label: "Match Date & Time",
      rules: { required: "Match date and time is required" },
      props: { xs: 6 }
    },
    {
      name: "summary",
      type: "string",
      multiline: true,
      rows: 4,
      label: "Match Summary",
      props: { xs: 6 }
    },
    {
      name: "users_websites",
      type: "select",
      label: "websites",
      selectType:"multiple",
      options: websites,
      option: "name",
      option_val: "id",
      rules: { required: "websites is required" },
      props: { xs: 6}
    },
    {
      name: 'players_to_watch',
      type: 'players_to_watch',
      label: 'Players to Watch',
      props: { xs: 12 }
    }
  ];

  const commonStyle = {
    xs: 12,
    sm: 6,
    md: 4,
  };

  return (
    <Container maxWidth={settings.themeStretch ? false : "xl"}>
      <Typography
        variant="h4"
        gutterBottom
        sx={{ mb: 4, color: "primary.main", fontWeight: "bold" }}
      >
        Create Manual News
      </Typography>

      <Box component="div" sx={{ display: "flex", gap: 2 }}>
        <BackButton />
      </Box>

      <Box
        sx={{
          gap: 2,
          mt: 3,
          width: 1,
          p: { xs: 1, sm: 3 },
          borderRadius: 2,
          border: (theme) => `dashed 1px ${theme.palette.divider}`,
        }}
      >
        {/* Tabs for Match Reviews and Previews */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={currentTab} onChange={handleTabChange}>
            <Tab label="Match Reviews" />
            <Tab label="Match Previews" />
          </Tabs>
        </Box>

        {/* Match Reviews Tab */}
        {currentTab === 0 && (
          <Box>
            <ManualNewsFormComponent
              redirect={`${paths.admin_dashboard.root}/manual_news/`}
              key={Date.now()}
              fields={matchReviewFields}
              action={onCreate}
              onField={onField}
              commonStyle={commonStyle}
              component="page"
              saveAtTop={true}
              // goalscorers={goalscorers}
              // onGoalscorersChange={setGoalscorers}
              currentTab={'match_reviews'}
            />
          </Box>
        )}

        {/* Match Previews Tab */}
        {currentTab === 1 && (
          <ManualNewsFormComponent
            redirect={`${paths.admin_dashboard.root}/manual_news/`}
            key={`preview-${Date.now()}`}
            fields={matchPreviewFields}
            action={onCreate}
            onField={onField}
            commonStyle={commonStyle}
            component="page"
            saveAtTop={true}
            currentTab={'match_previews'}
          />
        )}
      </Box>
    </Container>
  );
}