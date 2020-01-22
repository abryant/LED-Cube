// This is a mash-up of the Due show() code + insights from Michael Miller's
// ESP8266 work for the NeoPixelBus library: github.com/Makuna/NeoPixelBus
// Needs to be a separate .c file to enforce ICACHE_RAM_ATTR execution.

#if defined(ESP8266) || defined(ESP32)

#include <Arduino.h>
#ifdef ESP8266
#include <eagle_soc.h>
#endif

static uint32_t _getCycleCount(void) __attribute__((always_inline));
static inline uint32_t _getCycleCount(void) {
  uint32_t ccount;
  __asm__ __volatile__("rsr %0,ccount":"=a" (ccount));
  return ccount;
}

// Assumes there are 512 LEDs to show, and pixels is 512*3 bytes long.
void ICACHE_RAM_ATTR espShow(uint8_t *pixels) {

#define CYCLES_800_T0H  (64) // 0.4us
#define CYCLES_800_T1H  (160) // 1us
#define CYCLES_800      (224) // 1.4us per bit

#define LAYER_BYTES (128 * 3)
#define PIN1 (9)
#define PIN2 (12)
#define PIN3 (13)
#define PIN4 (14)

  uint8_t *p1, *p2, *p3, *p4, *end1, mask;
  uint32_t c, startTime, pix, pinMask;

  pinMask = _BV(PIN1) | _BV(PIN2) | _BV(PIN3) | _BV(PIN4);
  p1 = pixels;
  p2 = pixels + LAYER_BYTES;
  p3 = pixels + (2 * LAYER_BYTES);
  p4 = pixels + (3 * LAYER_BYTES);
  end1 =  pixels + LAYER_BYTES;
  mask = 0x80;
  // pix has 1 bits for the ports that we want to send 0 for
  pix = ((*p1 & mask) ? 0x0 : _BV(PIN1)) |
        ((*p2 & mask) ? 0x0 : _BV(PIN2)) |
        ((*p3 & mask) ? 0x0 : _BV(PIN3)) |
        ((*p4 & mask) ? 0x0 : _BV(PIN4));
  startTime = 0;

  while (true) {
    while(((c = _getCycleCount()) - startTime) < CYCLES_800);     // Wait for bit start
    startTime = c;                                                // Save start time
    GPIO_REG_WRITE(GPIO_OUT_W1TC_ADDRESS, pinMask);               // Set high
    while(((c = _getCycleCount()) - startTime) < CYCLES_800_T0H); // Wait 0 high duration
    GPIO_REG_WRITE(GPIO_OUT_W1TS_ADDRESS, pix);                   // Set low for 0 bits
    while(((c = _getCycleCount()) - startTime) < CYCLES_800_T1H); // Wait the rest of the 1 high duration
    GPIO_REG_WRITE(GPIO_OUT_W1TS_ADDRESS, pinMask);               // Set low
    if(!(mask >>= 1)) {                                           // Next bit/byte
      mask = 0x80;
      p1++;
      p2++;
      p3++;
      p4++;
      if(p1 >= end1) break;
    }
    pix = ((*p1 & mask) ? 0x0 : _BV(PIN1)) |
          ((*p2 & mask) ? 0x0 : _BV(PIN2)) |
          ((*p3 & mask) ? 0x0 : _BV(PIN3)) |
          ((*p4 & mask) ? 0x0 : _BV(PIN4));
  }
  while((_getCycleCount() - startTime) < CYCLES_800); // Wait for last bit
}

#endif // ESP8266
