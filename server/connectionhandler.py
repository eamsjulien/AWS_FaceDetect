"""
Module supporting the ConnectionHandler class and various connectivity
functions needed for the FaceDetect server.

function init_flask_environ_folder: concatenates paths together and returns
the img_loc, where resides, and json_loc, where json files should be.

function init_server_socket: Initialize the server socket.

function receive_bytes_to_string: Receive and convert bytes messages in str.

function receive_frame: Receive and save one frame.

function send_frame_ack: Send one ack to client for a specific frame.

class ConnectionHandler: Create a server instance with a frame and a socket.
Useful for receiving only one frame on one socket.
"""

import socket
import os


def init_flask_environ_folder(img_loc=None, json_loc=None):
    """Return necessary img and json locations based on environ.

    Variable img_log is used to determine where to save and process
    frames received from the client. This is typically the folder where
    Flask static/instance images/json data reside.
    It relies on ENV parameter, AWS_FLASK_FOLDER.

    Args:
        img_loc: Optional string defining the capture loc.
        json_loc: Optional string defining the json folder loc.

    Returns:
        (img_loc, json_loc): A str tuple including img_loc and json_loc.
    """
    if img_loc is None:
        img_loc = os.path.join(os.environ['AWS_FLASK_FOLDER'],
                               'aws/static',
                               'client_img/')
    if json_loc is None:
        json_loc = os.path.join(os.environ['AWS_FLASK_FOLDER'],
                                'aws/static',
                                'json/current.json')
    return (img_loc, json_loc)

def init_server_socket(address=None, port=5000):
    """Initialize server socket.

    Args:
        address: Optional string representing the IP address to bind to.
        port: Optional int representing the port to connect to.

    Returns:
        A server socket where the program can receive messages.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if address is None:
        address = socket.gethostbyname(socket.gethostname())
    server_socket.bind((address, port))
    return server_socket

def receive_bytes_to_string(client_sock):
    """Convert incoming messages from bytes to str.

    Receives message first, then do the byte to str translation.

    Args:
        client_sock: A socket instance representing the client socket.

    Returns:
        None
    """
    byte_msg = client_sock.recv(1024)
    str_msg = byte_msg.decode('utf-8').replace("\n", "")
    return str_msg

def receive_frame(client_sock, frame, frame_size, img_loc):
    """Receive and save one frame.

    Main function responsible for storing and saving exactly one frame from
    a remote client. In order to properly delimitate a frame from a stream,
    the function also takes the frame size as a parameter and compute the
    necessary incoming byte number to expect.

    Args:
        client_sock: A socket instance representing a client connection.
        frame: An int representing the frame number to receive.
        frame_size: An int representing the frame size to expect.
        img_loc: A string representing the destination where to save the
        frame

    Returns:
        None
    """
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
    """Send ACK for the frame to the client.

    Client expects a message of the form 'OK FRAME X' from the server,
    where X is the frame number wainting to be ack'ed.

    Args:
        client_sock: A socket instance representing the client connection.
        frame: An int representing the frame number to ack.

    Returns:
        None
    """
    client_sock.send(("OK FRAME " + str(frame)).encode('ascii'))


class ConnectionHandler:
    """Handles and manage incoming connections for one frame and one socket.

    The ConnectionHandler  class is used when only one frame (or one image)
    needs to be received from a client over one socket. It puts together a
    file location and a socket waiting for connection with a remote client.

    Attributes:
        addr: A string representing the server IP.
        filename: A string representing the frame location and name.
        port: An optional int representing the port to connect to.`
    """

    def __init__(self, address='127.0.0.1', port=5000, filename='default.jpg'):
        """Init ConnectionHandler with addr, port and filename."""
        self.address = address
        self.port = port
        self.filename = filename

    def getip(self):
        """Getter for ConnectionHandler instance address.

        Args:
            None

        Returns:
            A string representing the binding IP address.
        """
        return self.address

    def getport(self):
        """Getter for ConnectionHandler instance port.

        Args:
            None

        Returns:
            An int representing the port to bind.
        """
        return self.port

    def getfilename(self):
        """Getter for ConnectionHandler instance filename.

        Args:
            None

        Returns:
            An string representing the file name.
        """
        return self.filename

    def setip(self, address):
        """Setter for ConnectionHandler instance address.

        Args:
            addr: A string representing the new IP address to bind.

        Returns:
            None
        """
        self.address = address

    def setport(self, port):
        """Setter for ConnectionHandler instance binding port.

        Args:
            port: An int representing the new port to bind.

        Returns:
            None
        """
        self.port = port

    def setfilename(self, filename):
        """Setter for ConnectionHandler instance filename.

        Args:
            filename: An string representing the new filename location and
            name.

        Returns:
            None
        """
        self.filename = filename

    def initialize(self):
        """Initialize the socket.

        Args:
            None

        Returns:
           server_socket: A socket instance needed for further client/serv
            connections.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.address, self.port))
        return server_socket

    def start_server(self, server_socket):
        """Listen and treat incoming connections.

        The start_server function initially put the provided socket in the
        listen mode for incoming connection. Backlog is hardcoded and not
        modifiable, set to 5. Once a connection with a remote client is
        initiated, the function will receive and save the frame to the
        specified location.

        Args:
            server_socket: A socket used for the transaction between client
            and server.

        Returns:
            None
        """
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
