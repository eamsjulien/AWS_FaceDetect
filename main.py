"""Main handler for the AWS server component."""

from server.connectionhandler import ConnectionHandler
from engine.facedetect import FaceDetect

connectd = ConnectionHandler()
socket = connectd.initialize()

while True:
    connectd.start_server(socket)
    faced = FaceDetect('default.jpg')
    faced.convertgrey()
    faced.detect()
