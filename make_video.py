from bibliotecas import *
import os

def make_video(width, height, img_array, nombre_archivo):

    filepath = os.path.join("results", f'Resultado_{nombre_archivo}.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    size = (width, height)

    out = cv2.VideoWriter(
        filepath,
        fourcc,
        fps,
        size
    )

    #filename = os.path.join("results", f'Resultado_{nombre_archivo}')
    #out = cv2.VideoWriter(filename ,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    
    for img in img_array:
        out.write(img)

    out.release()