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
