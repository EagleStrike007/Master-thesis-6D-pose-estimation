To test the trained model on a real environment, a data set was created. Several scenes were recorded with an RGB(D) camera (Realsense L515). These scenes were then processed to extract ground truth information. Two different methods are proposed. 

The RGB(D) camera saves an RGB and depth image. After camera calibration, these images can be processed into ground truth information. The first method works on the basis of Aruco markers and an ICP algorithm. This mehode requires a number of steps. The second method works only on the basis of the ICP algorithm. 
The main libraries/packages used are [OpenCV](https://opencv.org/) and [Open3D](http://www.open3d.org/). OpenCV is mainly used for the calibration and detection of the Aruco markers. Whereas Open3D is used for the ICP algorithm. 
