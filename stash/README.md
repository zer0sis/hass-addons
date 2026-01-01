# Stash - Home Assistant Docker Ingress Setup

[Stash](https://github.com/stashapp/stash) is an organizer for your media, with a web-based UI.

## Quick Setup

### 1. Create directories

```bash
mkdir -p stash/{config,data,metadata,cache,blobs,generated}
```

### 2. Add service to docker-compose.yml

Copy the contents of `docker-compose.service.yml` into your main `docker-compose.yml` under the `services:` section.

### 3. Configure Home Assistant ingress

Add the contents of `ingress-config.yaml` to your Home Assistant's `configuration.yaml`.

### 4. Deploy

```bash
docker compose up -d stash
```

### 5. Reload Ingress

In Home Assistant:
1. Go to **Developer Tools** > **YAML**
2. Click **INGRESS** under "YAML configuration reloading"

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `STASH_PORT` | 9999 | Web UI port |
| `STASH_STASH` | /data/ | Media library path |
| `STASH_GENERATED` | /generated/ | Generated content path |
| `STASH_METADATA` | /metadata/ | Metadata storage path |
| `STASH_CACHE` | /cache/ | Cache directory |

## Volumes

| Container Path | Purpose |
|---------------|---------|
| `/root/.stash` | Configuration, database, settings |
| `/data` | Your media library |
| `/metadata` | Scene/performer metadata |
| `/cache` | Temporary files |
| `/blobs` | Binary blob storage |
| `/generated` | Thumbnails, previews, transcodes |

## DLNA Support

If you need DLNA functionality, uncomment `network_mode: host` in the docker-compose service and comment out the ingress URL (DLNA requires host networking).

## First Run

1. Access Stash at `http://your-ha-ip:9999` or via the HA sidebar
2. Complete the initial setup wizard
3. Point to your media directories
4. Run a scan to import your library

## Resources

- [Stash Documentation](https://docs.stashapp.cc/)
- [Docker Hub](https://hub.docker.com/r/stashapp/stash)
- [GitHub Repository](https://github.com/stashapp/stash)
