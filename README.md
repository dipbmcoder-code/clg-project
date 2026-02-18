# AI News Generator

An automated news generation platform that scrapes content from Reddit and X (Twitter), uses AI to transform social media posts into professional news articles, and publishes them to configured WordPress websites.

## Architecture

```
┌─────────────────────────────────────────────┐
│              Docker Compose                  │
│                                              │
│  ┌──────────────┐  ┌────────────────────┐   │
│  │  PostgreSQL   │  │   Node.js Backend  │   │
│  │  (python-db)  │◄─│   (Express API)    │   │
│  │  :5444        │  │   :4000            │   │
│  └──────┬───────┘  └────────┬───────────┘   │
│         │                    │               │
│  ┌──────┴───────┐  ┌────────┴───────────┐   │
│  │ Python Cron  │  │  Next.js Dashboard  │   │
│  │ (Scrapers)   │  │  (Admin UI)         │   │
│  │              │  │  :3033              │   │
│  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────┘
```

### 1. Node.js Backend (`backend/`)
- **Express 4.21** REST API on port `4000`
- JWT authentication (SHA-256 password hashing)
- Full CRUD for: Websites, Users, News Prompts, News Logs, Social Posts, Dashboard Stats
- PostgreSQL via `pg` driver
- Auto database initialization + migration on startup

### 2. Admin Dashboard (`admin-dashboard/`)
- **Next.js 14** with App Router
- **MUI 5** component library with DataGrid
- Server-side rendering with cookie-based JWT auth
- Pages: Dashboard, Websites, Social Posts, AI Prompts, News Logs, Users

### 3. Python Scraping Engine (`news-engine/`)
- **PRAW** for Reddit scraping
- **Selenium + BeautifulSoup** for X (Twitter) scraping
- **OpenAI / Google AI** for content generation
- **Boto3** for image storage (AWS S3)
- Scheduled via `cron_all.py` (runs every 3 hours)

### 4. PostgreSQL Database
- Shared between Node.js backend and Python scraper
- Tables: `websites`, `users`, `news_prompts`, `news_logs`, `social_media_posts`

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### 1. Environment Setup

Configure the root `.env` file:
```bash
# Edit .env with your credentials
```

Key environment variables:
| Variable | Description | Default |
|----------|-------------|---------|
| `DB_USER` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `postgres` |
| `DB_NAME` | Database name | `strapi` |
| `JWT_SECRET` | JWT signing secret | (required) |
| `REDDIT_CLIENT_ID` | Reddit API client ID | (optional) |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | (optional) |
| `OPENAI_API_KEY` | OpenAI API key | (optional) |

### 2. Run with Docker Compose

```bash
docker-compose up --build -d
```

Services will be available at:
- **Dashboard**: http://localhost:3033
- **API**: http://localhost:4000
- **Health Check**: http://localhost:4000/health

### 3. Default Login
- **Email**: `admin@ainews.com`
- **Password**: `admin123`

---

## Local Development

### Backend
```bash
cd backend
npm install
npm run dev            # Starts with nodemon on :4000
```

### Dashboard
```bash
cd admin-dashboard
npm install
npm run dev            # Starts Next.js on :3033
```

### Python Scraper
```bash
cd news-engine
pip install -r requirements.txt
python cron_all.py     # Runs scraping jobs
```

---

## Project Structure

```
├── .env                     # Root environment variables (Docker)
├── .gitignore               # Git ignore rules
├── docker-compose.yml       # Docker orchestration
│
├── backend/                 # Node.js Express API
│   ├── src/
│   │   ├── index.js         # Server entry point
│   │   ├── config/db.js     # PostgreSQL pool
│   │   ├── middleware/auth.js # JWT auth
│   │   ├── utils/db-init.js # DB schema + migrations
│   │   └── routes/
│   │       ├── auth.js      # Login & profile
│   │       ├── websites.js  # Website CRUD
│   │       ├── users.js     # User management
│   │       ├── prompts.js   # AI prompt config
│   │       ├── logs.js      # News log viewer
│   │       ├── posts.js     # Social posts list
│   │       └── dashboard.js # Dashboard stats
│   ├── Dockerfile
│   └── package.json
│
├── admin-dashboard/         # Next.js Admin UI
│   ├── src/
│   │   ├── app/             # Next.js App Router pages
│   │   ├── sections/        # Page-level view components
│   │   ├── custom/          # Reusable form components
│   │   ├── auth/            # JWT auth context
│   │   ├── utils/           # API helpers
│   │   └── config-global.js # App configuration
│   ├── Dockerfile
│   └── package.json
│
├── news-engine/             # Python scraping engine
│   ├── cron_all.py          # Scheduler entry point
│   ├── social_media/        # Reddit & X scrapers
│   ├── publication/         # WordPress publishing
│   ├── requirements.txt
│   └── Dockerfile
│
└── Documentation/           # Feature documentation
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/auth/login` | Login (returns JWT) |
| `GET` | `/api/auth/me` | Current user profile |
| `GET/POST/PUT/DELETE` | `/api/websites` | Website management |
| `GET/POST/PUT/DELETE` | `/api/users` | User management |
| `GET/PUT` | `/api/news-prompts` | AI prompt configuration |
| `GET` | `/api/news-logs` | News generation logs |
| `GET` | `/api/social-posts` | Scraped social posts |
| `GET` | `/api/dashboard/stats` | Dashboard statistics |
| `GET` | `/health` | Health check |

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | Express.js | 4.21 |
| Frontend | Next.js | 14.2 |
| UI Library | MUI | 5.16 |
| Database | PostgreSQL | 17 |
| Auth | JWT (jsonwebtoken) | 9.0 |
| Scraping | PRAW, Selenium | Latest |
| AI | OpenAI, Google AI | Latest |
| Container | Docker Compose | v2 |

---

**Built with ❤️ using Next.js, Express, and Material-UI**

