from base64 import b64encode
from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue, Empty
from socketserver import ThreadingMixIn
from threading import Lock
from .controller import Controller, FileOutput
import os.path
import ssl
import threading
import urllib

CERTIFICATE_CHAIN_FILE='/etc/letsencrypt/live/bryants.eu/fullchain.pem'
CERTIFICATE_PRIVKEY_FILE='/etc/letsencrypt/live/bryants.eu/privkey.pem'

control_queue_lock = Lock()
cube_control_queues = {}

path_whitelist = {
  '/': 'text/html',
  '/index.html': 'text/html',
  '/style.css': 'text/css',
  '/bootstrap.min.css': 'text/css',
  '/base64js.min.js': 'application/javascript',
  '/cube-api.js': 'application/javascript',
  '/three.min.js': 'application/javascript',
}

def start_cube_controller(name, file):
  control_queue = Queue()
  with control_queue_lock:
    if name in cube_control_queues:
      file.write(b'Cube already exists\n')
      return
    cube_control_queues[name] = control_queue
  try:
    controller = Controller(control_queue, FileOutput(file))
    controller.control_cube()
  finally:
    with control_queue_lock:
      del cube_control_queues[name]

def send_to_cube(name, command):
  with control_queue_lock:
    if name not in cube_control_queues:
      return False
    for cmd in command.split('/'):
      cube_control_queues[name].put({'command': urllib.parse.unquote(cmd)})
    return True

class Server(ThreadingMixIn, HTTPServer):
  pass

class CubeRequestHandler(BaseHTTPRequestHandler):
  def setup(self):
    self.timeout = 10
    self.disable_nagle_algorithm = True
    BaseHTTPRequestHandler.setup(self)
    pass

  def do_GET(self):
    if self.path.startswith('/api/cube/') and len(self.path) > len('/api/cube/'):
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      start_cube_controller(self.path[len('/api/cube/'):], self.wfile)
    elif self.path.startswith('/api/listen/') and len(self.path) > len('/api/listen/'):
      name = self.path[len('/api/listen/'):]
      self.listen_to_cube(name)
    elif self.path == '/api/list-cubes':
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
      names = []
      with control_queue_lock:
        names = [k for k in cube_control_queues]
      self.wfile.write(b'{"cubes":[')
      for i in range(len(names)):
        self.wfile.write(b'"' + bytes(names[i], encoding="UTF-8") + b'"')
        if i != len(names) - 1:
          self.wfile.write(b',')
      self.wfile.write(b']}\n')
    elif self.path in path_whitelist:
      filename = self.path
      if filename == '/':
        filename = '/index.html'
      with open('server/static' + filename, 'rb') as f:
        self.send_response(200)
        self.send_header('Content-Type', path_whitelist[filename])
        self.end_headers()
        self.wfile.write(f.read())
    else:
      self.send_response(404)
      self.end_headers()

  def do_POST(self):
    if self.path.startswith('/api/send/') and len(self.path) > len('/api/send/') and self.path[len('/api/send/'):].find('/') > 0:
      rest = self.path[len('/api/send/'):]
      name = rest[:rest.find('/')]
      command = rest[rest.find('/')+1:]
      if send_to_cube(name, command):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("Sent " + command + " to " + name, encoding="UTF-8"))
      else:
        self.send_response(500)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("Failed to send to " + name + "\n", encoding="UTF-8"))
    else:
      self.send_response(404)
      self.end_headers()

  def listen_to_cube(self, name):
    data_queue = Queue()
    cube_exists = False
    with control_queue_lock:
      if name in cube_control_queues:
        cube_control_queues[name].put({'command': 'listen', 'data_queue': data_queue})
        cube_exists = True
    if not cube_exists:
      self.send_response(500)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'Failed to listen to ' + bytes(name, encoding="UTF-8") + b'\n')
      return
    self.send_response(200)
    self.send_header('Content-Type', 'text/event-stream')
    self.end_headers()
    while True:
      data = data_queue.get()
      if data[-1] == b'\n':
        data = data[:-1]
      if data == b'quit':
        return
      self.wfile.write(b'data: ' + b64encode(data) + b'\n\n')
      self.wfile.flush()

def start_http(http_port):
  http_address = ('', http_port)
  httpd = Server(http_address, CubeRequestHandler)
  httpd.serve_forever()

def start_https(https_port):
  https_address = ('', https_port)
  httpd_ssl = Server(https_address, CubeRequestHandler)
  ssl_context = ssl.SSLContext()
  ssl_context.load_cert_chain(CERTIFICATE_CHAIN_FILE, keyfile=CERTIFICATE_PRIVKEY_FILE)
  httpd_ssl.socket = ssl_context.wrap_socket(httpd_ssl.socket, server_side=True)
  httpd_ssl.serve_forever()

def main(http_port = 2823, https_port = 2824):
  print('HTTP Port %d' % http_port)
  http_thread = threading.Thread(target = start_http, args = (http_port,))
  http_thread.start()
  https_thread = None
  if os.path.isfile(CERTIFICATE_CHAIN_FILE) and os.path.isfile(CERTIFICATE_PRIVKEY_FILE):
    print('HTTPS Port %d' % https_port)
    https_thread = threading.Thread(target = start_https, args = (https_port,))
    https_thread.start()
  else:
    print('Can\'t find SSL certificate files, starting in HTTP-only mode.')

if __name__ == "__main__":
  main()

