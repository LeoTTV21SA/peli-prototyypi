import cv2
import numpy as np

# Open the webcam (usually the default webcam)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

new_width = 640  
new_height = 480  
cap.set(3, new_width)
cap.set(4, new_height)

# ROI boundaries (x, y, width, height)
roi_values = [
(400, 0, 200, 150),
(0, 330, 200, 150),
(0, 0, 200, 150),
(400, 330, 200, 150)
]
# Flags to track movement detection for each corner
movement_detected = [False] * len(roi_values)

# Create windows for each corner
#for i in range(len(roi_values)):
#    cv2.namedWindow(f'Camera Feed - Corner {i + 1}')


while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    frame = cv2.resize(frame, (new_width, new_height))
    for i, (roi_x, roi_y, roi_width, roi_height) in enumerate(roi_values):
        # Define ROI
        roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # Convert ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Calculate absolute difference between consecutive frames
        if f'prev_gray_roi_{i}' in locals():
            frame_diff = cv2.absdiff(eval(f'prev_gray_roi_{i}'), gray_roi)

            # Apply a threshold to detect motion areas
            _, threshold = cv2.threshold(frame_diff, 200, 255, cv2.THRESH_BINARY)

            # Check for movement
            if np.sum(threshold) > 0 and not movement_detected[i]:
                print(f"Corner {i + 1}: Movement detected")
                movement_detected[i] = True
            elif np.sum(threshold) == 0:
                movement_detected[i] = False

            # Find contours in the thresholded image
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw rectangles around detected motion areas
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (roi_x + x, roi_y + y), (roi_x + x + w, roi_y + y + h), (0, 255, 0), 2)


        # Update previous grayscale ROI
        exec(f'prev_gray_roi_{i} = gray_roi.copy()')
        
    cv2.imshow('Webcam',frame)

    
    # Wait for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
