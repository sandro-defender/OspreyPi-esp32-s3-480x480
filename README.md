<div align="center">

# OspreyPi ESP32-S3 Smart Display

**A modular 480×480 ESPHome/LVGL dashboard for Home Assistant**

[![ESPHome](https://img.shields.io/badge/ESPHome-2026.8%2B-blue?logo=esphome)](https://esphome.io/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Native-41BDF5?logo=home-assistant)](https://www.home-assistant.io/)

</div>

## What changed in the modular version

`Display01.yaml` and `Display02.yaml` now load the **same shared firmware and dashboard**. They differ only where hardware requires it:

| Value | Display 01 | Display 02 |
|---|---:|---:|
| Device name | `display01` | `display02` |
| Initial rotation | 0° | 180° |
| API key | `api_encryption_key` | `api_encryption_key2` |

All common logic now lives in reusable packages. A fix made to the shared display, settings, hardware, page, or button module automatically applies to both panels.

### Main features

- Shared modular firmware for any number of displays
- Native Home Assistant entity control and live state feedback
- On-device **Settings** page
- The same settings exposed as Home Assistant entities
- Persistent brightness, timeout, theme, rotation, and screensaver settings
- Central dashboard profile with one-line entity/button overrides
- Light dimming and color page
- Climate control page
- Weather screensaver
- OTA progress overlay
- Device diagnostics page
- Local fonts, including Georgian and Material Design Icons, for repeatable builds

## Project layout

```text
.
├── Display01.yaml                         # Identity + orientation + API key
├── Display02.yaml                         # Identity + orientation + API key
├── partitions_16mb.csv
├── secrets(example).yaml
└── esphome-modular-lvgl-buttons/
    ├── common/
    │   ├── display.yaml                   # Shared package aggregator/defaults
    │   ├── display_settings.yaml          # Brightness, timeout, theme, rotation
    │   ├── home_assistant.yaml            # HA buttons and buzzer control
    │   ├── assets.yaml                    # Shared fonts/images
    │   ├── wifi.yaml
    │   ├── ota.yaml
    │   └── ...
    ├── dashboards/
    │   └── home.yaml                      # Main cards, entities, and state sources
    ├── buttons/                           # Reusable card templates
    ├── sensors/                           # Reusable HA state listeners
    ├── pages/                             # Settings, info, climate, light, saver
    ├── hardware/                          # ESP32-S3/ST7701S/FT6336 definition
    └── assets/
```

## Requirements

- ESPHome **2026.8.0 or newer**
- Home Assistant with the ESPHome integration for entity control
- A 2.4 GHz Wi-Fi network
- OspreyPi ESP32-S3 480×480 display described in [DEVICE_SPECS.md](DEVICE_SPECS.md)

## Installation

### 1. Create secrets

```bash
cp 'secrets(example).yaml' secrets.yaml
```

Edit `secrets.yaml`:

```yaml
wifi_ssid: "Primary WiFi"
wifi_password: "primary-password"
wifi_ssid2: "Backup WiFi"
wifi_password2: "backup-password"

api_encryption_key: "DISPLAY01_BASE64_KEY"
api_encryption_key2: "DISPLAY02_BASE64_KEY"

latitude: 41.7151
longitude: 44.8271
```

Generate each API key with:

```bash
openssl rand -base64 32
```

If there is no second access point, use the primary credentials for both Wi-Fi entries.

### 2. Validate

```bash
esphome config Display01.yaml
esphome config Display02.yaml
```

### 3. Flash

```bash
esphome run Display01.yaml
esphome run Display02.yaml
```

Use USB for the first installation. Later updates can use OTA.

### 4. Allow Home Assistant actions

Dashboard cards call Home Assistant actions such as `light.toggle` and `script.turn_on`. In the Home Assistant ESPHome integration, enable **Allow the device to perform Home Assistant actions** for each display.

## Runtime settings

Tap the **Settings** card on the main page. Each control is also exposed under the display device in Home Assistant and is restored after a restart.

| Setting | Touchscreen | Home Assistant | Persistent |
|---|:---:|:---:|:---:|
| Brightness mode: Day/Evening/Night | Yes | Yes | Yes |
| Day brightness | Yes | Yes | Yes |
| Evening brightness | Yes | Yes | Yes |
| Night brightness | Yes | Yes | Yes |
| Screen timeout (15–600 seconds) | Yes | Yes | Yes |
| Screensaver enabled | Yes | Yes | Yes |
| Dark/Light dashboard theme | Yes | Yes | Yes |
| Rotation: 0/90/180/270 | Yes | Yes | Yes |
| Display backlight | — | Yes | ESPHome restore |
| Buzzer | — | Yes | Off after boot |
| Show Home/Settings/exit saver | — | Yes | — |

Sunrise and sunset automatically select Day and Evening mode. The configured night time selects Night mode. Manual changes from the screen or Home Assistant take effect immediately.

## Change buttons and entities

The default dashboard is defined in:

[`esphome-modular-lvgl-buttons/dashboards/home.yaml`](esphome-modular-lvgl-buttons/dashboards/home.yaml)

All frequently changed values are substitutions at the top of that file. To customize only one display, override them in that display's small YAML file; there is no need to edit button logic or duplicate a page.

Display behaviour can be changed live from Home Assistant, but dashboard target assignments stay in YAML because ESPHome's native Home Assistant state subscriptions are created at compile time. Keeping entity assignments compile-time preserves reliable live button state without requiring Home Assistant helper automations.

### Example: change Button 1 on Display 01

```yaml
substitutions:
  device_name: "display01"
  device_friendly_name: "Display 01"
  fallback_ap_ssid: "Display 01 Setup"
  display_rotation: "0"
  display_rotation_index: "0"

  dashboard_button_1_text: "office"
  dashboard_button_1_entity: "light.office_lights"
  dashboard_button_1_action: "light.toggle"
  dashboard_button_1_icon: "\U000F0335" # mdi-lightbulb
  dashboard_button_1_height: "228px"
```

The same entity substitution is used for both the press action and its live state listener, so it only needs to be changed once.

### Available card overrides

| Card | Main substitutions | Notes |
|---|---|---|
| 1, 2, 3, 6, 9 | `text`, `entity`, `action`, `icon`, `height` | Generic HA action cards |
| 4 | Same values plus `state_entity` | Action can be a script while state follows a light/switch |
| 5 | `entity`, `action`, `icon`, `height` | Large play/pause icon card |
| 7 | `text`, `entity`, `icon`, `height` | Dimmable light + long-press color page |
| AC | `${climate_entity}` | Climate entity from shared substitutions |
| Settings | Built in | Opens the runtime settings page |

The full names follow this pattern:

```text
dashboard_button_<number>_text
dashboard_button_<number>_entity
dashboard_button_<number>_action
dashboard_button_<number>_icon
dashboard_button_<number>_height
```

Common Home Assistant actions include:

```yaml
light.toggle
switch.toggle
script.turn_on
scene.turn_on
button.press
automation.trigger
media_player.media_play_pause
```

Use an action that matches the target entity's domain. If you choose an icon that is not already used by the default dashboard, also add its glyph to `common/assets.yaml`. Button state subscriptions are generated at compile time so that feedback remains fast and reliable; after changing a target entity, validate and upload the firmware again.

### Change shared weather and climate entities

Override these in either display file:

```yaml
substitutions:
  weather_entity: "weather.home"
  climate_entity: "climate.living_room"
```

### Create a different dashboard profile

1. Copy `dashboards/home.yaml` to a new file, for example `dashboards/upstairs.yaml`.
2. Add/remove/reorder cards in that profile.
3. Point one display at it:

```yaml
packages:
  display: !include esphome-modular-lvgl-buttons/common/display.yaml
  dashboard: !include esphome-modular-lvgl-buttons/dashboards/upstairs.yaml
```

The hardware, settings, diagnostics, OTA, weather, and shared styles remain untouched.

## Add another display

Copy one of the thin device files and change only these values:

```yaml
substitutions:
  device_name: "display03"
  device_friendly_name: "Display 03"
  fallback_ap_ssid: "Display 03 Setup"
  display_rotation: "0"
  display_rotation_index: "0"

packages:
  display: !include esphome-modular-lvgl-buttons/common/display.yaml
  dashboard: !include esphome-modular-lvgl-buttons/dashboards/home.yaml

api:
  encryption:
    key: !secret api_encryption_key3
```

Add `api_encryption_key3` to `secrets.yaml`.

## Hardware

| Component | Specification |
|---|---|
| MCU | ESP32-S3, 16 MB flash, 8 MB octal PSRAM |
| Display | 3.95/4.0 inch IPS, 480×480 |
| Display controller | ST7701S, SPI initialization + RGB bus |
| Touch controller | FT6336 over I²C |
| Backlight | GPIO13 PWM |
| Buzzer | GPIO42 PWM |

See [DEVICE_SPECS.md](DEVICE_SPECS.md) for the complete pinout and panel initialization sequence.

## Device gallery

<p align="center">
  <img src="hardware/img/IMG_4671.jpeg" width="28%" />
  <img src="hardware/img/IMG_4672.jpeg" width="28%" />
  <img src="hardware/img/IMG_4678.jpeg" width="28%" />
</p>

## Troubleshooting

### A card does nothing

1. Confirm Home Assistant is connected on the Device Info page.
2. Enable **Allow the device to perform Home Assistant actions** in the ESPHome integration.
3. Check that the action matches the entity domain.
4. Check the ESPHome log for the offline warning.

### State color is wrong

The card action target and state source must represent the same state. Generic cards use one shared entity substitution. Script cards can use a separate `dashboard_button_4_state_entity` because scripts do not have a persistent on/off state.

### Display 02 is upside down

Display 02 intentionally starts at 180° for its current mounting. Change `display_rotation` and `display_rotation_index` together, or use the runtime Rotation setting.

| Rotation | `display_rotation` | `display_rotation_index` |
|---:|---:|---:|
| 0° | `"0"` | `"0"` |
| 90° | `"90"` | `"1"` |
| 180° | `"180"` | `"2"` |
| 270° | `"270"` | `"3"` |

### Wi-Fi is unavailable

The panel starts an open fallback access point named `Display 01 Setup` or `Display 02 Setup`. The Device Info page displays its QR code when disconnected.

### Memory or rendering problems

- Keep `lvgl_buffer_size` at `12%` unless testing a known-safe value.
- Avoid adding entire icon ranges; include only used glyphs in `common/assets.yaml`.
- Keep large images in RGB565-compatible sizes.

## Validation in CI

GitHub Actions validates both entrypoints with the pinned ESPHome container:

```text
.github/workflows/esphome-validate.yml
```

Because both displays consume the same packages, validation catches shared changes for both orientations and API configurations.

## Upstream projects

- [ESPHome](https://esphome.io/)
- [LVGL](https://lvgl.io/)
- [Home Assistant](https://www.home-assistant.io/)
- Original modular button inspiration: [agillis/esphome-modular-lvgl-buttons](https://github.com/agillis/esphome-modular-lvgl-buttons)
