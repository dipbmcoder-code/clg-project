"use strict";

module.exports = {
  async afterFindOne(result, params) {
    if (!result) return result;

    // Inject documentId for convenience
    result.documentId = result.documentId || result.id;

    // Populate users_website if it's only an ID
    if (result.users_website && typeof result.users_website === "string") {
      try {
        const website = await strapi.db
          .query("api::users-website.users-website")
          .findOne({
            where: { documentId: result.users_website },
            select: ["id", "documentId", "name"], // select fields you need
          });
        result.users_website = website;
      } catch (err) {
        console.error("Failed to populate users_website:", err);
        result.users_website = null;
      }
    }

    return result;
  },
};
