[RasterTraingle](https://github.com/ethnhe/raster_triangle) is a non-photorealtic rendering software created by the creators of FFB6D. It is a simple renderer for synthesis data with as input a mesh and poses, and as output the rendered RGB image, depth image, mask image and annotations. Each set of images (RGB, depth and mask) along with their annotation are stored in a .pkl-file. RasterTriangle can create two types of data named *Rendered* and *Fused*. 

# Table of contents 
1. Installation of RasterTriangle 
2. *Rendered* data
3. *Fused* data
4. Change to RasterTriangle

# Installation of RasterTriangle

# *Rendered* data

**Note:** the poses are saved per object in a pkl file. This contains 70,000 poses and this for each object separately. This means that it is possible to generate the same images each time but the number is also limited to the amount in the .pkl-files.

<img src="images/example_render_rgb.png" width="300"> <img src="images/example_render_depth.png" width="300"> <img src="images/example_render_mask.png" width="300">

# *Fused* data

<img src="images/example_fuse_rgb.png" width="300"> <img src="images/example_fuse_depth.png" width="300"> <img src="images/example_fuse_mask.png" width="300">

# Change to RasterTriangle
