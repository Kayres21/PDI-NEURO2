from bibliotecas import *
import ast
def gen_roi(h, w, filename):
    src = np.zeros((h, w), dtype = np.uint8)
    lines = open(filename, 'r').readlines()
    ROI = [ast.literal_eval(line[:-1]) for line in lines]
    points_and_contours = []
    for roi in ROI:
        temp = np.zeros((h, w), dtype = np.uint8)
        p = np.array(roi, np.int32).reshape((-1, 1, 2))
        temp = cv2.polylines(temp, [p], True, ( 255 ), 2)
        cont, _ = cv2.findContours(temp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        src = cv2.bitwise_or(src, temp)

        points_and_contours.append((p, cont[0]))
    return src, points_and_contours

def pisadas_roi(imagen, pisada_x, pisada_y, baricentro_derecho, baricentro_izquierdo, points_and_contours):
    '''
        Si ocurrió una pisada, se busca dónde se pisó y se pinta.
    '''
    index = -1
    if pisada_x or pisada_y:
        for i in range(len(points_and_contours)):
            der = cv2.pointPolygonTest(points_and_contours[i][1], (baricentro_derecho[0], baricentro_derecho[1]), False)
            izq = cv2.pointPolygonTest(points_and_contours[i][1], (baricentro_izquierdo[0], baricentro_izquierdo[1]), False)
            if (der >= 0) or (izq >= 0):
                    imagen = cv2.fillPoly(imagen, [points_and_contours[i][0]], (0, 255, 0))
                    index = i
                    # print("baliza: ", i)
    return imagen, index
    