"""
Main handler for the AWS server component.

Usage: python3 main.py
"""


import os

import server.connectionhandler as ch
from engine.facedetect import FaceDetect

def main():
    """Main function for server loop."""

    # FACEDETECT SERVER #

    print(" -------------------------")
    print("| AWS FACEDETECT - SERVER |")
    print(" -------------------------")

    print("\n Initializing ENV variables...", end='')
    img_loc, _json_loc = ch.init_flask_environ_folder()
    print("Done!")

    print("\n Initializing server socket...", end='')
    server_socket = ch.init_server_socket()
    print("Done!")

    server_socket.listen(5)
    print("\nWaiting for incoming connection...")
    client, addr = server_socket.accept()
    print("Incoming connection from " + str(addr))

    frame_nbr = int(ch.receive_bytes_to_string(client))
    print("Expecting " + str(frame_nbr) + " frames from remote host.")

    print("\n **** RECEIVING FRAMES ****")

    for curr_frame in range(frame_nbr):

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

    for item in range(frame_nbr):
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

    # FLASK CONFIGURATION UPDATE #

    flask_config_content = []

    with open(os.environ['AWS_FLASK_FOLDER'] + '/instance/config.py',
              'r') as filedesc:
        config_content = filedesc.readlines()
        for line in config_content:
            if "SECRET" in line.strip():
                flask_config_content.append(line)

    flask_config_content.append("FRAMES_NBR = " + str(frame_nbr) + "\n")

    with open(os.environ['AWS_FLASK_FOLDER'] + '/instance/config.py',
              'w') as filedesc:
        for items in flask_config_content:
            filedesc.write(items)

    print("\n")


if __name__ == '__main__':
    main()
