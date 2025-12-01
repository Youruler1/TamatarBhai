# # Multi-stage Dockerfile for Tamatar-Bhai Frontend
# # Stage 1: Build the React application
# # Stage 2: Serve with nginx

# # ============================================================================
# # Stage 1: Build
# # ============================================================================
# FROM node:20-alpine AS build

# # Set working directory
# WORKDIR /app

# # Copy package files
# COPY package*.json ./

# # Install dependencies
# RUN npm ci --include=dev

# # Copy source code
# COPY . .

# # Build the application
# RUN npm run build

# # ============================================================================
# # Stage 2: Production
# # ============================================================================
# FROM nginx:alpine

# # Copy custom nginx configuration
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# # Copy built files from build stage
# COPY --from=build /app/dist /usr/share/nginx/html

# # Expose port 80
# EXPOSE 80

# # Health check
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#   CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# # Start nginx
# CMD ["nginx", "-g", "daemon off;"]



# frontend/Dockerfile - multi-stage (recommended)
# ---------- Build stage ----------
FROM node:20-alpine AS build
WORKDIR /app

# copy package files first to leverage layer cache
COPY package*.json ./

# install all deps (including dev) for build tools such as tsc
RUN npm ci --include=dev

# copy source and build
COPY . .
RUN npm run build

# ---------- Production stage ----------
FROM nginx:alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
