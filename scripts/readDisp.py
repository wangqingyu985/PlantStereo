import cv2
import numpy as np


def PlantStereo_min_max():
    my_image = cv2.imread("/home/wangqingyu/PlantStereo/PlantStereo2021/pumpkin/testing/disp_high_acc/000041.tiff", -1)
    height, width = my_image.shape
    now_min = 230
    now_max = 240
    my_image[my_image > 265] = 0
    for v in range(height):
        for u in range(width):
            if my_image[v, u] < now_min and my_image[v, u] != 0:
                now_min = my_image[v, u]
            if my_image[v, u] > now_max and my_image[v, u] != 0:
                now_max = my_image[v, u]
    print(now_min)
    print(now_max)

    for v in range(height):
        for u in range(width):
            if my_image[v, u] != 0:
                my_image[v, u] = (my_image[v, u] - 158) / (now_max - 158)
                my_image[v, u] = my_image[v, u] * 255
    my_image = my_image.astype(np.uint8)
    color_map = cv2.applyColorMap(my_image, cv2.COLORMAP_TURBO)
    cv2.imwrite(filename="/home/wangqingyu/桌面/" + "20" + ".png",
                img=color_map, params=None
                )


def cal_density():
    disparity_map = cv2.imread("/media/wangqingyu/机械硬盘2/立体匹配公开数据集/21_Cityscapes数据集(不完全)/disparity_trainvaltest/disparity/test/bielefeld/bielefeld_000000_008581_disparity.png")
    num_0 = np.sum(disparity_map == 0)
    num = disparity_map.shape[0] * disparity_map.shape[1]
    density = (num - num_0) / num * 100
    a = 1


if __name__ == '__main__':
    PlantStereo_min_max()
    # cal_density()
