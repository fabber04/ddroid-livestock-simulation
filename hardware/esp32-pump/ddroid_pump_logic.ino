// DDROID water-point pump logic - ESP32 demo
// Buttons simulate the float switches and STOP command.
//   LOW  -> pump ON  (start filling)
//   FULL -> pump OFF (stop filling)
//   STOP -> pump OFF (stop filling)
// Pump starts OFF. Mirrors the XOD flip-flop (SR latch) and the Node-RED flow.

const int PIN_LOW  = 32;   // LOW water button
const int PIN_FULL = 33;   // FULL water button
const int PIN_STOP = 25;   // STOP button
const int PIN_PUMP = 26;   // Pump LED (red)   - ON when filling
const int PIN_IDLE = 27;   // Idle LED (green) - ON when stopped

bool pumpOn = false;       // pump state: starts OFF

const unsigned long DEBOUNCE_MS = 40;

struct Button { int pin; int stable; int lastRaw; unsigned long tChange; };
Button bLow  = { PIN_LOW,  HIGH, HIGH, 0 };
Button bFull = { PIN_FULL, HIGH, HIGH, 0 };
Button bStop = { PIN_STOP, HIGH, HIGH, 0 };

// returns true once per clean press (falling edge, active-low)
bool pressed(Button &b) {
  int raw = digitalRead(b.pin);
  if (raw != b.lastRaw) { b.lastRaw = raw; b.tChange = millis(); }
  if ((millis() - b.tChange) > DEBOUNCE_MS && raw != b.stable) {
    b.stable = raw;
    if (b.stable == LOW) return true;   // pressed
  }
  return false;
}

void applyOutputs() {
  digitalWrite(PIN_PUMP, pumpOn ? HIGH : LOW);
  digitalWrite(PIN_IDLE, pumpOn ? LOW  : HIGH);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LOW,  INPUT_PULLUP);
  pinMode(PIN_FULL, INPUT_PULLUP);
  pinMode(PIN_STOP, INPUT_PULLUP);
  pinMode(PIN_PUMP, OUTPUT);
  pinMode(PIN_IDLE, OUTPUT);
  pumpOn = false;            // start OFF
  applyOutputs();
  Serial.println("DDROID pump logic ready. Pump OFF.");
}

void loop() {
  bool low  = pressed(bLow);
  bool full = pressed(bFull);
  bool stop = pressed(bStop);

  if (low)            pumpOn = true;    // LOW  -> start filling
  if (full || stop)   pumpOn = false;   // FULL or STOP -> stop filling

  if (low || full || stop) {
    applyOutputs();
    Serial.printf("Pump %s\n", pumpOn ? "ON (filling)" : "OFF");
  }
}
