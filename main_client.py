"""Main handler for the client component."""

import os

from client.client import Client
from client.camera import Camera

FRAME_NBR = 200

capture_loc = os.path.join(os.environ(['AWS_FACEDETECT_FOLDER']), 'client/capture/')

cam = Camera(frames=FRAME_NBR, path=capture_loc)
cam.capture()

for nbr in range(0, FRAME_NBR):
    filen = "frame" + nbr + ".jpg"
    client = Client(filen, ip="18.222.248.133")
    socketd = client.initialize()
    client.send_data(socketd)
    socketd.close()
