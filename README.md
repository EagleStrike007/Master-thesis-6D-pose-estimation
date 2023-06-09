# 6D Object Pose Estimation Using Synthetic Training Data and Deep Learning: Evaluation on Real RGBD Data
This thesis was written to graduate from the joint program Industrial Engineering Technology offered by [UHasselt](https://www.uhasselt.be/nl) and [KU Leuven](https://www.kuleuven.be/kuleuven). The thesis was carried out in collaboration with KU Leuven research group [ACRO](https://iiw.kuleuven.be/onderzoek/acro).

<p align="center">
 <img src="images/uhasselt_kuleuven.png" width="500">
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
 <img src="images/ACRO.png" width="250">
</p>
The full text of the thesis can be found [TO BE ADDED].

# Abstract
6D Object pose estimation is applied in a variety of applications such as robotic manipulation, augmented reality and Human-Robot Collaboration (HRC). Recently, machine learning techniques such as neural networks have shown to be effective for the task of 6D pose estimation. These neural networks need much training data. Even more, these approaches often use real data as (part of) their training set. Because generating accurateand labelled real data is a hard and time-consuming process, synthetic data can be used to quickly generate data.

This thesis focuses on the implementation of a 6D pose estimation algorithm which is trained solely on synthetic data and tested on real data. First, an algorithm needs to be selected. Second, some synthetic data generation tools need to be implemented. Third, the chosen algorithm needs to be trained and evaluated on a real dataset.

A suitable algorithm named FFB6D was selected based on HRC specific criteria. To train this algorithm photorealistic rendering software named BlenderProc was used. In addition, a real dataset, including ground truth information was created using markers and/or an ICP algorithm. The algorithm was evaluated on the synthetic and real dataset. Most importantly, the results show that while using a synthetic training dataset, consisting of 80,000 synthetic RGBD images, FFB6D can achieve an accuracy of up to 84% when allowing an error of 2.0 cm on the real dataset.  It can thus be concluded that using BlenderProc is a valid way to train FFB6D for real world applications.

 # Followed method
The course of the thesis can be divided into 6 major parts: 
1. search the most promising 6D object pose estimation method through literature study
2. search and implement suitable synthetic data generation tool(s)
3. implement the chosen algorithm and verify its working principle
4. train the selected algorithm on synthetic data for the real object
5. create a real dataset, of a custom object, which includes ground truth information
6. evaluate the performance of the algorithm on the real dataset

 # Used software
From the literature study followed that the 6D pose estimation algorithm named FFB6D showed promising results. For synthetic data generation, software packages named BlenderProc an RasterTriangle were found. After installing FFB6D, BlenderProc and RasterTriangle, an attempt was made to reproduce the results given by the authors of FFB6D. Once it was validated that FFB6D worked as expected, some custom models were implemented. A synthetic training set was generated, as well as a real test dataset for the custom object. Real images, taken using a RealSense L515 RGBD camera, were annotated with ground truth information in order to be able to quantify FFB6D’s performance on the real dataset.

This repository is split into different folders to provide the most important scripts for each of the used software packages. These subfolders will elaborate on the different packages. The subfolders and their contents are:
1. BlenderProc: rendering scripts and example images
2. RasterTriangle: rendering script and example images
3. FFB6D: more detailed installation tutorial and most important scripts
4. Ground truth annotations and RealSense data capture script

# Results
Two real datasets were recorded and annotated. The two real datasets are:
<br>Dataset 1: static images of the driller and distractor objects (occluded + non-occluded scenes)
<br>Dataset 2: movie where the driller is moved across the field of view

FFB6D was trained on 80,000 BlenderProc training images for 15 epochs. The performance of the trained model is given in the table below.
<p align="center">
 <img src="images/table_results.png" width="600">
</p>
<br>The images below show some examples of scenes in dataset 1, with projected mask to visualise the predicted pose.<br>
<p align="center">
 <img src="images/example_1.jpg" width="300"> <img src="images/example_2.jpg" width="300">
</p>
<p align="center">
 <img src="images/example_3.jpg" width="300"> <img src="images/example_4.jpg" width="300">
</p>
The images below show some examples of scenes in dataset 2, with projected mask to visualise the predicted pose.<br>
<p align="center">
 <img src="images/example_5.jpg" width="300"> <img src="images/example_6.jpg" width="300">
</p>
<p align="center">
 <img src="images/example_7.jpg" width="300"> <img src="images/example_8.jpg" width="300">
</p>
 
