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
        self.labelDisplayCamera = QLabel(self)
        self.labelDisplayCamera.setFixedSize(640, 480)


        # Thread in charge of updating the image
        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        # Model group
        self.group_model = QGroupBox("Selecciona el video")
        self.group_model.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        model_layout = QHBoxLayout()

        self.combobox = QComboBox()

        model_layout.addWidget(QLabel("Archivo:"), 20)
        model_layout.addWidget(self.combobox, 80)
        self.group_model.setLayout(model_layout)

        # Listing different models into model group

        sampleDirectory = os.path.join(os.getcwd(), "samples")
        for fname in os.listdir(sampleDirectory):
            if fname.endswith(".mp4") or fname.endswith(".m4v"):
                self.combobox.addItem(fname)
        
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

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.labelDisplayCamera)
        layout.addLayout(right_layout)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connections
        self.buttonStart.clicked.connect(self.start)
        self.buttonStop.clicked.connect(self.kill_thread)
        self.buttonStop.setEnabled(False)
        self.combobox.currentTextChanged.connect(self.set_file)

    @Slot()
    def set_file(self, text):
        self.th.set_file(text)

    @Slot()
    def kill_thread(self):
        print("Finishing...")
        self.buttonStop.setEnabled(False)
        self.buttonStart.setEnabled(True)
        self.th.cap.release()
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
        self.th.set_file(self.combobox.currentText())

        time.sleep(1)
        print("Archivo de entrenamiento: " + self.th.archivo)

        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.labelDisplayCamera.setPixmap(QPixmap.fromImage(image))
