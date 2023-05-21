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
import pickle
import argparse
import os
import numpy as np
from datetime import date
import sys
from typing import Any

#####################################################
#####################################################
file = open('Original.txt', 'rb')
data = pickle.load(file)
file.close()
#####################################################
#####################################################
if data["BOP-Tookit_Path_bool"]:
    sys.path.append(data["BOP-Tookit_Path"])
    sys.path.append(data["BOP-Tookit_Path"] + '/bop_toolkit_lib')
#####################################################
#####################################################

"""
Settings path
"""
bop_parent_path = data["bop_parent_path"]
bop_dataset_name = data["bop_dataset_name"]
cc_textures_path = data["cc_textures_path"]
output_dir = data["output_dir"]
external_obj = data["external_obj"]
external_object_model = data["clock_model"]
"""
list of objects to import
"""
list_bop_objects = data["list_bop_objects"]
"""
background en light plane
"""
side = float(data["side"])
min_intensity = float(data["min_intensity"])
max_intensity = float(data["max_intensity"])
color_1 = float(data["color_1"])
color_2 = float(data["color_2"])
light_plane_intensity = np.random.uniform(min_intensity, max_intensity)
light_plane_color = np.random.uniform([color_1, color_1, color_1, 1.0], [color_2, color_2, color_2, 1.0])
"""
point light
"""
random_placing = data["random_placing"]
random_intensity = data["random_intensity"]
random_color = data["random_color"]
point_light_intensity_min = float(data["point_light_intensity_min"])
point_light_intensity_max = float(data["point_light_intensity_max"])
min_elevation = float(data["min_elevation"])
max_elevation = float(data["max_elevation"])
"""
background
"""
use_backgrond = data["use_backgrond"]
change_background = data["change_background"]
change_ground_plane = data["change_ground_plane"]
number_of_it = float(data["number_of_it"])
if number_of_it == 0:
    number_of_it = 1
backgrounds = data["backgrounds"]
"""
number of poses and camera position
"""
number_of_poses = float(data["number_of_poses"])
camera_position = float(data["camera_position"])
projection_ground = float(data["projection_ground"])
max_distance_to_cam = float(data["max_distance_to_cam"])
min_distance_to_cam = float(data["min_distance_to_cam"])
print(max_distance_to_cam)
print(min_distance_to_cam)
"""
placing objects
"""
min_distance = float(data["min_distance"])
print(min_distance)
max_distance = float(data["max_distance"])
print(max_distance)
"""
output data
"""
output_coco = data["output_coco"]
output_hdf5 = data["output_hdf5"]
output_bop_data = data["output_bop_data"]

one_object_anno = data["one_object_anno"]
one_object_anno_id = int(data["one_object_anno_id"])

m_or_mm = data["m_or_mm"]

txt_record_file_extension = "" #"data/000000/"

"""
Open text file
"""

with open(os.path.join(output_dir, "readme.txt"), "w") as f:
    f.write("Date: " + str(date.today()) + "\n")
    f.write("Number of poses: " + str(number_of_poses) + "\n")
    f.write("Camera position: " + str(camera_position) + "\n")

    f.write("Light plane min int.: " + str(min_intensity) + "\n")
    f.write("Light plane max int.: " + str(max_intensity) + "\n")
    f.write("Light plane color 1: " + str(color_1) + "\n")
    f.write("Light plane color 2: " + str(color_2) + "\n")
    f.write("Light plane int.: " + str(light_plane_intensity) + "\n")
    f.write("Light plane color: " + str(light_plane_color) + "\n")

    f.write("Point light random: " + str(random_placing) + "\n")
    f.write("Point light int.: " + str(random_intensity) + "\n")
    f.write("Point light color: " + str(random_color) + "\n")

    f.write("Max distance objects: " + str(max_distance) + "\n")
    f.write("Min distance objects: " + str(min_distance) + "\n")

"""
Start BlenderProc
"""

# initialize BlenderProc
bproc.init()

