"""Client class for remote hosts ready to send images to AWS."""

import socket
import os
import time


def init_facedetect_environ_folder(capture_loc=None):
    """Return necessary capture_loc based on environ."""
    if capture_loc is None:
        capture_loc = os.path.join(os.environ['AWS_FACEDETECT_FOLDER'], 'client/capture/')
    return capture_loc

def init_client_socket(address, port=None):
    """Initialize client socket. Address is mandatory argument, default port is 5000."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))
    return client_socket

def send_total_frame_nbr(client_socket, frame_nbr):
    """Send frame number to server."""
    client_socket.send(str(frame_nbr).encode('ascii'))

def send_frame_size(client_socket, frame_loc):
    """Send frame size to client."""
    filesize = os.path.getsize(frame_loc)
    client_socket.send(str(filesize).encode('ascii'))

def send_frame(client_socket, frame_loc, sleep=1):
    """Send frame to client with a default sleep of 1s."""
    time.sleep(sleep)
    with open(frame_loc, 'rb') as f:
        buf = f.readline(1024)
        while buf:
            client_socket.send(buf)
            buf = f.readline(1024)
        f.close()

def waiting_for_ack(client_socket, frame):
    """Wait for a particular frame to be acked by server."""
    msg = client_socket.recv(1024).decode('UTF-8')
    while (msg != 'OK FRAME ' + str(frame)):
        msg = client_socket.recv(1024).decode('UTF-8')

class Client:
    """Takes optional arguments. Handle incoming connections."""

    def __init__(self, filename, ip='127.0.0.1', port=5000):
        """Construct with three attributes."""
        self.ip = ip
        self.port = port
        self.filename = filename

    def getip(self):
        """Return the IP."""
        return self.ip

    def getport(self):
        """Return the port."""
        return self.port

    def getfilename(self):
        """Return the filename."""
        return self.filename

    def setip(self, ip):
        """Set the ip."""
        self.ip = ip

    def setport(self, port):
        """Set the port."""
        self.port = port

    def setfilename(self, filename):
        """Set the filename."""
        self.filename = filename

    def initialize(self):
        """Initialize the connection. Return a socket."""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.ip, self.port))
        return client_socket

    def send_data(self, client_socket):
        """Send data to remote host."""
        with open(self.filename, 'rb') as f:
            buf = f.readline(1024)
            while buf:
                client_socket.send(buf)
                buf = f.readline(1024)
            f.close
        client_socket.close()
