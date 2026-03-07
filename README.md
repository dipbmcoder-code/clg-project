# AI News Generator
### Automated Social Media to News Publishing System

**College/University Name**
Department of Computer Science & Engineering
B.E. / B.Tech — Computer Science & Engineering
Academic Year: 2025–2026

---

## Table of Contents

| Sr. No. | Section | Page |
|---------|---------|------|
| 3 | Introduction | 3 |
| 3.1 | About Institute | 5 |
| 4 | System Analysis | 7 |
| 4.1 | Project Introduction | 7 |
| 4.2 | Need For System | 7 |
| 4.3 | Project Advantages | 8 |
| 4.4 | Project Disadvantages | 9 |
| 5 | Functional Specification | 10 |
| 5.1 | Users of the System | 10 |
| 5.2 | Modules of the System | 11 |
| 6 | System Requirements | 12 |
| 6.1 | Hardware Requirements | 12 |
| 6.2 | Software Requirements | 13 |
| 6.3 | Network Requirements | 14 |
| 7 | System Design | 15 |
| 7.1 | ER Diagram | 15 |
| 7.2 | Data Flow Diagram | 16 |
| 7.3 | Data Dictionary | 18 |

---

## 3. Introduction

The **AI News Generator** is a fully automated, end-to-end news generation and publishing platform that bridges the gap between raw social media content and professionally written news articles using Artificial Intelligence.

The system continuously monitors social media platforms — **Reddit** and **X (formerly Twitter)** — extracts trending posts and discussions, transforms them into polished news articles using state-of-the-art AI language models, and automatically publishes the generated content to configured **WordPress** websites.

This project demonstrates the practical application of modern software engineering principles including:

- Microservices Architecture
- Containerization (Docker)
- RESTful API Design
- JWT-based Authentication
- AI-driven Content Generation

### Key Highlights

| Feature | Description |
|---------|-------------|
| **Automated Content Pipeline** | From social media scraping to WordPress publishing — fully automated without human intervention |
| **AI-Powered Writing** | Uses OpenAI GPT-4 and Google Gemini AI to generate human-quality news articles |
| **Multi-Platform Scraping** | Supports Reddit (via PRAW API) and X/Twitter (via Selenium web automation) |
| **Admin Dashboard** | A professional Next.js-based admin panel to manage websites, prompts, logs, and users |
| **Containerized Deployment** | Entire stack runs via Docker Compose for easy, reproducible deployment |

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Compose                            │
│                                                                  │
│  ┌─────────────────┐         ┌──────────────────────────────┐   │
│  │   PostgreSQL    │         │     Node.js Backend          │   │
│  │   Database      │◄────────│     Express REST API         │   │
│  │   Port: 5444    │         │     Port: 4000               │   │
│  └────────┬────────┘         └──────────────┬───────────────┘   │
│           │                                  │ REST API          │
│           │                                  ▼                   │
│  ┌────────┴────────┐         ┌──────────────────────────────┐   │
│  │  Python Cron    │         │   Next.js Admin Dashboard    │   │
│  │  (news-engine)  │         │   Port: 3033                 │   │
│  │  - Scrapers     │         │   - MUI Components           │   │
│  │  - AI Generator │         │   - JWT Auth (Cookies)       │   │
│  │  - WP Publisher │         │   - Server-Side Rendering    │   │
│  └─────────────────┘         └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

External Services:
  ├── OpenAI API (GPT-4)
  ├── Google Gemini API
  ├── Reddit API (PRAW)
  ├── X / Twitter (Selenium)
  ├── AWS S3 (Image Storage)
  └── WordPress REST API (Publishing)
