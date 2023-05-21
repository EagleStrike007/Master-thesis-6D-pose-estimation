"""
@article{Denninger2023,
    doi = {10.21105/joss.04901},
    url = {https://doi.org/10.21105/joss.04901},
    year = {2023},
    publisher = {The Open Journal},
    volume = {8},
    number = {82},
    pages = {4901},
    author = {Maximilian Denninger and Dominik Winkelbauer and Martin Sundermeyer
                and Wout Boerdijk and Markus Knauer and Klaus H. Strobl and Matthias Humt and Rudolph Triebel},
    title = {BlenderProc2: A Procedural Pipeline for Photorealistic Rendering},
    journal = {Journal of Open Source Software}
}
"""

import blenderproc as bproc
import os
import numpy as np
import sys

"""
Path to BOP-toolkit
"""
sys.path.append('path_to_BOP_tookit')
"""
Path
"""
bop_parent_path = "path_to_folder_with_object_dataset"
bop_dataset_name = "<name_of_dataset>"
cc_textures_path = "path_to_ccTextures_dataset"
output_dir = "path_to_output_folder"
external_object_model = "path_to_folder_with_external_object"
"""
Textures
"""
texture_lst = []
    # empty list: all textures are used
    # names: only first letters of texture name should be typed
        # for example: ["wood", "stone", "concrete"]
"""
Point light settings
"""
point_light_min = 100  # minimal strength/intensity of point light
point_light_max = 300  # maximal strength/intensity of point light
"""
Plane light settings
"""
plane_light_min = 2  # minimal strength/intensity of light light
plane_light_max = 8  # maximal strength/intensity of light light
"""
Number of poses + settings
"""
number_camera_poses = 20000  # number of images
number_camera_poses_change_texture = 5   # number of images when the background is changes
"""
Objects 
"""
obj_ids_lst = [1,2,3,4,6,7,8,9,10,11,12,10]  # list of object
    # object id's from the specified dataset above, see <bop_parent_path> + <bop_dataset_name>
    # duplicates are possible
"""
Writers 
"""
one_object_anno = True
    # True: only for 1 object the annotations are written in BOP format
    # False: the annotations are written for all objects in the scene
one_object_anno_id = 17  # object id of the object whose annotations are written

"""
Program 
"""

# initialize BlenderProc
bproc.init()

# loading of external object
# first, object with id 16 (.obj file)
# second, object with id 17 (.ply file)
sampled_bop_objs = bproc.loader.load_obj(filepath=os.path.join(external_object_model, "geometry2.obj"))
sampled_bop_objs[0].set_scale([1, 1, 1])  # scaling of object / 3D model
sampled_bop_objs[0].set_cp("category_id", 16) # Set category id which will be used in the BopWriter
sampled_bop_objs[0].set_name("obj_000016")  # Set name of object
sampled_bop_objs[0].set_cp("supercategory", bop_dataset_name)

sampled_bop_objs = bproc.loader.load_obj(filepath=os.path.join(external_object_model, "geometry2.ply"))
sampled_bop_objs[0].set_scale([0.001, 0.001, 0.001])  # scaling of object / 3D model from mm to m
sampled_bop_objs[0].set_cp("category_id", 17)  # Set category id which will be used in the BopWriter
sampled_bop_objs[0].set_name("obj_000017")  # Set name of object
sampled_bop_objs[0].set_cp("supercategory", bop_dataset_name)

# load object form the BOP dataset
sampled_bop_objs += bproc.loader.load_bop_objs(
    bop_dataset_path=os.path.join(bop_parent_path, bop_dataset_name),
    mm2m=True,
    num_of_objs_to_sample=len(obj_ids_lst),
    obj_ids=obj_ids_lst)

# load BOP dataset intrinsics
bproc.loader.load_bop_intrinsics(bop_dataset_path=os.path.join(bop_parent_path, bop_dataset_name))

# set shading properties
for j, obj in enumerate(sampled_bop_objs):
    obj.set_shading_mode('auto')

# create a plane and set location (+ rotation)
room_planes = [bproc.object.create_primitive('PLANE', scale=[4, 4, 2], location=[0, -2, 2], rotation=[-1.570796, 0, 0])]


def change_light(light_point):
    """
    Function to random change or set the strength/intensity and color of point light

    Parameters:
        light_point (object):   point light
    """
    light_point_energy = np.random.uniform(point_light_min, point_light_max)
    light_point_color = np.random.uniform([0.7, 0.7, 0.7], [1, 1, 1])
    light_point.set_energy(light_point_energy)
    light_point.set_color(light_point_color)


def change_light_postion(light_point):
    """
    Function to random change or set to position of point light

    Parameters:
        light_point (object):   point light
    """
    light_point.set_location(np.array([0, 5, 2]))


