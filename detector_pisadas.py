from bibliotecas import *

def detector_pisadas( baricentros, tols, state):
    '''
        imagen: frame a ingresar
        baricentros: lista de baricentros
        tols: lista de tolerancias
        state: posicion actual de ambos pies
    '''

    baricentro_derecho = baricentros[0]
    baricentro_izquierdo = baricentros[1]
    tol_x = tols[0]
    tol_y = tols[1]
    derecho = state[0]
    izquierdo = state[1]
    
    pisada_x = False
    pisada_y = False

    # Pisadas del pie derecho (eje x)
    if (np.absolute(baricentro_derecho[0] - derecho[0]) <= tol_x) and (np.absolute(baricentro_derecho[1] - derecho[1]) <= tol_y):
        # Se detecta una pisada en el pie derecho
        pisada_x = True
    if (np.absolute(baricentro_izquierdo[0] - izquierdo[0]) <= tol_x) and (np.absolute(baricentro_izquierdo[1] - izquierdo[1]) <= tol_y):
        # Se detecta una pisada en el pie izquierdo
        pisada_y = True
    return  pisada_x, pisada_y


def dibujar_pisadas(baricentros , tols,state,imagen):
    baricentro_derecho = baricentros[0]
    baricentro_izquierdo = baricentros[1]
    tol_x = tols[0]
    tol_y = tols[1]
    derecho = state[0]
    izquierdo = state[1]
    frame_pintado= imagen
    
    
    if (np.absolute(baricentro_derecho[0] - derecho[0]) <= tol_x) and (np.absolute(baricentro_derecho[1] - derecho[1]) <= tol_y):
        # Se detecta una pisada en el pie derecho
        cv2.circle(frame_pintado, (int(baricentro_derecho[0]), int(baricentro_derecho[1])), 10, (255,0,0), 2)
        
    if (np.absolute(baricentro_izquierdo[0] - izquierdo[0]) <= tol_x) and (np.absolute(baricentro_izquierdo[1] - izquierdo[1]) <= tol_y):
        # Se detecta una pisada en el pie izquierdo
        cv2.circle(frame_pintado, (int(baricentro_izquierdo[0]), int(baricentro_izquierdo[1])), 10, (0,0,255), 2)
    
    return frame_pintado