```

---

## 3.1 About Institute

| Field | Details |
|-------|---------|
| **Institute Name** | *(Your College / University Name)* |
| **Department** | Department of Computer Science & Engineering |
| **Course** | B.E. / B.Tech — Computer Science & Engineering |
| **Academic Year** | 2025–2026 |
| **Project Guide** | *(Prof. / Dr. Guide Name)* |
| **Project Title** | AI News Generator — Automated Social Media to News Publishing System |
| **Team Members** | *(Student Names and Roll Numbers)* |

---

## 4. System Analysis

### 4.1 Project Introduction

The **AI News Generator** is a web-based software system designed to automate the complete process of news article creation and publication. In the modern digital era, news organizations and content creators face the challenge of producing high-quality, timely content at scale.

This project addresses that challenge by creating an intelligent pipeline that operates through four distinct stages:

| Stage | Process | Technology Used |
|-------|---------|----------------|
| **Stage 1** | Scrape trending posts from Reddit and X (Twitter) | Python, PRAW, Selenium |
| **Stage 2** | Process raw social media data and store it | PostgreSQL, psycopg2 |
| **Stage 3** | Generate professional news articles using AI models | OpenAI GPT-4, Google Gemini |
| **Stage 4** | Publish generated articles to WordPress websites | WordPress REST API |
| **Stage 5** | Monitor the entire process through admin dashboard | Next.js, Node.js Express |

The system is built using a **microservices architecture** with three primary services:

1. A **Node.js Express** backend providing a RESTful API
2. A **Next.js** admin dashboard as the frontend interface
3. A **Python** scraping and AI generation engine (news-engine)

All services communicate through a shared **PostgreSQL** database and are fully orchestrated using **Docker Compose**.

---

### 4.2 Need For System

The need for this system arises from several real-world challenges faced by digital media organizations and content creators:

#### 1. Content Velocity Demand
Modern news consumers expect real-time updates. Manual news writing cannot keep pace with the speed at which events unfold on social media. An automated system can generate and publish articles within minutes of a trending event — a task that would take a human writer 30–60 minutes.

#### 2. Resource Constraints
Hiring large editorial teams is expensive. Small and medium-sized news portals often lack the resources to produce consistent, high-volume content. This system acts as a **force multiplier**, enabling a small team to manage multiple news websites simultaneously.

#### 3. Social Media as a Primary News Source
A significant portion of breaking news originates on platforms like Reddit and X. Manually monitoring these platforms is time-consuming and error-prone. An automated scraper ensures no trending topic is missed.

#### 4. Consistency and Quality
AI-generated content, when guided by well-crafted prompts, maintains a consistent **tone, style, and structure** across all articles — something that is difficult to achieve with multiple human writers working independently.

#### 5. Scalability
The system is designed to manage multiple WordPress websites from a single dashboard. As the business scales, new websites can be added without any changes to the core infrastructure.

#### 6. Centralized Management
Without a system like this, managing scrapers, AI prompts, publication logs, and website credentials would require separate tools. This project **consolidates everything** into one unified admin panel.

---

### 4.3 Project Advantages

| # | Advantage | Description |
|---|-----------|-------------|
| 1 | **Full Automation** | The entire pipeline — from scraping to publishing — runs automatically on a scheduled cron job (every 3 hours), requiring zero manual intervention. |
| 2 | **AI-Quality Content** | Uses state-of-the-art AI models (OpenAI GPT-4, Google Gemini) to produce grammatically correct, contextually accurate, and engaging news articles. |
| 3 | **Multi-Website Support** | A single installation can manage and publish to multiple WordPress websites simultaneously, each with its own configuration and AI prompts. |
| 4 | **Customizable AI Prompts** | Administrators can configure custom prompts for each website, allowing fine-grained control over writing style, tone, and content focus. |
| 5 | **Centralized Dashboard** | The Next.js admin panel provides a single interface to manage websites, view scraped posts, monitor news logs, and manage users. |
| 6 | **Secure Authentication** | JWT-based authentication with SHA-256 password hashing ensures secure access to the admin panel and API. |
| 7 | **Containerized Deployment** | Docker Compose makes the system deployable on any server with a single command, ensuring full environment consistency. |
| 8 | **Scalable Architecture** | The microservices design allows individual components (backend, scraper, dashboard) to be scaled independently based on load. |
| 9 | **Image Support** | Integration with AWS S3 (via Boto3) allows AI-generated articles to include relevant cloud-stored featured images. |
| 10 | **Comprehensive Logging** | All news generation events are logged in the database, providing full audit trails and debugging capabilities. |

---

### 4.4 Project Disadvantages

| # | Disadvantage | Description |
|---|-------------|-------------|
| 1 | **AI API Cost** | The system relies on paid AI APIs (OpenAI, Google Gemini). High-volume usage can result in significant API costs. |
| 2 | **Platform Dependency** | The scraping engine depends on the structure of Reddit and X (Twitter). Changes to these platforms' layouts or APIs can break the scrapers. |
| 3 | **Content Accuracy** | AI-generated content may occasionally contain factual inaccuracies or hallucinations. Human editorial review is recommended before publishing to high-stakes websites. |
| 4 | **Rate Limiting** | Both Reddit's PRAW API and X's web interface impose rate limits, which can slow down the scraping process during high-traffic periods. |
| 5 | **WordPress Dependency** | The publishing module is tightly coupled to WordPress. Publishing to other CMS platforms (e.g., Ghost, Drupal) would require additional development. |
| 6 | **Internet Dependency** | The system requires a stable internet connection for scraping, AI generation, and publishing. Any network disruption halts the pipeline. |
| 7 | **Selenium Fragility** | The X (Twitter) scraper uses Selenium browser automation, which is inherently fragile and may break with browser or website updates. |

---

## 5. Functional Specification

### 5.1 Users of the System

The system defines two primary user roles with distinct levels of access and responsibility:

#### Role 1: Super Administrator

| Permission | Access Level |
|-----------|--------------|
| User account management (create, edit, delete) | ✅ Full Access |
| Website management (all websites) | ✅ Full Access |
| AI prompt configuration | ✅ Full Access |
| View scraped social media posts | ✅ Full Access |
| View news generation logs | ✅ Full Access |
| Dashboard statistics overview | ✅ Full Access |
| System-level settings | ✅ Full Access |

#### Role 2: Regular Administrator

| Permission | Access Level |
|-----------|--------------|
| User account management | ❌ No Access |
| Website management (assigned websites only) | ✅ Limited Access |
| AI prompt configuration (own websites) | ✅ Limited Access |
| View scraped social media posts | ✅ Full Access |
| View news generation logs | ✅ Full Access |
| Dashboard statistics overview | ✅ Full Access |
| System-level settings | ❌ No Access |

---

### 5.2 Modules of the System

The system is divided into **seven functional modules**, each responsible for a specific area of functionality:

---

#### Module 1: Authentication Module

**Objective**: Handle user login, session management, and access control.

| Feature | Description |
|---------|-------------|
| Secure Login | Email + password authentication (SHA-256 hashing) |
| JWT Token Generation | Issued on successful login for API authorization |
| Cookie-based Sessions | Persistent sessions in the Next.js admin dashboard |
| Protected API Routes | All sensitive endpoints require a valid JWT token |
| User Profile Retrieval | Endpoint: `GET /api/auth/me` |

---

#### Module 2: Website Management Module

**Objective**: Allow administrators to manage WordPress websites targeted for news publication.

| Feature | Description |
|---------|-------------|
| CRUD Operations | Add, Edit, View, Delete WordPress site configurations |
| Credential Storage | Stores WordPress URL, username, and Application Password |
| Prompt Association | Link AI prompts to specific websites |
| Enable / Disable | Toggle individual sites in/out of the publishing pipeline |

---

#### Module 3: Social Media Scraping Module

**Objective**: Automatically scrape and store posts from Reddit and X (Twitter) on a schedule.

| Feature | Description |
|---------|-------------|
| Reddit Scraping | Via PRAW API — subreddit-based post fetching |
| X (Twitter) Scraping | Via Selenium + BeautifulSoup browser automation |
| Deduplication | Prevents reprocessing of already-scraped posts |
| Data Storage | Normalizes and stores posts in `social_media_posts` table |
| Configurable Schedule | Default interval: every 3 hours via cron scheduler |

---

#### Module 4: AI News Generation Module

**Objective**: Transform raw social media posts into professional news articles using AI.

| Feature | Description |
|---------|-------------|
| Multi-Model Support | Supports both OpenAI GPT-4 and Google Gemini AI |
| Custom Prompts | Uses per-website AI prompts stored in the database |
| Article Components | Generates article title, body content, and meta description |
| Image Handling | Fetches and uploads featured images to AWS S3 via Boto3 |
| Event Logging | Logs every generation attempt (success/failure) to `news_logs` |

---

#### Module 5: WordPress Publishing Module

**Objective**: Publish AI-generated articles to configured WordPress websites automatically.

| Feature | Description |
|---------|-------------|
| REST API Publishing | Publishes via WordPress REST API |
| Authentication | Basic Auth using WordPress Application Passwords |
| Category & Tags | Assigns categories and tags to published posts |
| Featured Image Upload | Uploads images to WordPress Media Library |
| Status Recording | Records WordPress Post ID and URL in `news_logs` table |

---

#### Module 6: Admin Dashboard Module

**Objective**: Provide a centralized Next.js web interface for complete system management.

| Page | Features |
|------|---------|
| **Dashboard** | Statistics overview — websites, posts scraped, articles generated, success rate |
| **Websites** | Full CRUD interface using MUI DataGrid |
| **Social Posts** | View all scraped posts with platform and status filters |
| **AI Prompts** | Configure and manage AI generation prompts per website |
| **News Logs** | Detailed logs of all generation and publishing events |
| **Users** | Manage admin accounts (Super Admin only) |

---

#### Module 7: User Management Module

**Objective**: Manage administrator accounts and access roles within the system.

| Feature | Description |
|---------|-------------|
| User CRUD | Create, View, Edit, Delete admin accounts |
| Role-Based Access | Super Admin vs. Regular Admin role enforcement |
| Secure Passwords | SHA-256 hashed password storage and management |

---

## 6. System Requirements

### 6.1 Hardware Requirements

| Component | Minimum Requirement | Recommended |
|-----------|--------------------|----|
| **Processor** | Intel Core i3 / AMD Ryzen 3 (2.0 GHz) | Intel Core i5 / AMD Ryzen 5 (3.0 GHz+) |
| **RAM** | 4 GB | 8 GB or more |
| **Storage** | 20 GB free disk space | 50 GB SSD |
| **Network** | Broadband Internet (10 Mbps) | High-speed Internet (50 Mbps+) |
| **Display** | 1280 × 720 resolution | 1920 × 1080 resolution |

---

### 6.2 Software Requirements

#### Server / Deployment Environment

| Software | Version | Purpose |
|----------|---------|---------|
| **Docker** | 24.0+ | Container runtime |
| **Docker Compose** | v2.0+ | Multi-container orchestration |
| **Ubuntu / Debian Linux** | 20.04 LTS+ | Recommended host operating system |

#### Backend (Node.js)

| Software | Version | Purpose |
|----------|---------|---------|
| **Node.js** | 20 LTS | JavaScript runtime environment |
| **npm** | 10+ | Package manager |
| **Express.js** | 4.21 | REST API framework |
| **PostgreSQL** | 17 | Relational database |
| **jsonwebtoken** | 9.0 | JWT authentication |
| **pg** | Latest | PostgreSQL client for Node.js |
| **bcryptjs / crypto** | Built-in | Password hashing (SHA-256) |
| **morgan** | Latest | HTTP request logger |
| **cors** | Latest | Cross-Origin Resource Sharing middleware |

#### Frontend (Admin Dashboard)

| Software | Version | Purpose |
|----------|---------|---------|
| **Next.js** | 14.2 | React framework with App Router |
| **React** | 18 | UI component library |
| **MUI (Material-UI)** | 5.16 | UI component framework |
| **MUI DataGrid** | 7.x | Advanced data table component |
| **Axios** | Latest | HTTP client for API requests |

#### Python News Engine

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.11+ | Primary scripting language |
| **PRAW** | 7.8.1 | Reddit API wrapper |
| **Selenium** | 4.9.1 | Browser automation for X scraping |
| **BeautifulSoup4** | 4.12.3 | HTML parsing |
| **OpenAI** | 1.63.2 | OpenAI GPT API client |
| **google-genai** | 1.52.0 | Google Gemini AI client |
| **Boto3** | 1.28.0 | AWS S3 image storage |
| **psycopg2-binary** | 2.9.10 | PostgreSQL client for Python |
| **FastAPI** | 0.111.0 | Optional internal API layer |
| **schedule** | 1.2.2 | Cron job scheduler |
| **python-dotenv** | 1.0.0 | Environment variable management |

#### External Services & APIs

| Service | Purpose |
|---------|---------|
| **OpenAI API** | GPT-4 model for news article generation |
| **Google Gemini API** | Alternative AI model for content generation |
| **Reddit API (PRAW)** | Authenticated access to Reddit posts |
| **AWS S3** | Cloud image storage for article featured images |
| **WordPress REST API** | Publishing generated articles to WordPress sites |

---

### 6.3 Network Requirements

| Requirement | Details |
|-------------|---------|
| **Application Ports** | 3033 (Dashboard), 4000 (Backend API), 5444 (PostgreSQL) |
| **Internet Access** | Required for AI APIs, Reddit API, X scraping, WordPress publishing |
| **CORS Configuration** | Configurable via `CORS_ORIGIN` environment variable |

---

## 7. System Design

### 7.1 ER Diagram

The database consists of **5 primary tables** with the following entity relationships:

```
╔═════════════════════════════════════════════════════════════════════╗
║                         ER DIAGRAM                                  ║
╠═════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  ┌──────────────┐              ┌───────────────────┐               ║
║  │    users     │              │     websites      │               ║
║  ├──────────────┤              ├───────────────────┤               ║
║  │ PK id        │              │ PK id             │               ║
║  │    name      │              │    name           │               ║
║  │    email     │              │    url            │               ║
║  │    password  │              │    wp_username    │               ║
║  │    role      │              │    wp_password    │               ║
║  │    created_at│              │    is_active      │               ║
║  │    updated_at│              │    created_at     │               ║
║  └──────────────┘              │    updated_at     │               ║
║   (Manages System)             └────────┬──────────┘               ║
║                                         │ 1                        ║
║                               ──────────┤                          ║
║                               │ 1:N     │ 1:N                      ║
║                               ▼         ▼                          ║
║                    ┌──────────────────┐ ┌──────────────────────┐   ║
║                    │  news_prompts    │ │     news_logs        │   ║
║                    ├──────────────────┤ ├──────────────────────┤   ║
║                    │ PK id            │ │ PK id                │   ║
║                    │ FK website_id    │ │ FK website_id        │   ║
║                    │    prompt_text   │ │ FK social_post_id ──►║   ║
║                    │    ai_model      │ │    article_title     │   ║
║                    │    is_active     │ │    article_body      │   ║
║                    │    created_at    │ │    wp_post_id        │   ║
║                    │    updated_at    │ │    wp_post_url       │   ║
║                    └──────────────────┘ │    status            │   ║
║                                         │    error_message     │   ║
║  ┌──────────────────────┐               │    ai_model_used     │   ║
║  │  social_media_posts  │◄──────────────│    created_at        │   ║
║  ├──────────────────────┤     1:1       └──────────────────────┘   ║
║  │ PK id                │                                          ║
║  │    platform          │                                          ║
║  │    post_id (UNIQUE)  │                                          ║
║  │    title             │                                          ║
║  │    content           │                                          ║
║  │    author            │                                          ║
║  │    url               │                                          ║
║  │    subreddit         │                                          ║
║  │    score             │                                          ║
║  │    is_processed      │                                          ║
║  │    scraped_at        │                                          ║
║  └──────────────────────┘                                          ║
╠═════════════════════════════════════════════════════════════════════╣
║  RELATIONSHIPS:                                                     ║
║  • Website    ──< News Prompts      (One-to-Many)                  ║
║  • Website    ──< News Logs         (One-to-Many)                  ║
║  • Social Post ─── News Log         (One-to-One)                   ║
║  • Users are independent (manage system, not linked to content)    ║
╚═════════════════════════════════════════════════════════════════════╝
```

---

### 7.2 Data Flow Diagram

#### Level 0 DFD — Context Diagram

The context diagram shows the system as a single process with all external entities:

```
╔═════════════════════════════════════════════════════════════╗
║                  LEVEL 0 — CONTEXT DIAGRAM                  ║
╠═════════════════════════════════════════════════════════════╣
║                                                             ║
║                                                             ║
║   ┌──────────┐   Raw Posts    ┌──────────────────────────┐ ║
║   │ Reddit / │ ──────────────►│                          │ ║
║   │ X (Twitter)│              │                          │ Publish ┌──────────┐
║   └──────────┘                │   AI NEWS GENERATOR      │ ───────►│WordPress │
║                               │        SYSTEM            │         └──────────┘
║   ┌──────────┐  Credentials / │                          │ Reports ┌──────────┐
║   │  Admin   │  Config ──────►│                          │ ───────►│Dashboard │
║   │  User    │                │                          │         └──────────┘
║   └──────────┘                └──────────────────────────┘
║                                         ▲
║                               Generated │
║   ┌──────────┐   Article Req  │ Content  │
║   │ OpenAI / │ ◄──────────────┘          │
║   │ Gemini AI│ ──────────────────────────┘
║   └──────────┘
║
╚═════════════════════════════════════════════════════════════╝
```

---

#### Level 1 DFD — Main Processes

```
╔══════════════════════════════════════════════════════════════════════╗
║                    LEVEL 1 — MAIN PROCESSES DFD                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  ┌──────────────┐                                                    ║
║  │  Reddit / X  │                                                    ║
║  │  (Twitter)   │                                                    ║
║  └──────┬───────┘                                                    ║
║         │ Raw Posts                                                  ║
║         ▼                                                            ║
║  ┌─────────────────────────────────────────────────────────────┐    ║
║  │            PROCESS 1: SOCIAL MEDIA SCRAPING                 │    ║
║  │        (Python: PRAW + Selenium + BeautifulSoup)            │    ║
║  │  • Fetch posts from Reddit subreddits and X accounts        │    ║
║  │  • Deduplicate against existing database records            │    ║
║  │  • Normalize post data (title, content, author, URL)        │    ║
║  └──────────────────────────┬────────────────────────────────┘     ║
║                             │ Normalized Posts                       ║
║                             ▼                                        ║
║                    ┌─────────────────┐                              ║
║                    │  D1: PostgreSQL │                              ║
║                    │   social_media_ │                              ║
║                    │      posts      │                              ║
║                    └────────┬────────┘                              ║
║                             │ Unprocessed Posts                      ║
║                             ▼                                        ║
║  ┌─────────────────────────────────────────────────────────────┐    ║
║  │            PROCESS 2: AI NEWS GENERATION                    │    ║
║  │           (Python: OpenAI / Google Gemini)                  │    ║
║  │  • Retrieve unprocessed posts from database                 │    ║
║  │  • Fetch AI prompt configuration for target website         │    ║
║  │  • Send post content + prompt to AI model                   │    ║
║  │  • Receive generated article (title, body, meta)            │    ║
║  │  • Fetch and upload featured image to AWS S3                │    ║
║  └──────────────────────────┬────────────────────────────────┘     ║
║                             │ Generated Article                      ║
║                             ▼                                        ║
║  ┌─────────────────────────────────────────────────────────────┐    ║
║  │          PROCESS 3: WORDPRESS PUBLISHING                    │    ║
║  │       (Python: WordPress REST API via requests)             │    ║
║  │  • Authenticate with WordPress Application Password         │    ║
║  │  • Upload featured image to WordPress Media Library         │    ║
║  │  • Create and publish post via REST API                     │    ║
║  │  • Record WordPress Post ID and status in news_logs         │    ║
║  └──────────────────────────┬────────────────────────────────┘     ║
║                             │ Publication Status                     ║
║                             ▼                                        ║
║                    ┌─────────────────┐                              ║
║                    │  D2: PostgreSQL │                              ║
║                    │   news_logs     │                              ║
║                    └────────┬────────┘                              ║
║                             │ Logs & Stats                           ║
║                             ▼                                        ║
║  ┌─────────────────────────────────────────────────────────────┐    ║
║  │          PROCESS 4: ADMIN DASHBOARD                         │    ║
║  │        (Next.js + Node.js Express API)                      │    ║
║  │  • Display dashboard statistics                             │    ║
║  │  • Manage websites, prompts, and users via CRUD             │    ║
║  │  • View scraped posts and news logs                         │    ║
║  │  • Authenticate administrators via JWT                      │    ║
║  └─────────────────────────────────────────────────────────────┘    ║
║         ▲                                                            ║
║         │ CRUD Operations (via REST API)                             ║
║  ┌──────┴───────┐                                                    ║
║  │  Admin User  │                                                    ║
║  └──────────────┘                                                    ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

