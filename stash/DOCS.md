# Stash

Stash is an organizer for your media with a web-based UI. It helps you organize, tag, and browse your media collection with powerful search and filtering capabilities.

## Features

- Web-based interface accessible via Home Assistant ingress
- Automatic scene detection and organization
- Performer and studio tracking
- Tag-based organization
- Hardware transcoding support (when available)
- DLNA server capabilities

## Installation

1. Add this repository to your Home Assistant add-on store
2. Install the "Stash" add-on
3. Configure the data path in the add-on settings
4. Start the add-on
5. Access via the Home Assistant sidebar

## Configuration

### Option: `data_path`

The path where your media files are located. This should be a path accessible to the add-on, typically under `/share/` or `/media/`.

**Default:** `/share/stash/data`

### Option: `log_level`

The verbosity level for logging.

**Options:** `Trace`, `Debug`, `Info`, `Warning`, `Error`

**Default:** `Info`

## Storage

The add-on uses the following storage locations:

| Path | Purpose |
|------|---------|
| `/config/stash` | Configuration and database |
| `/share/stash/data` | Media files (configurable) |
| `/generated` | Generated content (thumbnails, previews) |
| `/metadata` | Scene/performer metadata |
| `/cache` | Temporary cache files |

## First Run

1. Open Stash from the Home Assistant sidebar
2. Complete the setup wizard
3. Add your media library paths
4. Run an initial scan

## Hardware Transcoding

This add-on enables video hardware access for potential hardware-accelerated transcoding. Availability depends on your host system's GPU capabilities.

## Support

- [Stash Documentation](https://docs.stashapp.cc/)
- [Stash GitHub](https://github.com/stashapp/stash)
- [Add-on Repository Issues](https://github.com/zer0sis/hass-addons/issues)
