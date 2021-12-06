from bibliotecas import *


def pose_detector(mp_drawing, mp_drawing_styles,mp_pose, pose,frame_original):
    
    frame = frame_original
    height, width, _ = frame.shape
    frame.flags.writeable = False
    frame = cv2.flip(frame,1)
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

    return results.pose_landmarks, frame




