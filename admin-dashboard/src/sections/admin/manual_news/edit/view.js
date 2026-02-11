"use client";

import { useState, useEffect } from "react";
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Button,
  Checkbox,
  FormControlLabel,
  CircularProgress,
  Stack,
  IconButton,
  Link,
  Tooltip,
} from "@mui/material";
import { alpha } from '@mui/material/styles';
import HomeIcon from '@mui/icons-material/Home';
import { useSettingsContext } from "src/components/settings";
import { useRouter } from 'src/routes/hooks';
import { RouterLink } from 'src/routes/components';
import {
  ManualNewsFormComponent,
  TransitionsDialog,
} from "src/custom";
import { paths } from "src/routes/paths";
import useCustomSnackbar from "src/hooks/use-custom-snackbar";
import { GlobalLoader } from "src/components/loading-screen";

export default function ManualNewsEdit({
  data,
  onEdit,
  onField,
  slug,
  leaguesData = [],
  websitesData = [],
  onPublishAll, // New prop for publishing all
  onRegenerate,
}) {
  const settings = useSettingsContext();
  const router = useRouter();
  const { customSnackbarAction } = useCustomSnackbar();
  const [leagues] = useState(leaguesData);
  const [websites] = useState(websitesData);
  const [publishStatus, setPublishStatus] = useState({});
  const [regeneratedStatus, setRegeneratedStatus] = useState({});
  const [selectedItems, setSelectedItems] = useState([]);
  const [selectAll, setSelectAll] = useState(true);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [isPublished, setIsPublished] = useState(data.published || false);
  const [loadingStates, setLoadingStates] = useState({
    publishAll: false,
    regenerate: {},
    bulkRegenerate: false,
  });
  const [websiteNewsData, setWebsiteNewsData] = useState(
    data.websites_news || [],
  );
  const isMatchReview =
    data.news_type === "match_reviews" || data.news_type === "match_review";
  // console.log(data.websites_news);
  // Initialize publish status and selected items
  useEffect(() => {
    if (data.websites_news) {
      const initialPublishStatus = {};
      const initialRegeneratedStatus = {};
      const initialSelected = [];

      data.websites_news.forEach((wn) => {
        initialPublishStatus[wn.documentId] = wn.published || false;
        initialRegeneratedStatus[wn.documentId] = wn.regenerated || false;
        initialSelected.push(wn.documentId);
      });
      if (data.websites_news && websites.length > 0) {
        const enriched = data.websites_news.map((wn) => {
          const website = websites.find(
            (w) =>
              w.id === wn.users_website || w.documentId === wn.users_website,
          );
          return { ...wn, users_website: website || { name: "Website" } };
        });
        setWebsiteNewsData(enriched);
      }

      setPublishStatus(initialPublishStatus);
      setRegeneratedStatus(initialRegeneratedStatus);
      setSelectedItems(initialSelected);
      // setWebsiteNewsData(data.websites_news);
    }
  }, [data.websites_news]);

  // Toggle checkbox select
  const toggleSelect = (id) => {
    setSelectedItems((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id],
    );
  };

  // Toggle select all
  const toggleSelectAll = () => {
    if (selectAll) {
      setSelectedItems([]);
    } else if (websiteNewsData) {
      setSelectedItems(websiteNewsData.map((wn) => wn.documentId));
    }
    setSelectAll(!selectAll);
  };

  // Update website news content after regeneration
  const updateWebsiteNewsContent = (documentId, newContent) => {
    setWebsiteNewsData((prev) =>
      prev.map((wn) =>
        wn.documentId === documentId ? { ...wn, content: newContent } : wn,
      ),
    );
  };

  // Handle single regenerate
  const handleRegenerate = async (websiteNewsId) => {
    setLoadingStates((prev) => ({
      ...prev,
      regenerate: { ...prev.regenerate, [websiteNewsId]: true },
    }));

    try {
      if (onRegenerate) {
        const result = await onRegenerate(websiteNewsId);

        if (result && !result.error) {
          setRegeneratedStatus((prev) => ({
            ...prev,
            [websiteNewsId]: true,
          }));

          // Update the content in the UI
          let contentToUpdate = "";

          if (result.content) {
            contentToUpdate = result.content;
          } else if (result.data && result.data.content) {
            contentToUpdate = result.data.content;
          } else if (typeof result === "string") {
            contentToUpdate = result;
          }

          if (contentToUpdate) {
            updateWebsiteNewsContent(websiteNewsId, contentToUpdate);
          }

          customSnackbarAction("Content regenerated successfully!", "success");
        } else {
          customSnackbarAction(
            result?.error || "Failed to regenerate content",
            "error",
          );
        }
      }
    } catch (error) {
      console.error("Error regenerating content:", error);
      customSnackbarAction("Error regenerating content", "error");
    } finally {
      setLoadingStates((prev) => ({
        ...prev,
        regenerate: { ...prev.regenerate, [websiteNewsId]: false },
      }));
    }
  };

  // Handle bulk regenerate
  const handleBulkRegenerate = async () => {
    if (selectedItems.length === 0) {
      customSnackbarAction(
        "Please select at least one item to regenerate.",
        "warning",
      );
      return;
    }

    setLoadingStates((prev) => ({ ...prev, bulkRegenerate: true }));

    try {
      if (onRegenerate) {
        const promises = selectedItems.map((id) => onRegenerate(id));
        const results = await Promise.all(promises);

        const updatedStatus = { ...regeneratedStatus };
        const allSuccess = results.every((r, index) => {
          if (r && !r.error) {
            const documentId = selectedItems[index];
            updatedStatus[documentId] = true;

            let contentToUpdate = "";

            if (r.content) {
              contentToUpdate = r.content;
            } else if (r.data && r.data.content) {
              contentToUpdate = r.data.content;
            } else if (typeof r === "string") {
              contentToUpdate = r;
            }

            if (contentToUpdate) {
              updateWebsiteNewsContent(documentId, contentToUpdate);
            }

            return true;
          }
          return false;
        });

        if (allSuccess) {
          setRegeneratedStatus(updatedStatus);
          customSnackbarAction(
            `Regenerated content for ${selectedItems.length} items successfully!`,
            "success",
          );
        } else {
          customSnackbarAction("Failed to regenerate some content", "error");
        }
      }
    } catch (error) {
      console.error("Error in bulk regenerate:", error);
      customSnackbarAction("Error regenerating contents", "error");
    } finally {
      setLoadingStates((prev) => ({ ...prev, bulkRegenerate: false }));
    }
  };

  // Handle publish all action
  const handlePublishAll = async () => {
    if (!onPublishAll) return;

    // Open confirmation dialog instead of using window.confirm
    setConfirmDialogOpen(true);
  };

  // Handle confirmed publish all
  const handleConfirmPublishAll = async () => {
    try {
      setLoadingStates((prev) => ({ ...prev, publishAll: true }));

      setConfirmDialogOpen(false); // Close dialog

      const result = await onPublishAll(true, data.documentId);

      if (result && !result.error) {
        // Update all publish statuses to true
        const newStatus = { ...publishStatus };
        Object.keys(newStatus).forEach((key) => {
          newStatus[key] = true;
        });
        setPublishStatus(newStatus);
        setIsPublished(true);

        customSnackbarAction("All content published successfully!", "success");
      } else {
        setIsPublished(false);
        customSnackbarAction(
          result?.error || "Failed to publish all content",
          "error",
        );
      }
    } catch (error) {
      console.error("Error publishing all content:", error);
      customSnackbarAction("Error publishing all content", "error");
    } finally {
      setLoadingStates((prev) => ({ ...prev, publishAll: false }));
    }
  };

  const matchReviewFields = [
    { name: "news_type", type: "hidden", value: "match_reviews" },
    {
      name: "league",
      type: "league_autocomplete",
      selectType: "single",
      label: "League",
      options: leagues,
      option: "name",
      option_val: "id",
      props: { xs: 12 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "home_team",
      type: "string",
      label: "Home Team",
      props: { xs: 12, sm: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "home_score",
      type: "number",
      label: "Home Score",
      props: { xs: 12, sm: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "away_team",
      type: "string",
      label: "Away Team",
      props: { xs: 12, sm: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "away_score",
      type: "number",
      label: "Away Score",
      props: { xs: 12, sm: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "summary",
      type: "string",
      multiline: true,
      rows: 4,
      label: "Match Summary",
      props: { xs: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "users_websites",
      type: "select",
      label: "Websites",
      selectType: "multiple",
      options: websites,
      option: "name",
      option_val: "id",
      props: { xs: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "venue",
      type: "string",
      label: "Match Venue",
      props: { xs: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "match_date",
      type: "date_time_picker",
      label: "Match Date & Time",
      props: { xs: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "goalscorers",
      type: "goalscorers",
      label: "Goalscorers",
      props: { xs: 12 },
      disabled: isPublished, // Add disabled property
    },
  ];

  const matchPreviewFields = [
    { name: "news_type", type: "hidden", value: "match_previews" },
    {
      name: "league",
      type: "league_autocomplete",
      selectType: "single",
      label: "League",
      options: leagues,
      option: "name",
      option_val: "id",
      props: { xs: 12 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "home_team",
      type: "string",
      label: "Home Team",
      props: { xs: 12, sm: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "home_team_position",
      type: "string",
      label: "Home Team Position",
      props: { xs: 12, sm: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "away_team",
      type: "string",
      label: "Away Team",
      props: { xs: 12, sm: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "away_team_position",
      type: "string",
      label: "Away Team Position",
      props: { xs: 12, sm: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "venue",
      type: "string",
      label: "Match Venue",
      props: { xs: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "match_date",
      type: "date_time_picker",
      label: "Match Date & Time",
      props: { xs: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "summary",
      type: "string",
      multiline: true,
      rows: 4,
      label: "Match Summary",
      props: { xs: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "users_websites",
      type: "select",
      label: "Websites",
      selectType: "multiple",
      options: websites,
      option: "name",
      option_val: "id",
      props: { xs: 6 },
      disabled: isPublished, // Add disabled property
    },
    {
      name: "players_to_watch",
      type: "players_to_watch",
      label: "Players to Watch",
      props: { xs: 12 },
      disabled: isPublished, // Add disabled property
    },
  ];

  const commonStyle = { xs: 12, sm: 6, md: 4 };

  return (
    <Container maxWidth={settings.themeStretch ? false : "xl"}>
      <Stack spacing={3}>
        {/* Header Section with Breadcrumb */}
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
                <Link
                  component={RouterLink}
                  href="/admin-dashboard/manual_news"
                  underline="hover"
                  sx={{
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                  }}
                >
                  <Typography
                    variant="h4"
                    sx={{
                      fontWeight: 700,
                      background: (theme) => `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                      backgroundClip: 'text',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                      '&:hover': {
                        opacity: 0.8,
                      },
                    }}
                  >
                    Manual News
                  </Typography>
                </Link>
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
                  Edit {isMatchReview ? "Review" : "Preview"}
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
                Edit {isMatchReview ? "match review" : "match preview"} details and content
              </Typography>
            </Box>
          </Stack>
        </Box>

        {/* Form Card */}
        <Card
          sx={{
            boxShadow: (theme) => theme.customShadows.card,
            borderRadius: 2,
            overflow: 'hidden',
          }}
        >
          <CardContent sx={{ p: 3 }}>
            {/* Form */}
            {isMatchReview ? (
              <ManualNewsFormComponent
                redirect={`${paths.admin_dashboard.root}/manual_news/`}
                key={Date.now()}
                dialog={{ mode: "edit", value: data }}
                fields={matchReviewFields}
                action={onEdit}
                onField={onField}
                commonStyle={commonStyle}
                component="page"
                saveAtTop
                currentTab="match_reviews"
                disabled={isPublished} // Pass disabled prop to form component
              />
            ) : (
              <ManualNewsFormComponent
                redirect={`${paths.admin_dashboard.root}/manual_news/`}
                key={Date.now()}
                dialog={{ mode: "edit", value: data }}
                fields={matchPreviewFields}
                action={onEdit}
                onField={onField}
                commonStyle={commonStyle}
                component="page"
                saveAtTop
                currentTab="match_previews"
                disabled={isPublished} // Pass disabled prop to form component
              />
            )}
          </CardContent>
        </Card>

        {/* Generated Content */}
        {websiteNewsData && websiteNewsData.length > 0 && (
          <Box>
            <Typography
              variant="h5"
              gutterBottom
              sx={{
                fontWeight: 700,
                mb: 2,
              }}
            >
              Generated Content
            </Typography>

            {websiteNewsData.map((wn) => (
              <Card
                key={wn.documentId}
                sx={{
                  mb: 2,
                  boxShadow: (theme) => theme.customShadows.card,
                  borderRadius: 2,
                  border: (theme) => `1px solid ${alpha(theme.palette.divider, 0.5)}`,
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      mb: 2,
                    }}
                  >
                    {/* Website name */}
                    <Box>
                      <Typography
                        variant="subtitle1"
                        gutterBottom
                        sx={{ fontWeight: 600, mb: 0 }}
                      >
                        {wn.users_website?.name || "Website"}
                      </Typography>
                    </Box>
                  </Box>

                  {/* Content Preview */}
                  {wn.title && (
                    <Typography
                      variant="h6"
                      gutterBottom
                      sx={{
                        mb: 2,
                        fontWeight: 600,
                      }}
                    >
                      {wn.title}
                    </Typography>
                  )}
                  <Box
                    sx={{
                      mt: 1,
                      border: (theme) => `1px solid ${theme.palette.divider}`,
                      borderRadius: 2,
                      p: 2.5,
                      bgcolor: (theme) => alpha(theme.palette.grey[500], 0.04),
                    }}
                    dangerouslySetInnerHTML={{ __html: wn.content }}
                  />

                  {wn.publishedAt && (
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{ mt: 2, display: "block", fontWeight: 500 }}
                    >
                      Last published:{" "}
                      {new Date(wn.publishedAt).toLocaleString()}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            ))}

            {/* Bulk action buttons */}
            <Box
              sx={{
                mb: 2,
                display: "flex",
                gap: 2,
                alignItems: "center",
                flexWrap: "wrap",
                justifyContent: "space-between",
              }}
            >
              <Typography
                variant="body2"
                sx={{
                  color: isPublished ? "success.main" : "text.secondary",
                  fontWeight: 600,
                  fontSize: '0.875rem',
                }}
              >
                Status: {isPublished ? "Published" : "Unpublished"}
              </Typography>

              {/* Publish All Button */}
              <Button
                variant="contained"
                color="primary"
                onClick={handlePublishAll}
                disabled={loadingStates.publishAll || isPublished}
                startIcon={
                  loadingStates.publishAll ? (
                    <CircularProgress size={16} />
                  ) : null
                }
                sx={{
                  px: 3,
                  fontWeight: 600,
                  boxShadow: (theme) => theme.customShadows.primary,
                }}
              >
                {loadingStates.publishAll
                  ? "Publishing All..."
                  : "Publish"}
              </Button>
            </Box>
          </Box>
        )}
      </Stack>
      {/* Confirmation Dialog */}
      <TransitionsDialog
        dialog={{
          value: confirmDialogOpen,
          onFalse: () => setConfirmDialogOpen(false),
        }}
        title="Confirm Publish All"
        content="Are you sure you want to publish?"
        action={handleConfirmPublishAll}
        buttonText="Confirm"
        refresh={() => { }} // Empty function as we don't need to refresh anything
      />
      <GlobalLoader open={loadingStates.publishAll} />
    </Container>
  );
}