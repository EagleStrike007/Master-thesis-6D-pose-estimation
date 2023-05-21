"""
6DoF pose annotator
Shuichi Akizuki, Chukyo Univ.
https://github.com/sakizuki/6DPoseAnnotator/tree/master
"""

import open3d as o3d 
import numpy as np
import cv2
import copy
import argparse
import os
import common3Dfunc as c3D
from math import *
import json

""" 
Object model to be transformed 
"""
CLOUD_ROT = o3d.geometry.PointCloud()
""" 
Transformation matrix
"""
all_transformation = np.identity(4)
""" 
Step size for rotation and translation 
"""
step = 0.025 * pi
STEP_ROT = step
STEP_TRANS = 0.01
""" 
Voxel size for downsampling
"""
voxel_size = 0.005
""" 
Running the process continuous  of step by step 
"""
CONTINUE = False


def get_argumets():
    """
        Parse arguments from command line
    """

    parser = argparse.ArgumentParser( description='Interactive 6DoF pose annotator')

    return parser.parse_args()


class Mapping():
    def __init__(self, camera_intrinsic_name, _w=640, _h=480, _d=1000.0 ):
        self.camera_intrinsic = o3d.io.read_pinhole_camera_intrinsic(camera_intrinsic_name)
        self.width = _w
        self.height = _h
        self.d = _d
        self.camera_intrinsic4x4 = np.identity(4)
        self.camera_intrinsic4x4[0,0] = self.camera_intrinsic.intrinsic_matrix[0,0]
        self.camera_intrinsic4x4[1,1] = self.camera_intrinsic.intrinsic_matrix[1,1]
        self.camera_intrinsic4x4[0,3] = self.camera_intrinsic.intrinsic_matrix[0,2]
        self.camera_intrinsic4x4[1,3] = self.camera_intrinsic.intrinsic_matrix[1,2]

    def showCameraIntrinsic(self):
        print(self.camera_intrinsic.intrinsic_matrix)
        print(self.camera_intrinsic4x4)

    def Cloud2Image( self, cloud_in ):
        
        img = np.zeros( [self.height, self.width], dtype=np.uint8 )
        img_zero = np.zeros( [self.height, self.width], dtype=np.uint8 )
        
        cloud_np1 = np.asarray(cloud_in.points)
        sorted_indices = np.argsort(cloud_np1[:,2])[::-1]
        cloud_np = cloud_np1[sorted_indices]
        cloud_np_xy = cloud_np[:,0:2] / cloud_np[:,[2]]
        # cloud_np ... (x/z, y/z, z)
        cloud_np = np.hstack((cloud_np_xy,cloud_np[:,[2]])) 

        cloud_color1 = np.asarray(cloud_in.colors)
        
        cloud_mapped = o3d.geometry.PointCloud()
        cloud_mapped.points = o3d.utility.Vector3dVector(cloud_np)
        
        cloud_mapped.transform(self.camera_intrinsic4x4)

        """ 
        If cloud_in has the field of color, color is mapped into the image. 
        """
        if len(cloud_color1) == len(cloud_np):
            cloud_color = cloud_color1[sorted_indices]
            img = cv2.merge((img,img,img))
            for i, pix in enumerate(cloud_mapped.points):
                if pix[0] < self.width and 0 < pix[0] and pix[1] < self.height and 0 < pix[1]:
                    img[int(pix[1]),int(pix[0])] = (cloud_color[i]*255.0).astype(np.uint8)
        else:
            for i, pix in enumerate(cloud_mapped.points):
                if pix[0] < self.width and 0 < pix[0] and pix[1] < self.height and 0 < pix[1]:
                    img[int(pix[1]),int(pix[0])] = int(255.0*(cloud_np[i,2]/cloud_np[0,2]))

            img = cv2.merge((img_zero,img,img_zero))
        
        return img
    
    def Pix2Pnt( self, pix, val ):
        pnt = np.array([0.0,0.0,0.0], dtype=np.float)
        depth = val / self.d
        pnt[0] = (float(pix[0]) - self.camera_intrinsic.intrinsic_matrix[0,2]) * depth / self.camera_intrinsic.intrinsic_matrix[0,0]
        pnt[1] = (float(pix[1]) - self.camera_intrinsic.intrinsic_matrix[1,2]) * depth / self.camera_intrinsic.intrinsic_matrix[1,1]
        pnt[2] = depth

        return pnt


