"""Class supporting the client video capture options."""

import cv2
import os
import numpy as np

class Camera:
    """Takes optional argument, the number of frames captured, and the savepath."""

    def __init__(self, frames=200, path='./'):
        """Two attributes, frames and path."""
        self.frames = frames
        self.path = path

    def getframes(self):
        """Return the frame number."""
        return self.frames

    def getpath(self):
        """Return the path loc."""
        return self.path

    def setframes(self, frames):
        """Set the frame number."""
        self.frames = frames

    def setpath(self, path):
        """Set the path loc."""
        self.path = path
    
    def capture(self):
        """Main capture function."""
        cap = cv2.VideoCapture(0)
        count = 0
        while count < self.frames:
            _, frm = cap.read()
            cv2.imwrite(os.path.join(self.path, "frame%d.jpg" % count), frm)
            count = count + 1
        cap.release()
