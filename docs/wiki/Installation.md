# Installation Guide

## Requirements

- ESPHome 2026.9.0+
- Home Assistant with ESPHome integration
- 2.4GHz WiFi
- OspreyPi hardware (ESP32-S3 480×480)

## 1. Secrets

```bash
cp 'secrets(example).yaml' secrets.yaml
```

Edit:

```yaml
wifi_ssid: "Your WiFi"
wifi_password: "password"
api_encryption_key: "BASE64_32_BYTES"
api_encryption_key2: "ANOTHER_BASE64"
latitude: 41.7151
longitude: 44.8271
```

Generate keys:

```bash
openssl rand -base64 32
```

Optional backup WiFi: uncomment in `common/wifi.yaml` and add `wifi_ssid2`/`wifi_password2`.

## 2. Validate

```bash
esphome config Display01.yaml
esphome config Display02.yaml
```

Should pass with no errors. New v2.1 validates faster due to fewer fonts.

## 3. Flash

First time USB:

```bash
esphome run Display01.yaml
```

Select serial port. Later OTA works.

## 4. Home Assistant

- ESPHome integration discovers device
- Enable **Allow the device to perform Home Assistant actions**
- Assign entities in `dashboards/home.yaml` if needed

## 5. Add Another Display

Copy Display01.yaml → Display03.yaml:

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

Add key to secrets.yaml

## Performance Tips After Install

- Keep lvgl_buffer_size 20% unless low PSRAM
- Keep log_level ERROR
- Avoid adding large images >480×480
- Use bpp 4 for fonts, not 8
