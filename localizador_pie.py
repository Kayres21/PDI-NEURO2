from bibliotecas import *


def localizador(pose_landmark, width, height,mp_pose):

    pos_x_dedo_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x*width
    pos_y_dedo_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y*height

    pos_x_dedo_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x*width
    pos_y_dedo_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y*height

    pos_x_talon_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_HEEL].x*width
    pos_y_talon_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_HEEL].y*height

    pos_x_talon_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_HEEL].x*width
    pos_y_talon_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_HEEL].y*height

    pos_x_tobillo_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x*width
    pos_y_tobillo_pie_izquierdo = pose_landmark.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y*height

    pos_x_tobillo_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x*width
    pos_y_tobillo_pie_derecho = pose_landmark.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y*height


    pos_x_baricentro_derecho =  (pos_x_tobillo_pie_derecho +pos_x_talon_pie_derecho+ pos_x_dedo_pie_derecho)/3
    pos_y_baricentro_derecho = (pos_y_tobillo_pie_derecho +pos_y_talon_pie_derecho+ pos_y_dedo_pie_derecho)/3

    pos_x_baricentro_izquierdo =  (pos_x_tobillo_pie_izquierdo +pos_x_talon_pie_izquierdo+ pos_x_dedo_pie_izquierdo)/3
    pos_y_baricentro_izquierdo = (pos_y_tobillo_pie_izquierdo +pos_y_talon_pie_izquierdo+ pos_y_dedo_pie_izquierdo)/3


    return [pos_x_baricentro_derecho,pos_y_baricentro_derecho], [pos_x_baricentro_izquierdo,pos_y_baricentro_izquierdo]