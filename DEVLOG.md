# Engineering DevLog - Air String Synthesizer

## Session 1: Enviornment Setup & Native Webcam Loop
- **what i buit:** set up a python virtual enviornment('venv'), installed OpenCV and MediaPipe, and wrote a mirroed webcam loop in 'main.py'.
- **why i did it this way:** moved the repo from WSL ('~/') to the windows drive ('C:\Users\lenovo\air-guitar-cv') so OpenCV gets native hardware webcam access without USB bridging ('usbipd') or missing Linux X11 GUI libraries. Used 'cv2.flip(frame,1)' so the camera acts like mirror.

- **bugs hit & fixed:**
    - Poweshell blocked 'Activate.ps1' -> fixed once with 'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser'.
    - Clicking the window 'X' didn't close OpenCV because the 'while' loop immediatelyredrew it -> press 'q' instead.
- **Terms learned:** 'venv' (isolated package sandbox), 'frame' (single still photo in a 30 FPS video loop), 'cap.read()' (grabs 'success' + 'frame'), 'cv2.waitKey(1)' (refreshes window & checks keyboard input).

## Session 2: Modern MediaPipe Tasks API & 21-Dot Hand Tracking
- **What I built:**
  - Pivoted the project toward a dynamic **Pinch-to-Create-Strings Air Synthesizer** (where pinching two endpoints spawns strings of adjustable length and pitch).
  - Upgraded `main.py` to detect up to 2 hands in real time using Google's modern **MediaPipe Tasks API (`HandLandmarker`)** and draw all 21 joint landmarks onto the live mirrored webcam feed.
  - Created `CHEATSHEET.md` to document every OpenCV, MediaPipe, and Python standard function along with its arguments and return values.
- **Why I did it this way (Decisions & Trade-offs):**
  - Chose the modern `mediapipe.tasks` API + standalone `hand_landmarker.task` model file instead of pinning the deprecated `mp.solutions` API so the project runs cleanly on Python 3.14 and stays up to date.
  - Streamlined the dev workflow: running `main.py` directly inside **VS Code** (using the Windows `venv` interpreter) gives native webcam/GUI access without needing a separate PowerShell window, while **WSL (Ubuntu)** handles all `git` and `gh` CLI commands in the shared `/mnt/c/Users/lenovo/air-guitar-cv` directory.
  - Added `*.task` to `.gitignore` to keep the ~7.8 MB binary model file out of Git version control.
- **Bugs hit & how I fixed them:**
  - `AttributeError: module 'mediapipe' has no attribute 'solutions'` -> Google removed `mp.solutions` in recent MediaPipe releases; migrated to `vision.HandLandmarker` with `RunningMode.VIDEO`.
  - `AttributeError: 'HandLandmarkerResult' object has no attribute 'landmarks'` -> Renamed property to `detection_result.hand_landmarks`.
- **New terms I learned:**
  - `BaseOptions` & `.task` file (separating pre-trained neural-network weights from Python code).
  - `mp.Image` & `SRGB` (MediaPipe's standardized RGB image wrapper).
  - Monotonic millisecond timestamp (`int(time.time() * 1000)` required by `detect_for_video` to track motion across frames).
  - Normalized coordinates (`0.0` to `1.0` scaled by frame `w` and `h` to compute pixel coordinates `(cx, cy)`).
  - `cv2.circle()` (drawing filled joint markers in BGR color order).