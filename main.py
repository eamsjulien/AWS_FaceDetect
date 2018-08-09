"""Main handler for the AWS server component."""

import server.connectionhandler as ch
from engine.facedetect import FaceDetect


print(" -------------------------")
print("| AWS FACEDETECT _ SERVER |")
print(" -------------------------")

print("\n Initializing ENV variables...", end='')
img_loc, json_loc = ch.init_flask_environ_folder()
print("Done!")

print("\n Initializing server socket...", end='')
server_socket = ch.init_server_socket()
print("Done!")

server_socket.listen(5)
print("\nWaiting for incoming connection...")
client, addr = server_socket.accept()
print("Incoming connection from " + str(addr))

FRAME_NBR = int(ch.receive_bytes_to_string(client))
print("Expecting " + str(FRAME_NBR) + " frames from remote host.")

print("\n **** RECEIVING FRAMES ****")

for curr_frame in range(FRAME_NBR):

    frame_size = int(ch.receive_bytes_to_string(client))
    ch.receive_frame(client, curr_frame, frame_size, img_loc)
    print("Frame " + str(curr_frame) + " received.")

    print("Sending ack...", end='')
    ch.send_frame_ack(client, curr_frame)
    print("Sent.")

print("\nFrames received!")

print("Closing sockets...", end='')
client.close()
server_socket.close()
print("Done!")

print("\n **** STARTING DETECTION ****")

for item in range(FRAME_NBR):
    print("Running detection on frame " + str(item))
    frame_name = img_loc + "frame" + str(item) + ".jpg"
    detection = FaceDetect(frame_name)
    faces = detection.detect()
    detection.image = detection.drawrectangle(faces)
    detection.saveimage(frame_name)

print("\nDetection completed!")
print("\n --------------------------")
print("| AWS FACEDETECT - GOODBYE |")
print(" --------------------------")