if external_obj:
    # loading of external object
    # first, object with id 16 (.obj file)
    # second, object with id 17 (.ply file)
    sampled_bop_objs = bproc.loader.load_obj(filepath=os.path.join(external_object_model, "geometry2.obj"))
    sampled_bop_objs[0].set_scale([1, 1, 1])  # scaling of object / 3D model
    sampled_bop_objs[0].set_cp("category_id", 16)  # Set category id which will be used in the BopWriter
    sampled_bop_objs[0].set_name("obj_000016")  # Set name of object
    sampled_bop_objs[0].set_cp("supercategory", bop_dataset_name)

    sampled_bop_objs = bproc.loader.load_obj(filepath=os.path.join(external_object_model, "geometry2.ply"))
    sampled_bop_objs[0].set_scale([0.001, 0.001, 0.001])  # scaling of object / 3D model from mm to m
    sampled_bop_objs[0].set_cp("category_id", 17)  # Set category id which will be used in the BopWriter
    sampled_bop_objs[0].set_name("obj_000017")  # Set name of object
    sampled_bop_objs[0].set_cp("supercategory", bop_dataset_name)
    sampled_bop_objs[0].set_cp("supercategory", bop_dataset_name)

# load object form the BOP dataset
distractor_bop_objs = bproc.loader.load_bop_objs(bop_dataset_path=os.path.join(bop_parent_path, bop_dataset_name),
                                                 mm2m=True,
                                                 obj_ids=list_bop_objects,
                                                 num_of_objs_to_sample=len(list_bop_objects))

# set shading properties
for j, obj in enumerate(distractor_bop_objs):
    obj.set_shading_mode('auto')

# set if external object is used
if external_obj:
    objects_in_scene = sampled_bop_objs + distractor_bop_objs
else:
    objects_in_scene = distractor_bop_objs

# load BOP dataset intrinsics
bproc.loader.load_bop_intrinsics(bop_dataset_path=os.path.join(bop_parent_path, bop_dataset_name))

# define a function for making background
if use_backgrond:
    # sample CC Texture and assign to room planes
    cc_textures = bproc.loader.load_ccmaterials(cc_textures_path, used_assets=backgrounds)


def create_background(plane):
    """
    Function to random change or set the background of one plane

    Parameters:
        plane (bject):          list with planes to change the texture/background
        cc_textures (object):   dataset with textures (cc_textures)
    """
    random_cc_texture = np.random.choice(cc_textures)
    plane.replace_materials(random_cc_texture)


def create_background_plane(room_planes):
    """
    Function to random change or set the background of planes

    Parameters:
        room_planes (list, object):     list with planes to change the texture/background
        cc_textures (object):           dataset with textures (cc_textures)
    """
    random_cc_texture = np.random.choice(cc_textures)
    for plane in room_planes:
        plane.replace_materials(random_cc_texture)


# create a plane and set location (+ rotation)
# the planes form a box
room_planes = [bproc.object.create_primitive('PLANE', scale=[side, side, side/2]),
               bproc.object.create_primitive('PLANE', scale=[side, side, side/2], location=[0, -side, side], rotation=[-1.570796, 0, 0]),
               bproc.object.create_primitive('PLANE', scale=[side, side, side/2], location=[0, side, side], rotation=[1.570796, 0, 0]),
               bproc.object.create_primitive('PLANE', scale=[side, side, side/2], location=[side, 0, side], rotation=[0, -1.570796, 0]),
               bproc.object.create_primitive('PLANE', scale=[side, side, side/2], location=[-side, 0, side], rotation=[0, 1.570796, 0])]

# make light plane
# sample light color and strength from plane
light_plane = bproc.object.create_primitive('PLANE', scale=[side, side, 1], location=[0, 0, (side * 2 + 1)])
light_plane.set_name('light_plane')  # set name of plane to 'light_plane'
light_plane_material = bproc.material.create('light_material')  # set material of plane to 'light_material'
light_plane_material.make_emissive(emission_strength=light_plane_intensity,
                                   emission_color=light_plane_color)  # set random set strength/intensity of plane
light_plane.replace_materials(light_plane_material)

