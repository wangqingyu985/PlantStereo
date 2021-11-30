from CameraClient import CameraClient, ImageType, Command, CameraIntri
import pyzed.sl as sl
import numpy as np
import open3d
from os.path import join
import sys
import argparse
import cv2
import os
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


SAVE_PATH = "/home/wangqingyu/桌面/mecheye_python_interface"
MECHEYE_IP = "169.254.108.2"
ZED_BASELINE = 0.1216
ZED_FOCAL_LENGTH = 1384.4
SAVE_FILE = True
K_ZED_LEFT = np.array([[1385.8813, 0, 1093.5342],
                       [0, 1386.0066, 606.4279],
                       [0, 0, 1]], dtype=float)  # 3*3
K_MECH = np.array([[2734.9911, 0, 964.9017],
                   [0, 2734.7569, 622.0475],
                   [0, 0, 1]], dtype=float)  # 3*3
R_MECH_ZED = np.array([[0.99022184, 0.01741097, -0.13840878],
                       [-0.02072163, 0.99953165, -0.0225139],
                       [0.13795202, 0.02516189, 0.990118958]], dtype=float)  # 3*3
T_MECH_ZED = np.array([[36.8203540533],
                       [-54.5903607433],
                       [-23.53339511167]], dtype=float)  # 3*1


def connect_to_mecheye(camera_ip):
    camera = CameraClient()
    camera_ip = camera_ip
    if not camera.connect(camera_ip):
        exit(-1)
    return camera


def set_mech_exposure(exposure_mode, exposure_time):
    camera.setParameter(paraName="scan2dExposureMode", value=exposure_mode)
    camera.setParameter(paraName="scan2dExposureTime", value=exposure_time)


def zed_capture():
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD2K  # Use 2K video mode
    init_params.camera_fps = 30  # Set fps at 30

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    i = 0
    image_left = sl.Mat()
    image_right = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()
    while i < 5:
        # Grab an image, a RuntimeParameters object must be given to grab()
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # A new image is available if grab() returns SUCCESS
            zed.retrieve_image(image_left, sl.VIEW.LEFT)
            zed.retrieve_image(image_right, sl.VIEW.RIGHT)
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)
            # Get the timestamp at the time the image was captured
            print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image_left.get_width(),
                                                                                 image_left.get_height(),
                  timestamp.get_milliseconds()))
            i = i + 1

    if SAVE_FILE:
        image_left = image_left.get_data()[:, :, :3]
        image_right = image_right.get_data()[:, :, :3]
        cv2.imwrite(SAVE_PATH + "/uncrop_left.png", image_left)
        cv2.imwrite(SAVE_PATH + "/uncrop_right.png", image_right)
    zed.close()
    return image_left, image_right, image_left.shape[0], image_left.shape[1]


def mech_zed_alignment(depth, mech_height, mech_width, zed_height, zed_width):
    ground_truth = np.zeros(shape=(zed_height, zed_width), dtype=float)
    for v in range(0, mech_height):
        for u in range(0, mech_width):
            i_mech = np.array([[u], [v], [1]], dtype=float)  # 3*1
            p_i_mech = np.dot(np.linalg.inv(K_MECH), i_mech * depth[v, u])  # 3*1
            p_i_zed = np.dot(R_MECH_ZED, p_i_mech) + T_MECH_ZED  # 3*1
            i_zed = np.dot(K_ZED_LEFT, p_i_zed) * (1 / p_i_zed[2])  # 3*1
            disparity = ZED_BASELINE * ZED_FOCAL_LENGTH * 1000 / p_i_zed[2]
            u_zed = i_zed[0]
            v_zed = i_zed[1]
            coor_u_zed = round(u_zed[0])
            coor_v_zed = round(v_zed[0])
            if coor_u_zed < zed_width and coor_v_zed < zed_height:
                ground_truth[coor_v_zed][coor_u_zed] = disparity
    return ground_truth


def align_one_pixel(depth, mech_u, mech_v):
    i_mech = np.array([[mech_u], [mech_v], [1]], dtype=float)  # 3*1
    p_i_mech = np.dot(np.linalg.inv(K_MECH), i_mech * depth)  # 3*1
    p_i_zed = np.dot(R_MECH_ZED, p_i_mech) + T_MECH_ZED  # 3*1
    i_zed = np.dot(K_ZED_LEFT, p_i_zed) * (1 / p_i_zed[2])  # 3*1
    u_zed = i_zed[0]
    v_zed = i_zed[1]
    zed_u = round(u_zed[0])
    zed_v = round(v_zed[0])
    return zed_u, zed_v


