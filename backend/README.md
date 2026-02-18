# AI News Generator Backend

This is the Node.js API backend for the AI News Generator project.

## Architecture & Structure

The codebase follows the MVC-ish pattern for organizing logic:

- `src/server.js`: Application entry point. Handles server startup and graceful shutdown.
- `src/app.js`: Express application configuration (middleware, routes).
- `src/controllers/`: Request handlers logic. Separates business logic from routing.
- `src/models/`: Database abstraction layer (Data Access Objects).
- `src/routes/`: Route definitions, mapping endpoints to controller methods.
- `src/middlewares/`: Express middleware (Authentication, Validation, Error handling).
- `src/utils/`: Utility functions.
- `src/config/`: Configuration files (Database, Logger, Seeder).
- `migrations/`: Database schema migrations.
- `tests/`: Integration tests.

## Usage

### Development

```bash
npm run dev
```

### Production

```bash
npm start
```

### Database Management

The application uses `node-pg-migrate` for schema management.

1.  **Up**: Apply pending migrations
    ```bash
    npm run migrate:up
    ```

2.  **Down**: Revert last migration
    ```bash
    npm run migrate:down
    ```

3.  **Seed**: Populate default data
    ```bash
    npm run db:seed
    ```

### Testing

```bash
npm test
```
