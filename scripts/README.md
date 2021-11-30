# Mech-Eye_python_interface
This is official Python interfaces for Mech-Eye cameras. If the version of MechEye camera is older than 1.2.0, please switch to older versions of sdk, see tags.

## Introduction

This project is developped by python. We use ZeroMQ library to connect camera devices in the LANs. And json is used to pack and unpack data from network. Supported on both Windows and Ubuntu OS.

## Features

By using these interfaces, you can easily control your mech_eye cameras in python programs. The features are as follows:

* Connect to your camera in your LANS.
* Set and get camera parameters like exposure time, period and so on.
* Get color images and depth images as numpy arrays.
* Get point cloud data as the format defined in open3d, a python lib which can deal with point clouds.

## Installation

We ran and tested interfaces on Python3.x. Make sure to install Python 3.x.

These python libraries are needed:

* opencv_python
* json
* open3d
* ZeroMQ

All these you can install with pip, by the following command:

```
pip3 install opencv-python json open3d zmq
```

Then clone this repo and you are good to go.

## Quick Start

In terminal, change your working directory to the repo, then in  **sample.py**, modify the IP address in line19 to your actual camera address, then run:

```powershell
python sample.py
```

Then a window will pop up and show point clouds. Some pictures will also be captured and stored in the same directory of the repo.

## Project hierarchy

The following shows the hierarchy of project files:

```
Mech-Eye_python_interface

├─ CameraClient.py
├─ README.md
├─ ZmqClient.py
└─ sample.py
```

CameraClient.py and ZmqClient.py contains most essential code for interfaces. 

## Brief Intro to interfaces

All interfaces and functions are in  **CameraClient.py**.

There are two main classes: CameraClient and ZmqClient. CameraClient is subclass of ZmqClient. You only need to focus on CameraClient.

* **CameraClient**
  * **connect()** : connect to the camera according to its IP address.

  * **captureDepthImg()** : capture a depth image and return it.

  * **captureColorImg()** : capture a color image and return it.

  * **getCameraIntri()**: get camera's intrinsic parameters.

  * **getCameraInfo()**: get camera's  some information, such as version, id, and temperature.

  * **getCameraVersion()**: get camera's version number.

  * **getColorImgSize()** : get the height and width of the color image to be captured.

  * **getDepthImgSize()** : get the height and width of the depth image to be captured.

  * **getParameter()** : get the value of a specific parameter in camera.

  * **setParameter()** : set the value of a specific parameter in camera.

    **Attention**: Please be sure to know the meaning of your setting of parameters, **wrong setting could cause some errors in the interfaces!**

  * **captureCloud()** : get a point cloud, open3d is used to store and process cloud data.

### Intro to samples

The original project provides a **sample.py** to show how to use interfaces. 

This sample mainly shows how to set camera's paramters like exposure time.

First, we need to know the actual IP address of camera and set it, and then connect:

```python
camera = CameraClient()
save_file = True
# camera IP should be modified to actual IP address
camera_ip = "192.168.3.146"
# always set IP before do anything else
if not camera.connect(camera_ip):
	exit(-1)

```

Then, we can get some brief info about camera:

```python
intri = camera.getCameraIntri()
print ("Camera Info: %s" % (camera.getCameraInfo())) 
print ("Camera ID: %s" % (camera.getCameraId()))
print ("Version: %s" % (camera.getCameraVersion()))
print ("Color Image Size: %s %s" % (camera.getColorImgSize()))
print ("Depth Image Size: %s %s" % (camera.getDepthImgSize()))
```

We can set and get the value of a specific parameter, in this case, we choose exposure time for color image:

```python
camera.setParameter("scan2dExposureMode", 0) # set exposure mode to Timed
print(camera.getParameter("scan2dExposureMode"))
camera.setParameter("scan2dExposureTime",20) # set exposure time to 20ms
print(camera.getParameter("scan2dExposureTime"))
```

We can capture color images and depth images by camera as arrays and also save them:

```python
if save_file:
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    cv2.imwrite(SAVE_PATH + "/mechmind_depth.png", depth)
    cv2.imwrite(SAVE_PATH + "/mechmind_color.jpg", color)
```



And also point clouds will be captured. We use open3d to show the point cloud.

```python
pcd = camera.captureCloud()
open3d.visualization.draw_geometries([pcd])
```

