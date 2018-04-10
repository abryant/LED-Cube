uint32_t endTime;
volatile uint8_t *port;
uint8_t pinMask;
uint8_t *data;

const uint8_t pin = 2;
const uint16_t leds = 12;

uint8_t *startBuf;

void setup() {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
  port = portOutputRegister(digitalPinToPort(pin));
  pinMask = digitalPinToBitMask(pin);
  Serial.begin(115200);
  while (!Serial) {
    // wait to connect
  }
  startBuf = (uint8_t*) malloc(4);
  Serial.write("\nREADY\n");
}

void loop() {
  if (Serial.available() > 0) {
    size_t n = Serial.readBytes(startBuf, 4);
    if (n < 4) {
      return;
    }
    if (startBuf[0] != 'G' || startBuf[1] != 'O' || startBuf[2] != ':') {
      return;
    }

    uint8_t len = startBuf[3];
    uint8_t *data = (uint8_t*) malloc(len);
    n = Serial.readBytes(data, len);
    if (n != len) {
      return;
    }
    // Signal to the controller that we're ready for more data.
    Serial.write(startBuf, 3);

    display(data, len);
    free(data);
  }
}

// timing:
// 0: 6 cycles on, 22 cycles off
// 1: 22 cycles on, 6 cycles off
// write with custom assembly as here:
// https://github.com/adafruit/Adafruit_NeoPixel/blob/master/Adafruit_NeoPixel.cpp#L959

void display(uint8_t *bytes, uint16_t len) {
  while((micros() - endTime) < 55); // datasheet says 50 microseconds

  noInterrupts();

  volatile uint16_t i = len;
  volatile uint8_t *ptr = bytes;
  volatile uint8_t b = *ptr;
  ptr++;
  volatile uint8_t hi = *port | pinMask;
  volatile uint8_t lo = *port & ~pinMask;
  volatile uint8_t bit = 8;
  volatile uint8_t next = lo;
  // HI at 0
  // LO at 6 (for 1) or 22 (for 0)
  // finish at 28

  asm volatile(
     "start%=:"                  "\n\t" // Clk  Pseudocode    (T =  0)
      "st   %a[port],  %[hi]"    "\n\t" // 2    PORT = hi     (T =  2)
      "sbrc %[byte],  7"         "\n\t" // 1-2  if(b & 128)
       "mov  %[next], %[hi]"     "\n\t" // 0-1   next = hi    (T =  4)
      "dec  %[bit]"              "\n\t" // 1    bit--         (T =  5)
      "nop"                      "\n\t" // 1    nop           (T =  6)
      "st   %a[port], %[next]"   "\n\t" // 2    PORT = next   (T =  8)
      "mov  %[next], %[lo]"      "\n\t" // 1    next = lo     (T =  9)
      "breq nextbyte%="          "\n\t" // 1-2  if(bit == 0) (from dec above)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 12)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 14)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 16)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 18)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 20)
      "nop"                      "\n\t" // 1    nop           (T = 21)
      "rol  %[byte]"             "\n\t" // 1    b <<= 1       (T = 22)
      "st   %a[port],  %[lo]"    "\n\t" // 2    PORT = lo     (T = 24)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 26)
      "rjmp start%="             "\n\t" // 2    -> start (next bit out)
     "nextbyte%=:"               "\n\t" //                    (T = 11)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 13)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 15)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 17)
      "rjmp .+0"                 "\n\t" // 2    nop nop       (T = 19)
      "ldi  %[bit]  ,  8"        "\n\t" // 1    bit = 8       (T = 21)
      "ld   %[byte] ,  %a[ptr]+" "\n\t" // 2    b = *ptr++    (T = 22)
      "st   %a[port], %[lo]"     "\n\t" // 2    PORT = lo     (T = 24)
      "sbiw %[count], 1"         "\n\t" // 2    i--           (T = 26)
       "brne start%="            "\n"   // 2    if(i != 0) -> (next byte)
    : [port]  "+e" (port),
      [byte]  "+r" (b),
      [bit]   "+r" (bit),
      [next]  "+r" (next),
      [count] "+w" (i)
    : [ptr]   "e" (ptr),
      [hi]    "r" (hi),
      [lo]    "r" (lo));

  interrupts();

  endTime = micros();
}

