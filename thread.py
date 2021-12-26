import os
import sys

import cv2
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage


from bibliotecas import *
from make_video import make_video
from media_pipe import pose_detector, dibujar_esqueleto
from localizador_pie import localizador
from detector_pisadas import detector_pisadas, dibujar_pisadas
from make_pdf import make_pdf

import time
from roi import gen_roi, pisadas_roi


from pathlib import Path





class Thread(QThread):
    updateVideoFrame = Signal(QImage)
    updateROIFrame = Signal(QImage)


    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True
        self.cap_video = True
        self.cap_roi = True
        self.archivo = None
        self.nombre_archivo = None
        self.roi = None

    def set_file(self, fname):

        self.archivo =        os.path.join("samples", fname)
        self.nombre_archivo = Path(fname).stem
        self.roi =            os.path.join("samples", f"ROI_{self.nombre_archivo[-1]}.txt")



    def run(self):
        tiempo_total = 0

        archivo = self.archivo
        nombre_archivo = self.nombre_archivo
        roi = self.roi
        img_array = []

        inicio = time.time()

        self.cap_video = cv2.VideoCapture(archivo)
        self.cap_roi = cv2.VideoCapture(roi)


        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose

        '''
        ----- PARÁMETROS PARA EL MÓDULO DETECTOR DE PISADAS -----
        '''
        derecho = [0, 0] # posicion actual del pie derecho
        izquierdo = [0, 0] # posicion actual del pie izquierdo
        tol_x = 8 # toleracia para detectar pisada en eje x
        tol_y = 5 # toleracia para detectar pisada en eje y
        seq = [] #arreglo que contiene la secuencia de balizas del jugador
        
        '''
        ----- GENERAR LAS REGIONES DE INTERÉS (ACTUALMENTE Prueba_experimental_B.mp4) -----
        '''
        ret, opencv_frame = self.cap_video.read()
        src, points_and_contours = gen_roi(opencv_frame.shape[0], opencv_frame.shape[1], self.roi) 
        #cv2.imshow("ROI", src)
        
        #  # mostrar las regiones de interés obtenidas manualmente
        qt_frame = opencv_to_qt(src)
        final_frame = qt_frame.scaled(640, 480, Qt.KeepAspectRatio)
        self.updateROIFrame.emit(final_frame)
        
        
        with mp_pose.Pose(static_image_mode=False) as pose:

            while self.status:

                '''
                ----- PROCESAR VIDEO NEUROENTRENAMIENTO -----
                '''
                ret, opencv_frame = self.cap_video.read()
                if not ret:
                    break


                height, width, _ = opencv_frame.shape


                ############
                # img_array.append(opencv_frame)

                # qt_frame = opencv_to_qt(opencv_frame)
                # final_frame = qt_frame.scaled(640, 480, Qt.KeepAspectRatio)
                # self.updateVideoFrame.emit(final_frame)

                # continue
                ############



                resultados = pose_detector(pose, opencv_frame)

                baricentro_derecho, baricentro_izquierdo = localizador(resultados.pose_landmarks, width, height, mp_pose)

                '''
                ----- MÓDULO DETECTOR DE PISADAS -----
                '''
                pisada_x, pisada_y = detector_pisadas([baricentro_derecho, baricentro_izquierdo], [tol_x, tol_y], [derecho, izquierdo])

                '''
                ----- MÓDULO DETECTOR DE PISADAS EN ZONAS DE INTERÉS -----
                '''
                imagen, index = pisadas_roi(opencv_frame, pisada_x, pisada_y, baricentro_derecho, baricentro_izquierdo, points_and_contours)
                if index > -1:
                    seq.append(index)
                '''
                ----- MÓDULO DE PINTADO DE PISADAS -----
                '''
                imagen = dibujar_pisadas( [baricentro_derecho, baricentro_izquierdo], [tol_x, tol_y], [derecho, izquierdo],imagen)
                '''
                ----- MÓDULO DE PINTADO DE ESQUELETO -----
                '''
                imagen = dibujar_esqueleto(mp_drawing,mp_drawing_styles ,mp_pose, resultados, imagen)


                img_array.append(imagen)

                qt_frame = opencv_to_qt(imagen)
                final_frame = qt_frame.scaled(640, 480, Qt.KeepAspectRatio)
                self.updateVideoFrame.emit(final_frame)

                derecho = baricentro_derecho
                izquierdo = baricentro_izquierdo


        ############
        #make_video(width, height, img_array, nombre_archivo)
        #return
        ############

        # ACÁAAAAA, ARMAR LA SECUENCIA DEL JUGADOR

        #1: quitemos los 4
        preprocesado_time=time.time()
        lista_sin_cuatro = list(filter((4).__ne__, seq))
        count = 1
        temp = -1
        res = []
        for i in range(len(lista_sin_cuatro)):
            if(temp == lista_sin_cuatro[i]):
                count += 1
                if(count >= 10):
                    if(len(res) == 0):
                        res.append(lista_sin_cuatro[i])
                    else:
                        if(res[-1] != lista_sin_cuatro[i]):
                            res.append(lista_sin_cuatro[i])                    
            else:
                count = 1
            temp = lista_sin_cuatro[i]

        #Comprobación de aciertos
        seq_correcta=[8,5,6,2,3,7,1,2,5]
        contador_aciertos=0

        for i in range(len(seq_correcta)):
            if(res[i]==seq_correcta[i]):
                contador_aciertos+=1

        final = time.time()
        tiempo_total=final-inicio

        make_pdf(tiempo_total, [contador_aciertos, len(res)], nombre_archivo)
        make_video(width, height, img_array, nombre_archivo)

        print(f"Secuencia del jugador:      {res}")
        print(f"tiempo antes del procesado: {preprocesado_time-inicio}")
        print(f"Tiempo total:               {final-inicio}")




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

