---
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
description: Generate Home Assistant add-on or Docker ingress setup from any Docker project
argument-hint: <docker-image-or-project-name> [--addon|--ingress]
---

# Home Assistant Add-on / Docker Ingress Generator

Generate a Home Assistant add-on repository structure OR a docker-compose ingress setup for any Docker project.

## Arguments
$ARGUMENTS

## Instructions

1. **Parse the arguments** to determine:
   - The Docker image name or project (e.g., `nodered/node-red`, `portainer/portainer`, `gitea/gitea`)
   - The mode: `--addon` for full HA add-on repo, `--ingress` for docker-compose with hass_ingress integration

2. **Research the Docker image** if needed:
   - Fetch the Docker Hub page or GitHub README to understand ports, volumes, and environment variables
   - Identify the web UI port (usually the main exposed port)

3. **For `--addon` mode**, generate a complete Home Assistant add-on repository:

   **Directory structure:**
   ```
   <addon-name>/
   ├── config.yaml          # Add-on configuration
   ├── Dockerfile           # Build instructions
   ├── build.yaml           # Build configuration
   ├── run.sh               # Entrypoint script
   ├── DOCS.md              # Documentation
   ├── CHANGELOG.md         # Version history
   ├── icon.png             # (note: user should add)
   ├── logo.png             # (note: user should add)
   └── translations/
       └── en.yaml          # English translations
   ```

   **config.yaml template:**
   ```yaml
   name: "<Display Name>"
   version: "1.0.0"
   slug: "<slug-name>"
   description: "<Description>"
   url: "https://github.com/<your-repo>"
   arch:
     - amd64
     - aarch64
     - armv7

   # Ingress configuration
   ingress: true
   ingress_port: <web-ui-port>
   ingress_stream: false
   panel_icon: "mdi:<icon-name>"
   panel_title: "<Display Name>"
   panel_admin: true

   # Startup
   startup: application
   boot: auto

   # Options and schema
   options: {}
   schema: {}

   # Ports (if needed externally)
   ports:
     "<port>/tcp": null
   ports_description:
     "<port>/tcp": "Web interface"

   # Volume mappings
   map:
     - config:rw
     - share:rw

   # Environment
   environment: {}
   ```

   **Dockerfile template:**
   ```dockerfile
   ARG BUILD_FROM
   FROM ${BUILD_FROM}

   # Install base image (usually based on the original Docker image)
   # Example: FROM nodered/node-red:latest

   # Copy run script
   COPY run.sh /
   RUN chmod a+x /run.sh

   CMD ["/run.sh"]
   ```

   **run.sh template:**
   ```bash
   #!/usr/bin/env bashio

   # Get config values
   # CONFIG_VALUE=$(bashio::config 'config_key')

   # Start the application
   exec <start-command>
   ```

4. **For `--ingress` mode (default)**, generate docker-compose service + ingress config:

   **Add to docker-compose.yml:**
   ```yaml
   services:
     <service-name>:
       image: <docker-image>
       container_name: <service-name>
       restart: unless-stopped
       environment:
         - TZ=${TZ:-UTC}
       volumes:
         - ./<service-name>:/data  # Adjust based on image
       # networks:
       #   default:
       #     aliases:
       #       - <service-name>
   ```

   **Add to Home Assistant configuration.yaml:**
   ```yaml
   ingress:
     <service-name>:
       work_mode: ingress
       ui_mode: normal
       require_admin: true
       title: "<Display Name>"
       icon: "mdi:<icon-name>"
       url: http://<service-name>:<port>
   ```

5. **Common MDI icons** for reference:
   - `mdi:home-assistant` - Home Assistant
   - `mdi:sitemap` - Node-RED
   - `mdi:microsoft-visual-studio-code` - VS Code
   - `mdi:zigbee` - Zigbee2MQTT
   - `mdi:access-point` - WiFi/Network
   - `mdi:database` - Database apps
   - `mdi:docker` - Docker/Portainer
   - `mdi:git` - Git services
   - `mdi:chart-line` - Monitoring/Grafana
   - `mdi:shield` - Security apps

6. **Output the generated files** and provide instructions for:
   - Where to place files
   - How to reload ingress (Developer Tools > YAML > Reload INGRESS)
   - Testing the integration

## Examples

- `/ha-addon nodered/node-red --ingress` - Generate docker-compose ingress setup for Node-RED
- `/ha-addon portainer/portainer --addon` - Generate full add-on repository for Portainer
- `/ha-addon gitea/gitea` - Generate ingress setup for Gitea (default mode)
