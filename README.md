# LED Cube

Visualizations for a cube of LEDs.

Examples: https://photos.app.goo.gl/b63fNjHddFoOuM0C2

## Starting the server in client-server mode

```
LED-Cube$ python server.py
```

To connect a virtual cube to the server:

```
$ curl http://localhost:2823/api/cube/test
```

This will connect a virtual cube called 'test', and keep the connection open to receive all of the commands to send to the cube.

After that, open http://localhost:2823/ to control the virtual test cube, and see what it is displaying in the web interface.

## Starting the server in serial mode

Instead of connecting a cube over the network with HTTP, you can connect an arduino running `arduino/esp8266_serial_leds/esp8266_serial_leds.ino` directly to a serial port. This requires pySerial.

```
LED-Cube$ python serial_cube.py
```

This will automatically connect to `/dev/ttyS1` at a baud rate of 500000. The port and baud rate can both be set on the command line, although the baud rate needs to be this high to reach ~20-30FPS.

So far, I have only tested this on a Raspberry Pi 3 Model B+. To set up the serial port correctly for this, use the following options in /boot/config.txt:
```
enable_uart=1
dtoverlay=pi3-disable-bt
```

This disables the Pi's bluetooth, so that the UART that usually controls bluetooth can be used for the serial port instead. This UART is needed to get a high enough baud rate to display the 8x8x8 cube at a high frame rate.

See https://www.raspberrypi.org/documentation/configuration/uart.md for more details.
