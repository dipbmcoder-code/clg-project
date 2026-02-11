export default {
  routes: [
    {
      method: 'GET',
      path: '/rapidapi/players/profiles',
      handler: 'rapidapi.fetchPlayers',
      config: {
        auth: false,
        middlewares: ["global::admin-auth"],
      },
    },
    {
      method: 'GET',
      path: '/rapidapi/leagues',
      handler: 'rapidapi.fetchLeagues',
      config: {
        auth: false,
        middlewares: ["global::admin-auth"],
      },
    }
  ],
};
