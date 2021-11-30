from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import cv2


def pfm_png(pfm_file_path):
    with open(pfm_file_path, 'rb') as pfm_file:
        header = pfm_file.readline().decode().rstrip()
        channel = 3 if header == 'PF' else 1

        dim_match = re.match(r'^(\d+)\s(\d+)\s$', pfm_file.readline().decode('utf-8'))
        if dim_match:
            width, height = map(int, dim_match.groups())
        else:
            raise Exception("Malformed PFM header.")

        scale = float(pfm_file.readline().decode().strip())
        if scale < 0:
            endian = '<'  # little endlian
            scale = -scale
        else:
            endian = '>'  # big endlian

        disparity = np.fromfile(pfm_file, endian + 'f')
        disparity = disparity / np.max(disparity) * 255

        img = np.reshape(disparity, newshape=(height, width))
        img = img.astype(np.uint8)
        color_map = cv2.applyColorMap(img, cv2.COLORMAP_TURBO)
        cv2.imwrite(filename="/home/wangqingyu/桌面/disparity_visualization/visualization/" + "19.png",
                    img=color_map, params=None
                    )


def main():
    pfm_file_path = "/home/wangqingyu/sceneflow示例数据集/FlyingThings3D/disparity/0006.pfm"
    pfm_png(pfm_file_path)


if __name__ == '__main__':
    main()
