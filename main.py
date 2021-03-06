from bibliotecas import *
from make_video import make_video
from media_pipe import pose_detector, dibujar_esqueleto
from localizador_pie import localizador
from detector_pisadas import detector_pisadas, dibujar_pisadas
from make_pdf import make_pdf

import time
from roi import gen_roi, pisadas_roi


from pathlib import Path

'''
----- DETECTOR DE EVENTOS PARA GENERAR MANUALMENTE EL ROI -----
'''

ROI_B, count = [], 0

def mouse_callback(event, x, y, flags, params):
    if event == 2:
        global ROI_B, count
        count += 1 
        if (count % 4 == 0):
            ROI_B.append([x, y])
            f = open('TEST.txt', 'a').write(str(ROI_B) + '\n') # Cambiar aquí para calibrar los ROI
            ROI_B = []
            f.close()
        else:
            ROI_B.append([x, y])
        print(ROI_B, count)

def main():
    mode = 1 # 0 para prueba A, 1 para prueba B
    tiempo_total=0
    if mode:
        archivo = "samples/Prueba_experimental_B.mp4"
        roi = "samples/ROI_B.txt"
        nombre_archivo = "Prueba_experimental_B"
    else:
        archivo = "samples/Prueba_experimental_A.m4v"
        roi = "samples/ROI_A.txt"
        nombre_archivo = "Prueba_experimental_A"

    inicio = time.time()
    cap = cv2.VideoCapture(archivo)
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
    ----- GENERAR LAS REGIONES DE INTERÉS -----
    '''
    ret, frame = cap.read()
    src, points_and_contours = gen_roi(frame.shape[0], frame.shape[1], roi) # se usa el frame obtenido en (2) para no iterar en el While
    cv2.imshow("ROI", src) # mostrar las regiones de interés obtenidas manualmente

    with mp_pose.Pose(static_image_mode=False) as pose:

        img_array = []
        while True:
            ret, frame = cap.read()
            if ret == False:
                break

            height, width, _ = frame.shape
            resultados =  pose_detector(pose ,frame)
            
            
            baricentro_derecho, baricentro_izquierdo = localizador(resultados.pose_landmarks, width, height, mp_pose)
            
            '''
            ----- MÓDULO DETECTOR DE PISADAS -----
            '''
            pisada_x, pisada_y = detector_pisadas([baricentro_derecho, baricentro_izquierdo], [tol_x, tol_y], [derecho, izquierdo])

            '''
            ----- MÓDULO DETECTOR DE PISADAS EN ZONAS DE INTERÉS -----
            '''
            imagen, index = pisadas_roi(frame, pisada_x, pisada_y, baricentro_derecho, baricentro_izquierdo, points_and_contours)
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
            
            
            cv2.imshow("Imagen", imagen)
            '''
            ----- GENERAR ROI MANUALMENTE -----
            '''
            # cv2.setMouseCallback("Imagen", mouse_callback)
            derecho = baricentro_derecho
            izquierdo = baricentro_izquierdo
            
            img_array.append(imagen)

            k = cv2.waitKey(1)
            

            if k & 0xFF == 27:
                break
            
        cap.release()
        cv2.destroyAllWindows()
    
    # Armar la secuencia del jugador
    preprocesado_time = time.time()
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
    #Comprobacion de aciertos
    seq_correcta = [8, 5, 6, 2, 3, 7, 1, 2, 5]
    contador_aciertos = 0
    for i in range(len(seq_correcta)):
        if(res[i] == seq_correcta[i]):
            contador_aciertos += 1

    final = time.time()
    tiempo_total = final - inicio

    make_pdf(tiempo_total, [contador_aciertos, len(res)], nombre_archivo)
    make_video(width, height, img_array, archivo)

    # print(f"Secuencia del jugador:      {res}")
    # print(f"tiempo antes del procesado: {preprocesado_time-inicio}")
    # print(f"Tiempo total:               {final-inicio}")









import sys
from PySide6.QtWidgets import QApplication


"""This example uses the video from a  webcam to apply pattern
detection from the OpenCV module. e.g.: face, eyes, body, etc."""


from window import Window
from pathlib import Path


if __name__ == "__main__":

    # Es necesario que exista un directorio "samples" y "results"
    # para que esto funcione.
    subdirs = {a for a in Path(".").iterdir()}

    if Path("samples") not in subdirs:
        print("No existe directorio samples, abortando")
        sys.exit()


    if Path("results") not in subdirs:
        print("No existe directorio results, abortando")
        sys.exit()


    GUI = True

    if (GUI):
        app = QApplication()
        w = Window()
        w.show()
        sys.exit(app.exec())

    else:
        main()
        
    