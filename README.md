# Football News App

A comprehensive football news platform built with modern web technologies, featuring a Next.js admin dashboard, Strapi CMS backend, and a news engine for content management.

## 🏗️ Project Architecture

This project consists of three main components:

### 1. Admin Dashboard (`admin-dashboard/`)
- **Technology**: Next.js 14 with React 18
- **UI Framework**: Material-UI (MUI) v5
- **Styling**: Emotion with custom theme system
- **Authentication**: JWT-based authentication
- **Features**: 
  - Modern admin interface with dashboard layouts
  - Responsive design with mobile support
  - Form handling with React Hook Form
  - Data visualization with charts and grids
  - Custom animations with Framer Motion
  - Multi-language support (RTL/LTR)
  - Theme customization and dark/light modes

### 2. CMS Backend (`cms-strapi/`)
- **Technology**: Strapi v5.17.0
- **Database**: PostgreSQL
- **Features**:
  - Headless CMS for content management
  - RESTful API endpoints
  - User permissions and roles
  - Media management
  - Content type builder
  - Admin panel for content editors

### 3. News Engine (`news-engine/`)
- **Purpose**: Content aggregation and processing system
- **Features**: Automated news collection and processing

## 🚀 Getting Started

### Prerequisites

- Node.js 20.x or higher
- PostgreSQL database
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FootballNewsApp
   ```

2. **Install Admin Dashboard dependencies**
   ```bash
   cd admin-dashboard
   npm install
   # or
   yarn install
   ```

3. **Install CMS Backend dependencies**
   ```bash
   cd ../cms-strapi
   npm install
   # or
   yarn install
   ```

4. **Set up environment variables**

   Create `.env.local` in `admin-dashboard/`:
   ```env
   NEXT_PUBLIC_SERVER_URL=http://localhost:1337
   NEXT_PUBLIC_ASSETS_DIR=http://localhost:1337
   ```

   Create `.env` in `cms-strapi/`:
   ```env
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=football_news
   DATABASE_USERNAME=your_username
   DATABASE_PASSWORD=your_password
   DATABASE_SSL=false
   JWT_SECRET=your_jwt_secret
   ADMIN_JWT_SECRET=your_admin_jwt_secret
   APP_KEYS=your_app_keys
   API_TOKEN_SALT=your_api_token_salt
   TRANSFER_TOKEN_SALT=your_transfer_token_salt
   ```

### Development

1. **Start the CMS Backend**
   ```bash
   cd cms-strapi
   npm run develop
   # or
   yarn develop
   ```
   The Strapi admin panel will be available at `http://localhost:1337/admin`

2. **Start the Admin Dashboard**
   ```bash
   cd admin-dashboard
   npm run dev
   # or
   yarn dev
   ```
   The admin dashboard will be available at `http://localhost:3033`

## 📁 Project Structure

```
FootballNewsApp/
├── admin-dashboard/          # Next.js frontend application
│   ├── src/
│   │   ├── app/             # Next.js app router pages
│   │   ├── components/      # Reusable UI components
│   │   ├── layouts/         # Layout components
│   │   ├── sections/        # Page sections
│   │   ├── theme/           # MUI theme configuration
│   │   ├── utils/           # Utility functions
│   │   └── routes/          # Routing configuration
│   ├── public/              # Static assets
│   └── package.json
├── cms-strapi/              # Strapi CMS backend
│   ├── src/
│   │   ├── api/             # API endpoints
│   │   ├── admin/           # Admin panel customization
│   │   └── extensions/      # Strapi extensions
│   ├── config/              # Strapi configuration
│   └── package.json
└── news-engine/             # News aggregation system
    └── readme.md
```

## 🎨 Features

### Admin Dashboard
- **Modern UI**: Clean, professional interface built with Material-UI
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Authentication**: Secure JWT-based authentication system
- **Dashboard Analytics**: Data visualization and reporting tools
- **Content Management**: Interface for managing news articles and media
- **User Management**: Admin tools for user roles and permissions
- **Theme System**: Customizable themes with dark/light mode support
- **Form Handling**: Advanced forms with validation using React Hook Form
- **Animations**: Smooth animations powered by Framer Motion

### CMS Backend
- **Content Types**: Flexible content type builder
- **Media Management**: File upload and management system
- **API Endpoints**: RESTful API for frontend consumption
- **User Permissions**: Role-based access control
- **Admin Panel**: Intuitive content management interface
- **Database**: PostgreSQL for reliable data storage

## 🛠️ Development Scripts

### Admin Dashboard
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run lint:fix     # Fix ESLint issues
npm run fm:fix       # Format code with Prettier
# or using yarn
yarn dev             # Start development server
yarn build           # Build for production
yarn start           # Start production server
yarn lint            # Run ESLint
yarn lint:fix        # Fix ESLint issues
yarn fm:fix          # Format code with Prettier
```

### CMS Backend
```bash
npm run develop      # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run strapi       # Run Strapi CLI commands
# or using yarn
yarn develop         # Start development server
yarn build           # Build for production
yarn start           # Start production server
yarn strapi          # Run Strapi CLI commands
```

## 🔧 Configuration

### Environment Variables

The application uses environment variables for configuration. See the installation section for required variables.

### Database Setup

1. Create a PostgreSQL database
2. Update the database configuration in `cms-strapi/config/database.js`
3. Run database migrations: `npm run strapi database:migrate` or `yarn strapi database:migrate`

### Content Types

After starting Strapi, you can create content types through the admin panel or by defining them in the `src/api/` directory.

## 🚀 Deployment

### Production Build

1. **Build Admin Dashboard**
   ```bash
   cd admin-dashboard
   npm run build
   # or
   yarn build
   ```

2. **Build CMS Backend**
   ```bash
   cd cms-strapi
   npm run build
   # or
   yarn build
   ```

3. **Deploy to your preferred hosting platform**

### Docker Deployment

Docker configurations can be added for containerized deployment.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue in the repository.

---

**Built with ❤️ using Next.js, Strapi, and Material-UI**
