import cv2
import mediapipe as mp
import numpy as np


def run():

    mp_hands = mp.solutions.mediapipe.python.solutions.hands
    mp_drawing = mp.solutions.mediapipe.python.solutions.drawing_utils

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
                h, w, _ = img.shape
                img = cv2.flip(img, 1)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Mediapipe use the RGB format
                results = hands.process(img_rgb)
                
                if results.multi_hand_landmarks is not None:
                    for landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(img, landmarks, mp_hands.HAND_CONNECTIONS)
                        
                        ## Separate non-serialized coordinates of the fingertips
                        thumb_tip_x = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                        thumb_tip_y = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                        index_tip_x = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                        index_tip_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                        ## Coordinates to line between fingertips
                        thumb_tip_x = int(thumb_tip_x * w)
                        thumb_tip_y = int(thumb_tip_y * h)
                        index_tip_x = int(index_tip_x * w)
                        index_tip_y = int(index_tip_y * h)

                        # Drawing a line between thumb finger tip and index finger tip
                        cv2.line(img, (thumb_tip_x, thumb_tip_y), (index_tip_x, index_tip_y), (0, 255, 0), 2)


                img = cv2.flip(img, 1)
                cv2.imshow('Video Capture', img)
                if cv2.waitKey(1) & 0xFF == ord('q'): #break the video captura if the 'q'q key is pessed.
                    break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    run()