def mouse_event(event, x, y, flags, param):
    w_name, img_c, img_d, mapping = param

    """Direct move. Object model will be moved to clicked position."""
    if event == cv2.EVENT_LBUTTONUP:
        global all_transformation
        print('Clicked({},{}): depth:{}'.format(x, y, img_d[y,x]))
        print(img_d[y,x])
        pnt = mapping.Pix2Pnt( [x,y], img_d[y,x] )
        print('3D position is', pnt)

        # compute current center of the cloud
        cloud_c = copy.deepcopy(CLOUD_ROT)
        cloud_c, center = c3D.Centering(cloud_c)
        np_cloud = np.asarray(cloud_c.points) 

        np_cloud += pnt
        print('Offset:', pnt )
        print('center:', center)
        offset = np.identity(4)
        offset[0:3,3] -= center
        offset[0:3,3] += pnt
        print('NEW Offset:', offset)
        all_transformation = np.dot( offset, all_transformation )
        print('all_transformation:', all_transformation)
        CLOUD_ROT.points = o3d.utility.Vector3dVector(np_cloud)
        generateImage( mapping, img_c )


def refine_registration(source, target, trans, voxel_size):
    # Pose refinement by ICP
    global all_transformation
    distance_threshold = voxel_size * 0.4
    print(":: Point-to-point ICP registration is applied on original point")
    print("   clouds to refine the alignment. This time we use a strict")
    print("   distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_icp(source, target, 
                                            distance_threshold, trans,
                                            o3d.pipelines.registration.TransformationEstimationPointToPoint(),
                                            o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=50,
                                                    relative_fitness=1.000000e-06, relative_rmse=1.000000e-06))

    return result.transformation


def generateImage( mapping, im_color ):
    global CLOUD_ROT

    img_m = mapping.Cloud2Image( CLOUD_ROT )
    img_mapped = cv2.addWeighted(img_m, 0.5, im_color, 0.5, 0 )
    cv2.imshow( window_name, img_mapped )


