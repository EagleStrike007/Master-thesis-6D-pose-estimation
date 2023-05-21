"""
Code based on: https://github.com/ankurhanda/simkinect/tree/master
"""

import numpy as np
import cv2 
import time
import matplotlib.pyplot as plt
import matplotlib


def add_gaussian_shifts(depth, std=1/2.0):
    """
    @article{handa:etal:2014,
      title   = {A benchmark for RGB-D visual odometry, 3D reconstruction and SLAM},
      author  = {Handa, Ankur and Whelan, Thomas and McDonald, John and Davison, Andrew J},
      journal = {ICRA},
      year    = {2014},
    }

    @article{Barron:etal:2013A,
      author  = {Jonathan T. Barron and Jitendra Malik},
      title   = {Intrinsic Scene Properties from a Single RGB-D Image},
      journal = {CVPR},
      year    = {2013},
    }

    @article{Bohg:etal:2014,
      title   = {Robot arm pose estimation through pixel-wise part classification},
      author  = {Bohg, Jeannette and Romero, Javier and Herzog, Alexander and Schaal, Stefan},
      journal = {ICRA},
      year    = {2014},
    }
    """

    rows, cols = depth.shape 
    gaussian_shifts = np.random.normal(0, std, size=(rows, cols, 2))
    gaussian_shifts = gaussian_shifts.astype(np.float32)

    # creating evenly spaced coordinates  
    xx = np.linspace(0, cols-1, cols)
    yy = np.linspace(0, rows-1, rows)

    # get xpixels and ypixels 
    xp, yp = np.meshgrid(xx, yy)

    xp = xp.astype(np.float32)
    yp = yp.astype(np.float32)

    xp_interp = np.minimum(np.maximum(xp + gaussian_shifts[:, :, 0], 0.0), cols)
    yp_interp = np.minimum(np.maximum(yp + gaussian_shifts[:, :, 1], 0.0), rows)

    depth_interp = cv2.remap(depth, xp_interp, yp_interp, cv2.INTER_LINEAR)

    return depth_interp


def rand_range(rng, lo, hi):
        return rng.rand()*(hi-lo)+lo


if __name__ == "__main__":

    count = 6

    depth_uint16_in = cv2.imread("./depth/{}.png".format(count), cv2.IMREAD_UNCHANGED)
    h, w = depth_uint16_in.shape

    depth_uint16 = add_gaussian_shifts(depth_uint16_in.copy(), rand_range(np.random, 0.5, 1.0))

    dst = cv2.Laplacian(src=depth_uint16, ddepth=cv2.CV_32F, ksize=3)

    value = rand_range(np.random, 200, 800)
    value2 = int(rand_range(np.random, 8, 8))
    smoot2 = cv2.bilateralFilter(dst, value2, value, value)

    gaus = cv2.GaussianBlur(smoot2, (5, 5), 0)

    gaus2 = add_gaussian_shifts(gaus, rand_range(np.random, 0.1, 0.5))

    depth_uint16_out = np.zeros((h,w), np.uint16)
    depth_uint16_out = depth_uint16_in.copy()
    depth_uint16_out[gaus2 > 5] = 0

    cv2.imwrite("./16-test/depth-new/{:06d}.png".format(count), depth_uint16_out)

    print(count)
    count = count + 1

