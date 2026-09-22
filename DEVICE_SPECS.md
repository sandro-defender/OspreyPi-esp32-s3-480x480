# osptek esp32-s3-48x48 Device Specifications

> Full used-vs-free GPIO map with connector pinouts: **[hardware/PINOUT.md](hardware/PINOUT.md)**.
> Official schematic: [hardware/SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf](hardware/SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf).

## Hardware Overview
- **MCU**: ESP32-S3 (16MB Flash, PSRAM)
- **Display**: 3.95" / 4.0" IPS TFT 480x480
- **Display Driver**: ST7701S (3-wire SPI + 16/18-bit RGB)
- **Touch Controller**: FT6336 (I2C)

## Pinout Configuration

### Display (ST7701S)
| Signal       | GPIO Pin | Note                  |
|--------------|----------|-----------------------|
| **CS**       | 45       | Chip Select           |
| **SCLK**     | 38       | SPI Clock             |
| **MOSI**     | 39       | SPI MOSI              |
| **DE**       | 47       | Data Enable           |
| **VSYNC**    | 21       | Vertical Sync         |
| **HSYNC**    | 14       | Horizontal Sync       |
| **PCLK**     | 48       | Pixel Clock (16MHz)   |
| **Backlight**| 13       | Init Freq: 1000Hz     |

### init_sequence:
      - [0xFF, 0x77, 0x01, 0x00, 0x00, 0x13]
      - [0xEF, 0x08]
      - [0xFF, 0x77, 0x01, 0x00, 0x00, 0x10]
      - [0xC0, 0x3B, 0x00]
      - [0xC1, 0x0B, 0x02]
      - [0xC2, 0x37, 0x02]
      - [0xCC, 0x10]
      - [0xB0, 0x00, 0x0F, 0x16, 0x0E, 0x11, 0x07, 0x09, 0x09, 0x08, 0x23, 0x05, 0x11, 0x0F, 0x28, 0x2D, 0x18]
      - [0xB1, 0x00, 0x0F, 0x16, 0x0E, 0x11, 0x07, 0x09, 0x08, 0x09, 0x23, 0x05, 0x11, 0x0F, 0x28, 0x2D, 0x18]
      - [0xFF, 0x77, 0x01, 0x00, 0x00, 0x11]
      - [0xB0, 0x4D]
      - [0xB1, 0x33]
      - [0xB2, 0x87]
      - [0xB5, 0x4B]
      - [0xB7, 0x8C]
      - [0xB8, 0x20]
      - [0xC1, 0x78]
      - [0xC2, 0x78]
      - [0xD0, 0x88]
      - [0xE0, 0x00, 0x00, 0x02]
      - [0xE1, 0x02, 0xF0, 0x00, 0x00, 0x03, 0xF0, 0x00, 0x00, 0x00, 0x44, 0x44]
      - [0xE2, 0x10, 0x10, 0x40, 0x40, 0xF2, 0xF0, 0x00, 0x00, 0xF2, 0xF0, 0x00, 0x00]
      - [0xE3, 0x00, 0x00, 0x11, 0x11]
      - [0xE4, 0x44, 0x44]
      - [0xE5, 0x07, 0xEF, 0xF0, 0xF0, 0x09, 0xF1, 0xF0, 0xF0, 0x03, 0xF3, 0xF0, 0xF0, 0x05, 0xED, 0xF0, 0xF0]
      - [0xE6, 0x00, 0x00, 0x11, 0x11]
      - [0xE7, 0x44, 0x44]
      - [0xE8, 0x08, 0xF0, 0xF0, 0xF0, 0x0A, 0xF2, 0xF0, 0xF0, 0x04, 0xF4, 0xF0, 0xF0, 0x06, 0xEE, 0xF0, 0xF0]
      - [0xEB, 0x00, 0x00, 0xE4, 0xE4, 0x44, 0x88, 0x40]
      - [0xEC, 0x78, 0x00]
      - [0xED, 0x20, 0xF9, 0x87, 0x76, 0x65, 0x54, 0x4F, 0xFF, 0xFF, 0xF4, 0x45, 0x56, 0x67, 0x78, 0x9F, 0x02]
      - [0xEF, 0x10, 0x0D, 0x04, 0x08, 0x3F, 0x1F]
      - [0x11]
      - delay 120ms
      - [0x29]

### RGB Data Bus
| Color Bit | GPIO Pin | Mapped As |
|-----------|----------|-----------|
| **R0**    | 17       | TFT_R0    |
| **R1**    | 16       | TFT_R1    |
| **R2**    | 15       | TFT_R2    |
| **R3**    | 7        | TFT_R3    |
| **R4**    | 6        | TFT_R4    |
| **G0**    | 46       | TFT_G0    |
| **G1**    | 3        | TFT_G1    |
| **G2**    | 20       | TFT_G2    |
| **G3**    | 19       | TFT_G3    |
| **G4**    | 8        | TFT_G4    |
| **G5**    | 18       | TFT_G5    |
| **B0**    | 0        | TFT_B0    |
| **B1**    | 12       | TFT_B1    |
| **B2**    | 11       | TFT_B2    |
| **B3**    | 10       | TFT_B3    |
| **B4**    | 9        | TFT_B4    |

### Touch Screen (FT6336)
| Signal | GPIO Pin | Note           |
|--------|----------|----------------|
| **SDA**| 5        | I2C Data       |
| **SCL**| 4        | I2C Clock      |
| **RST**| N/C (-1) | Not Connected  |
| **IRQ**| N/C (-1) | Not Connected  |

### Other
- **Flash Size**: 16MB
- **PSRAM**: Octal, 80MHz
- **UART0 TX**: 43 (→ CH340K USB-UART, flashing/logs)
- **UART0 Rx**: 44 (← CH340K USB-UART)
- **Buzzer**: 42 (active HIGH, passive 2700Hz element — see PINOUT.md)
- **RS485/Modbus (SP3485EEN + SN74HC14 auto-direction, no flow-control pin)**:
    - **TX**: GPIO1 (`IO1/485_TX` on MCU sheet)
    - **RX**: GPIO2 (`IO2/485_RX`, via HC14 buffer)
    - **Direction**: automatic in hardware (TX-low-drive: DI tied to GND by design,
      MARK held by 10kΩ fail-safe bias) — keep bus short, ≤38400 baud (9600 recommended)
    - **Terminal P1**: 1:VCC (12–24VDC) 2:GND 3:RS485_A 4:RS485_B
    - *Verified against official schematic R2 (2025-02-05). Older notes claiming
      UART0 43/44 + EN 40 were wrong — 43/44 are the CH340K USB-UART.*

### Free / Reusable GPIOs (see hardware/PINOUT.md for details)
- **GPIO40, GPIO41**: not connected anywhere — the only truly free pins
  (solder-only, module pads, no connector).
- **GPIO1/GPIO2**: hardwired to RS485, but unused by current firmware
  (no `uart:` enabled) — reclaimable only if you give up RS485.
- **GPIO4/GPIO5**: I²C bus shared with touch, broken out to the MX1.25 sensor
  header — best option for adding sensors / port expanders.
- **GPIO43/44**: USB-UART (CH340K) — keep for flashing, do not reuse.
- **GPIO22–25**: don't exist on ESP32-S3. **GPIO26–34**: in-package flash/no pads.
  **GPIO35–37**: reserved for onboard octal Flash/PSRAM (N16R8).


