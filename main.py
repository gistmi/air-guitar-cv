import cv2

"""# 1. Open the default webcam (index 0)
cap = cv2.VideoCapture(0)"""

# 1. Open the default webcam using DirectShow for fast Windows capture at 640x480
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# mediapipe is google's  ai image processing library. Helps track hands in this project
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
import math
import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100

# Makes the video very laggy by calling np.append 52,920 times
"""def play_plucked_string(freq, duration = 1.2):
    # Calculate loop buffer length N (smaller N = faster vibration = higher pitch)
    N = max(2,int(SAMPLE_RATE/freq))
    total_samples = int(SAMPLE_RATE * duration)

    # Fill the initial buffer with random noise (-1.0 to +1.0) to simulate a pick snap
    buf = np.random.uniform(-1.0, 1.0, N).astype(np.float32)
    wave = np.zeros(total_samples, dtype = np.float32)

    "Karplus-Strong loop: smooth sharp frequencies & decay volume slightly on every bounce"
    for i in range(total_samples):
        wave[i] = buf[0]
        avg = 0.996*0.5*(buf[0] + buf[1])
        buf = np.append(buf[1:], avg)
    # Play the generated sound wave asynchronously so the camera loop never freezes
    sd.play(wave, samplerate = SAMPLE_RATE)"""

# Instead Use this:

def generate_plucked_wave(freq,duration = 1.2):
    N = max(2, int(SAMPLE_RATE / freq))
    total_samples = int(SAMPLE_RATE * duration)

    buf = np.random.uniform(-1.0, 1.0, N).astype(np.float32)
    wave = np.zeros(total_samples, dtype=np.float32)

    #Ring-buffer loop: modifies buf in-place with zero np.append memory copies!
    for i in range(total_samples):
        idx = i%N
        next_idx = (idx + 1)%N
        wave[i] = buf[idx]
        buf[idx] = 0.996 * 0.5 * (buf[idx] + buf[next_idx])
    return wave

def length_to_freq(p1,p2):
    # Measure straight-line pixel length between the string's two endpoints
    length = math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    # Clamp length between 60px (shortest) and 450px (longest) so pitch stays musical
    clamped = max(60,min(450,length))

    # Map short strings -> 660 Hz (high) and long strings -> 130 Hz (low)
    ratio = (clamped - 60.0)/(450.0 - 60.0)
    freq = 660 - ratio*(660.0 - 130.0)
    return freq

def  point_to_segment_dist(px,py,p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    dx,dy = x2-x1,y2-y1
    seg_len_sq = dx*dx + dy*dy
    if(seg_len_sq == 0):
        return math.hypot(px - p1, py - y1)

    t = max(0.0, min(1.0, ((px - x1)*dx + (py - y1)*dy)/ seg_len_sq))
    closest_x = x1 + t*dx
    closest_y = y1 + t*dy
    return math.hypot(px - closest_x, py - closest_y)


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

# Tracks whether a valid string pull was started while both hands were close together
is_creating_string = False
active_string = None  # Holds (p1, p2) of the string currently being stretched
strings = []          # Permanent list of locked-in strings: [(p1, p2), ...]

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

    #not needed now!
    """# Always redraw all previously locked-in strings in Electric Cyan
    for s_p1, s_p2 in strings:
        cv2.line(frame, s_p1, s_p2, (255, 255, 0), 3)"""

    # Store (x, y) coordinates of each hand that is currently pinching in this frame
    pinch_points = []
        
    # Holds (x, y) of unpinched Index Fingertips (Landmark 8)
    pluck_tips = []

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

            # Grab Thumb Tip (4) and Index Fingertip (8) and convert normalized (0..1) coords to screen pixels
            thumb_tip = hand_landmarks[4]
            index_tip = hand_landmarks[8]
            x1,y1 = int(thumb_tip.x * w),int(thumb_tip.y * h)
            x2,y2 = int(index_tip.x * w), int(index_tip.y * h)
            
            #cv2.line(frame,(x1,y1), (x2,y2),(0,255,255), 3)

            # Calculate straight-line pixel distance between thumb and index tip
            pinch_dist =  math.hypot(x2-x1,y2-y1)

            # Midpoint between thumb and index tip (where the string endpoint will attach)
            pinch_x, pinch_y = (x1 + x2) // 2, (y1 + y2) // 2

            # If fingertips are closer than 40 pixels, draw a bright yellow indicator dot at the pinch point
            if pinch_dist < 40:
                cv2.circle(frame, (pinch_x,pinch_y), 10, (0,255,255), -1)
                pinch_points.append((pinch_x, pinch_y))
            else:
                # Open hand -> Index Fingertip (x2,y2) can pluck strings
                pluck_tips.append((x2,y2))

    now = time.time()
    for s in strings:
        cv2.line(frame,s["p1"], s["p2"], (255,255,0), 3)

        for tip_x, tip_y in pluck_tips:
            if point_to_segment_dist(tip_x,tip_y, s["p1"], s["p2"]) < 15:
                if now - s["last_pluck"] > 0.25:
                    s["last_pluck"] = now
                    #play_plucked_string(s["freq"])
                    sd.play(s["wave"], samplerate= SAMPLE_RATE)

    # When BOTH hands are pinching simultaneously, draw a live string stretching between them
    if len(pinch_points) == 2:
        p1,p2 = pinch_points[0], pinch_points[1]

        if not is_creating_string:
            hands_dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            if hands_dist < 80:
                is_creating_string = True

        if is_creating_string:
            active_string = (p1, p2)
            cv2.line(frame,p1, p2,(255,0,255), 3)

    else:
        if is_creating_string and active_string is not None:
            p1,p2 = active_string
            freq = length_to_freq(p1, p2)
            strings.append({
                "p1": p1,
                "p2": p2,
                "freq": length_to_freq(p1,p2),
                "wave": generate_plucked_wave(freq),
                "last_pluck": 0.0
            })
        # Reset state as soon as either hand releases its pinch
        is_creating_string = False
        active_string = None

    # Show the frame in a window
    cv2.imshow("Webcam Test", frame)

    # Wait 1ms; if you press 'q', break out of the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'): 
        strings.clear()

# 3. Clean up when done
cap.release()
cv2.destroyAllWindows()