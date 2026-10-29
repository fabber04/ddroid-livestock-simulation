# XOD pump logic

`ddroid-pump.xodball` is the DDROID water-point pump logic built in [XOD](https://xod.io),
mirroring the Node-RED flow in this repo. Unlike Node-RED, XOD compiles straight to the
ESP32 / Arduino, so this patch is the path to real firmware.

## Logic
- The pump state is held in a `flip-flop` (SR latch), starting **OFF** (MEM = false).
- **LOW** water pulse -> `flip-flop` **SET** -> pump **ON** (start filling).
- **FULL** or **STOP** pulse -> combined by an `any` node -> `flip-flop` **RST** -> pump **OFF** (stop filling).
- A `watch` node shows the pump state (true = ON, false = OFF).

`LOW`, `FULL` and `STOP` are `tweak-pulse` nodes so the logic can be driven by hand in the
XOD simulator. For hardware, replace them with digital-input (float-switch / button) nodes
and feed the `flip-flop` MEM output to a pump-driver output pin.

## Open it
1. Go to https://xod.io/ide/ (or the XOD desktop IDE).
2. **File -> Open Project** and choose `ddroid-pump.xodball`.
3. **Deploy -> Simulate** to run it, or **Deploy -> Upload to Arduino** to flash hardware.
