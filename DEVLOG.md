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

  ## Session 3: Pinch-to-Create & Stretch Indefinite Strings
- **What I built:** Added dual-hand pinch detection (`Landmark 4` Thumb Tip + `Landmark 8` Index Fingertip), proximity-gated string creation (strings only spawn if both hands start pinching close together), real-time length stretching, and a persistent `strings` list so indefinite strings stay suspended in mid-air (`c` to clear).
- **Why I did it this way:** Used Euclidean distance (`math.hypot`) to detect pinches (`< 40px`) and initial hand proximity (`< 120px`), plus cross-frame state variables (`is_creating_string`, `active_string`, `strings`) so strings persist after releasing the pinch.
- **Bugs hit & fixed:**
  - Broken `venv` / `WSL: Ubuntu` interpreter mismatch in VS Code -> rebuilt clean Windows `venv` via PowerShell and kept VS Code local on Windows while using WSL for Git.
  - `key` variable undefined when adding `'c'` clear shortcut -> stored `key = cv2.waitKey(1) & 0xFF` once per frame.
  - Pinch detection failing in areas cluttered with existing strings -> realized saved cyan strings were being drawn on `frame` *before* `detector.detect_for_video()`, visually obscuring fingers from MediaPipe's AI; moved all `cv2.line()` drawing calls *after* hand detection.
- **Terms learned:** `math.hypot(dx, dy)` (Euclidean pixel distance), state variables outside the `while` loop, list `.append()` & `.clear()`, `cv2.line()`.

## Session 4: Karplus-Strong Audio Synthesis & Fingertip Plucking
- **What I built:** Installed `numpy` and `sounddevice`, built a Karplus-Strong plucked-string synthesizer (`generate_plucked_wave`), mapped string pixel length to musical pitch (`length_to_freq`), and added point-to-segment fingertip pluck detection (`point_to_segment_dist`) with a per-string cooldown timer (`last_pluck`).
- **Why I did it this way:** Pre-computed each string's audio wave once at creation using an in-place ring buffer (`i % N`) instead of calling `np.append()` inside the sample loop, eliminating memory-copy lag during live video; also switched OpenCV to `cv2.CAP_DSHOW` at `640x480` for smoother Windows webcam FPS.
- **Bugs hit & fixed:**
  - `AttributeError: module 'numpy' has no attribute 'zeroes'` -> fixed spelling to `np.zeros`.
  - `ValueError: too many values to unpack` -> removed legacy tuple-unpacking draw loop after switching `strings` entries to 4-key dictionaries.
  - Parentheses placement in `point_to_segment_dist` (`/ seg_len_sq` outside `min()`) and over-indented drawing loop -> fixed projection clamping and unindented string rendering so strings stay visible even when hands leave the frame.
  - Severe frame lag from `np.append` inside a 52,920-step loop -> replaced with an in-place modulo ring buffer and cached each string's generated wave.
- **Terms learned:** `SAMPLE_RATE` (`44100 Hz`), Karplus-Strong synthesis (noise burst + low-pass moving average + decay factor `0.996`), ring buffer (`i % N`), point-to-line-segment projection, and cooldown debouncing (`last_pluck`).