# when background is used, set the background
if use_backgrond:
    create_background_plane(room_planes)
    # when ground plane should be a different texture
    if change_ground_plane:
        create_background(room_planes[0])


def sample_position():
    """
    Set camera location
    """
    if camera_position == 3:
        location_sample_camera = np.random.uniform([-side * 0.8, -side * 0.8, 0], [side * 0.3, side * 0.3, 0])
    elif camera_position == 4:
        location_sample_camera = np.random.uniform([-side * 0.8, -side * 0.25, 0], [-side * 0.35, side * 0.25, 0])
    else:
        location_sample_camera = np.random.uniform([-side / 3, -side / 3, 0], [side / 3, side / 3, 0])
    return location_sample_camera


def sample_target():
    """
    Sample location of object depending of used camera
        function to sample onto a different area for target object(s)
    """
    if camera_position == 3:
        location_sample_obj = np.random.uniform([-side * 0.65, -side * 0.65, 0], [-side * 0.4, -side * 0.4, 0])
        if (location_sample_obj[0] < -side * 0.5) & (location_sample_obj[1] < -side * 0.5):
            if np.random.random() > 0.5:
                location_sample_obj += np.array([0.3, -0.3, 0])
            else:
                location_sample_obj += np.array([-0.3, 0.3, 0])
        print(location_sample_obj)
    elif camera_position == 4:
        location_sample_obj = np.random.uniform([-side * 0.7, -side * 0.15, 0], [-side * 0.45, side * 0.15, 0])
    else:
        location_sample_obj = np.random.uniform([-side / 3, -side / 3, 0], [side / 3, side / 3, 0])
    return location_sample_obj


def sample_pose(obj: bproc.types.MeshObject):
    """
    Function that samples the pose of a given object
        Depending a the object id of object name the area to sample of changed

    Parameters:
        obj (object mesh):   object to sample
    """
    # set position of object
    if (obj.get_name() == "obj_000017") or (obj.get_cp("category_id") == one_object_anno_id):
        location_sample_obj = sample_target()
    else:
        location_sample_obj = sample_position()
    if camera_position == 3:
        # check projected distance on ground plane
        while check_distance_form_obj_to_cam(location_sample_obj) is False:
            if (obj.get_name() == "obj_000017") or (obj.get_cp("category_id") == one_object_anno_id):
                location_sample_obj = sample_target()
            else:
                location_sample_obj = sample_position()
    obj.set_location(location_sample_obj)

    # set rotation of object
    if obj.get_name() == "obj_000015":
        obj.set_rotation_euler([np.pi / 2, 0, np.random.uniform(0, np.pi * 2)])
    elif obj.get_name() == "obj_000016":
        obj.set_rotation_euler([0, -np.pi / 2, np.random.uniform(0, np.pi * 2)])
        # set random rotation of object
        # obj.set_rotation_euler([np.random.uniform(-np.pi * 2, np.pi * 2),
        #                           np.random.uniform(-np.pi * 2, np.pi * 2),
        #                           np.random.uniform(0, np.pi * 2)])
    elif obj.get_name() == "obj_000017":
        i = np.random.random() * 4
        if i < 1:
            obj.set_rotation_euler([0, 0, np.random.uniform(0, np.pi * 2)])
        elif (i > 1) and (i < 2):
            obj.set_rotation_euler([0, np.random.uniform(0, np.pi * 2), np.random.uniform(0, np.pi * 2)])
        elif (i > 2) and (i < 3):
            obj.set_rotation_euler([np.random.uniform(0, np.pi * 2), 0, np.random.uniform(0, np.pi * 2)])
        else:
            obj.set_rotation_euler([np.random.uniform(0, np.pi * 2), np.random.uniform(0, np.pi * 2), np.random.uniform(0, np.pi * 2)])
    else:
        obj.set_rotation_euler([0, 0, np.random.uniform(0, np.pi * 2)])
        # set random rotation of object
        # obj.set_rotation_euler([np.random.uniform(-np.pi * 2, np.pi * 2),
        #                           np.random.uniform(-np.pi * 2, np.pi * 2),
        #                           np.random.uniform(0, np.pi * 2)])


