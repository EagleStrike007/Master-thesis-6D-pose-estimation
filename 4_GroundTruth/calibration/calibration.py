import numpy as np
import cv2
import glob

# Define the calibration pattern
pattern_size = (17, 10)
square_size = 0.021  # meters

# Prepare object points
object_points = np.zeros((pattern_size[0]*pattern_size[1], 3), np.float32)
object_points[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
object_points *= square_size

# Create empty lists to store the object points and image points from all calibration images
object_points_list = []
image_points_list = []

# Load the calibration images
# Note that the extension is .png
images = glob.glob('path_to_folder_with_images/*.png')

# Loop over all calibration images
for image_file in images:
    # Load the image
    image = cv2.imread(image_file)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
    if not ret:
        print(ret, image_file)
    else:
        print(ret)
    # If corners are found, add object points and image points to the lists
    if not ret:
        object_points_list.append(object_points)
        image_points_list.append(corners)

# Perform camera calibration
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(object_points_list, image_points_list, gray.shape[::-1], None, None)

print(K)
print(dist)