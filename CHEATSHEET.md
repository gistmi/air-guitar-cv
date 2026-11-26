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

## Session 3 Additions

### 1. OpenCV (`cv2`) — Drawing Lines

#### `cv2.line(img, pt1, pt2, color, thickness)`
- **Purpose:** Draws a straight line segment onto an image frame (used to render active and locked-in virtual strings between pinch points).
- **Arguments:**
  - `img`: The image array (`frame`) to draw on.
  - `pt1`: `(x1, y1)` tuple of integer pixel coordinates for the start point.
  - `pt2`: `(x2, y2)` tuple of integer pixel coordinates for the end point.
  - `color`: `(B, G, R)` color tuple (e.g., `(255, 0, 255)` for Neon Magenta, `(255, 255, 0)` for Electric Cyan).
  - `thickness`: Line width in pixels (e.g., `3` or `4`).
- **Returns:** The modified image array (`frame`).

---

### 2. Python `math` Module — Geometry & Distance

#### `math.hypot(dx, dy)`
- **Purpose:** Calculates the exact straight-line (Euclidean) distance $\sqrt{dx^2 + dy^2}$ between two 2D points (used to measure the pixel gap between Thumb Tip #4 and Index Tip #8, as well as the distance between both hands).
- **Arguments:**
  - `dx`: Horizontal pixel difference (`x2 - x1`).
  - `dy`: Vertical pixel difference (`y2 - y1`).
- **Returns:** Float representing the straight-line pixel distance between the two points.

---

### 3. Python Built-in List Methods & Operators

#### `list.append(item)`
- **Purpose:** Adds a single item onto the end of a Python list (used to record active pinch coordinates in `pinch_points` and save released strings into `strings`).
- **Arguments:**
  - `item`: Any object or tuple to add (e.g., `(pinch_x, pinch_y)` or `(p1, p2)`).
- **Returns:** `None` (modifies the list in place).

#### `list.clear()`
- **Purpose:** Removes all items from a list at once (used when pressing `'c'` to wipe all saved strings off the screen).
- **Arguments:** None.
- **Returns:** `None` (empties the list in place).

#### `len(collection)`
- **Purpose:** Counts how many items are currently inside a list or sequence (used to check `len(pinch_points) == 2` so strings only form when both hands are pinching).
- **Arguments:**
  - `collection`: A list, tuple, or string.
- **Returns:** Integer count of items in `collection`.

#### `//` (Floor Division Operator)
- **Purpose:** Divides two numbers and rounds down to the nearest whole integer (used in `(x1 + x2) // 2` to compute the exact integer pixel midpoint between thumb and index fingertips).
- **Arguments:** Left and right numeric operands (`a // b`).
- **Returns:** Integer quotient (when both operands are integers).

## Session 4 Additions

### 1. NumPy (`numpy` as `np`) — Audio Wave Arrays & Math

#### `np.random.uniform(low, high, size)`
- **Purpose:** Generates an array of random decimal numbers evenly spread between `low` and `high` (used to create the initial white-noise "pick snap" buffer in Karplus-Strong synthesis).
- **Arguments:**
  - `low`: Minimum float value (e.g., `-1.0`).
  - `high`: Maximum float value (e.g., `1.0`).
  - `size`: Integer count of random numbers to generate (`N`).
- **Returns:** A 1D NumPy array of `size` random floats.

#### `ndarray.astype(dtype)`
- **Purpose:** Converts a NumPy array's data type (used to convert 64-bit floats into 32-bit floats `np.float32`, which audio drivers require).
- **Arguments:**
  - `dtype`: Target NumPy data type (e.g., `np.float32`).
- **Returns:** A new NumPy array cast to `dtype`.

#### `np.zeros(shape, dtype)`
- **Purpose:** Creates a pre-allocated NumPy array filled with `0.0`s (used to hold the full `total_samples` audio waveform before filling it in the loop).
- **Arguments:**
  - `shape`: Integer length (or tuple of dimensions) of the array (e.g., `total_samples`).
  - `dtype`: Data type of the zeros (e.g., `np.float32`).
- **Returns:** A NumPy array of the given shape filled with zeros.

---

### 2. SoundDevice (`sounddevice` as `sd`) — Audio Playback

#### `sd.play(data, samplerate)`
- **Purpose:** Sends a 1D NumPy audio wave array to your default laptop speakers asynchronously (non-blocking) so the webcam loop keeps running smoothly.
- **Arguments:**
  - `data`: 1D NumPy array of `float32` audio samples in the range `[-1.0, 1.0]`.
  - `samplerate`: Integer playback speed in samples per second (e.g., `44100`).
- **Returns:** `None`.

---

### 3. OpenCV (`cv2`) — Windows Camera Backend & Resolution

#### `cv2.VideoCapture(index, apiPreference)`
- **Purpose:** Opens a camera device using a specific OS video driver backend for faster startup and frame rates on Windows.
- **Arguments:**
  - `index`: Integer camera ID (`0` = default webcam).
  - `apiPreference`: Backend flag (e.g., `cv2.CAP_DSHOW` for Windows DirectShow).
- **Returns:** A `VideoCapture` object (`cap`).

#### `cap.set(propId, value)`
- **Purpose:** Configures hardware capture properties such as frame width and height (`640x480`) to keep MediaPipe processing fast.
- **Arguments:**
  - `propId`: Property constant (e.g., `cv2.CAP_PROP_FRAME_WIDTH`, `cv2.CAP_PROP_FRAME_HEIGHT`).
  - `value`: Numeric target value (e.g., `640` or `480`).
- **Returns:** Boolean (`True` if the camera accepted the setting, `False` otherwise).

---

### 4. Python Built-ins & Operators (`max`, `min`, `%`)

#### `max(a, b)` & `min(a, b)`
- **Purpose:** Returns the largest or smallest of the given arguments (combined as `max(low, min(high, val))` to clamp string lengths between `60` and `450` pixels and projection values between `0.0` and `1.0`).
- **Arguments:** Two or more comparable numbers.
- **Returns:** The maximum or minimum value.

#### `%` (Modulo / Remainder Operator)
- **Purpose:** Returns the remainder after integer division (`i % N`), wrapping a growing counter neatly around `0` to `N - 1` so an array acts as a circular **ring buffer** without copying memory.
- **Arguments:** Dividend `i` and divisor `N` (`i % N`).
- **Returns:** Integer remainder in the range `[0, N - 1]`.