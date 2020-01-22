# Starts a server with a default cube that runs on a serial port with the given baud rate.
# Requires pySerial.

from queue import Queue
from serial import Serial
from server import CubeServer, Output
import sys
import threading

class SerialOutput(Output):
  def __init__(self, tty):
    self.tty = tty
    self.output_queue = Queue(maxsize = 1)

  def send_data(self, data):
    self.output_queue.put(data)

  def send_text(self, text):
    print('[serial output]: ' + text.strip())

  def send_keepalive(self):
    self.send_data(b'\n')

  def run_serial(self):
    # Send an initial newline to wake up the device from sleeping,
    # so it prints the first '.' when it's ready.
    self.tty.write(b'\n')
    self.tty.flush()
    while True:
      # Wait for the connected cube to signal that it's ready for more data.
      self.tty.read()
      # Skip all of the other input.
      self.tty.reset_input_buffer()
      # Write the next frame to the cube.
      data = self.output_queue.get()
      self.tty.write(data)
      self.tty.flush()

if __name__ == '__main__':
  server = CubeServer()
  server.start()
  tty_filename = sys.argv[1] if len(sys.argv) >= 2 else '/dev/ttyS1'
  baud_rate = int(sys.argv[2]) if len(sys.argv) >= 3 else 500000
  tty = Serial(port = tty_filename, baudrate = baud_rate)
  output = SerialOutput(tty)
  serial_thread = threading.Thread(target = output.run_serial)
  serial_thread.start()
  # Start in a while loop, so if the controller quits it will restart immediately.
  while True:
    server.start_cube_controller(tty_filename.split('/')[-1], output)

