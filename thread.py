import os
import sys

import cv2
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage


from bibliotecas import *
from make_video import make_video
from media_pipe import pose_detector


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose



class Thread(QThread):
    updateFrame = Signal(QImage)


    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.archivo = None
        self.status = True
        self.cap = True
        self.img_array = []
        self.height = None
        self.width = None

    def set_file(self, fname):

        sample_directory = os.path.join(os.getcwd(), "samples")
        sample_file  = os.path.join(sample_directory, fname)

        sample_file  = os.path.join("samples", fname)
        self.archivo = sample_file



    def run(self):
        archivo = self.archivo
        self.cap = cv2.VideoCapture(archivo)
        
        with mp_pose.Pose(static_image_mode=False) as pose:

            while self.status:
                ret, opencv_frame = self.cap.read()
                if not ret:
                    continue

                opencv_frame = self.processOpencvFrame(opencv_frame, pose)

                qt_frame = opencv_to_qt(opencv_frame)

                final_frame = qt_frame.scaled(640, 480, Qt.KeepAspectRatio)
                self.updateFrame.emit(final_frame)

            self.cap.release()
            cv2.destroyAllWindows()


        sys.exit(-1)



    # Procesa el video dentro del dominio de OpenCV.
    def processOpencvFrame(self, opencv_frame, pose):

        self.height, self.width, _ = opencv_frame.shape

        resultados, imagen =  pose_detector(mp_drawing,mp_drawing_styles ,mp_pose,pose ,opencv_frame)

        self.img_array.append(imagen)

        return imagen

        cascade = cv2.CascadeClassifier(self.archivo)

        detections = cascade.detectMultiScale(
            cv2.cvtColor(opencv_frame, cv2.COLOR_BGR2GRAY), # Gray image
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Drawing green rectangle around the pattern
        for (x, y, w, h) in detections:
            cv2.rectangle(
                img=opencv_frame,
                pt1=(x, y),
                pt2=(x + w, y + h),
                color=(0, 255, 0),
                thickness=2
            )   

        return opencv_frame




# Transforma un frame de OpenCV a QImage.
def opencv_to_qt(opencv_frame):

    # Reading the image in RGB to display it
    color_frame = cv2.cvtColor(opencv_frame, cv2.COLOR_BGR2RGB)

    # Creating and scaling QImage
    h, w, ch = color_frame.shape

    return QImage(
        color_frame.data,
        w,
        h,
        ch * w,
        QImage.Format_RGB888
    )

