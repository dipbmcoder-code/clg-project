const { withHydrationOverlay } = require('@builder.io/react-hydration-overlay/next');

const nextConfig = {
  transpilePackages: ['mui-tel-input'],
  trailingSlash: false,
  distDir: 'build',
  eslint: {
    ignoreDuringBuilds: true,
  },
  modularizeImports: {
    '@mui/icons-material': {
      transform: '@mui/icons-material/{{member}}',
    },
    '@mui/material': {
      transform: '@mui/material/{{member}}',
    },
    '@mui/lab': {
      transform: '@mui/lab/{{member}}',
    },
  },
  webpack(config) {
    config.module.rules.push({
      test: /\.svg$/,
      use: ['@svgr/webpack'],
    });
    return config;
  },
  async rewrites() {
    return [
      {
        source: '/admin/login',
        destination: `${process.env.NEXT_PUBLIC_STRAPI_API_URL}/admin/login`,
      },
      {
        source: '/admin/users/me',
        destination: `${process.env.NEXT_PUBLIC_STRAPI_API_URL}/admin/users/me`,
      },
      {
        source: '/uploads/:path*',
        destination: `${process.env.NEXT_PUBLIC_STRAPI_API_URL}/uploads/:path*`,
      },
    ];
  },
};

const isDevelopment = process.env.NODE_ENV === 'development';
 
module.exports = isDevelopment
  ? withHydrationOverlay({
      appRootSelector: 'main',
    })(nextConfig)
  : nextConfig;
