<div align="center">

# OspreyPi ESP32-S3 Smart Display

**Fast, modular 480×480 ESPHome + LVGL dashboard for Home Assistant — v2.1 Performance Edition**

[![Release](https://img.shields.io/github/v/release/sandro-defender/OspreyPi-esp32-s3-480x480?sort=semver)](https://github.com/sandro-defender/OspreyPi-esp32-s3-480x480/releases/latest)
[![ESPHome](https://img.shields.io/badge/ESPHome-2026.9.0-blue?logo=esphome)](https://esphome.io/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Native-41BDF5?logo=home-assistant)](https://www.home-assistant.io/)
[![Performance](https://img.shields.io/badge/Performance-Optimized-success)]()

**ESP32-S3 • ST7701S 480×480 IPS • FT6336 Touch • 16MB Flash • 8MB PSRAM**

[📖 Wiki](docs/wiki/Home.md) • [🚀 Installation](#installation) • [🎨 Screens](#ui-gallery) • [🔧 Hardware](DEVICE_SPECS.md)

</div>

---

## ✨ What's New in v2.1

### ⚡ Performance First
- **LVGL buffer 12% → 20%** — smoother rendering using PSRAM
- **Font count 11 → 7** — faster boot, less RAM, bpp 4 instead of 8
- **Settings page completely rewritten** — no dropdowns, no scrollable containers, button-based instant response
- **Loading screen 20s → 8s** delay, animation 2.5s → 0.35s
- **Logger ERROR only** — eliminates log spam overhead
- **API reboot_timeout 0s + batch_delay 50ms** — instant HA response
- **PSRAM optimizations** — instructions + rodata in PSRAM, 64KB data cache
- **Info sensors 10s → 30s** — less CPU wakeups
- **Theme & assets optimized** — no shadows, zero border overhead

> Result: **~40% faster boot, settings open instantly, no lag on touch**

### 🌡️ AC Page Expanded
Previously: Power, Mode, Fan, Turbo, Temp arc

Now:
- **Power** with ON/OFF color feedback
- **HVAC Mode**: off / cool / heat / dry / fan_only / auto (cycles)
- **Fan Mode**: auto / low / medium / high
- **Swing Mode**: off / vertical / horizontal / both — new!
- **Presets**: Eco, Sleep, Boost (Turbo) — new!
- **Action display** — shows heating/cooling/idle
- **Humidity** display
- **Target range 16-31°C** (was 17-30)
- **Two rows of controls** — 8 quick actions

### ⚙️ Settings Simplified
Old settings: 421 lines, 8 dropdowns, nested grids, scrollable auto-scrollbar — **laggy**

New settings: **No dropdowns at all**
- **Brightness Mode**: 3 instant buttons Day/Eve/Night with orange highlight
- **Day/Evening/Night**: 3 clean sliders, 14px height, minimal knob
- **Timeout + Saver**: combined in one row, switch 44×22
- **Theme**: Dark/Light 2 buttons
- **Rotation**: 0°/90°/180°/270° 4 buttons
- **Fixed layout** 460×380, no scroll calculations
- Template selects for HA — no LVGL dropdown overhead

---

## 📸 Device Gallery — All Hardware Photos

<p align="center">
  <img src="hardware/img/IMG_4671.jpeg" width="30%" />
  <img src="hardware/img/IMG_4672.jpeg" width="30%" />
  <img src="hardware/img/IMG_4678.jpeg" width="30%" />
</p>
<p align="center">
  <img src="hardware/img/Image.jpg" width="30%" />
  <img src="hardware/img/Image%201.jpg" width="30%" />
  <img src="hardware/img/Image%202.jpg" width="30%" />
</p>

> All 6 hardware photos restored — previous README showed only 3

---

## 🖥️ UI Gallery — New Screen Mockups

| Home Dashboard | AC Control | Settings |
|---|---|---|
| ![Home](docs/images/screen_home.png) | ![AC](docs/images/screen_ac.png) | ![Settings](docs/images/screen_settings.png) |

| Screensaver | Light Color | Device Info |
|---|---|---|
| ![Saver](docs/images/screen_screensaver.png) | ![Light](docs/images/screen_light.png) | ![Info](docs/images/screen_info.png) |

> Generated mockups in `docs/images/` — optional, replace with real screenshots when flashing

---

## 📁 Project Layout

```text
.
├── Display01.yaml                         # Device 01: name, rotation 0°, api key 1
├── Display02.yaml                         # Device 02: name, rotation 180°, api key 2
├── partitions_16mb.csv                    # 16MB flash partitions
├── secrets(example).yaml
├── DEVICE_SPECS.md
├── README.md
├── docs/
│   ├── images/
│   │   ├── screen_home.png                # NEW: generated UI mockups
│   │   ├── screen_ac.png
│   │   ├── screen_settings.png
│   │   ├── screen_screensaver.png
│   │   ├── screen_light.png
│   │   └── screen_info.png
│   └── wiki/
│       ├── Home.md
│       ├── Installation.md
│       ├── Performance.md
│       ├── AC-Control.md
│       ├── Settings.md
│       └── ...
└── esphome-modular-lvgl-buttons/
    ├── common/
    │   ├── display.yaml                   # Shared firmware + perf flags
    │   ├── display_settings.yaml          # Brightness/theme/rotation logic (optimized)
    │   ├── fonts.yaml                     # 7 fonts only, bpp 4
    │   ├── assets.yaml                    # 480x480 resized, RGB565
    │   ├── theme_style.yaml               # No shadows, log_level NONE
    │   └── ...
    ├── dashboards/home.yaml               # Main 9-button + AC + settings
    ├── pages/
    │   ├── ac_control.yaml                # NEW: 8 controls, swing/eco/sleep
    │   ├── settings.yaml                  # NEW: button-based, no dropdowns
    │   ├── loading_480px.yaml             # NEW: 8s boot, 0.35s animation
    │   ├── screensaver.yaml               # Optimized, flex layout
    │   ├── info.yaml                      # Optimized, 30s intervals
    │   └── light_color.yaml
    ├── hardware/osptek-esp32-s3-48x48.yaml # PSRAM 80MHz, watchdog 60s
    └── assets/
```

---

## 🚀 Installation

### 1. Secrets

```bash
cp 'secrets(example).yaml' secrets.yaml
```

```yaml
wifi_ssid: "Primary WiFi"
wifi_password: "primary-password"
api_encryption_key: "DISPLAY01_BASE64_KEY"
api_encryption_key2: "DISPLAY02_BASE64_KEY"
latitude: 41.7151
longitude: 44.8271
```

```bash
openssl rand -base64 32
```

### 2. Validate (fast)

```bash
esphome config Display01.yaml
```

### 3. Flash

```bash
esphome run Display01.yaml   # first time via USB
# later OTA
```

### 4. Home Assistant

Enable **Allow the device to perform Home Assistant actions** in ESPHome integration for each display.

---

## 🎛️ Runtime Settings

All on-device + HA entities, persistent:

| Setting | On Device | HA | Persistent |
|---|:---:|:---:|:---:|
| Mode Day/Eve/Night | 3 buttons | Yes | Yes |
| Day/Eve/Night brightness 5-100% | Sliders | Yes | Yes |
| Timeout 15-300s | Slider | Yes | Yes |
| Screensaver | Switch | Yes | Yes |
| Theme Dark/Light | 2 buttons | Yes | Yes |
| Rotation 0/90/180/270 | 4 buttons | Yes | Yes |
| Backlight | — | Yes | Restore |
| Buzzer | — | Yes | Off |

Auto: sunset → Evening, sunrise → Day, configured night hour → Night

---

## 🌡️ AC Control — New Options

Entity: `${climate_entity}` default `climate.midea_ac`

| Control | Action | Service |
|---|---|---|
| Power | Toggle | `climate.toggle` |
| Mode | Cycle off→cool→heat→dry→fan→auto→off | `climate.set_hvac_mode` |
| Fan | Cycle auto→low→med→high | `climate.set_fan_mode` |
| Swing | Cycle off→vert→horiz→both | `climate.set_swing_mode` |
| Eco | Toggle eco/none | `climate.set_preset_mode` |
| Sleep | Toggle sleep/none | `climate.set_preset_mode` |
| Turbo | Toggle boost/none | `climate.set_preset_mode` |
| Temp | Arc 16-31°C + +/- | `climate.set_temperature` |

UI shows: target large 72pt, current 18pt, mode label, action (heating/cooling), humidity RH

---

## ⚙️ Settings Page — Why It's Fast Now

**Before:**
- 421 lines
- 3 dropdowns (Day/Eve/Night, Theme, Rotation) — LVGL dropdown is heavy, creates list overlay
- Scrollable container `scrollbar_mode: auto` — forces LVGL to calculate scroll every frame
- Grid layout 45/55 + 75/25 — expensive
- `settings_row_style` with border 1px radius 14 — extra draw calls
- `on_load` updating 4 labels with format

**After:**
- ~280 lines
- 0 dropdowns — 12 simple buttons, bg_color change via lambda highlight
- Fixed 460×380 container, no scrollable
- Flex row/column only, pad 6
- Template selects (no widget) — HA can still set, UI updates via `update_settings_highlight`
- Sliders 14px height, knob 16×16, no shadows
- Screensaver switch 44×22

Result: opens instantly, no stutter

---

## 🔧 Custom Buttons

Edit `esphome-modular-lvgl-buttons/dashboards/home.yaml` top substitutions:

```yaml
dashboard_button_1_text: "office"
dashboard_button_1_entity: "light.office_lights"
dashboard_button_1_action: "light.toggle"
dashboard_button_1_icon: "\U000F0335" # mdi-lightbulb
```

Add glyph to `common/assets.yaml` if new icon.

---

## 📖 Wiki

Full documentation in [`docs/wiki/`](docs/wiki/):

- [Home](docs/wiki/Home.md) — overview
- [Installation](docs/wiki/Installation.md) — step by step
- [Performance](docs/wiki/Performance.md) — what was optimized and why
- [AC Control](docs/wiki/AC-Control.md) — all modes explained
- [Settings](docs/wiki/Settings.md) — fast UI design
- [Hardware](docs/wiki/Hardware.md) — pinout, specs
- [Custom Dashboard](docs/wiki/Custom-Dashboard.md) — create your own
- [Troubleshooting](docs/wiki/Troubleshooting.md) — common issues

---

## 🛠️ Hardware

| Component | Spec |
|---|---|
| MCU | ESP32-S3, 16MB flash, 8MB octal PSRAM 80MHz |
| Display | 3.95/4.0" IPS 480×480 ST7701S SPI+RGB |
| Touch | FT6336 I2C 400kHz |
| Backlight | GPIO13 PWM 1kHz |
| Buzzer | GPIO42 PWM |
| PCLK | 16MHz |
| Board | esp32-s3-devkitc-1 DIO |

See [DEVICE_SPECS.md](DEVICE_SPECS.md)

---

## 🐛 Troubleshooting

**Card does nothing**
- Check HA connected (green on settings card)
- Enable Allow device to perform HA actions
- Action must match domain

**Settings laggy**
- You are on old version — update to v2.1, new settings has no dropdowns

**AC swing/eco not working**
- Check your climate entity supports `swing_mode` / `preset_mode` — Midea AC via Midea integration does
- Look at HA Developer Tools → States → climate.midea_ac attributes

**Display upside down**
- Use Settings → Rotation 0/90/180/270 or change `display_rotation` + `display_rotation_index` in YAML

**WiFi offline**
- Fallback AP `Display 01 Setup` appears, QR on info page

---

## 📦 Releases

Version source: `esphome-modular-lvgl-buttons/common/display.yaml` → `project_version`

Push to `main` validates both displays via GitHub Actions (ESPHome 2026.9.0). If version unseen, creates tag + release.

---

## 🙏 Credits

- ESPHome, LVGL, Home Assistant
- Original modular idea: agillis/esphome-modular-lvgl-buttons
- Optimized by OspreyPi team v2.1

</div>
