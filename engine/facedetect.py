"""
Module support the engine route, more specifically, the FaceDetect class.
Provides support for face detection on one or a set of frames.

class FaceDetect: Provide face detection support for an image.
"""

import cv2

HAAR_CASC = "engine/haarcascade_frontalface_alt.xml"


class FaceDetect:
    """Provides support for face detection.

    One instance can only work on one frame or image at a time.

    Attributes:
        image: A string representating the image to act on.
    """

    def __init__(self, image=None):
        """Init FaceDetect with one image and turn it to grayscale."""
        self.image = cv2.imread(image, 0)

    def isvalid(self):
        """Check if attribute has been set.

        Method to confirm whether or not image has been defined.

        Args:
            None

        Returns:
            A boolean True is the image is defined and valid, False otherwise.
        """
        try:
            return bool(self.image.all() is not None)
        except AttributeError:
            return False

    def convertgrey(self):
        """Convert image to grayscale.

        Args:
            None

        Returns:
            None
        """
        if self.isvalid():
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            print("Image undefined.")

    def convertrgb(self):
        """Convert image from grayscale to RGB.

        Args:
            None

        Returns:
            None
        """
        if self.isvalid():
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        else:
            print("Image undefined.")

    def getimage(self):
        """Getter for the image.

        Args:
            None

        Returns:
            A string representing the image name and loc.
        """
        return self.image

    def setimage(self, img):
        """Setter for the image.

        Args:
            img: A string representing the new image name and loc.

        Returns:
            None
        """
        self.image = img

    def detect(self, scale=1.1, neighbors=5):
        """Detect if a face is found.

        Use a cascade classifier from cv2 library to determine whether or
        not the attribute image has a face in it. Relies on an external
        XML library, based on HAAR classifier.

        Args:
            scale: An optional float to adjust the classifier.
            neighbors: An optional int to adjust the classifier.

        Returns:
            A list of faces if faces are found. None if the image is invalid.
        """
        if self.isvalid():
            haar_face_casc = cv2.CascadeClassifier(HAAR_CASC)
            faces = haar_face_casc.detectMultiScale(self.image,
                                                    scale,
                                                    neighbors)
            print('Faces found: ', len(faces))
            return faces
        print('Image format invalid.')
        return None

    def drawrectangle(self, faces):
        """Draw rectangles on the picture based on faces.

        Takes the face list from the detect method output and draw rectangles
        where faces are supposed to be on the frame.

        Args:
            faces: An array list representing faces location.

        Returns:
            The modified frame.
        """
        if self.isvalid():
            for (coordx, coordy, width, height) in faces:
                cv2.rectangle(self.image, (coordx, coordy),
                              (coordx+width, coordy+height), (0, 255, 0), 2)
            return self.image
        print('Image format invalid.')
        return None

    def saveimage(self, loc):
        """Save image to a location specified by loc.

        Args:
            loc: A string representing the image location.

        Returns:
            None
        """
        if self.isvalid():
            cv2.imwrite(loc, self.image)
        else:
            print('Image format invalid.')