def check_distance_form_obj_to_cam(location_sample_obj):
    """
    Function to check the projected distance on the ground plane between the camera and an object

    Parameters:
        location_sample_obj (array):    3D location of object
    """
    if projection_ground:
        distance_to_cam = (location_sample_obj[0] + side) ** 2 + (location_sample_obj[1] + side) ** 2
    else:
        return True
    if (distance_to_cam ** 0.5) > (max_distance_to_cam) or (distance_to_cam ** 0.5) < (min_distance_to_cam ):
        return False
    else:
        return True


def point_light_reset_location(light_point):
    """
    Function to random change or set to position of point light

    Parameters:
        light_point (object):   point light
    """
    location = bproc.sampler.shell(center=[0, 0, 0], radius_min=1, radius_max=side / 2,
                                   elevation_min=min_elevation, elevation_max=max_elevation, uniform_volume=False)
    light_point.set_location(location)
    with open(os.path.join(output_dir, "readme.txt"), "a") as f:
        f.writelines("Location point light: " + str(location) + "\n")


def point_light_reset_intensity(light_point):
    """
    Function to random change or set the strength/intensity of point light

    Parameters:
        light_point (object):   point light
    """
    energy = np.random.uniform(point_light_intensity_min, point_light_intensity_max)
    light_point.set_energy(energy)
    with open(os.path.join(output_dir, "readme.txt"), "a") as f:
        f.writelines("Intensity point light: " + str(energy) + "\n")


def point_light_reset_color(light_point):
    """
    Function to random change or set the color of point light

    Parameters:
        light_point (object):   point light
    """
    color = np.random.uniform([color_1, color_1, color_1], [color_2, color_2, color_2])
    light_point.set_color(color)
    with open(os.path.join(output_dir, "readme.txt"), "a") as f:
        f.writelines("Color point light: " + str(color) + "\n")


def point_light():
    """
    Function to initialize light point
    """
    light_point = bproc.types.Light()
    if not random_placing:
        point_light_reset_location(light_point)
    if not random_intensity:
        point_light_reset_intensity(light_point)
    if not random_color:
        point_light_reset_color(light_point)
    return light_point


# make light point
light_point = point_light()
light_point_2 = point_light()

# set camera location and point of interest
if camera_position == 1:
    # sample camera location in a shell
    location = bproc.sampler.shell(center=[0, 0, 0],  # center of shell
                                   radius_min=1.2,  # maximum radius
                                   radius_max=1.5,  # minimum radius
                                    elevation_min=30,  # minimum elevation in degrees
                                   elevation_max=50,  # maximum elevation in degrees
                                   uniform_volume=False)
elif camera_position == 2:
    location = np.array([0, 0, side * 2])
    poi = np.array([0, 0, 0])
elif camera_position == 3:
    location = np.array([-side, -side, side/3])
    poi = np.array([side / 2, side / 2, -side/4])
elif camera_position == 4:
    location = np.array([-side, 0, side/4])
    poi = np.array([-side/4, 0, 0])

# for camera 2, 3 and 4 build camera matrix
if camera_position > 1:
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=0)
    # Add homog cam pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)

# activate depth rendering
bproc.renderer.enable_depth_output(activate_antialiasing=False)
bproc.renderer.set_max_amount_of_samples(50)

