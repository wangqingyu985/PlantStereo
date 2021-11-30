import cv2
import numpy as np


if __name__ == '__main__':

    mech_rotation_vector = np.array([-0.0008, -0.0008, -0.0005])
    zed_rotation_vector = np.array([0.0408, 0.0898, -2.7714])
    mech_translation_matrix = np.array([[-2.2206],
                                       [70.7245],
                                       [823.7151]])
    zed_translation_matrix = np.array([[-78.1540],
                                       [-2.3509],
                                       [793.2586]])

    mech_rotation_matrix = np.zeros(shape=(3, 3))
    cv2.Rodrigues(src=mech_rotation_vector, dst=mech_rotation_matrix)
    print(mech_rotation_matrix)

    zed_rotation_matrix = np.zeros(shape=(3, 3))
    cv2.Rodrigues(src=zed_rotation_vector, dst=zed_rotation_matrix)
    print(zed_rotation_matrix)

    mech_zed_rotation_matrix = np.dot(zed_rotation_matrix, np.linalg.inv(mech_rotation_matrix))
    print(mech_zed_rotation_matrix)

    mech_zed_translation_matrix = zed_translation_matrix - np.dot(np.dot(zed_rotation_matrix,
                                                                         np.linalg.inv(mech_rotation_matrix)),
                                                       mech_translation_matrix)
    print(mech_zed_translation_matrix)