def change_plane(light_plane):
    """
    Function to random change or set the strength/intensity and color of light plane

    Parameters:
        light_plane (object):   point plane
    """
    light_plane_emission_strength = np.random.uniform(plane_light_min, plane_light_max)
    light_plane_emission_color = np.random.uniform([0.7, 0.7, 0.7, 1.0], [1.0, 1.0, 1.0, 1.0])
    light_plane.make_emissive(emission_strength=light_plane_emission_strength,
                                       emission_color=light_plane_emission_color)


def change_texture(room_planes, cc_textures):
    """
    Function to random change or set the background of planes

    Parameters:
        room_planes (list, object):     list with planes to change the texture/background
        cc_textures (object):           dataset with textures (cc_textures)
    """
    random_cc_texture = np.random.choice(cc_textures)
    for plane in room_planes:
        plane.replace_materials(random_cc_texture)


# make light plane
# sample light color and strength from plane
light_plane = bproc.object.create_primitive('PLANE', scale=[3, 3, 1], location=[0, 0, 10])
light_plane.set_name('light_plane')  # set name of plane to 'light_plane'
light_plane_material = bproc.material.create('light_material')  # set material of plane to 'light_material'
change_plane(light_plane_material)  # set strength/intensity of plane
light_plane.replace_materials(light_plane_material)

# make light point
light_point = bproc.types.Light()
change_light(light_point)  # set strength/intensity of light point
change_light_postion(light_point)  # set position of light point

# sample CC Texture and assign to room planes
cc_textures = bproc.loader.load_ccmaterials(cc_textures_path, used_assets=texture_lst)
change_texture(room_planes, cc_textures)


def sample_pose_func(obj: bproc.types.MeshObject):
    """
    Function that samples the pose of a given object

    Parameters:
        obj (object mesh):   object to sample
    """
    # set position of object
    obj.set_location(np.random.uniform([-0.35, 1.5, 1.75], [0.35, 2, 2.5]))
    # set rotation of object
    obj.set_rotation_euler(bproc.sampler.uniformSO3())  # uniform distributed in SO3

# activate depth rendering
bproc.renderer.enable_depth_output(activate_antialiasing=False)
bproc.renderer.set_max_amount_of_samples(50)

# loop to make scenes
poses = 0
while poses < number_camera_poses:
    # first, reset the scene
    bproc.utility.reset_keyframes()

    # check if background should be changes
    if (poses % number_camera_poses_change_texture) == 0 and poses != 0:
        # change texture of planes in the list "room_planes"
        change_texture(room_planes, cc_textures)

    # increment pose
    poses += 1

    # change position, strength/intensity and color of light point
    change_light(light_point)
    change_light_postion(light_point)
    # change strength/intensity and color of light plane
    change_plane(light_plane_material)

    # sample objects with the function "sample_pose_func"
    placed_objects = bproc.object.sample_poses(objects_to_sample=sampled_bop_objs, # object to sample
                                               sample_pose_func=sample_pose_func,  # function to sample
                                               objects_to_check_collisions=sampled_bop_objs, # object to  check collisions
                                               max_tries=100)

    # BVH tree used for camera obstacle checks
    bop_bvh_tree = bproc.object.create_bvh_tree_multi_objects(placed_objects)

    # set location for camera
    location = np.array([0, 3, 2])
    # set point of interest in scene for the camera
    poi = np.array([0, 0, 2])
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=0)
    # make homogeneous camera pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)

    # Check that obstacles are at least 0.3 meter away from the camera and make sure the view interesting enough
    if bproc.camera.perform_obstacle_in_view_check(cam2world_matrix, {"min": 0.3}, bop_bvh_tree):
        # set camera pose
        bproc.camera.add_camera_pose(cam2world_matrix)

        # render the whole pipeline
        data = bproc.renderer.render()
        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])
        data.update(seg_data)

        # write .hdf5 container
        # append to existing output is True
        bproc.writer.write_hdf5(output_dir, data, append_to_existing_output=True)

        # if one_object_anno is True
        # only the annotations of the object of interest (object with id equal to one_object_anno_id)
        # is written in the .json file
        annotation_object = []
        if one_object_anno:
            for obj in placed_objects:
                print(obj.get_cp("category_id"))
                if obj.get_cp("category_id") == one_object_anno_id:
                    annotation_object.append(obj)
        else:
            annotation_object.append(obj)

        # Write data in bop format
        bproc.writer.write_bop(output_dir,
                               target_objects=annotation_object,
                               dataset="",
                               depths=data["depth"],
                               depth_scale=1.0,
                               colors=data["colors"],
                               color_file_format="PNG",
                               append_to_existing_output=True,
                               frames_per_chunk=100000,
                               m2mm=True)

        # output .txt file with the number of poses
        with open(os.path.join(output_dir, "train.txt"), "a") as f:
            new_str = str(poses - 1)
            f.write(new_str.zfill(6) + "\n")