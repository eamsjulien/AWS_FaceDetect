"""Main handler for the AWS server component."""

import os
import json

from server.connectionhandler import ConnectionHandler
from engine.facedetect import FaceDetect

connectd = ConnectionHandler(ip="172.31.33.238")
img_loc = os.path.join(os.environ['AWS_FLASK_FOLDER'], 'aws/static', 'client_img/default.jpg')
json_loc = os.path.join(os.environ['AWS_FLASK_FOLDER'], 'aws/static', 'json/current.json')

while True:
    socket = connectd.initialize()
    connectd.start_server(socket)
    socket.close()
    print("Starting detection...")
    faced = FaceDetect('default.jpg')
    faces = faced.detect()
    faced.image = faced.drawrectangle(faces)
    faced.convertrgb
    faced.saveimage(img_loc)
    faces_dict = {'count':len(faces)}
    with open(json_loc, 'w') as js:
        json.dump(faces_dict, js)