<div align="center">

# OspreyPi ESP32-S3 Smart Display

**Fast, modular 480×480 ESPHome + LVGL dashboard — v2.5 Performance Edition**

[![Release](https://img.shields.io/github/v/release/sandro-defender/OspreyPi-esp32-s3-480x480?sort=semver)](https://github.com/sandro-defender/OspreyPi-esp32-s3-480x480/releases/latest)
[![ESPHome](https://img.shields.io/badge/ESPHome-2026.9.0-blue?logo=esphome)](https://esphome.io/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Native-41BDF5?logo=home-assistant)](https://www.home-assistant.io/)
[![Themes](https://img.shields.io/badge/Themes-4%20Selectable-orange)]()
[![Performance](https://img.shields.io/badge/Performance-Optimized-success)]()

**ESP32-S3 • ST7701S 480×480 IPS • FT6336 Touch • 16MB Flash • 8MB PSRAM**

[📖 Wiki](docs/wiki/Home.md) • [🚀 Installation](#-installation) • [🎨 Themes](#-four-selectable-themes) • [🤖 AI Agents](AGENTS.md) • [🔧 Hardware](DEVICE_SPECS.md)

</div>

---

## ✨ What's New in v2.5 — Performance Edition

A response-time and throughput pass across the whole firmware. Every knob now
carries a `#options:` comment in the YAML marking the **stable** value and the
**fast** alternative applied (or available commented out for on-device
testing). Full details: [docs/CHANGELOG-v2.5-PERFORMANCE.md](docs/CHANGELOG-v2.5-PERFORMANCE.md).

- **Touch polls at 10 ms instead of the 50 ms default** (FT6336 IRQ pin is not
  connected) — taps and swipes register up to 5× sooner
- **Quick taps no longer dropped** on the Light page (`min_length` 50 ms → 10 ms)
- **Wake script gated** — the brightness service call no longer restarts on
  every touch while the panel is already awake
- **Homescreen fix: the status halo/icon on the Settings card no longer
  swallow taps and swipes** (`clickable: false` — touches pass through)
- **Page transitions 300 ms → 150 ms** (Home ↔ AC ↔ Light swipe ring)
- **WiFi `fast_connect`** — boot associates in ~1–2 s instead of ~5–8 s
- **API batch delay 50 ms → 20 ms**, UART logger fully disabled (`baud_rate: 0`)
- **4 unused fonts removed** (~400 KB smaller firmware, faster OTA)
- **Light-page halo repaint halved** while dragging sliders
- **Info page 1 s timer gated** to when the page is actually shown
- New commented `#options:` test knobs (flip on device, revert if unhappy):
  PSRAM 120 MHz, PCLK 20 MHz, LVGL buffer 100%, code/rodata-XIP off

### Everything from v2.3 — Four Selectable Themes

### 🎨 Theme 4: Daylight (dark orange-glow)

The **Daylight** theme joins Classic, Modern and Performance — a warm, raised-card
dark variant built to match `docs/images/screen_light.png`: near-black `#0B0C0D`
surfaces, raised dark cards (`#1F242C → #151A20` gradient + `#242A33` bevel),
white text and warm orange `#E37220 / #F8953D` accents and glows.
(A bright off-white "daylight" palette was tried first and dropped — it was
unreadable behind the AC/light artwork. The name stayed.)

### Everything else that's in this release

- **4 themes, one file each** — `common/themes/{classic,modern,performance,daylight}.yaml`,
  registered in `common/themes.yaml`. Every page (home, AC, light, settings, info)
  repaints itself through `apply_display_theme` + per-page repaint scripts.
- **Theme switch in ~100 ms** — on device (Settings → Theme) or from Home
  Assistant (`select.display01_theme`), persistent across reboots.
- **Raised "3D" tiles + neon glow rings** for Modern/Daylight (`depth_dark`,
  `depth_light`, `glow_green/blue/orange` LVGL styles).
- **Full theme gallery** — every screen re-rendered at true 480×480 device
  resolution for all four themes (see below), regenerable with
  `python3 tools/generate_screenshots.py`.
- **AI-agent guide** — [`AGENTS.md`](AGENTS.md) documents the whole project for
  AI editors, including the version-bump-on-push policy.

### ⚡ v2.1/v2.2 performance & features still included

- LVGL buffer 50%, fonts bpp 4, logger ERROR, API `reboot_timeout: 0s` + 50 ms batch,
  PSRAM instruction/rodata fetch, 64 KB cache lines, boot screen 8 s, info page 30 s
- **AC page**: Power, Mode (off/cool/heat/dry/fan/auto), Fan (auto/low/med/high),
  Swing (off/vert/horiz/both), Eco / Sleep / Turbo presets, Preset readout,
  16–31 °C arc + −/+ steppers (long-press = 0.5 °C fine step), live action +
  humidity + room temperature
- **Settings page**: zero dropdowns, 15 buttons, fixed 460 px layout, instant highlight
- **Swipe ring**: Home ↔ AC ↔ Light pages with edge-swipe navigation

---

## 🎨 Four Selectable Themes

| Theme | Style | Colors | Radius | Performance |
|---|---|---|---|---|
| **Classic** | Original flat dark | Black bg, slate `#343645` tiles, white icons, orange `#F37320` active | 14 px | Balanced |
| **Modern** | Mockup look, raised tiles + glow | Navy `#0A0E14` bg, gradient tiles `#323B4D→#1A212C`, glowing orange `#FF8C00` icons, green Power `#00E676`, blue Cool `#29B6F6` | 20 px | Medium (glow) |
| **Performance** | Minimal for max speed | Pure black, `#1A1A1A` tiles, white only, no colors/glow/borders | 4 px | Fastest |
| **Daylight** | Warm raised-card dark | Near-black `#0B0C0D` bg, raised cards `#1F242C→#151A20` + `#242A33` bevel, white text, orange `#E37220` accent/glow | 20 px | Balanced |

**Selectable on device:** Settings → Theme → [ Classic ] [ Modern ] [ Perf ] [ Day ] —
instant switch, persistent, also exposed as HA select entity `Theme`.

### Theme 1: Classic — original flat dark

| Home | AC | Settings |
|---|---|---|
| ![Classic Home](docs/images/theme_classic_home.png) | ![Classic AC](docs/images/theme_classic_ac.png) | ![Classic Settings](docs/images/theme_classic_settings.png) |

### Theme 2: Modern — raised tiles, orange glow, green/blue AC

| Home | AC | Settings |
|---|---|---|
| ![Modern Home](docs/images/theme_modern_home.png) | ![Modern AC](docs/images/theme_modern_ac.png) | ![Modern Settings](docs/images/theme_modern_settings.png) |

### Theme 3: Performance — minimal, fastest

| Home | AC | Settings |
|---|---|---|
| ![Perf Home](docs/images/theme_performance_home.png) | ![Perf AC](docs/images/theme_performance_ac.png) | ![Perf Settings](docs/images/theme_performance_settings.png) |

### Theme 4: Daylight — warm raised cards (NEW in v2.3)

| Home | AC | Settings |
|---|---|---|
| ![Daylight Home](docs/images/theme_daylight_home.png) | ![Daylight AC](docs/images/theme_daylight_ac.png) | ![Daylight Settings](docs/images/theme_daylight_settings.png) |

**All four home screens side by side:** ![Theme preview sheet](docs/images/theme_preview_sheet.png)

### All Screens Gallery

| Home | AC | Light / WLED | Settings | Info | Screensaver |
|---|---|---|---|---|---|
| ![Home](docs/images/preview_modern_v2_home.png) | ![AC](docs/images/screen_ac.png) | ![Light](docs/images/screen_light.png) | ![Settings](docs/images/screen_settings.png) | ![Info](docs/images/screen_info.png) | ![Saver](docs/images/screen_screensaver.png) |

> All mockups are rendered at true 480×480 device resolution with the real UI
> fonts and assets by [`tools/generate_screenshots.py`](tools/generate_screenshots.py).
> Replace with real device photos any time — the layout matches 1:1.

---

## 📸 Hardware Docs — Board Guide & Schematics

Screenshots from the vendor user guide (`hardware/ESP32-S3-Touch-LCD-4_User-Guide_CN.pdf`).
Full vector schematic: [`hardware/SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf`](hardware/SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf) ·
Pin-by-pin map (used vs free): [`hardware/PINOUT.md`](hardware/PINOUT.md).

| PCB component callouts | Main components table | Product page |
|---|---|---|
| ![PCB callouts](hardware/img/IMG_4671.jpeg) | ![Components table](hardware/img/IMG_4672.jpeg) | ![Product page](hardware/img/IMG_4678.jpeg) |
| Buzzer, ESP32-S3-WROOM-1-N16R8, power LED, IP5306 BMS, 5.08 mm wiring port, SP3485EEN RS485, SN74HC14 auto-direction, CH340K USB-UART, SGM6132 DCDC, USB-C, I²C sensor header, LCD FPC. HW/SW setup + power (USB 5 V / terminal 12–24 V) below. | What each chip does: N16R8 module (16 MB Flash + 8 MB PSRAM), IP5306 2.1 A charge / 2.4 A discharge, SP3485EEN half-duplex RS485, SN74HC14 auto TX/RX switching, CH340K (≤2 Mbaud), SGM6132 12–24 V→5 V, I²C sensor port, 0.5 mm LCD FPC. | ESP32-S3-Touch-LCD-4: mainboard ESP32-TPCB4, ESP32-S3-WROOM-1-N16R8, 4″ 480×480 RGB capacitive touch. For smart panels, gateways, HMI, industrial control, lighting. |

| System + LCD FPC schematic | Power + I²C schematic | UART + backlight + RS485 schematic |
|---|---|---|
| ![FPC schematic](hardware/img/Image.jpg) | ![Power schematic](hardware/img/Image%201.jpg) | ![UART schematic](hardware/img/Image%202.jpg) |
| **The pinout page**: FPC 40-pin map — IO39/MOSI, IO38/SCLK, IO45/CS, IO48/PCLK, IO47/DE, IO21/VSYNC, IO14/HSYNC, DB1–DB17 (IO0/12/11/10/9/46/3/20/19/8/18/…/17/16/15/7/6), IO5/SDA, IO4/SCL, TP-INT (pull-up only). Plus buzzer (IO42 → AO3400) and USB-C blocks. | I²C sensor header U9 (3V3/GND/SDA/SCL, 4.7 kΩ pull-ups — shared with touch), AMS1117-3.3 LDO, IP5306 battery BMS (BAT+/BAT− pads), SGM6132 DCDC (terminal 12–28.5 V → 5 V/3 A). | CH340K USB-UART (MCU_TXD/RXD = GPIO43/44) with DTR/RTS auto-download to EN + IO0; SY7200 boost backlight driver (LCD_BK = GPIO13 PWM); SP3485EEN RS485 with 120 Ω termination, bias + TVS (MCU side = GPIO1 TX / GPIO2 RX, auto-direction, no EN pin). |

---

## 📁 Project Layout v2.5

```text
.
├── AGENTS.md                        # AI-editor guide + version policy
├── Display01.yaml / Display02.yaml  # per-device identity + dashboard choice
├── partitions_16mb.csv
├── DEVICE_SPECS.md                  # pinout, init sequence, specs
├── secrets(example).yaml
├── tools/
│   └── generate_screenshots.py      # renders every mockup in docs/images
├── docs/
│   ├── images/                      # 480×480 theme + screen mockups
│   ├── OPTIMIZATION-AND-UPGRADES.md
│   ├── README.md
│   └── wiki/                        # Home, Themes, Installation, Performance,
│                                    # AC-Control, Settings, Hardware,
│                                    # Custom-Dashboard, Troubleshooting
├── hardware/                        # datasheets + device photos
└── esphome-modular-lvgl-buttons/    # shared firmware
    ├── common/
    │   ├── display.yaml             # firmware entry: substitutions + packages
    │   ├── themes.yaml              # theme registry (one package per theme)
    │   ├── themes/                  # classic / modern / performance / daylight
    │   ├── display_settings.yaml    # brightness, rotation, sun/time automation
    │   ├── fonts.yaml               # Nunito + DejaVu + Georgian + MDI icons
    │   ├── mdi_glyph_substitutions.yaml
    │   └── ...
    ├── dashboards/home.yaml         # default 10-card dashboard + theme scripts
    ├── pages/                       # ac_control, light_color, settings, info,
    │                                # screensaver, loading_480px, weather_simple
    ├── buttons/                     # reusable LVGL button widgets
    ├── sensors/                     # per-button HA state listeners (theme-aware)
    ├── widgets/                     # swipe_navigation
    ├── custom_components/noaa_tides/
    ├── homeassistant_config/        # helper automations
    └── hardware/osptek-esp32-s3-48x48.yaml
```

---

## 🚀 Installation

```bash
cp 'secrets(example).yaml' secrets.yaml
# edit wifi, api keys (openssl rand -base64 32), lat/lon
esphome config Display01.yaml
esphome run Display01.yaml   # USB first time, OTA later
```

Enable **Allow device to perform HA actions** in the ESPHome integration.

Full guide: [docs/wiki/Installation.md](docs/wiki/Installation.md).

---

## 🎛️ Runtime Settings

| Setting | On Device | HA | Persistent |
|---|:---:|:---:|:---:|
| Mode Day/Eve/Night | 3 buttons | Yes | Yes |
| Day/Eve/Night brightness | 3 sliders | Yes | Yes |
| Timeout 15–300 s | Slider | Yes | Yes |
| Screensaver | Switch | Yes | Yes |
| **Theme Classic/Modern/Perf/Daylight** | **4 buttons** | **Yes** | **Yes** |
| Rotation 0/90/180/270 | 4 buttons | Yes | Yes |
| Backlight | — | Yes | Restore |

**Theme select HA entity:** `select.display01_theme` → Classic / Modern / Performance / Daylight

Sunrise/sunset automation switches brightness mode automatically; 00:00 switches to Night.

---

## 🌡️ AC Control

Entity `${climate_entity}` (default `climate.midea_ac`), page `pages/ac_control.yaml`:

| Control | Cycle / Range | Service |
|---|---|---|
| Power | toggle | `climate.toggle` |
| Mode | off→cool→heat→dry→fan→auto→off | `set_hvac_mode` |
| Fan | auto→low→med→high | `set_fan_mode` |
| Swing | off→vert→horiz→both | `set_swing_mode` |
| Eco / Sleep / Turbo | preset / none | `set_preset_mode` |
| Preset | live readout, cycles preset | `set_preset_mode` |
| Temp | 16–31 °C arc + −/+ (long-press = 0.5 °C) | `set_temperature` |

Header shows live `hvac_action` (STANDBY/COOLING/…), current humidity and room
temperature. Colors adapt to the active theme automatically.

---

## 📖 Wiki

- [Home](docs/wiki/Home.md)
- [Themes](docs/wiki/Themes.md) — all 4 themes detailed
- [Installation](docs/wiki/Installation.md)
- [Performance](docs/wiki/Performance.md)
- [AC Control](docs/wiki/AC-Control.md)
- [Settings](docs/wiki/Settings.md)
- [Hardware](docs/wiki/Hardware.md)
- [Custom Dashboard](docs/wiki/Custom-Dashboard.md)
- [Troubleshooting](docs/wiki/Troubleshooting.md)

---

## 🛠️ Hardware

| Component | Spec |
|---|---|
| MCU | ESP32-S3 16 MB flash, 8 MB octal PSRAM 80 MHz |
| Display | 3.95/4.0" IPS 480×480 ST7701S (3-wire SPI init + 16-bit RGB) |
| Touch | FT6336 I²C 400 kHz |
| Backlight | GPIO13 PWM 1 kHz |
| Buzzer | GPIO42 PWM |
| RS485 | GPIO1 TX / GPIO2 RX, auto-direction (no EN pin), terminal 12–24 V + A/B |
| Free GPIOs | GPIO40 + GPIO41 (solder-only) · GPIO4/5 I²C sensor header (shared with touch) |

See [DEVICE_SPECS.md](DEVICE_SPECS.md) for specs + init sequence and
[`hardware/PINOUT.md`](hardware/PINOUT.md) for the full used-vs-free GPIO map.

---

## 📦 Releases & Version Policy

Version lives in `esphome-modular-lvgl-buttons/common/display.yaml` →
`project_version` (currently **2.5**). Pushing to `main` validates both display
configs and publishes a GitHub release/tag when the version changed.

**On every push / PR merge, bump `project_version`** (and the docs that mention
it) — the exact checklist is in [`AGENTS.md`](AGENTS.md) § 7 *Version Policy*.

---

## 🙏 Credits

- ESPHome, LVGL, Home Assistant
- Original modular framework: agillis/esphome-modular-lvgl-buttons
- v2.1 Performance Edition — OspreyPi team
- v2.2 Themes Edition — Classic / Modern / Performance
- v2.3 — Daylight theme, 480×480 pixel-accurate mockups, AI-agent guide
- v2.5 — Response-time & throughput pass, `#options` stable/fast tuning knobs

</div>
