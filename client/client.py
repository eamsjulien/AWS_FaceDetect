"""
Module supporting the Client class and various connection handlers functions.

function init_facedetect_environ_folder: concatenates path together and returns
the capture_loc where frames reside.

function init_client_socket: Initialize the client socket.

function send_total_frame_nbr: Send the frame number to client.

function send_frame_size: Send the frame size to the client.

function send_frame: Send a frame to the client.

function waiting_for_ack: Waits for client's ack based on frame.

class Client: Create a client instance with a frame and a socket. Useful for
sending only one frame on one socket.
"""

import socket
import os
import time


def init_facedetect_environ_folder(capture_loc=None):
    """Return necessary capture_loc based on environ.

    Variable capture_loc is used to determine where frames captured
    by the Camera class resides. It relies on an ENV parameter, called
    AWS_FACEDETECT_FOLDER.

    Args:
        capture_loc: Optional string defining the capture loc.

    Returns:
        The capture_loc string defining where frames taken by the Camera
        class reside.
    """
    if capture_loc is None:
        capture_loc = os.path.join(os.environ['AWS_FACEDETECT_FOLDER'],
                                   'client/capture/')
    return capture_loc

def init_client_socket(address, port=5000):
    """Initialize client socket.

    Args:
        address: string representing the IP address to connect to.
        port: Optional int representing the port to connect to.

    Returns:
        A client socket where the program can start sending messages.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))
    return client_socket

def send_total_frame_nbr(client_socket, frame_nbr):
    """Send frame number to server.

    This function is useful for the server since it will use it to
    determine the number of frames it needs to process and iniate
    a Flask configuration parameter accordingly.

    Args:
        client_socket: A socket instance, used for client/server interactions.
        frame_nbr: An int representing the frame number to agree upon with
        the server.

    Returns:
        None

    """
    client_socket.send(str(frame_nbr).encode('ascii'))

def send_frame_size(client_socket, frame_loc):
    """Send frame size to client.

    Function useful for the server since it will use this result to compute
    frame size and bytes reception accordingly. With this number, a
    server can exactly knows how many bytes to expect from a stream flow in
    order to fully receive a frame.

    Args:
        client_socket: A socket instance, used for client/server interactions.
        frame_loc: A string representing the frame location to compute and
        send size from.

    Returns:
        None
    """
    filesize = os.path.getsize(frame_loc)
    client_socket.send(str(filesize).encode('ascii'))

def send_frame(client_socket, frame_loc, sleep=1):
    """Send frame to client.

    Send one frame to the client, but wait for sleep seconds before sending
    it. Sleep parameter is useful when a lot of frames are sent in a row,
    in order to avoid broken pipe with the server, when the other end
    cannot keep up the rythm.

    Args:
        client_socket: A socket instance, used for client/server interactions.
        frame_loc: A string representing the frame location.
        sleep: Optional float representing the number of second to wait
        before sending.

    Returns:
        None
    """
    time.sleep(sleep)
    with open(frame_loc, 'rb') as filedesc:
        buf = filedesc.readline(1024)
        while buf:
            client_socket.send(buf)
            buf = filedesc.readline(1024)
        filedesc.close()

def waiting_for_ack(client_socket, frame):
    """Wait for a particular frame to be acked by server.

    Client expects a message of the form 'OK FRAME X' from the server,
    where X is the frame number waiting to be ack'ed.

    Args:
        client_socket: A socket instance, used for client/server interactions.
        frame: An int representing the current frame number waiting to be
        ack'ed.

    Returns:
        None
    """
    msg = client_socket.recv(1024).decode('UTF-8')
    while msg != 'OK FRAME ' + str(frame):
        msg = client_socket.recv(1024).decode('UTF-8')

class Client:
    """Handles and manage incoming connections for one frame and one socket.

    The client class is used when only one frame (or one image) needs to be
    send to a server over one socket. It puts together a file location and
    a socket connection with a remote server.

    Attributes:
        addr: A string representing the server IP.
        filename: A string representing the frame location and name.
        port: An optional int representing the port to connect to.`
    """

    def __init__(self, filename, addr='127.0.0.1', port=5000):
        """Init Client with addr, port and filename."""
        self.addr = addr
        self.port = port
        self.filename = filename

    def getip(self):
        """Getter for Client instance remote address.

        Args:
            None

        Returns:
            A string representing the remote IP address.
        """
        return self.addr

    def getport(self):
        """Getter for Client instance remote port.

        Args:
            None

        Returns:
            An int representing the remote IP port to connect to.
        """
        return self.port

    def getfilename(self):
        """Getter for Client instance filename.

        Args:
            None

        Returns:
            An string representing the file name.
        """
        return self.filename

    def setip(self, addr):
        """Setter for Client instance remote address.

        Args:
            addr: A string representing the new IP address to connect to.

        Returns:
            None
        """
        self.addr = addr

    def setport(self, port):
        """Setter for Client instance remote port.

        Args:
            port: An int representing the new port to connect to.

        Returns:
            None
        """
        self.port = port

    def setfilename(self, filename):
        """Setter for Client instance filename.

        Args:
            filename: An string representing the new filename location and
            name.

        Returns:
            None
        """
        self.filename = filename

    def initialize(self):
        """Initialize the connection.

        Args:
            None

        Returns:
            client_socket: A socket instance needed for further client/serv
            connections.
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.addr, self.port))
        return client_socket

    def send_data(self, client_socket):
        """Send data to remote host.

        Main function of the class, responsible for sending the file over
        the socket. Directly acts on the instance self.filename.

        Args:
            client_socket: A socket used for the transaction between client
            and server.

        Returns:
            None
        """
        with open(self.filename, 'rb') as filedesc:
            buf = filedesc.readline(1024)
            while buf:
                client_socket.send(buf)
                buf = filedesc.readline(1024)
        client_socket.close()
