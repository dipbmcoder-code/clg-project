# AI News Generator

An AI-powered news generation and publishing platform with automated content creation, image generation, WordPress publishing, and social media distribution.

## Architecture

```
+---------------------+     +------------------+     +-----------------+
|  Admin Dashboard    |---->|  Node.js Backend |---->|  PostgreSQL DB  |
|  (Next.js 14)       |     |  (Express/Prisma)|     |  (Backend)      |
+---------------------+     +------------------+     +-----------------+
                                     ^
                                     |
+---------------------+     +------------------+     +-----------------+
|  News Engine        |---->|  Python FastAPI   |---->|  PostgreSQL DB  |
|  (AI Generation)    |     |  (Cron + API)    |     |  (Engine)       |
+---------------------+     +------------------+     +-----------------+
         |
         v
  +--------------+  +----------+  +---------+
  |  WordPress   |  |  Twitter |  |  Reddit |
  |  Publishing  |  |  Posts   |  |  Posts  |
  +--------------+  +----------+  +---------+
```

## Components

### Node.js Backend (node-backend/)
Express.js REST API with Prisma ORM replacing the previous Strapi CMS.

- **Auth**: JWT-based authentication with role-based access (Super Admin, Admin, Agent)
- **Websites**: CRUD for WordPress site configurations with connection validation
- **News Prompts**: AI prompt templates for 8 news types
- **Manual News**: Create and assign manual articles to websites
- **News Logs**: Track all generation and publishing activity
- **AI Settings**: Manage OpenAI, Gemini, OpenRouter API keys and models
- **Social Media**: Twitter and Reddit auto-posting configuration and execution
- **WordPress**: Category sync, health checks, recent posts
- **RapidAPI**: Proxy for sports data (API-Football v3)

### Admin Dashboard (admin-dashboard/)
Next.js 14 admin panel with Material UI.

- Website management with WP connection testing
- News prompt editor for AI content templates
- Manual news creation workflow
- AI credentials settings (OpenAI, Gemini, OpenRouter, AWS, SendGrid)
- Social media configuration (Twitter API, Reddit API per website)
- WordPress category browser with tree view
- News generation logs viewer
- Role-based access control

### News Engine (news-engine/)
Python FastAPI service for AI content generation and automation.

- AI-powered article generation (OpenAI, OpenRouter)
- AI image generation (Google Gemini)
- Web scraping with Selenium
- Sports data via RapidAPI
- Automated WordPress publishing
- Social media auto-posting (Twitter + Reddit) after publish
- Cron-based scheduling for all news types

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Environment Variables

Create a .env file in the project root:

```
# Backend Database
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=ainews_backend
POSTGRES_DATA_PATH=./data/backend-db

# Node.js Backend
JWT_SECRET=your-jwt-secret-key
JWT_EXPIRES_IN=7d
PASSWORD_SECRET_KEY=your-aes-encryption-key
CORS_ORIGIN=http://localhost:3033

# Admin Dashboard
NEXT_PUBLIC_API_URL=http://node-backend:4000

# Python Engine Database
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=ainews_engine
PYTHON_DB_DATA_PATH=./data/python-db

# Python Engine
CMS_BASE_URL=http://node-backend:4000
CMS_ADMIN_USER_EMAIL=admin@ainews.com
CMS_ADMIN_USER_PASSWORD=admin123456
```

### Docker Deployment

```bash
# Start all services
docker-compose up -d

# With nginx-proxy (production)
docker-compose -f docker-compose.proxy.yml -f docker-compose.yml up -d

# View logs
docker-compose logs -f node-backend
docker-compose logs -f admin-dashboard
docker-compose logs -f news-engine
```

### Local Development

#### Node.js Backend
```bash
cd node-backend
npm install
cp .env.example .env
npx prisma migrate dev
npx prisma db seed
npm run dev
```

#### Admin Dashboard
```bash
cd admin-dashboard
npm install
npm run dev
```

#### News Engine
```bash
cd news-engine
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## API Endpoints

### Auth
- POST /api/auth/login - Login with email/password
- GET /api/auth/me - Get current user
- POST /api/auth/register - Register new user (admin only)

### Websites
- GET /api/websites - List all websites
- POST /api/websites - Create website
- PUT /api/websites/:id - Update website
- DELETE /api/websites/:id - Delete website
- POST /api/websites/:id/validate - Test WordPress connection

### AI Settings
- GET /api/ai-settings - Get settings (keys masked)
- PUT /api/ai-settings - Update settings
- POST /api/ai-settings/test - Test AI provider connection

### Social Media
- GET /api/social-media/config/:websiteId - Get social config
- PUT /api/social-media/config/:websiteId - Update social config
- POST /api/social-media/post - Post to Twitter/Reddit
- GET /api/social-media/posts - List all social posts

### WordPress
- GET /api/wordpress/categories/:websiteId - Get cached categories
- POST /api/wordpress/sync-categories/:websiteId - Sync from WordPress
- GET /api/wordpress/health/:websiteId - Check WP connection

## License

Private - All rights reserved.
