from bibliotecas import *


def pose_detector(pose,frame_original):
    
    frame = frame_original
    height, width, _ = frame.shape
    frame.flags.writeable = False
    # frame = cv2.flip(frame,1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    ##Se procesa la imagen con el modelo entregando las landmarks
    results = pose.process(frame_rgb)
    
    

    return results

def dibujar_esqueleto(mp_drawing, mp_drawing_styles,mp_pose, results, frame):
    
    frame_pintado = frame
    
    if results.pose_landmarks is not None:
        # mp_drawing.draw_landmarks(
        #     img1, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        mp_drawing.draw_landmarks(
            frame_pintado, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        return frame_pintado


