#include <user_interface.h>
#include <ESP8266WiFi.h>

#define DEFAULT_LEDS (512)
#define TIMEOUT_MILLIS (70 * 1000)

bool hasConnected = false;
uint32_t lastReceiveTimeMillis = 0;

void setup() {
  system_update_cpu_freq(160);

  WiFi.mode(WIFI_OFF);
  WiFi.forceSleepBegin();

  pinMode(2, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(14, OUTPUT);
  // The signal is inverted by a transistor, so we need to set it to low to begin with.
  digitalWrite(2, HIGH);
  digitalWrite(9, HIGH);
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);
  digitalWrite(14, HIGH);

  delay(100);

  // Set all of the LEDs to black.
  uint8_t *data = (uint8_t*) calloc(DEFAULT_LEDS * 3, sizeof(uint8_t));
  display(data, DEFAULT_LEDS * 3);
  free(data);

  Serial.begin(500000);
  while (!Serial) {
    // Make sure serial is connected.
  }
}

bool waitingForData(uint32_t len) {
  return Serial && (Serial.available() < len) && (millis() < lastReceiveTimeMillis + TIMEOUT_MILLIS);
}

bool checkPrefix(uint8_t first) {
  if (first != 'C') {
    return false;
  }
  while (waitingForData(1)) { delay(1); }
  uint8_t c = Serial.read();
  if (c != 'U') {
    return false;
  }
  while (waitingForData(1)) { delay(1); }
  c = Serial.read();
  if (c != 'B') {
    return false;
  }
  while (waitingForData(1)) { delay(1); }
  c = Serial.read();
  if (c != 'E') {
    return false;
  }
  while (waitingForData(1)) { delay(1); }
  c = Serial.read();
  return c == ':';
}

void loop() {
  Serial.write("."); // Send a single '.' to tell the server we're ready for data.
  Serial.flush();

  while (waitingForData(1)) { delay(1); }
  lastReceiveTimeMillis = millis();
  uint8_t c = Serial.read();
  if (!checkPrefix(c)) {
    while (Serial && Serial.available()) {
      c = Serial.read();
      if (c == '\n' || c == -1) {
        break;
      }
    }
    return;
  }
  while (waitingForData(3)) { delay(1); }
  int l = Serial.read();
  if (l < 0 || l > 255) {
    return;
  }
  uint16_t length = ((uint16_t) l) << 8;
  l = Serial.read();
  if (l < 0 || l > 255) {
    return;
  }
  length |= ((uint16_t) l);
  uint8_t *data = (uint8_t*) malloc(length * 3);
  size_t readLength = Serial.readBytes(data, length * 3);
  if (readLength != (length * 3)) {
    return;
  }
  display(data, length * 3);
  free(data);

  while (Serial && Serial.available()) {
    c = Serial.read();
    if (c == '\n' || c == -1) {
      break;
    }
  }
}


// ESP8266 show() is external to enforce ICACHE_RAM_ATTR execution
extern "C" void ICACHE_RAM_ATTR espShow(uint8_t *pixels);

uint32_t endTime;

void display(uint8_t *bytes, uint16_t len) {
  if (len != (DEFAULT_LEDS * 3)) {
    return;
  }
  while((micros() - endTime) < 55); // datasheet says 50 microseconds

  noInterrupts();

  espShow(bytes);

  interrupts();

  endTime = micros();
}
