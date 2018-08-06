"""Main handler for the AWS server component."""

from server.connectionhandler import ConnectionHandler
from engine.facedetect import FaceDetect

connectd = ConnectionHandler(ip="172.31.33.238")

while True:
    socket = connectd.initialize()
    connectd.start_server(socket)
    socket.close()
    print("Starting detection...")
    faced = FaceDetect('default.jpg')
    faced.detect()
