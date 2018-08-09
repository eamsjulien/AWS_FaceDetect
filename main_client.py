"""Main handler for the client component."""

import client.client as cl
from client.camera import Camera

FRAME_NBR = 20
SERVER_ADDR = '13.115.118.145'

print(" -------------------------")
print("| AWS FACEDETECT _ SERVER |")
print(" -------------------------")

print("\n Initializing ENV variables...", end='')
capture_loc = cl.init_facedetect_environ_folder()
print("Done!")

print("\n Initializing server socket...", end='')
client_socket = cl.init_client_socket(SERVER_ADDR)
print("Done!")

print("\n **** CAPTURING FRAMES ****")
cam = Camera(frames=FRAME_NBR, path=capture_loc)
cam.capture()
print(" " + str(FRAME_NBR) + " frames captured!")

print("\n **** SENDING FRAMES NBR ****")
cl.send_total_frame_nbr(client_socket, FRAME_NBR)
print(" Frames number sent to server!")

print("\n **** SENDING FRAMES ****")
for frame in range(FRAME_NBR):
    frame_loc = capture_loc + "frame" + str(frame) + ".jpg"
    cl.send_frame_size(client_socket, frame_loc)
    print("Sending frame %s..." % str(frame), end='')
    cl.send_frame(client_socket, frame_loc, sleep=0.1)
    print("Done.")
    print("Waiting for frame " + str(frame) + " reception...", end='')
    cl.waiting_for_ack(client_socket, frame)
    print("ACK")

print("\nFrames sent!")
print("\n --------------------------")
print("| AWS FACEDETECT - GOODBYE |")
print(" --------------------------")
