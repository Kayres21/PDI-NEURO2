import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture("Prueba_experimental_A.m4v")
with mp_pose.Pose(
    static_image_mode=False) as pose:
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(frame_rgb)


        img1 = cv2.imread("Fondo_Negro.jpg")
        
        if results.pose_landmarks is not None:
            print(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y*height)
            mp_drawing.draw_landmarks(
                img1, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(128, 0, 250), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(128, 0, 250), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))
        cv2.imshow("Esqueleto", img1)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()