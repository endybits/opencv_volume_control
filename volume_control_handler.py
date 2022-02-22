import cv2
import mediapipe as mp
import numpy as np


def run():
    cap = cv2.VideoCapture(0) # Camera 0
    while cap.isOpened():
        success, img = cap.read()
        if success:
            cv2.imshow('Video Capture', img)
            if cv2.waitKey(1) & 0xFF == ord('q'): #break the video captura if the 'q'q key is pessed.
                break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()