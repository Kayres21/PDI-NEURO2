from bibliotecas import *

def make_video(width, height, img_array, nombre_archivo):
    size = (width,height)
    out = cv2.VideoWriter('Resultado_' + nombre_archivo ,cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()