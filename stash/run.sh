#!/usr/bin/with-contenv bashio
# Stash Add-on Run Script

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

mkdir -p "${DATA_PATH}" || true
mkdir -p /config/stash
mkdir -p /generated
mkdir -p /metadata
mkdir -p /cache
mkdir -p /blobs

# Link stash config directory to addon config
if [ ! -L /root/.stash ]; then
    rm -rf /root/.stash 2>/dev/null || true
    ln -sf /config/stash /root/.stash
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

exec /usr/bin/stash --nobrowser
