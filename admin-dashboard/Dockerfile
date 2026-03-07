# Use Node.js 20 base image
FROM node:20-alpine

WORKDIR /app

# Install dependencies separately (for better caching)
COPY package*.json ./
RUN npm ci

# Copy rest of the project
COPY . .

# Accept build-time environment variables
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build the Next.js app
RUN npm run build

# Expose port
EXPOSE 3033

# Start app
CMD ["npm", "start"]
