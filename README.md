# OpenCV Volume Control

The aim of this project is to show how develop a volume control using hand landmarks detection with OpenCV and Mediapipe Python libraries.

But before starting with the volume control let me show you the 21th hand landmarks that we can identify using Mediapipe. 

![](https://google.github.io/mediapipe/images/mobile/hand_landmarks.png)

In our specific example, we'll only use the `4.THUMB_TIP` and `8.INDEX_TIP` hand landmarks.

**here i must put an image (the connection between 4 and 8 landmarks)

The main trick of the exercise consists of extract the non-serialized coordinates to each `4.THUMB_TIP` and `8.INDEX_TIP` hand landmarks, then convert them to coordinates in pixels.

The next logic step is calculate the distance between our two points. Do you remember the Pythagorean Theorem?

<!-- &Delta;X  = abs(x_thumb_tip - x_index_tip) -->
![](https://latex.codecogs.com/svg.image?%5CDelta%20x%20=%20%5Cleft%7C%20thumbTip_%7Bx%7D%20-%20indexTip_%7Bx%7D%20%5Cright%7C%20)

<!-- &Delta;y = abs(y_thumb_tip - y_index_tip) -->
![](https://latex.codecogs.com/svg.image?%5CDelta%20y%20=%20%5Cleft%7C%20thumbTip_%7By%7D%20-%20indexTip_%7By%7D%20%5Cright%7C%20)

![](https://latex.codecogs.com/svg.image?hypotenuse&space;=&space;\sqrt{\Delta&space;x^{2}&space;&plus;&space;\Delta&space;y^{2}})

The hypotenuse value is the distance.

Finally you should use a function to set the volume, making an interpolation between the volume range of your pc and a defined range of min and max distance in pixels to the fingertips.

This process is repetitive. Which means it will repeat while the OpenCV's VideoCapture function is running and Mediapipe detect hands.
