#include <ESP8266WiFi.h>

#include <DNSServer.h>            //Local DNS Server used for redirecting all requests to the configuration portal
#include <ESP8266WebServer.h>     //Local WebServer used to serve the configuration portal
#include <WiFiManager.h>          //https://github.com/tzapu/WiFiManager WiFi Configuration Magic

#define DEFAULT_LEDS (512)
#define TIMEOUT_MILLIS (70 * 1000)

WiFiManager wifiManager;

bool hasConnected = false;
uint32_t lastReceiveTimeMillis = 0;

void setup() {
  system_update_cpu_freq(160);
  pinMode(2, OUTPUT);
  // The signal is inverted by a transistor, so we need to set it to low to begin with.
  digitalWrite(2, HIGH);

  // Set all of the LEDs to black.
  uint8_t *data = (uint8_t*) calloc(DEFAULT_LEDS * 3, sizeof(uint8_t));
  display(data, DEFAULT_LEDS * 3);
  free(data);

  wifiManager.autoConnect("ESP-12E", "ddr;rtoE");
}

WiFiClient client;

void makeGetRequest() {
  // If we're already connected, client.connect() will disconnect.
  int retries = 3;
  while (!client.connect("bryants.eu", 2823)) {
    // If we've ever connected to the server before (this boot), then keep retrying forever.
    // This helps when the server is temporarily down during testing.
    if (!hasConnected) {
      retries--;
      if (retries == 0) {
        wifiManager.resetSettings();
        ESP.restart();
      }
    }
    delay(500);
  }
  hasConnected = true;
  lastReceiveTimeMillis = millis();

  client.setNoDelay(true);
  client.print("GET /api/cube/yocto HTTP/1.1\r\n\r\n");
  client.flush();
}

bool waitingForData(uint32_t len) {
  return client.connected() && (client.available() < len) && (millis() < lastReceiveTimeMillis + TIMEOUT_MILLIS);
}

bool checkPrefix(uint8_t first) {
  if (first != 'C') {
    return false;
  }
  while (waitingForData(1)) { delay(1); }
  uint8_t c = client.read();
  if (c != 'U') {
    return false;
  }
  while (waitingForData(1)) { delay(1); }
  c = client.read();
  if (c != 'B') {
    return false;
  }
  while (waitingForData(1)) { delay(1); }
  c = client.read();
  if (c != 'E') {
    return false;
  }
  while (waitingForData(1)) { delay(1); }
  c = client.read();
  return c == ':';
}

void loop() {
  if (!client.connected() || (millis() > lastReceiveTimeMillis + TIMEOUT_MILLIS)) {
    makeGetRequest();
  }
  while (waitingForData(1)) { delay(1); }
  if (client.connected() && client.available()) {
    lastReceiveTimeMillis = millis();
  }
  uint8_t c = client.read();
  if (!checkPrefix(c)) {
    while (client.connected() && client.available()) {
      c = client.read();
      if (c == '\n' || c == -1) {
        break;
      }
    }
    return;
  }
  while (waitingForData(3)) { delay(1); }
  uint8_t l = client.read();
  if (l == -1) {
    return;
  }
  uint16_t length = l << 8;
  l = client.read();
  if (l == -1) {
    return;
  }
  length |= l;
  uint8_t *data = (uint8_t*) malloc(length * 3);
  while (waitingForData(length * 3)) {
    delay(1);
  }
  size_t readLength = client.read(data, length * 3);
  if (readLength != (length * 3)) {
    return;
  }
  display(data, length * 3);
  free(data);

  while (client.connected() && client.available()) {
    if (client.read() == '\n') {
      break;
    }
  }
}


// ESP8266 show() is external to enforce ICACHE_RAM_ATTR execution
extern "C" void ICACHE_RAM_ATTR espShow(
  uint8_t pin, uint8_t *pixels, uint32_t numBytes);

uint32_t endTime;

void display(uint8_t *bytes, uint16_t len) {
  while((micros() - endTime) < 55); // datasheet says 50 microseconds

  noInterrupts();

  espShow(2, bytes, len);

  interrupts();

  endTime = micros();
}

