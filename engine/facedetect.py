"""Main file for the engine routine.

Expected to run on a AWS EC2 instance.
Exposes a FaceDetect class which expects an image as argument.
"""

import cv2

HAAR_CASC = "engine/haarcascade_frontalface_alt.xml"


class FaceDetect:
    """Takes image as argument. Provides support for face detections."""

    def __init__(self, image=None):
        """Construct with only image as attribute and convert the img to grayscale."""
        self.image = cv2.imread(image, 0)

    def isvalid(self):
        """Check if attribute has been set."""
        try:
            if self.image.all() is not None:
                return True
            else:
                return False
        except AttributeError:
            return False

    def convertgrey(self):
        """Convert image to grayscale."""
        if self.isvalid():
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            print("Image undefined.")

    def convertrgb(self):
        """Convert image from grayscale to RGB."""
        if self.isvalid():
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        else:
            print("Image undefined.")

    def getimage(self):
        """Return the image."""
        return self.image

    def setimage(self, img):
        """Set the new image."""
        self.image = img

    def detect(self, scale=1.1, neighbors=5):
        """Detect if a face is found."""
        if self.isvalid():
            haar_face_casc = cv2.CascadeClassifier(HAAR_CASC)
            faces = haar_face_casc.detectMultiScale(self.image,
                                                    scale,
                                                    neighbors)
            print('Faces found: ', len(faces))
        else:
            print('Image format invalid.')
