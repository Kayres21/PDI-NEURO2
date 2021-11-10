import tensorflow as tf
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths
import cv2
from matplotlib import pyplot as plt
import numpy as np



def main():
    
    
    bodypix_model = load_model(download_model(BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16))

    cap = cv2.VideoCapture("Prueba_experimental_A.m4v") 

    # loop through frame
    while cap.isOpened(): 
        ret, frame = cap.read()
        
        # BodyPix Detections
        
        result = bodypix_model.predict_single(frame)
        mask = result.get_mask(threshold=0.09).numpy().astype(np.uint8)
        masked_image = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Show result to user on desktop
        cv2.imshow('BodyPix', masked_image)
        
        # Break loop outcome 
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release() # Releases webcam or capture device
    cv2.destroyAllWindows() # Closes imshow frames


if __name__ == "__main__":
    main()