if __name__ == "__main__":
    """
    Setting 
    """
    vis = True  # vizualization
    max_counter = 300  # number of images that is processed
    begin = 0  # number of the first image of the dataset

    model = "path_to_3D_model"
    init = "path_to_input_transformations"
    intrin = "path_to_camera_intrinsic"

    """
    Loading of the object model
    """
    print('Loading: {}'.format(model))
    cloud_m = o3d.io.read_point_cloud(model)
    cloud_m_ds = cloud_m.voxel_down_sample(voxel_size)

    poses = []
    for i in range(max_counter):
        """
        Loading an image
        """
        print(":: Load two point clouds to be matched.")
        print(":: Load RGB")
        rgb_path = "data/Pose-film_2/color/{:06d}.png".format(i + begin)
        depth_path = "data/Pose-film_2/depth/{:06d}.png".format(i + begin)
        print("rgb_path", rgb_path)
        print("depth_path", depth_path)
        # Loading the RGB image
        color_raw = o3d.io.read_image(rgb_path)
        print(":: Load Depth")
        # Loading the depth image
        depth_raw = o3d.io.read_image(depth_path)
        # Loading the camera intrinsic matrix
        camera_intrinsic = o3d.io.read_pinhole_camera_intrinsic( intrin )

        im_color = np.asarray(color_raw)
        im_color = cv2.cvtColor(im_color, cv2.COLOR_BGR2RGB )
        im_depth = np.asarray(depth_raw) / 4  # Scaling the depth image to mm should be done here
        # for example from scale 0.25 mm to 1 mm, is dividing with 4 or multiplying with 0.25

        # converting the RGB and depth image to one RGBD image
        # scaling the depth image should also be done their, but this time to meters
        # for example from 0.00025 m to 1.0 m, is scaling with 4000
        # note that the last parameter (5.0) is the maximum depth in meter in the depth image
        rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw, 4000.0, 5.0 )
        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera_intrinsic )
        o3d.io.write_point_cloud( "cloud_in.ply", pcd )
        cloud_in_ds = pcd.voxel_down_sample(voxel_size)
        o3d.io.write_point_cloud( "cloud_in_ds.ply", cloud_in_ds )

        np_pcd = np.asarray(pcd.points)

        """
        Loading of the initial transformation - which is a default value 
        """
        initial_trans = np.identity(4)
        cloud_m_c, offset = c3D.Centering( cloud_m_ds )
        mat_centering = c3D.makeTranslation4x4( -1.0*offset )
        all_transformation = np.dot( mat_centering, all_transformation )

        CLOUD_ROT = copy.deepcopy(cloud_m_ds)
        CLOUD_ROT.transform( all_transformation )

        mapping = Mapping('./data/realsense_intrinsic.json')

        window_name = '6DoF Pose Annotator'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window_name, mouse_event,
                             [window_name, im_color, im_depth, mapping])

        generateImage(mapping, im_color)

        all_transformation_previous = all_transformation

        """
        Running ICP algorithm continuous  
        See code line 36
        """
        if CONTINUE:
            result_icp = refine_registration(CLOUD_ROT, pcd, np.identity(4), 10.0 * voxel_size)
            CLOUD_ROT.transform(result_icp)
            all_transformation = np.dot(result_icp, all_transformation)

            result_icp = refine_registration(CLOUD_ROT, pcd, np.identity(4), 5.0 * voxel_size)
            CLOUD_ROT.transform(result_icp)
            all_transformation = np.dot(result_icp, all_transformation)

            result_icp = refine_registration(CLOUD_ROT, pcd, np.identity(4), 2.0 * voxel_size)
            CLOUD_ROT.transform(result_icp)
            all_transformation = np.dot(result_icp, all_transformation)

            result_icp = refine_registration(CLOUD_ROT, pcd, np.identity(4), 1.0 * voxel_size)
            CLOUD_ROT.transform(result_icp)
            all_transformation = np.dot(result_icp, all_transformation)
        else:
            while True:
                key = cv2.waitKey(1) & 0xFF
                """
                ICP algorithm 
                """
                if key == ord("a"):
                    all_transformation_previous = all_transformation
                    result_icp = refine_registration(CLOUD_ROT, pcd, np.identity(4), 10.0 * voxel_size)
                    CLOUD_ROT.transform(result_icp)
                    all_transformation = np.dot(result_icp, all_transformation)
                    generateImage(mapping, im_color)

                if key == ord("z"):
                    all_transformation_previous = all_transformation
                    result_icp = refine_registration(CLOUD_ROT, pcd, np.identity(4), 5.0 * voxel_size)
                    CLOUD_ROT.transform(result_icp)
                    all_transformation = np.dot(result_icp, all_transformation)
                    generateImage(mapping, im_color)

                if key == ord("e"):
                    all_transformation_previous = all_transformation
                    result_icp = refine_registration(CLOUD_ROT, pcd, np.identity(4), 2.0 * voxel_size)
                    CLOUD_ROT.transform(result_icp)
                    all_transformation = np.dot(result_icp, all_transformation)
                    generateImage(mapping, im_color)

                if key == ord("r"):
                    all_transformation_previous = all_transformation
                    for i in range(2):
                        result_icp = refine_registration(CLOUD_ROT, pcd, np.identity(4), 1.0 * voxel_size)
                        CLOUD_ROT.transform(result_icp)
                        all_transformation = np.dot(result_icp, all_transformation)
                    generateImage(mapping, im_color)

                """
                Next image 
                """
                if key == ord("n"):
                    cv2.destroyAllWindows()
                    CONTINUE = True
                    break

                """
                Go to previous 
                """
                if key == ord("p"):
                    cloud_c = copy.deepcopy(CLOUD_ROT)
                    cloud_c, center = c3D.Centering(cloud_c)

                    offset_pr = np.identity(4)
                    offset_pr[0:3, 3] -= center
                    offset_pr[0:3, 3] += all_transformation_previous[0:3, 3]
                    all_transformation = np.dot(offset_pr, all_transformation_previous)
                    CLOUD_ROT.transform(offset_pr)
                    generateImage(mapping, im_color)

                """
                Rotation (possible in both directions)
                """
                if key == ord("1"):
                    print('Rotation around roll axis')
                    rotation = c3D.ComputeTransformationMatrixAroundCentroid(CLOUD_ROT, STEP_ROT, 0, 0)
                    CLOUD_ROT.transform(rotation)
                    all_transformation = np.dot(rotation, all_transformation)

                    generateImage(mapping, im_color)

                if key == ord("2"):
                    print('Rotation around pitch axis')
                    rotation = c3D.ComputeTransformationMatrixAroundCentroid(CLOUD_ROT, 0, STEP_ROT, 0)
                    CLOUD_ROT.transform(rotation)
                    all_transformation = np.dot(rotation, all_transformation)

                    generateImage(mapping, im_color)

                if key == ord("3"):
                    print('Rotation around yaw axis')
                    rotation = c3D.ComputeTransformationMatrixAroundCentroid(CLOUD_ROT, 0, 0, STEP_ROT)
                    CLOUD_ROT.transform(rotation)
                    all_transformation = np.dot(rotation, all_transformation)

                    generateImage(mapping, im_color)

                if key == ord("4"):
                    print('Rotation around roll axis')
                    rotation = c3D.ComputeTransformationMatrixAroundCentroid(CLOUD_ROT, -STEP_ROT, 0, 0)
                    CLOUD_ROT.transform(rotation)
                    all_transformation = np.dot(rotation, all_transformation)

                    generateImage(mapping, im_color)

                if key == ord("5"):
                    print('Rotation around pitch axis')
                    rotation = c3D.ComputeTransformationMatrixAroundCentroid(CLOUD_ROT, 0, -STEP_ROT, 0)
                    CLOUD_ROT.transform(rotation)
                    all_transformation = np.dot(rotation, all_transformation)

                    generateImage(mapping, im_color)

                if key == ord("6"):
                    print('Rotation around yaw axis')
                    rotation = c3D.ComputeTransformationMatrixAroundCentroid(CLOUD_ROT, 0, 0, -STEP_ROT)
                    CLOUD_ROT.transform(rotation)
                    all_transformation = np.dot(rotation, all_transformation)

                    generateImage(mapping, im_color)

                """
                Changing the rotation steps from coarse to fine or vice versa 
                Changing the translation steps from negative to positive or vice versa 
                """
                if key == ord("c"):
                    STEP_TRANS = -STEP_TRANS
                    if STEP_ROT == (step / 2):
                        STEP_ROT = step
                    else:
                        STEP_ROT = step / 2

                """
                Translation 
                """
                if key == ord("7"):
                    translation = np.identity(4)
                    translation[:, :3] += np.array([STEP_TRANS, 0, 0])
                    CLOUD_ROT.transform(translation)
                    all_transformation = np.dot(translation, all_transformation)

                    generateImage(mapping, im_color)

                if key == ord("8"):
                    translation = np.identity(4)
                    translation[:, :3] += np.array([0, STEP_TRANS, 0])
                    CLOUD_ROT.transform(translation)
                    all_transformation = np.dot(translation, all_transformation)

                    generateImage(mapping, im_color)

                if key == ord("9"):
                    translation = np.identity(4)
                    translation[:, :3] += np.array([0, 0, STEP_TRANS])
                    CLOUD_ROT.transform(translation)
                    all_transformation = np.dot(translation, all_transformation)

                    generateImage(mapping, im_color)

        print("\n\nFinal transformation is\n", all_transformation)
        poses.append(all_transformation)

        o3d.io.write_point_cloud("cloud_rot_ds.ply", CLOUD_ROT)
        cloud_m.transform(all_transformation)
        o3d.io.write_point_cloud("cloud_rot.ply", cloud_m)

    """
    Writing the poses (annotations)
    """
    f_out = open('./data/trans_refine.json', 'w')
    for i in range(len(poses)):
        trans = poses[i].tolist()
        transform = {"transformation4x4":[trans]}
        json.dump(transform, f_out)
        f_out.write('\n')
    f_out.close()