# loop to make scenes
poses = 0
while poses < number_of_poses:
    with open(os.path.join(output_dir, "readme.txt"), "a") as f:
        f.write("Poses: " + str(poses) + "\n")

    # first, reset the scene
    bproc.utility.reset_keyframes()

    # when True, reset location of light points
    if random_placing:
        point_light_reset_location(light_point)
        point_light_reset_location(light_point_2)

    # when True, reset strength/intensity of light points
    if random_intensity:
        point_light_reset_intensity(light_point)
        point_light_reset_intensity(light_point_2)

    # when True, reset color of light points
    if random_color:
        point_light_reset_color(light_point)
        point_light_reset_color(light_point_2)

    # when True, check if object placement should be changed
    if use_backgrond:
        if (poses%number_of_it) == 0 and poses != 0:
            if change_background:
                create_background_plane(room_planes)
        # when True, change the texture of the ground plane
        if change_ground_plane:
            create_background(room_planes[0])

    # sample objects on surface
    placed_objects = bproc.object.sample_poses_on_surface(objects_to_sample=objects_in_scene,  # object to sample
                                                              surface=room_planes[0],  # plane of which to sample the object
                                                                # this is the ground plane
                                                              sample_pose_func=sample_pose,
                                                                # function to sample to objects
                                                              min_distance=min_distance,
                                                                # minimum distance between the center point of
                                                                # two consecutively placed objects
                                                              max_distance=max_distance)
                                                                # maximum distance between the center point of
                                                                # two consecutively placed objects

    for object in placed_objects:
        location_object = object.get_location()
        rotation_object = object.get_rotation()
        bbox = object.get_bound_box()
        origin_object = object.get_origin()
        name_object = object.get_name()
        with open(os.path.join(output_dir, "readme.txt"), "a") as f:
            f.write("Place " + str(name_object) + ": " + str(location_object) + "\n")
            f.write("Rotation " + str(name_object) + ": " + str(rotation_object) + "\n")
            f.write("bbox " + str(name_object) + ": " + str(bbox) + "\n")
            f.write("origin " + str(name_object) + ": " + str(origin_object) + "\n")

    # BVH tree used for camera obstacle checks
    bop_bvh_tree = bproc.object.create_bvh_tree_multi_objects(placed_objects)

    # when camera 1 is used
    if camera_position == 1:
        # set point of interest in scene for the camera
        # takes first placed object as point
        poi = bproc.object.compute_poi(np.random.choice(placed_objects, size=1))
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=0)
        # make homogeneous camera pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)

    # Check that obstacles are at least 0.3 meter away from the camera and make sure the view interesting enough
    if bproc.camera.perform_obstacle_in_view_check(cam2world_matrix, {"min": 0.3}, bop_bvh_tree):
        # set camera pose
        bproc.camera.add_camera_pose(cam2world_matrix)

    # when an object of interest is specified, only this object is written to the annotations
    # first, check that this object is present in the scene
    # if not, the rendering does not persist and a new scene is made
    render_true = False
    if one_object_anno:
        for obj in placed_objects:
            if obj.get_cp("category_id") == one_object_anno_id:
                render_true = True
    else:
        render_true = True

    if render_true:
        # render the whole pipeline
        data = bproc.renderer.render()
        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])
        data.update(seg_data)

        # increment pose
        poses += 1

        if output_coco:
            # Write data to coco format
            bproc.writer.write_coco_annotations(os.path.join(output_dir, 'coco_data'),
                                                supercategory='coco_annotations',
                                                instance_segmaps=seg_data["instance_segmaps"],
                                                instance_attribute_maps=seg_data["instance_attribute_maps"],
                                                colors=data["colors"],
                                                color_file_format="JPEG",
                                                append_to_existing_output=True)
        if output_hdf5:
            # write .hdf5 container
            # append to existing output is True
            bproc.writer.write_hdf5(output_dir, data, append_to_existing_output=True)

        # if one_object_anno is True
        # only the annotations of the object of interest (object with id equal to one_object_anno_id)
        # is written in the .json file
        if output_bop_data:
            annotation_object = []
            if one_object_anno:
                for obj in placed_objects:
                    if obj.get_cp("category_id") == one_object_anno_id:
                        annotation_object.append(obj)
            else:
                annotation_object.append(obj)

            # Write data in bop format
            bproc.writer.write_bop(output_dir,
                                   target_objects=annotation_object,
                                   dataset="",
                                   depths=data["depth"],
                                   depth_scale=1,
                                   colors=data["colors"],
                                   color_file_format="PNG",
                                   append_to_existing_output=True,
                                   m2mm=m_or_mm,
                                   frames_per_chunk=100000)

            # output .txt file with the number of poses
            with open(os.path.join(output_dir, "train.txt"), "a") as f:
                new_str = str(poses-1)
                f.write(txt_record_file_extension + new_str.zfill(6) + "\n")