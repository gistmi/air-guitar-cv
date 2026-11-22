import cv2

# 1. Open the default webcam (index 0)
cap = cv2.VideoCapture(0)

# 2. Loop forever while the camera stays open
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Could not read frame from webcam.")
        break

    # Flip the photo horizontally (1 = mirror mode, 0 = upside down)
    frame = cv2.flip(frame, 1)

    # Show the frame in a window
    cv2.imshow("Webcam Test", frame)

    # Wait 1ms; if you press 'q', break out of the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 3. Clean up when done
cap.release()
cv2.destroyAllWindows()
