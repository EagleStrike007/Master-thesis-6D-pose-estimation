import open3d as o3d
import numpy as np
import cv2
import copy
from math import *
import json
from matplotlib import *
import matplotlib.pyplot as plt


def ply_vtx(pth):
    f = open(pth)
    assert f.readline().strip() == "ply"
    f.readline()
    f.readline()
    f.readline()
    N = int(f.readline().split()[-1])
    while f.readline().strip() != "end_header":
        continue
    pts = []
    for _ in range(N):
        pts.append(np.float32(f.readline().split()[:3]))
    return np.array(pts)


def get_model_points():
    pointxyz = ply_vtx(r".\powerdrill.ply")
    return pointxyz


def project_p3d(p3d, cam_scale, K):
    if type(K) == str:
        K = intrinsic_matrix[K]
    p3d = p3d * cam_scale
    p2d = np.dot(p3d, K.T)
    p2d_3 = p2d[:, 2]
    p2d_3[np.where(p2d_3 < 1e-8)] = 1.0
    p2d[:, 2] = p2d_3
    p2d = np.around((p2d[:, :2] / p2d[:, 2:])).astype(np.int32)
    return p2d


def draw_p2ds(img, p2ds, r=1, color=[(255, 0, 0)]):
    if type(color) == tuple:
        color = [color]
    if len(color) != p2ds.shape[0]:
        color = [color[0] for i in range(p2ds.shape[0])]
    h, w = img.shape[0], img.shape[1]
    for pt_2d, c in zip(p2ds, color):
        pt_2d[0] = np.clip(pt_2d[0], 0, w)
        pt_2d[1] = np.clip(pt_2d[1], 0, h)
        img = cv2.circle(
            img, (pt_2d[0], pt_2d[1]), r, c, -1
        )
    return img


# camera matrix
camera_matrix = np.array([[606.91,   0.     ,   326.68717083],
                          [0.    ,   608.623,   249.21760803],
                          [0.    ,   0.     ,   1.           ]])

root = "path_to_depth_images"
init = "path_to_annorations"
max_counter = 50  # max number of images to process
begin = 200  # number of the first image of the dataset

data = [json.loads(line) for line in open(init, 'r')]

for count in range(max_counter):
    depth_path = root + "/depth/{:06d}.png".format(count + begin)

    np_depth = np.asarray(o3d.io.read_image(depth_path)) / 4000

    pose = np.array(data[count]["transformation4x4"])[0]

    mesh_pts = get_model_points().copy()
    mesh_pts = np.dot(mesh_pts, pose[:3, :3].T) + pose[:3, 3]
    mesh_p2ds = project_p3d(mesh_pts, 1.0, camera_matrix)

    mask2 = np.zeros((480,640), dtype="float")
    mask3 = np.zeros((480,640), dtype="uint8")
    mask4 = np.zeros((480,640), dtype="uint8")
    depth_hole = np.zeros((480,640), dtype="uint8")
    for i in range(mesh_p2ds.shape[0]):
        if mesh_pts[i][2] < mask2[mesh_p2ds[i][1], mesh_p2ds[i][0]]:
            mask2[mesh_p2ds[i][1], mesh_p2ds[i][0]] = mesh_pts[i][2]
        elif mask2[mesh_p2ds[i][1], mesh_p2ds[i][0]] == 0:
            mask2[mesh_p2ds[i][1], mesh_p2ds[i][0]] = mesh_pts[i][2]

    depth_hole[np_depth == 0.0] = 255

    mask3[abs(np_depth - mask2) < 0.05] = 255
    mask3[depth_hole == 255] = 255
    mask3[mask2 == 0] = 0

    cv2.imwrite('img.jpg', mask3)

    image = cv2.imread('img.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((5, 5), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)

    cv2.imwrite('./output-depth/{:06d}.png'.format(count), image)
