"""
    This is the epipole rectification code for ZED stereo camera.
    Need to calibrate the left and right camera before run the code.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def main():
    imgl = cv2.imread(filename='/home/wangqingyu/桌面/left.png', flags=0)
    imgr = cv2.imread(filename='/home/wangqingyu/桌面/right.png', flags=0)
    h, w = imgl.shape
    im_L = Image.fromarray(imgl)
    im_R = Image.fromarray(imgr)
    img_compare = Image.new('RGBA', (w * 2, h))
    img_compare.paste(im_L, box=(0, 0))
    img_compare.paste(im_R, box=(w, 0))
    line_num = 10
    for i in range(1, line_num):
        len = h / line_num
        plt.axhline(y=i * len, color='b', linestyle='-')
    plt.imshow(img_compare)
    plt.savefig('/home/wangqingyu/桌面/output-before.png')

    cml = np.array([[1386.8541, 0, 1094.9152],
                    [0, 1386.6979, 606.3491],
                    [0, 0, 1]])  # 3*3
    dcl = np.array([0.0092, -0.0275, 0, 0, 0])  # 1*5
    cmr = np.array([[1387.8287, 0, 1095.7680],
                    [0, 1387.3782, 605.0184],
                    [0, 0, 1]])  # 3*3
    dcr = np.array([0.0053, -0.0153, 0, 0, 0])  # 1*5
    R = np.array([[0.99999, 0.00050, -0.00080],
                 [-0.00050, 0.99999, 0.00080],
                 [0.00080, -0.00080, 0.99999]])  # 3*3
    T = np.array([[-119.9949],
                  [0.0158],
                  [-0.0369]]
                 )

    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cml, dcl, cmr, dcr, (w, h), R, T, 1, (0, 0))
    # only R1, R2, P1, P2 is useful
    Left_Stereo_Map = cv2.initUndistortRectifyMap(cml, dcl, R1, P1, (w, h), cv2.CV_16SC2)
    Right_Stereo_Map = cv2.initUndistortRectifyMap(cmr, dcr, R2, P2, (w, h), cv2.CV_16SC2)
    Left_rectified = cv2.remap(imgl, Left_Stereo_Map[0], Left_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    Right_rectified = cv2.remap(imgr, Right_Stereo_Map[0], Right_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    # cv2.imwrite('output/left_rectified.png', Left_rectified)
    # cv2.imwrite('output/right_rectified.png', Right_rectified)

    im_L = Image.fromarray(Left_rectified)
    im_R = Image.fromarray(Right_rectified)
    img_compare = Image.new('RGBA', (w * 2, h))
    img_compare.paste(im_L, box=(0, 0))
    img_compare.paste(im_R, box=(w, 0))

    for i in range(1, line_num):
        len = h/line_num
        plt.axhline(y=i*len, color='b', linestyle='-')
    plt.imshow(img_compare)
    plt.savefig('/home/wangqingyu/桌面/output.png')


if __name__ == '__main__':
    main()
