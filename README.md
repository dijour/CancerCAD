# CancerCAD - A Carnegie Mellon University 15-112 Term Project

CancerCAD is a medical imaging tool to help doctors and patients understand the three-dimensional characteristics of tumors, using only two-dimensional tumor data (magnetic resonance images).

* Author: Dean Dijour
* Mentor: Lukas Peraza
* Instructors: David Kosbie & David Andersen

## DEPENDENCIES
* Python 3 (https://www.python.org/downloads/)
* OpenCV (http://docs.opencv.org/3.2.0/d5/de5/tutorial_py_setup_in_windows.html)
* Numpy (pip install numpy)
* Numpy-STL (pip install numpy-stl)
* Scipy (pip install scipy)
* MatplotLib (pip install matplotlib)
* PIL (pip install pillow)


## Running CancerCAD
Download the project as a ZIP file. Run the "Main.py" file, and select a directory for the MRI JPGs (sample images have been provided in this repository, in "Brain Folder").

## Video
https://www.youtube.com/watch?v=mPYeTJd8klQ

## Features
* High-precision manual two-dimensional tumor selection:
![drawing a blob](https://cloud.githubusercontent.com/assets/26984516/25586969/e2d17ff4-2e6f-11e7-90ca-9318b9388efa.png)
![finished drawing a blob](https://cloud.githubusercontent.com/assets/26984516/25586982/eaf2c756-2e6f-11e7-8462-41372ed6bac8.png)
* True-to-shape 3D modeling capabilities, as well as 3D printing functionality:
![3d working](https://cloud.githubusercontent.com/assets/26984516/25586763/d46015e4-2e6e-11e7-96d5-a735ef7b6a74.png)
* Automatic two-dimensional tumor detection via OpenCV "blob detector":
![2017-05-01 13_08_47-keypoints](https://cloud.githubusercontent.com/assets/26984516/25586885/69bf64d2-2e6f-11e7-8b72-530ed18eb7a7.png)

