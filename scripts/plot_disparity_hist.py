import matplotlib.pyplot as plt
import numpy as np
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
    return disparity


if __name__ == '__main__':
    plt.figure(figsize=(7, 4), dpi=100)
    # disparity = pfm_png()
    disparity = cv2.imread("/home/wangqingyu/PlantStereo/PlantStereo2021/pepper/training/disp_high_acc/000000.tiff", -1)
    # disparity = disparity[:, :, 0]
    disparity_height = disparity.shape[0]
    disparity_width = disparity.shape[1]
    disparity = np.reshape(disparity, [disparity_width * disparity_height])
    disparity[disparity == np.inf] = 0
    # 定义一个间隔大小
    a = 1
    # 得出组数
    group_number = int((np.max(disparity) - np.min(disparity)) / a)
    print(np.max(disparity))
    # 画出直方图
    plt.hist(x=disparity,
             bins=group_number,
             range=(0, 270),
             density=False,
             weights=None,
             cumulative=False,
             bottom=None,
             histtype='bar',
             align='mid',
             orientation='vertical',
             rwidth=None,
             log=False,
             color='darkblue',
             label=None,
             stacked=False
             )
    plt.xlabel("disparity")
    plt.ylabel("pixel number")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("/home/wangqingyu/桌面/disparity_hist.png", dpi=500)
    plt.show()
