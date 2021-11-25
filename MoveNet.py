
from funciones import *

def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 4, (0,255,0), -1) 

def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 2)


def main():
    interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_thunder_3.tflite')
    interpreter.allocate_tensors()

    EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}
    

    cap = cv2.VideoCapture("Prueba_experimental_B.mp4")
    while cap.isOpened(): 
        ret, frame = cap.read()

        # Reshape image
        img = frame.copy()
        input_image = tf.expand_dims(img, axis=0)
        input_image = tf.image.resize_with_pad(input_image, 256, 256)

        # Setup input and output
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Make predictions 
        interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
        interpreter.invoke() #Hace la prediccion de moviemiento
        keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
        
        display_image = tf.expand_dims(img, axis=0)
        display_image = tf.cast(tf.image.resize_with_pad(
            display_image, 300, 300), dtype=tf.int32)
        output_overlay = draw_prediction_on_image(
            np.squeeze(display_image.numpy(), axis=0), keypoints_with_scores)

        
        cv2.imshow("Prueba", output_overlay)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    

    cap.release() # Releases webcam or capture device
    cv2.destroyAllWindows() # Closes imshow frames


if __name__ == "__main__":
    main()