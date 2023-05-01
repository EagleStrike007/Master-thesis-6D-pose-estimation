Training a neural network requires a large amount of data. The chosen algorithm, called FFB6D, uses RGB, depth and mask images as input data. Creating these images using a camera and setup is a very time-consuming and intensive process. Therefore, it was chosen to generate the data using an open-source software called BlenderProc. BlenderProc is a modular procedural pipeline for generating real looking images for the training of (convolutional) neural networks. BlenderProc is programmable in Python and built on the open-source rendering software Blender. On top of this, the BOP toolkit is being used to extend BlendeRProc to have more functionality. 

# Table of contents
1. Installation of BlenderProc and BOP toolkit 
2. Usage of BlenderProc
3. Implentation in Thesis 
  1. Implentation cutom object
  2. Scripts 
  3. Graphical User Interface
  4. Output data
