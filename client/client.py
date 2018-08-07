"""Client class for remote hosts ready to send images to AWS."""

import socket


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
