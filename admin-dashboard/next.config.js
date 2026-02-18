/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: false,
  distDir: 'build',
  turbopack: {},
  transpilePackages: ['mui-tel-input'],
  experimental: {
    optimizePackageImports: [
      '@mui/icons-material',
      '@mui/material',
      '@mui/lab',
    ],
  },
};

module.exports = nextConfig;
