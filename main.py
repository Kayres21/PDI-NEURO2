from os import times
from bibliotecas import *
from make_video import make_video
from media_pipe import pose_detector, dibujar_esqueleto
from localizador_pie import localizador
from detector_pisadas import detector_pisadas, dibujar_pisadas

import time
from roi import gen_roi, pisadas_roi

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
            f = open('TEST.txt', 'a').write(str(ROI_B) + '\n')
            ROI_B = []
            f.close()
        else:
            ROI_B.append([x, y])
        print(ROI_B, count)

def main():
    mode = 0 # 0 para prueba A, 1 para prueba B
    if mode:
        archivo = "Prueba_experimental_B.mp4"
        roi = "ROI_B.txt"
    else:
        archivo = "Prueba_experimental_A.m4v"
        roi = "ROI_A.txt"
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

    '''
    ----- GENERAR LAS REGIONES DE INTERÉS (ACTUALMENTE Prueba_experimental_B.mp4) -----
    '''
    ret, frame = cap.read()
    src, points_and_contours = gen_roi(frame.shape[0], frame.shape[1], roi) # se usa el frame obtenido en (2) para no iterar en el While
    cv2.imshow("ROI", src) # mostrar las regiones de interés obtenidas manualmente

    with mp_pose.Pose(static_image_mode=
        False) as pose:

        img_array = []
        while True:
            ret, frame = cap.read()
            if ret == False:
                break

            height, width, _ = frame.shape
            resultados =  pose_detector(pose ,frame)
            # cv2.imshow("Imagen", imagen)
            
            baricentro_derecho, baricentro_izquierdo = localizador(resultados.pose_landmarks, width, height, mp_pose)
            
            '''
            ----- MÓDULO DETECTOR DE PISADAS -----
            '''
            pisada_x, pisada_y = detector_pisadas([baricentro_derecho, baricentro_izquierdo], [tol_x, tol_y], [derecho, izquierdo])

            '''
            ----- MÓDULO DETECTOR DE PISADAS EN ZONAS DE INTERÉS -----
            '''
            imagen = pisadas_roi(frame, pisada_x, pisada_y, baricentro_derecho, baricentro_izquierdo, points_and_contours)
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
            ----- (1) GENERAR ROI MANUALMENTE (se usó para generar ROI_B.txt) -----
            '''
            ##cv2.setMouseCallback("Imagen", mouse_callback)

            derecho = baricentro_derecho
            izquierdo = baricentro_izquierdo
            # print("---------------------------")
            # print(f" pos x {baricentro_derecho[0]} y: {baricentro_derecho[1]}")
            # print(f"El 1% del ancho es {width/100} y el 1% del alto de {height/100}")
            # print("---------------------------")

            img_array.append(imagen)

            k = cv2.waitKey(1)

            if k & 0xFF == 27:
                break


        make_video(width,height, img_array,archivo )
        cap.release()
        cv2.destroyAllWindows()
    final = time.time()
    print(final-inicio)



if __name__ == "__main__":
    main()
    
    