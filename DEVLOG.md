# Engineering DevLog - Air String Synthesizer

## Session 1: Enviornment Setup & Native Webcam Loop
- **what i buit:** set up a python virtual enviornment('venv'), installed OpenCV and MediaPipe, and wrote a mirroed webcam loop in 'main.py'.
- **why i did it this way:** moved the repo from WSL ('~/') to the windows drive ('C:\Users\lenovo\air-guitar-cv') so OpenCV gets native hardware webcam access without USB bridging ('usbipd') or missing Linux X11 GUI libraries. Used 'cv2.flip(frame,1)' so the camera acts like mirror.

- **bugs hit & fixed:**
    - Poweshell blocked 'Activate.ps1' -> fixed once with 'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser'.
    - Clicking the window 'X' didn't close OpenCV because the 'while' loop immediatelyredrew it -> press 'q' instead.
- **Terms learned:** 'venv' (isolated package sandbox), 'frame' (single still photo in a 30 FPS video loop), 'cap.read()' (grabs 'success' + 'frame'), 'cv2.waitKey(1)' (refreshes window & checks keyboard input).
