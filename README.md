# zer0sis Home Assistant Add-ons

Custom Home Assistant add-ons repository.

[![Add repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fzer0sis%2Fhass-addons)

## Available Add-ons

| Add-on | Description |
|--------|-------------|
| [Stash](./stash) | An organizer for your media with a web-based UI |

## Installation

1. Click the button above, or manually add this repository URL in Home Assistant:
   ```
   https://github.com/zer0sis/hass-addons
   ```
2. Go to **Settings** → **Add-ons** → **Add-on Store**
3. Click the menu (⋮) → **Repositories**
4. Add the repository URL
5. Find and install the desired add-on

---

## Development

This repository also includes a Claude Code skill and templates for creating Home Assistant add-ons or Docker ingress setups from any Docker project.

## Overview

In late 2025, there are **two main approaches** to running additional software with Home Assistant OS:

### 1. Official Add-ons (for HA OS / Supervised)
Full add-on packages that integrate with the HA Supervisor, providing:
- One-click installation from the add-on store
- Automatic updates
- Configuration UI in Home Assistant
- Native ingress (web UI embedded in HA sidebar)

### 2. Docker + hass_ingress Integration (for HA Container/Core)
For users running Home Assistant in Docker without the Supervisor:
- Run any Docker container alongside Home Assistant
- Use the [hass_ingress](https://github.com/lovelylain/hass_ingress) custom integration
- Access services through the HA sidebar with authentication

## Quick Start

### Using the Claude Code Skill

```bash
# Generate docker-compose ingress setup for Node-RED
/ha-addon nodered/node-red --ingress

# Generate full add-on repository structure for Portainer
/ha-addon portainer/portainer --addon

# Default mode is --ingress
/ha-addon gitea/gitea
```

### Manual Setup with hass_ingress

1. **Install HACS** if not already installed
2. **Install hass_ingress** integration via HACS
3. **Copy the base docker-compose**:
   ```bash
   cp templates/docker-compose.base.yaml docker-compose.yml
   mkdir -p nginx
   cp templates/nginx/dns_proxy.conf nginx/
   ```
4. **Add your services** to docker-compose.yml
5. **Configure ingress** in Home Assistant's configuration.yaml

## File Structure

```
.
├── .claude/
│   └── commands/
│       └── ha-addon.md          # Claude Code skill definition
├── templates/
│   ├── config.yaml.template     # HA add-on config template
│   ├── Dockerfile.template      # Add-on Dockerfile template
│   ├── run.sh.template          # Add-on entrypoint script
│   ├── build.yaml.template      # Add-on build configuration
│   ├── docker-compose.base.yaml # Base compose for hass_ingress
│   ├── service.yaml.template    # Service entry template
│   ├── ingress-entry.yaml.template  # Ingress config entry
│   └── nginx/
│       └── dns_proxy.conf       # DNS proxy for container resolution
├── .env                         # Environment variables (HA_API_KEY, TZ)
└── README.md
```

## hass_ingress Configuration

Add to your Home Assistant `configuration.yaml`:

```yaml
ingress:
  nodered:
    work_mode: ingress
    ui_mode: normal
    require_admin: true
    title: "Node-RED"
    icon: "mdi:sitemap"
    url: http://nodered:1880

  vscode:
    work_mode: ingress
    require_admin: true
    title: "VS Code"
    icon: "mdi:microsoft-visual-studio-code"
    url: http://vscode:8443
```

### Work Modes

| Mode | Description |
|------|-------------|
| `ingress` | Full ingress proxy (like Supervisor add-ons) |
| `iframe` | Simple iframe embed (like Webpage dashboard) |
| `auth` | Works with nginx auth_request for unsupported backends |
| `hassio` | Proxy to existing Supervisor add-on |

## Creating a Full Add-on Repository

For HA OS users who want to create distributable add-ons:

1. Create a GitHub repository
2. Add `repository.yaml` at the root:
   ```yaml
   name: My Home Assistant Add-ons
   url: 'https://github.com/username/ha-addons'
   maintainer: Your Name <email@example.com>
   ```
3. Create a subdirectory for each add-on
4. Use the templates in this repo to scaffold each add-on
5. Users add your repo URL in: **Settings → Add-ons → Add-on Store → ⋮ → Repositories**

## Common Docker Images for HA

| Service | Image | Port | Icon |
|---------|-------|------|------|
| Node-RED | `nodered/node-red` | 1880 | `mdi:sitemap` |
| VS Code | `linuxserver/code-server` | 8443 | `mdi:microsoft-visual-studio-code` |
| Portainer | `portainer/portainer-ce` | 9000 | `mdi:docker` |
| Grafana | `grafana/grafana` | 3000 | `mdi:chart-line` |
| InfluxDB | `influxdb` | 8086 | `mdi:database` |
| Zigbee2MQTT | `koenkk/zigbee2mqtt` | 8080 | `mdi:zigbee` |
| ESPHome | `esphome/esphome` | 6052 | `mdi:chip` |
| AdGuard | `adguard/adguardhome` | 3000 | `mdi:shield-check` |
| Mosquitto | `eclipse-mosquitto` | 1883 | `mdi:access-point` |
| Frigate | `ghcr.io/blakeblackshear/frigate` | 5000 | `mdi:cctv` |

## Environment Variables

Create a `.env` file:

```env
TZ=America/New_York
HA_API_KEY=your_long_lived_access_token
```

## Resources

- [Home Assistant Add-on Developer Docs](https://developers.home-assistant.io/docs/add-ons/configuration/)
- [hass_ingress Integration](https://github.com/lovelylain/hass_ingress)
- [hass_ingress Docker Guide](https://github.com/lovelylain/hass_ingress/blob/main/addons-for-docker-installation.md)
- [Official Add-on Tutorial](https://developers.home-assistant.io/docs/add-ons/tutorial/)
- [Community Add-ons Repository](https://github.com/hassio-addons/repository)
