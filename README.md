# AWS_FaceDetect

Simple OpenCV project to analyze a media (image/frame, video) and detect faces. Runs on AWS EC2 and accept inputs from remote hosts. With [AWS_Flask](https://github.com/eamsjulien/AWS_Flask), it can display resulting frames in a web browser. EC2 instance is publicly available so are the results once proper permissions have been granted.

AWS_FaceDetect consists of two parts: the client and the server. Both parts are also divided in two distinct components. Client part includes camera and socket component and server part includes face detection and socket component as well.

With the client part, one user can send an arbitrary number of frames (hence a video) to the server. The client does not need a public IP, only internet connectivity is enough. Requirements on the client are rather heavy for this implementation since it relies on python-opencv for the sake of simplicity. However, a more lightweight webcam handler would work too since we only require from the client to be able to take frames and save them, before sending them over to the server via TCP sockets.

With the server part, a host, typically a cloud instance such as AWS, can receive incoming frames from a client and perform some simple face detection on them. Requirements on this part are heavier since opencv is required for face detection. If the AWS_Flask project is installed, user can leverage one Flask instance to display result frames in a web browser, publicly accessible if needed. Current implementation requires AWS_Flask project to be installed as well.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Current implementation also requires the [AWS_Flask](https://github.com/eamsjulien/AWS_Flask) project to be installed on the server and in the same directory as the AWS_FaceDetect one.

### Prerequisites

What things you need to install the software and how to install them. Python3 libraries are in requirements.txt for easy installation with pip.

#### Client Prerequisites

- Linux >= 4.17.11
- Bash >= 4.4.23
- Python >= 3.7.0
- Numpy >= 1.15.0
- opencv-python >= 3.4.2.17

Earlier program/package versions might work too but haven't been tested. Numpy/opencv-python are required dependencies for the current implementation but minimal changes should be required to adapt the videocapture to a more lightweight backend.

#### Server Prerequisites

- Linux >= 4.14.59
- Bash >= 4.2.46
- Python >= 3.7.0
- Numpy >= 1.15.0
- opencv-python >= 3.4.2.17
- [AWS_Flask](https://github.com/eamsjulien/AWS_Flask)

AWS_Flask is a requirement in the current implementation but eliminating it in the dependency list should be straightforward since only one file, the launch.sh one, needs to be edited.

### Installing

A step by step series of examples that tell you how to get a development env running.

#### Client Installation

Simply clone the repository and ensure that you're on the **devel** branch.

```bash
git clone https://github.com/eamsjulien/AWS_FaceDetect.git ; git checkout origin/devel
```

And that's it !

#### Server Installation

Move to the parent directory where your AWS Flask installation is.

```bash
cd $YOUR_AWS_FLASK_PARENT_DIRECTORY
```

Then simply clone the repository and ensure that you're on the **devel** branch.

```bash
git clone https://github.com/eamsjulien/AWS_FaceDetect.git ; git checkout origin/devel
```

And good to go !

### Running

This section will introduce a quick way to get the client and server running and to receive/process frames.

- On the server, in the AWS_FaceDetect folder:

```bash
./launch.sh --mode server
```

- On the client, in the AWS_FaceDetect folder:

```bash
./launch.sh --mode client --frames 30 --sleep 0.1 --address "pub-ip-address-of-your-server"
```

Replace 30 by the number of frames you wish to capture, 0.1 by the amount of time you wish to wait (in second) between two send, and the address by your server IP address.

- Once all frames have been sent, you can access to the Flask server by typing in your browser "ip-address":8080 (without quotes and by replacing ip-address by the ip address of your server.)

- Choose a login to register, then access the index where frames have been processed and displayed. To stop the server, simply ctrl+c in the server open terminal.