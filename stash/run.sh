#!/usr/bin/with-contenv bashio
# Stash Add-on Run Script

set -e

# =============================================================================
# Configuration
# =============================================================================

DATA_PATH=$(bashio::config 'data_path')
LOG_LEVEL=$(bashio::config 'log_level')

bashio::log.info "Starting Stash add-on..."
bashio::log.info "Data path: ${DATA_PATH}"
bashio::log.info "Log level: ${LOG_LEVEL}"

# =============================================================================
# Setup directories
# =============================================================================

# Create data directories if they don't exist
mkdir -p "${DATA_PATH}"
mkdir -p /config/stash
mkdir -p /generated
mkdir -p /metadata
mkdir -p /cache
mkdir -p /blobs

# Link stash config directory
if [ ! -L /root/.stash ]; then
    rm -rf /root/.stash
    ln -s /config/stash /root/.stash
fi

# =============================================================================
# Set environment variables
# =============================================================================

export STASH_STASH="${DATA_PATH}"
export STASH_GENERATED="/generated"
export STASH_METADATA="/metadata"
export STASH_CACHE="/cache"
export STASH_PORT="9999"

# =============================================================================
# Start Stash
# =============================================================================

bashio::log.info "Starting Stash on port 9999..."

# Execute the stash binary
exec /usr/bin/stash --nobrowser