def visualize_ground_truth(disparity_map):
    plt.figure(figsize=(23.08, 13))
    plt.axis('off')
    plt.imshow(disparity_map)
    plt.colorbar()  # orientation="horizontal"
    plt.savefig(SAVE_PATH + "/ground_truth.png", dpi=100)


def main(number):
    """
    # get some parameters of the mech camera
    intri = camera.getCameraIntri()
    fx, fy, u0, v0 = intri[0], intri[1], intri[2], intri[3]
    mech_color_width, mech_color_height = camera.getColorImgSize()
    mech_depth_width, mech_depth_height = camera.getDepthImgSize()

    # set exposure mode to 0 and exposure time to 300ms
    set_mech_exposure(exposure_mode=0, exposure_time=300)

    # capture depth image and color image and save them
    depth = camera.captureDepthImg()
    color = camera.captureColorImg()
    if len(depth) == 0 or len(color) == 0:
        exit(-2)
    if SAVE_FILE:
        if not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH)
        cv2.imwrite(SAVE_PATH + "/mechmind_color.png", color)

    # get rgb point cloud. Using open3d to store and visualize the cloud.
    # pcd = camera.captureCloud()
    # open3d.visualization.draw_geometries([pcd])
    # open3d.io.write_point_cloud(filename=SAVE_PATH + "/mechmind_pointcloud.pcd", pointcloud=pcd)
    """

    # capture left image and right image from zed camera
    image_left, image_right, zed_height, zed_width = zed_capture()
    cv2.imwrite(filename='/home/wangqingyu/桌面/left/9.png', img=image_left)
    cv2.imwrite(filename='/home/wangqingyu/桌面/right/9.png', img=image_right)

    cv2.imwrite(filename=SAVE_PATH + "/depth.tiff", img=depth)

    # align mech to zed
    ground_truth = mech_zed_alignment(depth=depth,
                                      mech_height=mech_depth_height,
                                      mech_width=mech_depth_width,
                                      zed_height=zed_height,
                                      zed_width=zed_width
                                      )
    cv2.imwrite(filename=SAVE_PATH + "/uncrop_ground_truth.png", img=ground_truth)

    # visualize the ground truth disparity map
    visualize_ground_truth(disparity_map=ground_truth)

    # crop the left, right and ground truth image
    uncrop_left = image_left
    uncrop_right = image_right
    uncrop_ground_truth = ground_truth
    left_top_u, left_top_v = align_one_pixel(depth=depth[10, 10], mech_v=11, mech_u=27)
    right_down_u, right_down_v = align_one_pixel(depth=depth[mech_depth_height - 1, mech_depth_width - 1 - 90],
                                                 mech_u=mech_depth_width, mech_v=mech_depth_height - 90)
    crop_left = uncrop_left[left_top_v:right_down_v, left_top_u:right_down_u, :]
    crop_right = uncrop_right[left_top_v:right_down_v, left_top_u:right_down_u, :]
    crop_ground_truth = uncrop_ground_truth[left_top_v:right_down_v, left_top_u:right_down_u]

    fmt = '{:06}.png'
    fmt_high_acc = '{:06}.tiff'

    cv2.imwrite(filename=join('/home/wangqingyu/PlantStereo/PlantStereo2021/pepper/testing/left_view/', fmt.format(number)), img=crop_left)
    cv2.imwrite(filename=join('/home/wangqingyu/PlantStereo/PlantStereo2021/pepper/testing/right_view/', fmt.format(number)), img=crop_right)
    cv2.imwrite(filename=join('/home/wangqingyu/PlantStereo/PlantStereo2021/pepper/testing/disp_high_acc/', fmt_high_acc.format(number)), img=crop_ground_truth)
    cv2.imwrite(filename=join('/home/wangqingyu/PlantStereo/PlantStereo2021/pepper/testing/disp/', fmt.format(number)), img=crop_ground_truth)
    visualize_ground_truth(disparity_map=crop_ground_truth)

    exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', default=0, type=int, help='number of the dataset')
    args = parser.parse_args()

    number = args.num
    # connect to mech-mind camera
    # camera = connect_to_mecheye(camera_ip=MECHEYE_IP)
    main(number)
