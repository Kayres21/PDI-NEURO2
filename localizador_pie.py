from bibliotecas import *


def localizador(pose_landmark, width, height,mp_pose):

    pos_x_dedo_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x*width
    pos_y_dedo_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y*height

    pos_x_dedo_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x*width
    pos_y_dedo_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y*height

    pos_x_tobillo_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_HEEL_INDEX].x*width
    pos_y_tobillo_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_HEEL_INDEX].y*height

    pos_x_tobillo_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_HEEL_INDEX].x*width
    pos_y_tobillo_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_HEEL_INDEX].y*height

