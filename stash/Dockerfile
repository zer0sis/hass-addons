ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# Install dependencies
RUN apk add --no-cache \
    ffmpeg \
    vips \
    curl \
    ca-certificates

# Download and install stash binary
ARG STASH_VERSION=v0.27.2
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then ARCH="amd64"; fi && \
    if [ "$ARCH" = "aarch64" ]; then ARCH="arm64"; fi && \
    curl -L -o /tmp/stash.tar.gz \
    "https://github.com/stashapp/stash/releases/download/${STASH_VERSION}/stash-linux-${ARCH}.tar.gz" && \
    tar -xzf /tmp/stash.tar.gz -C /usr/bin/ && \
    chmod +x /usr/bin/stash && \
    rm /tmp/stash.tar.gz

# Environment defaults
ENV STASH_STASH=/data/ \
    STASH_GENERATED=/generated/ \
    STASH_METADATA=/metadata/ \
    STASH_CACHE=/cache/ \
    STASH_PORT=9999

# Create required directories
RUN mkdir -p /data /generated /metadata /cache /blobs /config/stash

# Copy run script
COPY run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 9999

CMD ["/run.sh"]
