import os
import numpy as np
import h5py
from PIL import Image


def count_hdf5_files(path):
    """
    Function to count the number of .hdf5 containers in a certain folder

    Parameters:
        path (str):   path to the folder
    Returns:
        count (int): number of .hdf5 containers
    """
    count = 0
    for root_dir, cur_dir, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == ".hdf5":
                count = count + 1
    return count


"""
Parameter
"""
path = "path_to_folder"
output_dir = "path_to_output_folder_for_masks"
obj_id = 17  # object id for creating binary mask

"""
When folder doesn't exist make folder
"""
try:
    os.mkdir(output_dir)
except OSError as error:
    print(error)
    print("Folder already exist")

"""
Open .hdf5 container and write masks
"""
for i in range(count_hdf5_files(path)):
    filename = path + "/{}.hdf5".format(i)
    with h5py.File(filename, "r") as f:
        group = f["class_segmaps"]

        # mask empty mask
        image = np.zeros((480, 640))
        # make binary mask
        image[group[:, :] == obj_id] = 255
        # convert mask into an image
        im = Image.fromarray(image[:, :])

        # convert image to correct format (uint8)
        im = im.convert("L")
        im.save(os.path.join(output_dir + '/' + str(i).zfill(6) + ".png"))