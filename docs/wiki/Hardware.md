# Hardware — OspreyPi ESP32-S3 480×480

> Full used-vs-free GPIO map with connector pinouts:
> [`hardware/PINOUT.md`](../../hardware/PINOUT.md).
> Official schematic: [`hardware/SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf`](../../hardware/SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf).

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

- UART0 TX 43 → CH340K, RX 44 ← CH340K (USB flashing/logs — do not reuse)
- Buzzer 42 (active HIGH, passive 2700 Hz element)
- RS485 (SP3485EEN + SN74HC14 auto-direction, verified on schematic R2):
  TX = GPIO1, RX = GPIO2, no flow-control pin. Terminal P1 =
  1:VCC (12–24 VDC) 2:GND 3:A 4:B. TX is low-drive/passive-high —
  keep ≤38400 baud (9600 recommended).

### Free GPIOs

- **GPIO40, GPIO41**: not connected — only truly free pins (solder-only, module pads)
- **GPIO1/2**: RS485-wired but unused by firmware (no `uart:` enabled)
- **GPIO4/5**: I²C bus shared with touch, on the MX1.25 sensor header — best expansion option
- GPIO22–25 don't exist; GPIO26–34 in-package/no pads; GPIO35–37 reserved (octal Flash/PSRAM)

See [`hardware/PINOUT.md`](../../hardware/PINOUT.md) for the complete per-pin table.

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

80MHz octal = 40MB/s, enough for the 50% LVGL buffer (480×480×2 bytes×50% ≈ 230KB per buffer, double buffered ≈ 460KB)

## Photos

`hardware/img/` holds the official vendor images plus 6 user-guide screenshots
(captioned in the [README gallery](../../README.md#-hardware-docs--board-guide--schematics)):

- board-layout.png (official hi-res PCB callouts), schematic-mcu.png (MCU sheet:
  `IO1/485_TX`, `IO2/485_RX`, `IO42/BUZZER`, `MCU_TXD/RXD`, `IO40/41` = NC),
  schematic-rs485.png, product.png
- IMG_4671.jpeg (PCB component callouts), IMG_4672.jpeg (component table),
  IMG_4678.jpeg (product page)
- Image.jpg (system + LCD FPC schematic), Image 1.jpg (power + I²C schematic),
  Image 2.jpg (UART + backlight + RS485 schematic)

## Datasheets

Full index with vendor-original links: [`hardware/README.md`](../../hardware/README.md).

- `hardware/D_FT_6336_U_Data_Sheet_V1_1_410131a74f.pdf` (FT6336U touch)
- `hardware/ESP32-S3-Touch-LCD-4_User-Guide_CN.pdf` (vendor user guide, Chinese)
- `hardware/SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf` (official full schematic, 7 pages)
- `hardware/ST7701S_SPEC_V1.3.pdf` (display driver)
- `hardware/YDP395BT003-V4.pdf` / `.dwg` (LCD panel datasheet + CAD)
- `hardware/BOE3.95_480x480_ST7701S_init.txt` (vendor init sequence)
