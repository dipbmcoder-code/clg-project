'use client';

import { useMemo } from 'react';
import { alpha } from '@mui/material/styles';
import { Box, Container, Typography, Card, CardContent, Stack, Tooltip, IconButton } from '@mui/material';

// Icons
import TvIcon from '@mui/icons-material/Tv';
import ShareIcon from '@mui/icons-material/Share';
import PublicIcon from '@mui/icons-material/Public';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';
import HistoryEduIcon from '@mui/icons-material/HistoryEdu';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import HomeIcon from '@mui/icons-material/Home';
import { useSettingsContext } from 'src/components/settings';

import {
    CustomAccordionForm,
} from 'src/custom/index';
import { useBoolean } from 'src/hooks/use-boolean';

/**
 * Renders a form for editing dealer information.
 * @param {Object} props - Component props.
 * @param {Object} props.data - Object containing the dealer's current information.
 * @param {Function} props.onEdit - Function to be called when the form is submitted.
 * @param {Function} props.onField - Function to handle changes in form fields.
 * @returns {JSX.Element} - Rendered component.
 */

function NewsPrompts({
    data,
    onEdit,
    onField,
    time,
    componentData,
    defaultImagedata
}) {

    const settings = useSettingsContext();

    const commonStyle = {
        xs: 12,
        sm: 6,
    };

    const editDataAction = async (data, formData) => {
        const response = await onEdit(data, formData);
        return response;
    }

    const viewCategory = useBoolean(false);

    data = useMemo(() => {
        return {
            ...data,
        };
    }, [data]);
    const sections = [
        // {
        //     id: 'previews',
        //     title: 'Previews',
        //     icon: <AssignmentTurnedInIcon sx={{ fontSize: 20 }} />,
        //     fields: [
        //         { name: 'preview_news_title_prompt', type: 'prompt', label: 'Preview News Title Prompt', rows: 8, props: { xs: 12 }, variables: ['league_name', 'home_team', 'away_team', 'match_date', 'venue'] },
        //         { name: 'preview_news_image_prompt', type: 'prompt', label: 'Preview News Image Prompt', rows: 8, props: { xs: 12 }, variables: ['league_name', 'home_team', 'away_team', 'match_date', 'venue'] },
        //         { name: 'preview_news_content_prompt', type: 'prompt', label: 'Preview News Content Prompt', rows: 8, props: { xs: 12 }, variables: ['home_team', 'away_team', 'match_date', 'rank1', 'rank2', 'league_name', 'top_player_a', 'top_home_total', 'top_player_b', 'top_away_total', 'home_forms', 'away_forms', 'home_biggest_win_in_home', 'home_biggest_win_in_away', 'home_biggest_lose_in_home', 'home_biggest_lose_in_away', 'home_win_once_in_home', 'home_draws_once_in_home', 'home_lose_once_in_home', 'away_win_once_in_away', 'away_draws_once_in_away', 'away_lose_once_in_away', 'clean_home', 'clean_away', 'away_biggest_win_in_home', 'away_biggest_win_in_away', 'away_biggest_lose_in_home', 'away_biggest_lose_in_away'] },
        //     ],
        // },
        // {
        //     id: 'reviews',
        //     title: 'Reviews',
        //     icon: <HistoryEduIcon sx={{ fontSize: 20 }} />,
        //     fields: [
        //         { name: 'review_news_title_prompt', type: 'prompt', label: 'Review News Title Prompt', rows: 8, props: { xs: 12 }, variables: ['home_team', 'away_team', 'goals_home', 'goals_away', 'match_date', 'league_name', 'venue'] },
        //         { name: 'review_news_image_prompt', type: 'prompt', label: 'Review News Image Prompt', rows: 8, props: { xs: 12 }, variables: ['home_team', 'away_team', 'goals_home', 'goals_away', 'match_date', 'league_name', 'venue'] },
        //         { name: 'review_news_content_prompt', type: 'prompt', label: 'Review News Content Prompt', rows: 8, props: { xs: 12 }, variables: ['team1', 'team2', 'goals_a', 'goals_b', 'review_match_date', 'league_name1', 'round', 'goals_for_openai', 'possession_team1', 'possession_team2', 'shots_team1_off', 'shots_team1_on', 'active_shots_player_home', 'shots_team2_off', 'shots_team2_on', 'active_shots_player_away', 'name_home_top_pass_accuracy', 'top__home_precent_accuracy', 'top__home_total_passes', 'name_away_top_pass_accuracy', 'top__away_precent_accuracy', 'top__away_total_passes', 'name_home_top_pass_key', 'top__home_amount_key', 'name_away_top_pass_key', 'top__away_amount_key', 'total_interceptions_home', 'name_top_inceptions_home', 'amount_interceptions_home', 'total_inteceptions_away', 'name_top_inceptions_away', 'amount_interseptions_away', 'total_blocks_home', 'name_top_blocks_home', 'amount_blocks_home', 'total_blocks_away', 'name_top_blocks_away', 'amount_blocks_away', 'name_duels_team1', 'amount_duels_team1', 'name_duels_team2', 'amount_duels_team2', 'first_paragraph', 'second_paragraph', 'threeth_paragraph', 'fourth_paragraph', 'fiveth_paragraph', 'var_for_title_1', 'var_for_title_2', 'var_for_title_3', 'summ_shorts_target', 'lineups_a', 'lineups_b', 'lineups_in_game_a', 'lineups_in_game_b', 'first_goal', 'all_scorers', 'total_shots_off', 'total_shots_on', 'total_assists_home', 'total_assists_away', 'arena', 'date', 'yellow_card', 'red_card', 'fouls_y_card', 'fouls_r_card', 'fouls', 'penalti_home', 'penalti', 'goals', 'img_lineups', 'round_for_text'] },
        //     ],
        // },
        {
            id: 'social_media',
            title: 'Social Media',
            icon: <ShareIcon sx={{ fontSize: 20 }} />,
            fields: [
                { name: 'social_media_news_title_prompt', type: 'prompt', label: 'Social Media News Title Prompt', rows: 6, props: { xs: 12 }, variables: ['tweet_text'] },
                { name: 'social_media_news_image_prompt', type: 'prompt', label: 'Social Media News Image Prompt', rows: 8, props: { xs: 12 }, variables: ['tweet_text'] },
                { name: 'social_media_news_content_prompt', type: 'prompt', label: 'Social Media News Content Prompt', rows: 8, props: { xs: 12 }, variables: ['tweet_text'] },
            ],
        },
        // {
        //     id: 'player_abroad',
        //     title: 'Player Abroad',
        //     icon: <PublicIcon sx={{ fontSize: 20 }} />,
        //     fields: [
        //         { name: 'player_abroad_news_title_prompt', type: 'prompt', label: 'Player Abroad News Title Prompt', rows: 8, props: { xs: 12 }, variables: ['player_name', 'team_name', 'event_type', 'event_detail', 'league_country', 'league_name', 'home_team', 'away_team', 'nationality'], },
        //         { name: 'player_abroad_news_image_prompt', type: 'prompt', label: 'Player Abroad News Image Prompt', rows: 8, props: { xs: 12 }, variables: ['player_name', 'team_name', 'event_type', 'event_detail', 'league_country', 'league_name', 'home_team', 'away_team', 'nationality'], },
        //         { name: 'player_abroad_news_content_prompt', type: 'prompt', label: 'Player Abroad News Content Prompt', rows: 8, props: { xs: 12 }, variables: ['player_name', 'team_name', 'event_type', 'event_detail', 'league_country', 'league_name', 'home_team', 'away_team', 'nationality', 'all_data'], },
        //     ],
        // },
        // {
        //     id: 'player_profile',
        //     title: 'Player Profile',
        //     icon: <AccountCircleIcon sx={{ fontSize: 20 }} />,
        //     fields: [
        //         { name: 'player_profile_news_title_prompt', type: 'prompt', label: 'Player Profile News Title Prompt', rows: 6, props: { xs: 12 } },
        //         { name: 'player_profile_news_image_prompt', type: 'prompt', label: 'Player Profile News Image Prompt', rows: 8, props: { xs: 12 } },
        //         { name: 'player_profile_news_content_prompt', type: 'prompt', label: 'Player Profile News Content Prompt', rows: 8, props: { xs: 12 } },
        //     ],
        // },
        // {
        //     id: 'transfer',
        //     title: 'Transfer',
        //     icon: <SwapHorizIcon sx={{ fontSize: 20 }} />,
        //     fields: [
        //         { name: 'transfer_news_title_prompt', type: 'prompt', rows: 6, label: 'Transfer News Title Prompt', props: { xs: 12 }, variables: ['player_name', 'position', 'from_club', 'from_country', 'to_club', 'to_country', 'from_league', 'to_league', 'transfer_date', 'transfer_fee', 'market_value', 'nationality'] },
        //         { name: 'transfer_news_image_prompt', type: 'prompt', rows: 8, label: 'Transfer News Image Prompt', props: { xs: 12 }, variables: ['player_name', 'position', 'from_club', 'from_country', 'to_club', 'to_country', 'from_league', 'to_league', 'transfer_date', 'transfer_fee', 'market_value', 'nationality'] },
        //         { name: 'transfer_news_content_prompt', type: 'prompt', rows: 8, label: 'Transfer News Content Prompt', props: { xs: 12 }, variables: ['player_name', 'position', 'from_club', 'from_country', 'to_club', 'to_country', 'from_league', 'to_league', 'transfer_date', 'transfer_fee', 'market_value', 'transfer_history', 'market_value_history', 'nationality', 'all_data'] },
        //     ],
        // },
        // {
        //     id: 'rumor',
        //     title: 'Rumor',
        //     icon: <RecordVoiceOverIcon sx={{ fontSize: 20 }} />,
        //     fields: [
        //         { name: 'rumor_news_title_prompt', type: 'prompt', label: 'Rumor News Title Prompt', rows: 6, props: { xs: 12 }, variables: ['player_name', 'position', 'from_club', 'from_country', 'to_club', 'to_country', 'from_league', 'to_league', 'rumor_date', 'market_value', 'nationality'], },
        //         { name: 'rumor_news_image_prompt', type: 'prompt', label: 'Rumor News Image Prompt', rows: 8, props: { xs: 12 }, variables: ['player_name', 'position', 'from_club', 'from_country', 'to_club', 'to_country', 'from_league', 'to_league', 'rumor_date', 'market_value', 'nationality'], },
        //         { name: 'rumor_news_content_prompt', type: 'prompt', label: 'Rumor News Content Prompt', rows: 8, props: { xs: 12 }, variables: ['player_name', 'position', 'from_club', 'from_country', 'to_club', 'to_country', 'from_league', 'to_league', 'rumor_date', 'market_value', 'probability', 'transfer_history', 'market_value_history', 'nationality', 'all_data'], },
        //     ],
        // },
        // {
        //     id: 'where_to_watch',
        //     title: 'Where To Watch',
        //     icon: <TvIcon sx={{ fontSize: 20 }} />,
        //     fields: [
        //         { name: 'where_to_watch_news_title_prompt', type: 'prompt', label: 'Where To Watch News Title Prompt', rows: 6, props: { xs: 12 }, variables: ['league_name', 'country_name', 'start_date', 'end_date', 'season_year'] },
        //         { name: 'where_to_watch_news_image_prompt', type: 'prompt', label: 'Where To Watch News Image Prompt', rows: 8, props: { xs: 12 }, variables: ['league_name', 'country_name', 'start_date', 'end_date', 'season_year'] },
        //         { name: 'where_to_watch_news_content_prompt', type: 'prompt', label: 'Where To Watch News Content Prompt', rows: 8, props: { xs: 12 }, variables: ['league_name', 'country_name', 'start_date', 'end_date', 'season_year', 'all_data', 'tv_channels'] },
        //     ],
        // },
    ];

    return (
        <Container maxWidth={settings.themeStretch ? false : 'xl'}>
            <Stack spacing={3}>
                {/* Header Section */}
                {(
                    <Box
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            gap: 2,
                            p: 3,
                            borderRadius: 2,
                            border: (theme) => `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                        }}
                    >
                        <Stack direction="row" alignItems="center" spacing={1.5}>


                            {/* Breadcrumb Navigation */}
                            <Box>
                                <Stack direction="row" alignItems="center" spacing={1}>
                                    {/* Home Icon */}
                                    <Tooltip title="Go to Dashboard" arrow>
                                        <IconButton
                                            size="small"
                                            onClick={() => router.push('/admin-dashboard')}
                                            sx={{
                                                color: 'primary.main',
                                                '&:hover': {
                                                    bgcolor: 'primary.lighter',
                                                },
                                            }}
                                        >
                                            <HomeIcon />
                                        </IconButton>
                                    </Tooltip>
                                    <Typography
                                        variant="h4"
                                        sx={{
                                            fontWeight: 700,
                                            color: 'text.secondary',
                                        }}
                                    >
                                        /
                                    </Typography>
                                    <Typography
                                        variant="h4"
                                        sx={{
                                            fontWeight: 700,
                                            color: 'text.primary',
                                        }}
                                    >
                                        News Prompts
                                    </Typography>
                                </Stack>
                                <Typography
                                    variant="body2"
                                    sx={{
                                        color: 'text.secondary',
                                        fontWeight: 500,
                                        mt: 0.5,
                                    }}
                                >
                                    Manage and customize AI generation prompts for all news categories.
                                </Typography>
                            </Box>
                        </Stack>
                    </Box>
                )}


                {/* Settings Form Card */}
                <Card
                    sx={{
                        boxShadow: (theme) => `0 0 2px 0 ${alpha(theme.palette.grey[500], 0.08)}, 0 12px 24px -4px ${alpha(theme.palette.grey[500], 0.08)}`,
                        borderRadius: 2,
                        border: (theme) => `1px solid ${theme.palette.divider}`,
                        overflow: 'hidden',
                        position: 'relative',
                    }}
                >
                    <CardContent sx={{ p: { xs: 2, md: 3 } }}>
                        <CustomAccordionForm
                            time={time}
                            // excludeSections={excludeSections}
                            selectedOffers={['general', 'leagues']}
                            sections={sections}
                            // custom_data={!!custom_data}
                            // ignoreDirty={!!ignoreDirty}
                            dialog={data}
                            refresh={true}
                            action={editDataAction}
                            viewCategory={viewCategory}
                            onField={onField}
                            type={"page"}
                            commonStyle={commonStyle}
                        // deleteEntry={deleteEntry}
                        />
                    </CardContent>
                </Card>
                {/* <LeaguesCategoryPopup data={data} handle={viewCategory} action={editDataAction} /> */}
            </Stack>
        </Container>
    );
}
export default NewsPrompts;
