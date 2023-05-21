import cv2
import numpy as np

# Load the camera calibration parameters
camera_matrix = np.array([[1.00289758e+03, 0.00000000e+00, 7.02203480e+02],
                          [0.00000000e+00, 1.01262290e+03, 3.27795298e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist_coeffs = np.array([[-0.12573108,  0.5330855 ,  0.0066565 ,  0.01988005, -0.97071966]])

# Create the aruco dictionary and detector
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters =  cv2.aruco.DetectorParameters()

# Start the video capture
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Detect the aruco markers in the frame
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)

    # If any markers are detected
    if markerIds is not None:
        # Estimate the pose of each marker
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coeffs)

        # Draw the axes of each marker
        for i in range(len(ids)):
            cv2.aruco.drawAxis(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.1)

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()