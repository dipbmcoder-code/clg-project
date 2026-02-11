"use strict";

let publish = true;
let regenerate = false;
module.exports = {
  async afterCreate(event) {
    const { result, params } = event;
    const data = params.data;

    if (!data) return;

    const ctx = strapi.requestContext.get();
    const authHeader = ctx?.request?.header?.authorization;

    if (!authHeader) {
      console.error("❌ No Authorization header found in request");
      return;
    }

    const accessToken = authHeader.replace("Bearer ", "");
    console.log("🔑 Extracted Access Token:", accessToken);

    try {
      const {
        news_type,
        home_team,
        away_team,
        home_score,
        away_score,
        summary,
        users_websites,
        goalscorers,
        league,
        match_date,
        venue,
        home_team_position,
        away_team_position,
        players_to_watch,
        // accessToken,
      } = data;

      const manualNewsId = result.id;
      console.log("🆔 Created Manual News ID:", manualNewsId);

      if (
        users_websites &&
        users_websites.set &&
        users_websites.set.length > 0
      ) {
        const websiteIds = users_websites.set.map((w) => w.id);

        const websites = await strapi.db
          .query("api::users-website.users-website")
          .findMany({
            where: { id: { $in: websiteIds } },
            select: ["id", "documentId"],
          });
        console.log("🌐 Website records:", websites);
        // 🔹 Format league properly
        let formattedLeague = league;
        if (Array.isArray(league)) {
          formattedLeague = {
            id: league[0]?.id,
            name: league[0]?.name,
          };
        }

        // Base request body (with all websites at once ✅)
        let requestBody = {
          id: result.documentId,
          league: formattedLeague,
          summary,
          venue,
          websites_ids: websites.map((w) => w.documentId),
        };

        let endpoint = "";
        if (news_type === "match_previews") {
          let formattedPlayersToWatch = players_to_watch?.map((g) => ({
            player_name: g.player_name,
            session_goals: g.session_goals,
            team:
              g.team === "HOME"
                ? home_team
                : g.team === "AWAY"
                  ? away_team
                  : g.team,
          }));
          endpoint = `${process.env.BOT_API_URL}/generate-news/preview`;
          requestBody = {
            ...requestBody,
            home_team,
            away_team,
            home_team_position,
            away_team_position,
            match_date,
            players_to_watch: formattedPlayersToWatch,
          };
        } else if (news_type === "match_reviews") {
          let formattedGoalscorers = goalscorers?.map((g) => ({
            player_name: g.player_name,
            minute: g.minute,
            team:
              g.team === "HOME"
                ? home_team
                : g.team === "AWAY"
                  ? away_team
                  : g.team,
          }));
          endpoint = `${process.env.BOT_API_URL}/generate-news/review`;
          requestBody = {
            ...requestBody,
            home_team,
            away_team,
            home_score,
            away_score,
            match_date,
            goalscorers: formattedGoalscorers,
          };
        } else {
          console.log("⚠️ Unknown news type:", news_type);
          return;
        }

        // ✅ One single call
        console.log(`🚀 Sending request to ${endpoint}`, requestBody);

        // Call internal API
        // Get Strapi access token from cookies

        const response = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify(requestBody),
        });
        console.log("API response", response);
        if (!response.ok) {
          throw new Error(
            `API call failed: ${response.status} ${response.statusText}`
          );
        }

        const apiResponse = await response.json();
        // console.log("✅ API Response:", apiResponse);

        if (!apiResponse.success || !apiResponse.data) {
          throw new Error("API returned unsuccessful response");
        }

        let createdWebsiteNewsIds = [];

        // Process each generated news item
        for (const newsItem of apiResponse.data) {
          const { website_id, image_url, title, content } = newsItem;

          // Find the corresponding website
          const website = websites.find((w) => w.documentId === website_id);
          if (!website) {
            console.warn(
              `⚠️ Website with ID ${website_id} not found, skipping`
            );
            continue;
          }

          // Create content with embedded image
          let finalContent = content;
          if (image_url) {
            const imageHtml = `<div class="match-image"><img src="${image_url}" alt="${home_team} vs ${away_team} ${news_type === "match_reviews" ? "match review" : "match preview"} image" style="max-width: 100%; height: auto; margin: 20px 0; border-radius: 8px;"></div>`;
            // Insert image at the beginning of the content
            finalContent = imageHtml + finalContent;
          }

          // ✅ Create websites-news entry
          const websiteNews = await strapi.entityService.create(
            "api::websites-news.websites-news",
            {
              data: {
                content: finalContent,
                title: title,
                manual_news: result.documentId,
                users_website: website.documentId,
                image_url: image_url, // Save the image URL directly
                publishedAt: null, // Set status to draft
              },
            }
          );

          createdWebsiteNewsIds.push(websiteNews.documentId);
        }

        if (createdWebsiteNewsIds.length > 0) {
          await strapi.entityService.update(
            "api::manual-news.manual-news",
            manualNewsId,
            {
              data: {
                websites_news: createdWebsiteNewsIds,
              },
            }
          );
          console.log("🔗 Linked generated websites_news back to manual-news");
        }
      }
    } catch (error) {
      strapi.log.error("❌ Error in afterCreate lifecycle:", error);
    }
  },
  async beforeUpdate(event) {
    console.log("🔔 [manual-news] beforeUpdate fired!");
    try {
      const { model, params } = event;
      // console.log("params:", params);
      const data = params.data;
      // console.log("data:", data);
      if (model?.uid !== "api::manual-news.manual-news") {
        console.log("ℹ️ Not the right model, skipping...");
        return;
      }

      const ctx = strapi.requestContext.get();
      const authHeader = ctx?.request?.header?.authorization;
      if (!authHeader) {
        console.error("❌ No Authorization header found in request");
        return;
      }
      const accessToken = authHeader.replace("Bearer ", "");
      console.log("🔑 Extracted Access Token:", accessToken);

      const manualNewsId = params?.where?.id;
      const { published, reganrate_slug } = data;
      // Regeneration 
      regenerate = reganrate_slug || false;
    
      if (!published) {
        console.log(
          "ℹ️ Not publishing, skipping regeneration in beforeUpdate..."
        );
        return;
      }

      // ======================================================
      // 2️⃣ Publishing (when published = true)
      // ======================================================
      console.log("🚀 Publishing flow started...");

      const manualNews = await strapi.entityService.findOne(
        "api::manual-news.manual-news",
        manualNewsId,
        { populate: { websites_news: true } }
      );

      if (!manualNews?.websites_news?.length) {
        console.log("ℹ️ No websites_news found, skipping publish...");
        return;
      }

      function sanitizeContent(content) {
        if (!content) return "";
        return content
          .replace(/\t/g, " ")
          .replace(/<div class="match-image".*?>.*?<\/div>/gs, "")
          .replace(/\*\*(.*?)\*\*/g, "$1")
          .trim();
      }

      const publishPayload = [];
      const manualLeagueIds = Array.isArray(manualNews.league)
        ? manualNews.league.map((l) => l.id)
        : [];

      for (const wn of manualNews.websites_news) {
        const website = await strapi.db
          .query("api::users-website.users-website")
          .findOne({ where: { documentId: wn.users_website } });

        if (!website) continue;

        publishPayload.push({
          id: manualNews.documentId,
          title: wn.title,
          content: sanitizeContent(wn.content?.trim()),
          image_url: wn.image_url,
          website: {
            id: website.documentId,
            platform_name: website.platform_name?.trim(),
            platform_url: website.platform_url,
            platform_user: website.platform_user,
            platform_password: website.platform_password,
            categories: (() => {
              let categories = [];

              // ✅ Try from website_leagues
              if (Array.isArray(website.website_leagues)) {
                categories = website.website_leagues
                  .filter((league) => manualLeagueIds.includes(league.id))
                  .flatMap((league) =>
                    Array.isArray(league.categories)
                      ? league.categories.map((c) => ({
                          id: c.id,
                          name: c.name,
                        }))
                      : []
                  );
              }

              // ✅ If still empty, fallback to preview/review categories
              if (categories.length === 0) {
                if (
                  manualNews.news_type === "match_previews" &&
                  Array.isArray(website.manual_preview_categories)
                ) {
                  categories = website.manual_preview_categories.map((c) => ({
                    id: c.id,
                    name: c.name,
                  }));
                } else if (
                  manualNews.news_type === "match_reviews" &&
                  Array.isArray(website.manual_review_categories)
                ) {
                  categories = website.manual_review_categories.map((c) => ({
                    id: c.id,
                    name: c.name,
                  }));
                }
              }

              return categories;
            })(),
          },
        });
      }

      if (!publishPayload.length) {
        console.log("ℹ️ No valid payloads, skipping publish...");
        return;
      }

      const requestBody = { data: publishPayload };
      // console.log("requestBody:", requestBody);
      const endpoint =
        manualNews.news_type === "match_previews"
          ? `${process.env.BOT_API_URL}/publish-news/preview`
          : `${process.env.BOT_API_URL}/publish-news/review`;

      console.log(
        "🚀 Sending publish request:",
        JSON.stringify(requestBody, null, 2)
      );

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `Publish API failed: ${response.status} ${response.statusText} → ${errorText}`
        );
      }

      const apiResponse = await response.json();
      console.log("✅ Publish API Response:", apiResponse);
    } catch (error) {
      strapi.log.error("❌ Error in beforeUpdate lifecycle:", error);
    }
  },
  async afterUpdate(event) {
    console.log("🔔 [manual-news] afterUpdate fired!");

    try {
      if (!regenerate) {
        console.log("ℹ️ Regenerate flag not set, skipping afterUpdate...");  
        return;
      }
      const { model, params } = event;
      const data = params.data;

      if (model?.uid !== "api::manual-news.manual-news") {
        console.log("ℹ️ Not the right model, skipping...");
        return;
      }

      const ctx = strapi.requestContext.get();
      const authHeader = ctx?.request?.header?.authorization;
      if (!authHeader) {
        console.error("❌ No Authorization header found in request");
        return;
      }
      const accessToken = authHeader.replace("Bearer ", "");

      const manualNewsId = params?.where?.id;

      // ✅ Fetch fresh manual-news
      const manualNews = await strapi.entityService.findOne(
        "api::manual-news.manual-news",
        manualNewsId,
        {
          populate: {
            users_websites: true,
            websites_news: true,
          },
        }
      );

      if (!manualNews) {
        console.log("⚠️ Manual-news not found, aborting update...");
        return;
      }

      // -------------------------------------------------------
      // 1️⃣ Sync websites_news with users_websites
      // -------------------------------------------------------
      const websites = manualNews.users_websites.map((w) => ({
        id: w.id,
        documentId: w.documentId,
      }));

      const existingWebsiteNews = manualNews.websites_news || [];

      // 🔍 Find removed websites
      const removedNews = existingWebsiteNews.filter(
        (wn) => !websites.some((w) => w.documentId === wn.users_website)
      );

      // 🗑️ Delete removed website news
      for (const news of removedNews) {
        await strapi.entityService.delete(
          "api::websites-news.websites-news",
          news.id
        );
        console.log(`🗑️ Deleted website news for site ${news.users_website}`);
      }

      const activeWebsites = websites;

      let createdWebsiteNewsIds = [];

      if (activeWebsites.length) {
        // Prepare request body for generator
        let formattedLeague = Array.isArray(manualNews.league)
          ? {
              id: manualNews.league[0]?.id,
              name: manualNews.league[0]?.name,
            }
          : manualNews.league;

        let requestBody = {
          id: manualNews.documentId,
          league: formattedLeague,
          summary: manualNews.summary,
          venue: manualNews.venue,
          websites_ids: activeWebsites.map((w) => w.documentId),
        };

        let endpoint = "";
        if (manualNews.news_type === "match_previews") {
          requestBody = {
            ...requestBody,
            home_team: manualNews.home_team,
            away_team: manualNews.away_team,
            home_team_position: manualNews.home_team_position,
            away_team_position: manualNews.away_team_position,
            match_date: manualNews.match_date,
            players_to_watch: manualNews.players_to_watch?.map((g) => ({
              player_name: g.player_name,
              session_goals: g.session_goals,
              team:
                g.team === "HOME"
                  ? manualNews.home_team
                  : g.team === "AWAY"
                    ? manualNews.away_team
                    : g.team,
            })),
          };
          endpoint = `${process.env.BOT_API_URL}/generate-news/preview`;
        } else if (manualNews.news_type === "match_reviews") {
          requestBody = {
            ...requestBody,
            home_team: manualNews.home_team,
            away_team: manualNews.away_team,
            home_score: manualNews.home_score,
            away_score: manualNews.away_score,
            match_date: manualNews.match_date,
            goalscorers: manualNews.goalscorers?.map((g) => ({
              player_name: g.player_name,
              minute: g.minute,
              team:
                g.team === "HOME"
                  ? manualNews.home_team
                  : g.team === "AWAY"
                    ? manualNews.away_team
                    : g.team,
            })),
          };
          endpoint = `${process.env.BOT_API_URL}/generate-news/review`;
        }

        console.log(`🚀 Regenerating website news from ${endpoint}`);
        const response = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error(
            `Generate API failed: ${response.status} ${response.statusText}`
          );
        }

        const apiResponse = await response.json();
        if (!apiResponse.success || !apiResponse.data) {
          throw new Error("API returned unsuccessful response");
        }

        // 🔄 Update existing OR create new
        for (const newsItem of apiResponse.data) {
          const { website_id, image_url, title, content } = newsItem;

          const website = activeWebsites.find(
            (w) => w.documentId === website_id
          );
          if (!website) continue;

          let finalContent = content;
          if (image_url) {
            const imageHtml = `<div class="match-image"><img src="${image_url}" alt="${manualNews.home_team} vs ${manualNews.away_team}" style="max-width:100%; height:auto; margin:20px 0; border-radius:8px;"></div>`;
            finalContent = imageHtml + finalContent;
          }

          let websiteNews = existingWebsiteNews.find(
            (wn) => wn.users_website === website.documentId
          );

          if (websiteNews) {
            // ✏️ Update existing
            websiteNews = await strapi.entityService.update(
              "api::websites-news.websites-news",
              websiteNews.id,
              {
                data: {
                  content: finalContent,
                  title,
                  image_url,
                  publishedAt: null,
                },
                fields: ["id", "documentId"],
              }
            );
            console.log(
              `✏️ Updated website news for site ${website.documentId}`
            );
          } else {
            // ➕ Create new
            websiteNews = await strapi.entityService.create(
              "api::websites-news.websites-news",
              {
                data: {
                  content: finalContent,
                  title,
                  manual_news: manualNews.documentId,
                  users_website: website.documentId,
                  image_url,
                  publishedAt: null,
                },
                fields: ["id", "documentId"],
              }
            );
            console.log(
              `➕ Created website news for site ${website.documentId}`
            );
          }

          createdWebsiteNewsIds.push(websiteNews.id);
        }

        // ✅ Update manualNews with synced list
        if (createdWebsiteNewsIds.length > 0) {
          // await strapi.db.query("api::manual-news.manual-news").update({
          //   where: { id: manualNews.id }, // ✅ numeric ID
          //   data: {
          //     websites_news: createdWebsiteNewsIds, // ✅ array of numeric IDs
          //   },
          // });
          // console.log("🔗 Websites_news fully synced!");
            await strapi.entityService.update("api::manual-news.manual-news", manualNews.id, {
              data: {
                websites_news: createdWebsiteNewsIds, // ✅ numeric IDs only
              },
            });
            console.log("🔗 Websites_news fully synced!");
        }
        
      }
    } catch (error) {
      strapi.log.error("❌ Error in afterUpdate lifecycle:", error);
    }
    regenerate = false; // reset flag
  },
};
