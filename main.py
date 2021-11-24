import tensorflow as tf
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths, segmentMultiPerson
import cv2
from matplotlib import pyplot as plt
import numpy as np



def main():
    
    
    bodypix_model = load_model(download_model("https://storage.googleapis.com/tfjs-models/savedmodel/bodypix/mobilenet/quant2/075/model-stride16.json"))

    cap = cv2.VideoCapture("Prueba_experimental_B.mp4") 

    # loop through frame
    while cap.isOpened(): 
        ret, frame = cap.read()
        
        # BodyPix Detections
        segment = segmentMultiPerson()      
        result = bodypix_model.predict_single(frame)
        mask = result.get_mask(threshold=0.05).numpy().astype(np.uint8)
        ##mask = mask*255
        masked_image = cv2.bitwise_or(frame, frame, mask=mask)
        ##ret, labels = cv2.connectedComponents(mask)

        # Show result to user on desktop
        cv2.imshow('BodyPix', masked_image)
        
        # Break loop outcome 
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release() # Releases webcam or capture device
    cv2.destroyAllWindows() # Closes imshow frames


if __name__ == "__main__":
    main()