from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue, Empty
from socketserver import ThreadingMixIn
from threading import Lock
from .controller import Controller

control_queue_lock = Lock()
cube_control_queues = {}

def start_cube_controller(name, file):
  control_queue = Queue()
  with control_queue_lock:
    if name in cube_control_queues:
      file.write(b'Cube already exists')
      return
    cube_control_queues[name] = control_queue
  try:
    controller = Controller(control_queue, file)
    controller.control_cube()
  finally:
    with control_queue_lock:
      del cube_control_queues[name]

def send_to_cube(name, command):
  with control_queue_lock:
    if name not in cube_control_queues:
      return False
    cube_control_queues[name].put(command)
    return True

class Server(ThreadingMixIn, HTTPServer):
  pass

class CubeRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.end_headers()
    self.wfile.write(b'Hello world!\n')
    if self.path.startswith('/cube/') and len(self.path) > 6:
      start_cube_controller(self.path[6:], self.wfile)
    elif self.path.startswith('/put/') and len(self.path) > 5 and self.path[5:].find('/') > 0:
      rest = self.path[5:]
      name = rest[:rest.find('/')]
      command = rest[rest.find('/')+1:]
      if send_to_cube(name, command):
        self.wfile.write(bytes("Sent " + command + " to " + name, encoding="UTF-8"))
      else:
        self.wfile.write(bytes("Failed to send to " + name, encoding="UTF-8"))

def main(port = 8080):
  server_address = ('', port)
  httpd = Server(server_address, CubeRequestHandler)
  httpd.serve_forever()

if __name__ == "__main__":
  main()

