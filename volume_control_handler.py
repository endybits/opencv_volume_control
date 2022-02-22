import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def vol_control(distance, min_vol, max_vol, volume):

    intepolation_vol_coord = int(np.interp(distance, [25, 180], [min_vol, max_vol]))
    volume.SetMasterVolumeLevel(intepolation_vol_coord, None)
    interpolation_volperc_coord = int(np.interp(distance, [25, 180], [0, 100]))
    interpolation_vol_bar = int(np.interp(interpolation_volperc_coord, [0, 100], [180, 420]))
    return interpolation_volperc_coord, interpolation_vol_bar

def run():

    ## Config Volume    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    vol_range = volume.GetVolumeRange()
    min_vol, max_vol = vol_range[0], vol_range[1]

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

                        ## Calculate hypotenuse (distance of drawn line)
                        delta_x = abs(thumb_tip_x - index_tip_x)
                        delta_y = abs(thumb_tip_y - index_tip_y)
                        hypot = int(np.sqrt(delta_x ** 2 + delta_y ** 2))
                        print(hypot)
                        
                        ## Middle circle
                        min_x = np.min([thumb_tip_x, index_tip_x])
                        min_y = np.min([thumb_tip_y, index_tip_y])
                        middle_x = min_x + delta_x // 2
                        middle_y = min_y + delta_y // 2
                        cv2.circle(img, (middle_x, middle_y), 10, (0, 255, 0), -1)

                        level, interpolation_vol_bar = vol_control(hypot, min_vol, max_vol, volume)
                        
                        
                        level_text = f'VOLUME: {level}%'
                        
                        #img = cv2.flip(img, 1)
                        cv2.putText(img, level_text, ((w - 210), (h - 20)), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)

                        cv2.rectangle(img, (180, h-50), (420, h-20), (0, 0, 0), 2)
                        cv2.rectangle(img, (180, h-50), (interpolation_vol_bar, h-20), (0, 0, 0), -1)

                cv2.imshow('Video Capture', img)
                if cv2.waitKey(1) & 0xFF == ord('q'): #break the video captura if the 'q'q key is pessed.
                    break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    run()