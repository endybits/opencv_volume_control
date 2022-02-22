import cv2
import mediapipe as mp
import numpy as np


def run():

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    ## Mediapipe hand tracker configuration
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1, # To our use case the performance is better if we use maximum 1 hand.
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        cap = cv2.VideoCapture(0) # Camera 0
        while cap.isOpened():
            success, img = cap.read()
            if success:
                img = cv2.flip(img, 1)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Mediapipe use the RGB format
                results = hands.process(img_rgb)
                print(results.multi_hand_landmarks)

                img = cv2.flip(img, 1)
                cv2.imshow('Video Capture', img)
                if cv2.waitKey(1) & 0xFF == ord('q'): #break the video captura if the 'q'q key is pessed.
                    break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    run()