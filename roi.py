from bibliotecas import *

def gen_roi(h, w, mode = 1):
    '''
        mode = 0, ROI para Prueba Experimental A
        mode = 1, ROI para Prueba Experimental B
    '''
    src = np.zeros((h, w), dtype = np.uint8)
    points = np.array([[350, 165], [265, 165], [260, 205], [355, 205]], np.int32).reshape((-1, 1, 2))
    src = cv2.polylines(src, [points], True, ( 255 ), 2)
    contours, _ = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return src, contours, points

def pisadas_roi(imagen, pisada_x, pisada_y, contours, baricentro_derecho, baricentro_izquierdo, points):
    if pisada_x or pisada_y:
        der =  cv2.pointPolygonTest(contours[0], (baricentro_derecho[0], baricentro_derecho[1]), False)
        izq =  cv2.pointPolygonTest(contours[0], (baricentro_izquierdo[0], baricentro_izquierdo[1]), False)
        if (der >= 0) or (izq >= 0):
                imagen = cv2.fillPoly(imagen, [points], (0, 255, 0))
    return imagen
    