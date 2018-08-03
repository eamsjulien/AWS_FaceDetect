"""Simple server based on Python socket module to handle media retrieval."""

import socket


class ConnectionHandler:
    """Takes optional arguments. Handle incoming connections."""

    def __init__(self, ip='127.0.0.1', port=5000, filename='default.jpg'):
        """Construct with three attributes."""
        self.ip = ip
        self.port = port
        self.filename = port

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
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        return server_socket

    def start_server(self, server_socket):
        """Listen and treat incoming connections."""
        while True:
            server_socket.listen(5)
            print("Waiting for incoming connections...")

            client, addr = server_socket.accept()
            print("Incoming connection from " + str(addr))

            with open(self.filename, 'wb') as img:
                while True:
                    data = client.recv(1024)
                    if not data:
                        break
                    img.write(data)

            print("Transfer Completed.")
            print("Closing " + str(addr))
