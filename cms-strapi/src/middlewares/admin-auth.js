import jwt from 'jsonwebtoken';

export default (config, { strapi }) => {
  return async (ctx, next) => {
    try {
      const authHeader = ctx.request.header.authorization;
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return ctx.unauthorized('No authorization token found');
      }

      const token = authHeader.split(' ')[1];
      const adminJwtSecret = strapi.config.get('admin.auth.secret');
      if (!adminJwtSecret) {
        return ctx.internalServerError('Admin JWT secret not configured');
      }

      let payload;
      try {
        payload = jwt.verify(token, adminJwtSecret);
      } catch (e) {
        return ctx.unauthorized('Invalid admin token');
      }

      const adminUser = await strapi.db
        .query('admin::user')
        .findOne({ where: { id: payload.id } });
      if (!adminUser) {
        return ctx.unauthorized('Admin user not found');
      }
      ctx.state.admin = adminUser;
      await next();
    } catch (err) {
      return ctx.unauthorized('Admin authentication failed');
    }
  };
}; 