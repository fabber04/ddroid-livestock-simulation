# ESP32 pump-logic demo

A breadboard build of the DDROID water-point pump logic, matching the Node-RED
flow (`../../flows.json`) and the XOD patch (`../../xod/ddroid-pump.xodball`).

Three push buttons simulate the sensors/command:

- **LOW** button = low-water float switch
- **FULL** button = high/full float switch
- **STOP** button = operator stop

Two LEDs show the pump state: red = pumping (filling), green = idle.

## Logic

- Pump starts **OFF**.
- **LOW** -> pump **ON** (start filling).
- **FULL** or **STOP** -> pump **OFF** (stop filling).

The software `pumpOn` latch in `ddroid_pump_logic.ino` is the same SR latch as the
XOD `flip-flop`: LOW sets it, FULL/STOP reset it.

## Bill of materials

| Qty | Part | Notes |
| --- | --- | --- |
| 1 | ESP32 dev board | e.g. ESP32 DevKit v1 (30-pin) |
| 1 | Breadboard | half or full size |
| 3 | Tactile push buttons | 4-leg, straddle the center gap |
| 2 | LEDs | 1 red (pump), 1 green (idle) |
| 2 | Resistors ~220-330 ohm | one in series per LED |
| ~10 | Male-male jumper wires | |
| 1 | USB cable | to program the ESP32 |

Buttons need no external resistors - the sketch uses the ESP32 internal pull-ups.

## Pin map

| Signal | ESP32 pin | Wiring |
| --- | --- | --- |
| LOW button | GPIO 32 | leg -> GPIO 32; other leg -> GND rail |
| FULL button | GPIO 33 | leg -> GPIO 33; other leg -> GND rail |
| STOP button | GPIO 25 | leg -> GPIO 25; other leg -> GND rail |
| Pump LED (red) | GPIO 26 | GPIO 26 -> resistor -> LED + (long leg); LED - -> GND rail |
| Idle LED (green) | GPIO 27 | GPIO 27 -> resistor -> LED + (long leg); LED - -> GND rail |
| Ground | GND | one ESP32 GND pin -> breadboard - rail |

These GPIOs avoid the ESP32 boot-strapping and input-only pins.

## Build steps

1. Seat the ESP32 across the breadboard center trench.
2. Jumper one ESP32 GND pin to the blue (-) rail.
3. For each button: one leg -> its GPIO (32/33/25), opposite leg -> (-) rail.
4. Red LED: long leg via a 220 ohm resistor to the GPIO 26 row; short leg -> (-) rail.
5. Green LED: same, from GPIO 27.
6. Check every LED short leg and button second-leg lands on the (-) rail.
7. Plug in USB only after wiring is complete.

## Upload and test

1. In the Arduino IDE, install the `esp32` boards package (Boards Manager).
2. Select your ESP32 board and serial port.
3. Open `ddroid_pump_logic.ino` and upload.
4. Open the Serial Monitor at **115200** baud.

| Press | Red (pump) | Green (idle) | Serial |
| --- | --- | --- | --- |
| power-on | off | on | `Pump OFF` |
| LOW | on | off | `Pump ON (filling)` |
| FULL | off | on | `Pump OFF` |
| LOW | on | off | `Pump ON (filling)` |
| STOP | off | on | `Pump OFF` |

## From demo to real water point

- Replace the LOW and FULL buttons with the trough float switches (same wiring).
- Keep STOP as a real push / emergency-stop button.
- Replace the red pump LED with a relay or MOSFET module on GPIO 26 to switch the
  actual pump; keep the pump supply separate and only share grounds.
- The green LED stays as an idle/ready indicator.

## XOD alternative

The same logic can be flashed from XOD: in `../../xod/ddroid-pump.xodball`, swap the
three `tweak-pulse` nodes for `button` nodes (GPIO 32/33/25) and the `watch` for a
`led` node (GPIO 26), then **Deploy -> Upload to Arduino**.
