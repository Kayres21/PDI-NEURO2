from bibliotecas import *
from make_video import make_video

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

archivo = "Prueba_experimental_A.m4v"

cap = cv2.VideoCapture(archivo)
img_array = []

## static_image_mode seteado en Falso para caso de video stream, videos o una imagen, 
## si es True es para ideal para procesar un lote de imágenes estáticas, posiblemente no relacionadas.  
with mp_pose.Pose(
    static_image_mode=False) as pose:
    ##While para leer el video
    while True:
        ret, frame = cap.read()
        if ret == False:
            break


        #Ancho y largo de la imagen y cambio de BGR a RGB, se hace no writeable para aumentar rendimiento.
        height, width, _ = frame.shape
        frame.flags.writeable = False
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        ##Se procesa la imagen con el modelo entregando las landmarks
        results = pose.process(frame_rgb)

        img1 = cv2.imread("Fondo_Negro.jpg")
        
        if results.pose_landmarks is not None:
           ## print(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x*width , results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y*height )
            mp_drawing.draw_landmarks(
                img1, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        cv2.imshow("Esqueleto", img1)
        cv2.imshow("Frame", frame)
        
        img_array.append(frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break


cap.release()
cv2.destroyAllWindows()

make_video(width,height, img_array,archivo )