#### Level 2 DFD — Authentication Sub-Process

```
╔══════════════════════════════════════════════════════════════════════╗
║              LEVEL 2 — AUTHENTICATION SUB-PROCESS DFD               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  ┌──────────────┐                                                    ║
║  │  Admin User  │                                                    ║
║  └──────┬───────┘                                                    ║
║         │ Email + Password                                           ║
║         ▼                                                            ║
║  ┌──────────────────────────────────────────────────────────┐       ║
║  │            PROCESS 4.1: INPUT VALIDATION                 │       ║
║  │   • Check email format                                   │       ║
║  │   • Check password field is not empty                    │       ║
║  └──────────────────────────┬───────────────────────────────┘       ║
║                             │ Valid Credentials                      ║
║                             ▼                                        ║
║  ┌────────────────────────���─────────────────────────────────┐       ║
║  │            PROCESS 4.2: USER LOOKUP                      │       ║
║  │   • Query users table by email                           │       ║
║  │   • Return user record if found                          │       ║
║  └──────────────────────────┬───────────────────────────────┘       ║
║                             │ User Record                            ║
║                             ▼                                        ║
║                    ┌─────────────────┐                              ║
║                    │  D3: PostgreSQL │                              ║
║                    │   users table   │                              ║
║                    └────────┬────────┘                              ║
║                             │ Stored Hash                            ║
║                             ▼                                        ║
║  ┌──────────────────────────────────────────────────────────┐       ║
║  │            PROCESS 4.3: PASSWORD VERIFICATION            │       ║
║  │   • Hash input password using SHA-256                    │       ║
║  │   • Compare with stored hash from database               │       ║
║  └──────────────────────────┬───────────────────────────────┘       ║
║                             │ Verified Identity                      ║
║                             ▼                                        ║
║  ┌──────────────────────────────────────────────────────────┐       ║
║  │            PROCESS 4.4: JWT TOKEN GENERATION             │       ║
║  │   • Generate signed JWT token with user ID + role        │       ║
║  │   • Set HTTP-only cookie in Next.js dashboard            │       ║
║  │   • Return success response to client                    │       ║
║  └──────────────────────────────────────────────────────────┘       ║
║                             │ JWT Token (Cookie)                     ║
║                             ▼                                        ║
║                    ┌─────────────────────────┐                      ║
║                    │  Admin Dashboard        │                      ║
║                    │  (Authenticated Session)│                      ║
║                    └─────────────────────────┘                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

### 7.3 Data Dictionary

#### Table 1: `users`

**Description**: Stores administrator account information for system access.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique user identifier (auto-increment) |
| `name` | VARCHAR(255) | NOT NULL | Full name of the administrator |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | Login email address |
| `password` | VARCHAR(255) | NOT NULL | SHA-256 hashed password string |
| `role` | VARCHAR(50) | DEFAULT `'admin'` | User role: `super_admin` or `admin` |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

#### Table 2: `websites`

**Description**: Stores WordPress website configurations for news publishing targets.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique website identifier |
| `name` | VARCHAR(255) | NOT NULL | Friendly name of the website |
| `url` | TEXT | NOT NULL | WordPress site base URL |
| `wp_username` | VARCHAR(255) | NOT NULL | WordPress admin username |
| `wp_password` | TEXT | NOT NULL | WordPress Application Password |
| `is_active` | BOOLEAN | DEFAULT TRUE | Whether the site is enabled for publishing |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

#### Table 3: `news_prompts`

**Description**: Stores AI prompt configurations associated with specific WordPress websites.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique prompt identifier |
| `website_id` | INTEGER | FK → `websites(id)` | Associated website reference |
| `prompt_text` | TEXT | NOT NULL | The AI system prompt / instruction text |
| `ai_model` | VARCHAR(100) | NOT NULL | AI model to use (e.g., `gpt-4`, `gemini-pro`) |
| `is_active` | BOOLEAN | DEFAULT TRUE | Whether this prompt is currently active |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

#### Table 4: `social_media_posts`

**Description**: Stores raw scraped post data from Reddit and X (Twitter).

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique post identifier |
| `platform` | VARCHAR(50) | NOT NULL | Source platform: `reddit` or `twitter` |
| `post_id` | VARCHAR(255) | NOT NULL, UNIQUE | Original post ID from the source platform |
| `title` | TEXT | — | Post title or headline |
| `content` | TEXT | — | Full post body / text content |
| `author` | VARCHAR(255) | — | Original post author username |
| `url` | TEXT | — | Direct URL to the original post |
| `subreddit` | VARCHAR(255) | — | Subreddit name (Reddit-only field) |
| `score` | INTEGER | DEFAULT 0 | Post upvotes / engagement score |
| `is_processed` | BOOLEAN | DEFAULT FALSE | Whether the post has been used for news generation |
| `scraped_at` | TIMESTAMP | DEFAULT NOW() | Timestamp when the post was scraped |

---

#### Table 5: `news_logs`

**Description**: Stores logs for every news generation and WordPress publishing event.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique log entry identifier |
| `website_id` | INTEGER | FK → `websites(id)` | Target website for publication |
| `social_post_id` | INTEGER | FK → `social_media_posts(id)` | Source social media post reference |
| `article_title` | TEXT | — | Generated article headline |
| `article_body` | TEXT | — | Full generated article content |
| `wp_post_id` | INTEGER | — | WordPress post ID after successful publishing |
| `wp_post_url` | TEXT | — | Published article URL on WordPress |
| `image_url` | TEXT | — | Featured image URL (AWS S3 or WordPress) |
| `status` | VARCHAR(50) | NOT NULL | Status: `success`, `failed`, or `pending` |
| `error_message` | TEXT | — | Error details if `status = 'failed'` |
| `ai_model_used` | VARCHAR(100) | — | AI model that generated the article |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Log entry creation timestamp |

---

## Appendix A: API Endpoint Reference

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/auth/login` | No | Login and receive JWT token |
| `GET` | `/api/auth/me` | Yes | Get current logged-in user profile |
| `GET` | `/api/websites` | Yes | List all configured websites |
| `POST` | `/api/websites` | Yes | Create a new website configuration |
| `PUT` | `/api/websites/:id` | Yes | Update an existing website |
| `DELETE` | `/api/websites/:id` | Yes | Delete a website |
| `GET` | `/api/users` | Yes (Super Admin) | List all administrator accounts |
| `POST` | `/api/users` | Yes (Super Admin) | Create a new administrator |
| `PUT` | `/api/users/:id` | Yes (Super Admin) | Update an administrator account |
| `DELETE` | `/api/users/:id` | Yes (Super Admin) | Delete an administrator account |
| `GET` | `/api/news-prompts` | Yes | Get all AI prompt configurations |
| `PUT` | `/api/news-prompts/:id` | Yes | Update an AI prompt |
| `GET` | `/api/news-logs` | Yes | View all news generation logs |
| `GET` | `/api/social-posts` | Yes | View all scraped social media posts |
| `GET` | `/api/dashboard/stats` | Yes | Get dashboard overview statistics |
| `GET` | `/health` | No | System health check |

---

*Document prepared for academic submission.*
*Project: AI News Generator — Automated Social Media to News Publishing System*
*Academic Year: 2025–2026*