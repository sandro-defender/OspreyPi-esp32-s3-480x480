# ESP32 Pinout — OspreyPi / Osptek ESP32-S3-Touch-LCD-4 (ESP32-TPCB4)

Module: **ESP32-S3-WROOM-1-N16R8** (ESP32-S3 · 16 MB octal Flash · 8 MB octal PSRAM)
Panel: 3.95″ 480×480 ST7701S (16-bit RGB + 3-wire SPI init) · Touch FT6336U (I²C)

Sources: vendor schematic `SCH_Esp32s3_3.95in_RS485[模组]_R2_2025-02-05`
(see [`hardware/SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf`](SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf)),
vendor ESP-IDF examples (`ESP32S3_3.95In_Box_rev2`),
firmware [`esphome-modular-lvgl-buttons/hardware/osptek-esp32-s3-48x48.yaml`](../esphome-modular-lvgl-buttons/hardware/osptek-esp32-s3-48x48.yaml),
user guide [`hardware/ESP32-S3-Touch-LCD-4_User-Guide_CN.pdf`](ESP32-S3-Touch-LCD-4_User-Guide_CN.pdf, Chinese).

---

## TL;DR — used vs free

| Group | GPIOs | Count |
|---|---|---:|
| ✅ **FREE** (no PCB net, module pad only — solder wire to use) | **40, 41** | 2 |
| 🟡 **Wired but unused by current firmware** (RS485 port) | 1 (TX), 2 (RX) | 2 |
| 🟡 **Shared bus, expandable** (I²C sensor header) | 4 (SCL), 5 (SDA) | 2 |
| 🔴 Used by display / touch / backlight / buzzer / USB | 0, 3, 6–21, 38, 39, 42–48 | 27 |
| ⛔ Not usable (chip/module reserved) | 22–25 (don't exist), 26–34 (flash/PSRAM / no pad), 35–37 (octal Flash/PSRAM) | — |

**Bottom line:** if you need extra I/O, you have **GPIO40 + GPIO41** (solder-only, no
connector), the **I²C sensor header** (GPIO4/5, shared with touch — best option for
sensors, port expanders, etc.), and **GPIO1/2** only if you give up the RS485 port
(see caveats below). Everything else is hardwired.

---

## Complete GPIO map (GPIO0 – GPIO48)

Dir = signal direction from the ESP32-S3 point of view.

| GPIO | Schematic net | Dir | Function on this board | Firmware status | Notes |
|---|---|---|---|---|---|
| 0 | IO0/DB1 + BOOT | O / in | LCD blue **B0** · BOOT strapping (CH340K auto-download) | `display.data_pins.blue[0]` | ⚠️ strapping: must be HIGH/floating at reset → SPI boot. Panel input only, safe. Don't add pulls/loads. |
| 1 | IO1/485_TX | O | **RS485 TX**: MCU TX → SN74HC14 `3A` → SP3485 DE/#RE (TX-low-drive scheme, 470 Ω pull-up R21) | unused (no `uart:` enabled) | Hardwired. Reusing as generic output makes the 485 transceiver chatter on A/B. See §RS485. |
| 2 | IO2/485_RX | I | **RS485 RX**: SP3485 RO → SN74HC14 buffer (`1A→1Y→2A→2Y`, non-inverting) → MCU | unused | Hardwired to a buffer **output** — never drive as output. |
| 3 | IO3/DB7 | O | LCD green **G1** | `display.data_pins.green[1]` | ⚠️ strapping: must float at reset (panel input only ✓). |
| 4 | IO4/I2C-SCL | IO | Touch SCL (FT6336U 400 kHz) + I²C sensor header, 4.7 kΩ pull-up R35 | `i2c.scl` | Shared bus — hang extra I²C devices here (touch = 0x38). |
| 5 | IO5/I2C-SDA | IO | Touch SDA + I²C sensor header, 4.7 kΩ pull-up R34 | `i2c.sda` | Same as above. |
| 6 | IO6/DB17 | O | LCD red **R4** | `red[4]` | |
| 7 | IO7/DB16 | O | LCD red **R3** | `red[3]` | |
| 8 | IO8/DB10 | O | LCD green **G4** | `green[4]` | |
| 9 | IO9/DB5 | O | LCD blue **B4** | `blue[4]` | |
| 10 | IO10/DB4 | O | LCD blue **B3** | `blue[3]` | |
| 11 | IO11/DB3 | O | LCD blue **B2** | `blue[2]` | |
| 12 | IO12/DB2 | O | LCD blue **B1** | `blue[1]` | |
| 13 | IO13/LCD_BK | O PWM | Backlight → SY7200 boost EN/PWM (10 kΩ pull-down R13) | `ledc` 1 kHz `gpio_backlight_pwm` | Active HIGH. Backlight is OFF at boot until firmware drives it. |
| 14 | IO14/HSYNC | O | LCD **HSYNC** | `hsync_pin` | |
| 15 | IO15/DB15 | O | LCD red **R2** | `red[2]` | |
| 16 | IO16/DB14 | O | LCD red **R1** | `red[1]` | |
| 17 | IO17/DB13 | O | LCD red **R0** | `red[0]` | |
| 18 | IO18/DB11 | O | LCD green **G5** | `green[5]` | |
| 19 | IO19/DB9 | O | LCD green **G3** | `green[3]` | Native USB D− unavailable (pin used by LCD). USB works via CH340K only. |
| 20 | IO20/DB8 | O | LCD green **G2** | `green[2]` | Native USB D+ unavailable (same reason). |
| 21 | IO21/VSYNC | O | LCD **VSYNC** | `vsync_pin` | |
| 22–25 | — | — | **Do not exist on ESP32-S3** | — | |
| 26–32 | — | — | In-package SPI Flash/PSRAM bus (SPICS1/HD/WP/CS0/CLK/Q/D). No module pads. | — | ⛔ never touch |
| 33, 34 | — | — | Octal SPIIO4/5. Exist on the bare chip, **no pads on WROOM-1**. | — | ⛔ |
| 35, 36, 37 | — | — | Octal SPIIO6/7 + SPIDQS → module's 16 MB Flash / 8 MB PSRAM | — | ⛔ RESERVED on all `N16R8` (R8 = octal) modules |
| 38 | IO38/SCLK | O | LCD 3-wire SPI clock (ST7701S init) | `spi.clk_pin` | |
| 39 | IO39/MOSI | O | LCD 3-wire SPI data | `spi.mosi_pin` | |
| 40 | IO40 | — | **NOT CONNECTED** (module pad exists, no PCB net) | — | ✅ **FREE** — solder a wire to the module pad. Input/output/ADC2/PWM capable. |
| 41 | IO41 | — | **NOT CONNECTED** (module pad exists, no PCB net) | — | ✅ **FREE** — same as GPIO40. |
| 42 | IO42/BUZZER | O PWM | Buzzer → R29 100 Ω → AO3400 MOSFET gate (10 kΩ pull-down R30, flyback D7) | `ledc buzzer_output` 1 kHz | Active HIGH. Passive 2700 Hz element — drive ≈2.7 kHz PWM for full volume (firmware 1 kHz works, quieter). |
| 43 | TXD0/MCU_TXD | O | USB serial TX → CH340K (flashing + logs) | `logger.baud_rate: 0` (idle) | Keep for USB flashing. Don't reuse (goes to USB host). |
| 44 | RXD0/MCU_RXD | I | USB serial RX ← CH340K TXD | same | CH340K output drives this pin — never drive as output. |
| 45 | IO45/CS | O | LCD 3-wire SPI chip-select | `cs_pin` (`ignore_strapping_warning: true`) | ⚠️ strapping (VDD_SPI 3.3 V select): floats as input at reset ✓, driven after boot. |
| 46 | IO46/DB6 | O | LCD green **G0** | `green[0]` | ⚠️ strapping (ROM boot messages): floats at reset ✓. |
| 47 | IO47/DE | O | LCD **DE** (data enable) | `de_pin` | |
| 48 | IO48/PCLK | O | LCD **pixel clock** 16 MHz | `pclk_pin` | |

Other module pins: **EN (CHIP_PU)** — 10 kΩ pull-up R33 + 1 µF power-on-reset C24,
CH340K DTR auto-download circuit; also tied to the LCD FPC (panel reset follows
system reset — no GPIO needed). **TP_INT** (touch interrupt) is pulled to 3.3 V
(R36) but **not routed to the MCU** — firmware polls the FT6336 (10 ms).
**TP_RST** is not routed either (vendor examples: `RST = GPIO_NUM_NC`,
`INT = GPIO_NUM_NC`).

---

## Connector pinouts

### P1 — 5.08 mm 4-pin pluggable terminal (power + RS485)

| Pin | Net | Description |
|---|---|---|
| 1 | VCC | 12–24 VDC in (schematic absolute max 28.5 V) → SGM6132 DCDC → 5 V / 3 A |
| 2 | GND | Ground |
| 3 | RS485_A | RS485 bus A (non-inverting) |
| 4 | RS485_B | RS485 bus B (inverting) |

Bus protection on board: 120 Ω termination R23, 10 kΩ fail-safe bias
(R20 → GND on B, R27 → 3.3 V on A), TVS diodes D5/D6 (P6SMB6.8CA), 10 Ω series
R22/R24.

### U9 — MX1.25 4-pin wafer (I²C sensor header)

| Pin (top→bottom on schematic) | Net | Description |
|---|---|---|
| 1 | +3.3V | Sensor power (from AMS1117 1 A rail) |
| 2 | GND | Ground |
| 3 | IO5/I2C-SDA | Shared with FT6336 touch (4.7 kΩ PU) |
| 4 | IO4/I2C-SCL | Shared with FT6336 touch (4.7 kΩ PU) |

Any 3.3 V I²C sensor/peripheral can be added here (touch uses address `0x38`).
Verify pin order against the PCB silkscreen before connecting.

### USB-C (TYPEC-302-BRP16SC16)

USB 2.0 DP/DM → CH340K (via USBLC6 ESD protection) for **flashing + serial logs**,
VBUS 5 V input, CC 5.1 kΩ. The ESP32-S3 native USB is unusable (GPIO19/20 are
LCD data), so this serial path is the only USB function. DTR/RTS auto-download
drives EN + IO0 — no boot buttons needed. CH340K supports up to ~2 Mbaud.

### FPC1 — 0.5 mm 40-pin LCD connector (FPC-05FB-40PH20)

| FPC pin | Net | FPC pin | Net |
|---|---|---|---|
| 1 | GND (shield) | 22 | IO46/DB6 (G0) |
| 2 | LEDA (backlight anode, SY7200 boost) | 23 | IO3/DB7 (G1) |
| 3 | LEDK (backlight cathode) | 24 | IO20/DB8 (G2) |
| 4 | GND | 25 | IO19/DB9 (G3) |
| 5 | +3.3V | 26 | IO8/DB10 (G4) |
| 6 | CHIP_PU (= system EN, panel reset) | 27 | IO18/DB11 (G5) |
| 7, 8 | NC | 28 | NC (DB12 skipped → 16-bit mode) |
| 9 | IO39/MOSI (SPI init) | 29 | IO17/DB13 (R0) |
| 10 | IO38/SCLK | 30 | IO16/DB14 (R1) |
| 11 | IO45/CS | 31 | IO15/DB15 (R2) |
| 12 | IO48/PCLK | 32 | IO7/DB16 (R3) |
| 13 | IO47/DE | 33 | IO6/DB17 (R4) |
| 14 | IO21/VSYNC | 34 | GND |
| 15 | IO14/HSYNC | 35 | TP-INT (2 kΩ PU only, NC at MCU) |
| 16 | NC | 36 | IO5/I2C-SDA |
| 17 | IO0/DB1 (B0) | 37 | IO4/I2C-SCL |
| 18 | IO12/DB2 (B1) | 38 | CHIP_PU (= system EN) |
| 19 | IO11/DB3 (B2) | 39 | +3.3V |
| 20 | IO10/DB4 (B3) | 40 | GND |
| 21 | IO9/DB5 (B4) | 41, 42 | GND (shield) |

### BAT+/BAT−

Bare pads for a single-cell Li-ion → IP5306 charge (2.1 A) / boost-discharge
(2.4 A) BMS. No connector fitted.

---

## RS485 port (SP3485EEN + SN74HC14 auto-direction)

- **ESP32 pins: TX = GPIO1, RX = GPIO2.** No direction/flow-control GPIO exists —
  direction is fully automatic in hardware. (Older revisions of our docs guessed
  UART0 43/44 + EN 40 — that was wrong; the MCU sheet shows IO1/485_TX and
  IO2/485_RX.)
- How it works: MCU TX feeds one HC14 inverter whose output drives DE + #RE
  together; the SP3485 DI pin is tied to GND by design, so the bus is **driven
  low for SPACE bits and released for MARK bits** (held by the 10 kΩ fail-safe
  bias). RX comes back through a double-inverter (non-inverting) buffer.
- Practical consequence: TX rising edges are passive (10 kΩ vs bus capacitance).
  Keep the bus short and **stay at ≤ 38400 baud (9600 recommended)**; RX works at
  normal rates. Half-duplex: ignore own echo while transmitting.
- ESPHome (currently commented out in firmware — enable to use):

```yaml
uart:
  - id: modbus_uart
    tx_pin: GPIO1
    rx_pin: GPIO2
    baud_rate: 9600
    stop_bits: 1
    # NO flow_control_pin — direction is automatic (SN74HC14)
```

---

## If you need more GPIOs

1. **I²C header (GPIO4/5)** — easiest: sensors, port expanders (PCF8574/TCA9554),
   PWM drivers… all share the touch bus. No soldering.
2. **GPIO40/41** — the only truly free pins, but **solder-only** (module castellated
   pads, no connector/test point). Both support digital I/O, ADC2, LEDC PWM, PCNT.
   Keep wires short; they sit next to the antenna end of the module.
3. **GPIO1/2** — only by abandoning RS485: GPIO1 can double as an output (at the cost
   of 485 bus chatter); GPIO2 must stay an input (buffer output). Not recommended.
4. GPIO43/44 (USB-UART) and all LCD/touch pins: not reclaimable without cutting
   traces.

---

## Strapping pins (boot-time rules)

| GPIO | Used as | Must be at reset | Why it's safe here |
|---|---|---|---|
| 0 | LCD B0 + BOOT | HIGH (SPI boot) / LOW (download, driven by CH340K circuit only when flashing) | Panel side is input-only; auto-download circuit drives it only during flash |
| 3 | LCD G1 | floating | Panel side is input-only |
| 45 | LCD CS | floating (→ VDD_SPI 3.3 V) | Input at reset, driven after boot |
| 46 | LCD G0 | floating (ROM messages on) | Input at reset, driven after boot |

Rule: never connect buttons, pull resistors, or loads to GPIO0/3/45/46 — the LCD
already owns them.

---

## Files in `hardware/`

| File | Content |
|---|---|
| `PINOUT.md` | This file — full used-vs-free pinout |
| `SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf` | Official full schematic (7 pages, R2 2025-02-05) |
| `ESP32-S3-Touch-LCD-4_User-Guide_CN.pdf` | Vendor user guide, Chinese (board intro + component table + schematics) |
| `D_FT_6336_U_Data_Sheet_V1_1_410131a74f.pdf` | FT6336U touch controller datasheet |
| `img/` | Screenshots from the user guide: product page, component callouts, component table, 3× schematic sheets (see README gallery captions) |
