import cv2

# 1. Open the default webcam (index 0)
cap = cv2.VideoCapture(0)

# mediapipe is google's  ai image processing library. Helps trcak kands in this project
import mediapipe as mp

# This worked in older version of mediapipe
"""
#Inside MediaPipe, Google organizes its AI models under solutions (hands, face, pose).
mp_hands = mp.solutions.hands

#MediaPipe's built-in drawing utilities—a helper tool that knows how to connect the 21 hand dots with skeleton lines.
mp_draw = mp.solutions.drawing_utils

#mp_hands.Hands(...): Creates our actual AI hand detector (hands)
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence = 0.7)
"""

# This is what works in new version

from mediapipe.tasks  import python
from mediapipe.tasks.python import vision

import time

#2. Configure where the AI brain lives and set tracking values

#Tell MediaPipe where the AI brain file lives on hard drive
base_options = python.BaseOptions(model_asset_path = "hand_landmarker.task")

#Set the rules for detector
options = vision.HandLandmarkerOptions(
    base_options = base_options,

    # Tell the AI it is watching a continuous video stream 
    running_mode = vision.RunningMode.VIDEO,
    num_hands = 2,
    min_hand_detection_confidence = 0.7,
)

#3. Wake up the modern hand detector
detector = vision.HandLandmarker.create_from_options(options)

# 4. Loop forever while the camera stays open
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Could not read frame from webcam.")
        break

    # Flip the photo horizontally (1 = mirror mode, 0 = upside down)
    frame = cv2.flip(frame, 1)

    # 5. Convert OpenCV's BGR frame to RGB and wrap it in mp.Image
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format= mp.ImageFormat.SRGB, data = rgb_frame)

    # 6. Ask the detector to find hands at the current millisecond timestamp

    # Generate a strictly increasing millisecond clock timestamp so VIDEO mode tracks motion across frames
    timestamp_ms = int(time.time() * 1000)
    # Run MediaPipe's neural network on the wrapped RGB frame at this timestamp to find hand joints
    detection_result = detector.detect_for_video(mp_image, timestamp_ms)

    
    # Check if MediaPipe detected at least one hand in the current frame
    if detection_result.hand_landmarks:
        # Unpack pixel height (h) and width (w) to convert normalized coordinates into screen pixels
        h, w, _ = frame.shape
        # Loop through each detected hand (up to 2 hands)
        for hand_landmarks in detection_result.hand_landmarks:
            # Loop through all 21 joint landmarks on the current hand
            for landmark in hand_landmarks:
                # Scale normalized (0.0 to 1.0) coordinates to exact pixel positions on the frame
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                # Draw a solid green dot (radius 5px, BGR color) at each joint
                cv2.circle(frame, (cx,cy), 5, (0,255,0), -1)


    # Show the frame in a window
    cv2.imshow("Webcam Test", frame)

    # Wait 1ms; if you press 'q', break out of the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 3. Clean up when done
cap.release()
cv2.destroyAllWindows()
