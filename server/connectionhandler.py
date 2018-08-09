"""Simple server based on Python socket module to handle media retrieval."""

import socket
import os
import subprocess


def init_flask_environ_folder(img_loc=None, json_loc=None):
    """Return necessary img and json locations based on environ."""
    if img_loc is None:
        img_loc = os.path.join(os.environ['AWS_FLASK_FOLDER'],
                               'aws/static',
                               'client_img/')
    if json_loc is None:
        json_loc = os.path.join(os.environ['AWS_FLASK_FOLDER'],
                               'aws/static',
                               'json/current.json')
    return (img_loc, json_loc)

def init_server_socket(address=None, port=None):
    """Initialize server socket. Takes eth0 IP and port 5000 by default."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if port is None:
        port = 5000
    if address is None:
        ips = subprocess.check_output(['hostname', '--all-ip-addresses'])
        address = ips.decode('utf-8')[:-3]
    server_socket.bind((port, address))
    return server_socket

def receive_bytes_to_string(client_sock):
    """Convert incoming messages from bytes to str."""
    byte_msg = client_sock.recv(1024)
    str_msg = byte_msg.decode('utf-8').replace("\n", "")
    return str_msg

def receive_frame(client_sock, frame, frame_size, img_loc):
    """Receive and save one frame."""
    img_size = 0
    filename = img_loc + "frame" + str(frame) + ".jpg"
    with open(filename, 'wb') as img:
        while img_size < frame_size:
            remain = frame_size - img_size
            if remain < 1024:
                data = client_sock.recv(remain)
            else:
                data = client_sock.recv(1024)
            img.write(data)
            img_size += len(data)

def send_frame_ack(client_sock, frame):
    """Send ACK for the frame to the client."""
    client_sock.send(("OK FRAME " + str(frame)).encode('ascii'))


class ConnectionHandler:
    """Takes optional arguments. Handle incoming connections."""

    def __init__(self, ip='127.0.0.1', port=5000, filename='default.jpg'):
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
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        return server_socket

    def start_server(self, server_socket):
        """Listen and treat incoming connections."""

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
