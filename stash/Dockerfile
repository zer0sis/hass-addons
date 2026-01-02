# Build Stash from source for security/trust
# Multi-stage build based on official stashapp/stash build process

ARG STASH_VERSION=v0.27.2
ARG BUILD_FROM=ghcr.io/hassio-addons/base:19.0.0

# =============================================================================
# Stage 1: Build Frontend
# =============================================================================
FROM node:20-alpine AS frontend

ARG STASH_VERSION
WORKDIR /stash

# Install build tools
RUN apk add --no-cache git make

# Clone source at specific version
RUN git clone --depth 1 --branch ${STASH_VERSION} https://github.com/stashapp/stash.git .

# Install pnpm and build UI
RUN npm install -g pnpm && \
    make pre-ui && \
    make generate-ui && \
    make ui

# =============================================================================
# Stage 2: Build Backend
# =============================================================================
FROM golang:1.22-alpine AS backend

ARG STASH_VERSION
WORKDIR /stash

# Install build dependencies including yarn for generate target
RUN apk add --no-cache git make alpine-sdk nodejs npm && \
    npm install -g yarn

# Clone source at specific version
RUN git clone --depth 1 --branch ${STASH_VERSION} https://github.com/stashapp/stash.git .

# Install UI dependencies (needed for generate target)
RUN cd ui/v2.5 && yarn install --frozen-lockfile

# Copy built frontend from stage 1
COPY --from=frontend /stash/ui/v2.5/build /stash/ui/v2.5/build

# Generate code and build binary
RUN make generate && \
    make flags-release flags-pie stash

# =============================================================================
# Stage 3: Home Assistant Add-on Runtime
# =============================================================================
FROM ${BUILD_FROM}

# Install runtime dependencies
RUN apk add --no-cache \
    ca-certificates \
    ffmpeg \
    vips-tools

# Copy built binary from backend stage
COPY --from=backend /stash/stash /usr/bin/stash
RUN chmod +x /usr/bin/stash

# Environment defaults
ENV STASH_STASH=/data/ \
    STASH_GENERATED=/generated/ \
    STASH_METADATA=/metadata/ \
    STASH_CACHE=/cache/ \
    STASH_PORT=9999

# Create required directories
RUN mkdir -p /data /generated /metadata /cache /blobs /config/stash

# Copy s6-overlay service files
COPY rootfs /

EXPOSE 9999
