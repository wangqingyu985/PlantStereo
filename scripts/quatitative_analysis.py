import cv2
import numpy as np
import pandas as pd


K_ZED_LEFT = np.array([[1385.8813, 0, 1093.5342],
                       [0, 1386.0066, 606.4279],
                       [0, 0, 1]], dtype=float)  # 3*3
K_MECH = np.array([[2734.9911, 0, 964.9017],
                   [0, 2734.7569, 622.0475],
                   [0, 0, 1]], dtype=float)  # 3*3
R_MECH_ZED = np.array([[0.99026077, 0.01803719, -0.13805172],
                       [-0.02128059, 0.99953026, -0.02205416],
                       [0.13758907, 0.02477719, 0.99017945]], dtype=float)  # 3*3
T_MECH_ZED = np.array([[36.5376164],
                       [-54.9934821],
                       [-23.49059584]], dtype=float)  # 3*1


def align_one_pixel(depth, mech_u, mech_v):
    i_mech = np.array([[mech_u], [mech_v], [1]], dtype=float)
    p_i_zed = np.dot(R_MECH_ZED, np.dot(np.linalg.inv(K_MECH), i_mech * depth)) + T_MECH_ZED
    i_zed = np.dot(K_ZED_LEFT, p_i_zed) * (1 / p_i_zed[2])
    return i_zed[0], i_zed[1]


def main():
    error_u_list = []
    error_v_list = []
    depth = cv2.imread('/home/wangqingyu/桌面/depth/1.tiff', -1)
    mech = cv2.imread('/home/wangqingyu/桌面/mech/1.png')
    left = cv2.imread('/home/wangqingyu/桌面/left/1.png')
    # cv2.imshow(winname='mech', mat=mech)
    # cv2.waitKey(0)

    _, corners_mech = cv2.findChessboardCorners(image=cv2.cvtColor(mech, cv2.COLOR_BGR2GRAY), patternSize=(8, 11))
    _, corners_left = cv2.findChessboardCorners(image=cv2.cvtColor(left, cv2.COLOR_BGR2GRAY), patternSize=(8, 11))
    draw_mech = cv2.drawChessboardCorners(image=mech, patternSize=(8, 11), corners=corners_mech, patternWasFound=_)
    draw_left = cv2.drawChessboardCorners(image=left, patternSize=(8, 11), corners=corners_left, patternWasFound=_)
    cv2.imwrite(filename='/home/wangqingyu/桌面/1.png', img=draw_mech, params=None)
    cv2.imwrite(filename='/home/wangqingyu/桌面/2.png', img=draw_left, params=None)
    assert corners_mech.shape[0] == corners_left.shape[0]
    for i in range(0, corners_mech.shape[0]):
        corner_mech = corners_mech[i, :, :]  # .astype(np.uint16)
        corner_left = corners_left[i, :, :]
        depthz = depth[round(corner_mech[0, 1]), round(corner_mech[0, 0])]
        u, v = align_one_pixel(depth=depthz, mech_u=corner_mech[0, 0], mech_v=corner_mech[0, 1])
        error_u = corner_left[0, 0] - u
        error_v = corner_left[0, 1] - v
        error_u_list.append(error_u)
        error_v_list.append(error_v)
    print(error_u_list)
    print(error_v_list)
    final_error_u_list = pd.DataFrame(data=error_u_list)
    final_error_v_list = pd.DataFrame(data=error_v_list)
    final_error_u_list.to_csv('/home/wangqingyu/桌面/1_u.csv')
    final_error_v_list.to_csv('/home/wangqingyu/桌面/1_v.csv')


if __name__ == '__main__':
    main()
