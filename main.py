from bibliotecas import *
from make_video import make_video
from media_pipe import pose_detector


def main():

    archivo = "Prueba_experimental_B.mp4"
    cap = cv2.VideoCapture(archivo)
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(static_image_mode=
        False) as pose:

        img_array = []
        while True:
            ret, frame = cap.read()
            if ret == False:
                break

            height, width, _ = frame.shape

            resultados, imagen =  pose_detector(mp_drawing,mp_drawing_styles ,mp_pose,pose ,frame)
            cv2.imshow("Imagen", imagen)
            

            img_array.append(imagen)
            if cv2.waitKey(1) & 0xFF == 27:
                break   
            
            


        make_video(width,height, img_array,archivo )
        cap.release()
        cv2.destroyAllWindows()
    



if __name__ == "__main__":
    main()