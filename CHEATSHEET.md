# Library & Function Reference (`CHEATSHEET.md`)

## 1. OpenCV (`cv2`) — Camera, Image Processing & Drawing

### `cv2.VideoCapture(index)`
- **Purpose:** Opens a connection to a camera device or video file.
- **Arguments:**
  - `index`: Integer camera ID (`0` = default built-in laptop webcam; `1` = external USB webcam).
- **Returns:** A `VideoCapture` object (`cap`) used to read frames and check camera status.

### `cap.isOpened()`
- **Purpose:** Checks whether the camera connection initialized and is currently active.
- **Arguments:** None.
- **Returns:** Boolean (`True` if the camera is open and ready, `False` otherwise).

### `cap.read()`
- **Purpose:** Grabs and decodes the next single photo (`frame`) from the live camera stream.
- **Arguments:** None.
- **Returns:** A 2-item tuple `(success, frame)`:
  - `success`: Boolean (`True` if a frame was captured, `False` if the camera disconnected/failed).
  - `frame`: A 3D NumPy array of pixel values `(height, width, 3)` in **BGR** color order.

### `cv2.flip(src, flipCode)`
- **Purpose:** Mirrors or flips an image array horizontally or vertically.
- **Arguments:**
  - `src`: The input image array (`frame`).
  - `flipCode`: Integer direction (`1` = horizontal mirror flip, `0` = vertical upside-down flip, `-1` = both).
- **Returns:** The flipped image array.

### `cv2.cvtColor(src, code)`
- **Purpose:** Converts an image from one color space to another (used here to bridge OpenCV's BGR format to MediaPipe's RGB format).
- **Arguments:**
  - `src`: The input image array (`frame`).
  - `code`: Color conversion constant (e.g., `cv2.COLOR_BGR2RGB`).
- **Returns:** A new image array in the target color format.

### `cv2.circle(img, center, radius, color, thickness)`
- **Purpose:** Draws a circle onto an image frame (used to mark the 21 hand joint landmarks).
- **Arguments:**
  - `img`: The image array (`frame`) to draw on.
  - `center`: `(x, y)` tuple of integer pixel coordinates.
  - `radius`: Circle radius in pixels (e.g., `5`).
  - `color`: `(B, G, R)` color tuple (e.g., `(0, 255, 0)` for bright green).
  - `thickness`: Outline width in pixels, or `-1` to fill the circle solid.
- **Returns:** The modified image array (`frame`).

### `cv2.imshow(winname, mat)`
- **Purpose:** Displays an image array inside a named desktop GUI window.
- **Arguments:**
  - `winname`: String title of the window (e.g., `"Webcam Test"`).
  - `mat`: The image array (`frame`) to display.
- **Returns:** `None`.

### `cv2.waitKey(delay)`
- **Purpose:** Refreshes OpenCV GUI windows and pauses briefly to listen for keyboard input.
- **Arguments:**
  - `delay`: Milliseconds to wait (`1` = wait 1 ms so live video doesn't stall; `0` = pause forever until a key is pressed).
- **Returns:** Integer ASCII code of the pressed key (masked with `& 0xFF` on Windows to isolate the standard key byte), or `-1` if no key was pressed.

### `cap.release()`
- **Purpose:** Closes the camera connection and unlocks the webcam hardware for other apps.
- **Arguments:** None.
- **Returns:** `None`.

### `cv2.destroyAllWindows()`
- **Purpose:** Closes all pop-up windows created by `cv2.imshow()`.
- **Arguments:** None.
- **Returns:** `None`.

---

## 2. MediaPipe Tasks (`mediapipe.tasks.python.vision`) — AI Hand Tracking

### `python.BaseOptions(model_asset_path)`
- **Purpose:** Tells MediaPipe where the pre-trained `.task` AI model file lives on your hard drive.
- **Arguments:**
  - `model_asset_path`: String file path to the model weights (e.g., `"hand_landmarker.task"`).
- **Returns:** A `BaseOptions` configuration object.

### `vision.HandLandmarkerOptions(base_options, running_mode, num_hands, min_hand_detection_confidence)`
- **Purpose:** Configures the behavior and thresholds of the hand-tracking detector.
- **Arguments:**
  - `base_options`: The `BaseOptions` object pointing to `"hand_landmarker.task"`.
  - `running_mode`: `vision.RunningMode.VIDEO` (optimizes tracking across continuous video frames).
  - `num_hands`: Integer maximum number of hands to detect (`2`).
  - `min_hand_detection_confidence`: Float from `0.0` to `1.0` (`0.7` = require 70% confidence before reporting a hand).
- **Returns:** A `HandLandmarkerOptions` configuration object.

### `vision.HandLandmarker.create_from_options(options)`
- **Purpose:** Loads the AI model into memory and initializes the hand-tracking detector.
- **Arguments:**
  - `options`: The `HandLandmarkerOptions` object created above.
- **Returns:** An active `HandLandmarker` detector instance (`detector`).

### `mp.Image(image_format, data)`
- **Purpose:** Wraps a raw NumPy pixel array into MediaPipe's standardized image container.
- **Arguments:**
  - `image_format`: Pixel encoding format (`mp.ImageFormat.SRGB` for standard 3-channel RGB).
  - `data`: The RGB NumPy array (`rgb_frame`).
- **Returns:** An `mp.Image` object ready for MediaPipe inference.

### `detector.detect_for_video(image, timestamp_ms)`
- **Purpose:** Runs neural-network hand detection and landmark prediction on a single video frame.
- **Arguments:**
  - `image`: The `mp.Image` object wrapping the current RGB frame.
  - `timestamp_ms`: Strictly increasing integer timestamp in milliseconds (`int(time.time() * 1000)`).
- **Returns:** A `HandLandmarkerResult` object containing `.hand_landmarks` (a list of detected hands, each with 21 normalized `(x, y, z)` landmarks from `0.0` to `1.0`) and `.handedness` (`"Left"` vs. `"Right"`).

---

## 3. Python Standard Library (`time` & Built-ins)

### `time.time()`
- **Purpose:** Reads the current system clock time.
- **Arguments:** None.
- **Returns:** Float representing seconds elapsed since the Unix epoch (Jan 1, 1970). Multiplying by `1000` and wrapping in `int()` converts it to milliseconds.

### `ord(c)`
- **Purpose:** Converts a single character into its integer Unicode/ASCII key code (used to compare against `cv2.waitKey(1)`).
- **Arguments:**
  - `c`: A 1-character string (e.g., `'q'`).
- **Returns:** Integer code (`113` for `'q'`).