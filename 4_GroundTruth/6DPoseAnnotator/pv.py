"""
6DoF pose annotator
Shuichi Akizuki, Chukyo Univ.
https://github.com/sakizuki/6DPoseAnnotator/tree/master
"""

import numpy as np
from open3d import *
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description='point cloud viewer')
    parser.add_argument('--input', nargs='*', help='input data (.ply or .pcd)')
    args = parser.parse_args()
    print(args.input)
    print(len(args.input))


    pcd = []
    for name in args.input:
        tmp = open3d.geometry.PointCloud()
        tmp = open3d.io.read_point_cloud( name )
        pcd.append(tmp)
        print(tmp)
        #draw_geometries([tmp])

    if len(args.input) == 1:
        open3d.visualization.draw_geometries([pcd[0]])
    elif len(args.input) == 2:
        open3d.visualization.draw_geometries([pcd[0],pcd[1]])
    elif len(args.input) == 3:
        open3d.visualization.draw_geometries([pcd[0],pcd[1],pcd[2]])
    elif len(args.input) == 4:
        open3d.visualization.draw_geometries([pcd[0],pcd[1],pcd[2],pcd[3]])
    elif 4 < len(args.input):
        print('Too many inputs.')
    