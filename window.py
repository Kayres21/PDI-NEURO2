import os
import time

import cv2
from PySide6.QtCore import Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)

from thread import Thread


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Title and dimensions
        self.setWindowTitle("Prototipo Neuroentrenamiento")
        self.setGeometry(0, 0, 800, 500)


        # Create a label for the display camera
        self.labelDisplayVideo = QLabel(self)
        # self.labelDisplayVideo.setText("Video")
        self.labelDisplayVideo.setFixedSize(640, 480)

        # Descomentar esto para incluir el ROI
        '''
        self.labelDisplayROI = QLabel(self)
        self.labelDisplayROI.setText("ROI")
        self.labelDisplayROI.setFixedSize(640, 480)
        '''

        # Thread in charge of updating the image
        self.th = Thread(self)
        self.th.finished.connect(self.close)
        #self.th.updateVideoFrame.connect(self.setImage)

        self.th.updateVideoFrame.connect(self.setVideoImage)
        # Descomentar esto para incluir el ROI
        # self.th.updateROIFrame.connect(self.setROIImage) 


        # Listing all the sample videos into availableVideos
        self.availableVideos = QComboBox()
        sampleDirectory = os.path.join(os.getcwd(), "samples")
        for fname in os.listdir(sampleDirectory):
            if fname.endswith(".mp4") or fname.endswith(".m4v"):
                self.availableVideos.addItem(fname)

        # Model group
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Archivo:"), 20)
        model_layout.addWidget(self.availableVideos, 80)


        self.group_model = QGroupBox("Selecciona el video")
        self.group_model.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.group_model.setLayout(model_layout)


        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        self.buttonStart = QPushButton("Iniciar")
        self.buttonStart.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.buttonStart)

        self.buttonStop = QPushButton("Cerrar")
        self.buttonStop.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.buttonStop)

        right_layout = QHBoxLayout()
        right_layout.addWidget(self.group_model, 1)
        right_layout.addLayout(buttons_layout, 1)


        # Video and ROI layout
        video_roi_layout = QHBoxLayout()
        # Descomentar esto para incluir el ROI
        # video_roi_layout.addWidget(self.labelDisplayROI)
        video_roi_layout.addWidget(self.labelDisplayVideo)


        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(video_roi_layout)
        layout.addLayout(right_layout)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connections
        self.buttonStart.clicked.connect(self.start)
        self.buttonStop.clicked.connect(self.kill_thread)
        self.buttonStop.setEnabled(False)
        self.availableVideos.currentTextChanged.connect(self.set_file)

    @Slot()
    def set_file(self, text):
        self.th.set_file(text)

    @Slot()
    def kill_thread(self):
        print("Finishing...")
        self.buttonStop.setEnabled(False)
        self.buttonStart.setEnabled(True)
        self.th.cap_roi.release()
        self.th.cap_video.release()
        cv2.destroyAllWindows()
        self.status = False
        self.th.terminate()
        # Give time for the thread to finish
        time.sleep(1)

    @Slot()
    def start(self):
        print("Starting...")
        self.buttonStop.setEnabled(True)
        self.buttonStart.setEnabled(False)
        self.th.set_file(self.availableVideos.currentText())

        time.sleep(1)
        print(f"{self.th.archivo        = }")
        print(f"{self.th.nombre_archivo = }")
        print(f"{self.th.roi            = }")

        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.labelDisplayVideo.setPixmap(QPixmap.fromImage(image))

    @Slot(QImage)
    def setVideoImage(self, image):
        self.labelDisplayVideo.setPixmap(QPixmap.fromImage(image))
    # Descomentar esto para incluir el ROI
    '''
    @Slot(QImage)
    def setROIImage(self, image):
        self.labelDisplayROI.setPixmap(QPixmap.fromImage(image))
    '''

