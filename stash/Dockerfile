ARG BUILD_FROM
FROM stashapp/stash:latest

# Environment defaults
ENV STASH_STASH=/data/ \
    STASH_GENERATED=/generated/ \
    STASH_METADATA=/metadata/ \
    STASH_CACHE=/cache/ \
    STASH_PORT=9999

# Create required directories
RUN mkdir -p /data /generated /metadata /cache /blobs /config

# Copy run script
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Stash stores its config in /root/.stash
VOLUME ["/root/.stash", "/data", "/generated", "/metadata", "/cache", "/blobs"]

EXPOSE 9999

CMD ["/run.sh"]
