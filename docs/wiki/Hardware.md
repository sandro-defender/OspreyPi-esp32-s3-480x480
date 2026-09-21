# Hardware — OspreyPi ESP32-S3 480×480

## Overview

- MCU: ESP32-S3, 16MB Flash, 8MB Octal PSRAM 80MHz
- Display: 3.95" / 4.0" IPS TFT 480×480, ST7701S controller
- Touch: FT6336 I2C
- Backlight: GPIO13 PWM 1kHz
- Buzzer: GPIO42 PWM
- Board: esp32-s3-devkitc-1, DIO flash mode

## Pinout

### Display ST7701S

| Signal | GPIO | Note |
|---|---|---|
| CS | 45 | Chip Select |
| SCLK | 38 | SPI Clock |
| MOSI | 39 | SPI MOSI |
| DE | 47 | Data Enable |
| VSYNC | 21 | Vertical Sync |
| HSYNC | 14 | Horizontal Sync |
| PCLK | 48 | Pixel Clock 16MHz |
| Backlight | 13 | PWM 1kHz |

### RGB Data Bus

| Color | GPIO | Mapped |
|---|---|---|
| R0 | 17 | TFT_R0 |
| R1 | 16 | TFT_R1 |
| R2 | 15 | TFT_R2 |
| R3 | 7 | TFT_R3 |
| R4 | 6 | TFT_R4 |
| G0 | 46 | TFT_G0 |
| G1 | 3 | TFT_G1 |
| G2 | 20 | TFT_G2 |
| G3 | 19 | TFT_G3 |
| G4 | 8 | TFT_G4 |
| G5 | 18 | TFT_G5 |
| B0 | 0 | TFT_B0 |
| B1 | 12 | TFT_B1 |
| B2 | 11 | TFT_B2 |
| B3 | 10 | TFT_B3 |
| B4 | 9 | TFT_B4 |

### Touch FT6336

| Signal | GPIO | Note |
|---|---|---|
| SDA | 5 | I2C Data 400kHz |
| SCL | 4 | I2C Clock |
| RST | N/C | Not connected |
| IRQ | N/C | Not connected |

### Other

- UART0 TX 43, RX 44
- Buzzer 42
- RS485 experimental: TX 43 inverted, RX 44 inverted, EN 40 inverted

## Init Sequence

```
[0xFF, 0x77, 0x01, 0x00, 0x00, 0x13]
[0xEF, 0x08]
[0xFF, 0x77, 0x01, 0x00, 0x00, 0x10]
[C0 3B 00] [C1 0B 02] [C2 37 02] [CC 10]
[B0 ...] [B1 ...]
[FF 77 01 00 00 11]
[B0 4D] [B1 33] [B2 87] [B5 4B] [B7 8C] [B8 20] [C1 78] [C2 78] [D0 88]
[E0 00 00 02]
[E1 02 F0 ...]
[E2 10 10 40 ...]
...
[11] delay 120ms [29]
```

See `hardware/osptek-esp32-s3-48x48.yaml` for full.

## Display Config

```yaml
display:
  platform: st7701s
  data_rate: 2MHz
  pclk_frequency: 16MHz
  dimensions: 480x480
  auto_clear_enabled: false
  update_interval: never
```

`auto_clear_enabled: false` + `update_interval: never` = LVGL drives refresh, not ESPHome loop — faster.

## PSRAM

```yaml
psram:
  mode: octal
  speed: 80MHz
```

80MHz octal = 40MB/s, enough for 20% LVGL buffer (480×480×2 bytes×20% ≈ 92KB per buffer, double buffered ≈ 184KB)

## Photos

All 6 hardware photos in `hardware/img/`:

- IMG_4671.jpeg, IMG_4672.jpeg, IMG_4678.jpeg
- Image.jpg, Image 1.jpg, Image 2.jpg

## Datasheet

- `hardware/D_FT_6336_U_Data_Sheet_V1_1_410131a74f.pdf`
- `hardware/ESP32-S..25.pdf`
