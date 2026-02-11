# Use Node.js 20 base image
FROM node:20-alpine

WORKDIR /app

# Install dependencies separately (for better caching)
COPY package*.json ./
RUN npm install --frozen-lockfile

# Copy rest of the project
COPY . .

# Accept build-time environment variables
ARG NEXT_PUBLIC_STRAPI_API_URL
ENV NEXT_PUBLIC_STRAPI_API_URL=$NEXT_PUBLIC_STRAPI_API_URL

# Build the Next.js app
RUN npm run build

# Expose port (Next.js default is 3000 inside container)
EXPOSE 3033

# Start app
CMD ["npm", "start"]
