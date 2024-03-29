# PlantStereo

This is the official implementation code for the paper "PlantStereo: A High Quality Stereo Matching Dataset for Plant Reconstruction".

## Paper

PlantStereo: A High Quality Stereo Matching Dataset for Plant Reconstruction[[link]](https://www.mdpi.com/2077-0472/13/2/330)

College of Biosystems Engineering and Food Science, Zhejiang University.

## Example and Overview

We give an example of our dataset, including spinach, tomato, pepper and pumpkin.

<img src="/imgs/example.png" width="100%" >

The data size and the resolution of the images are listed as follows:

|   Subset    | Train | Validation | Test | All  | Resolution |
| :---------: | :---: | :--------: | :--: | :--: | :--------: |
| **Spinach** |  160  |     40     | 100  | 300  |  1046×606  |
| **Tomato**  |  80   |     20     |  50  | 150  |  1040×603  |
| **Pepper**  |  150  |     30     |  32  | 212  |  1024×571  |
| **Pumpkin** |  80   |     20     |  50  | 150  |  1024×571  |
|   **All**   |  470  |    110     | 232  | 812  |            |

## Analysis

We evaluated the disparity distribution of different stereo matching datasets.

<img src="/imgs/disparity distribution.png" width="60%" >

## Format

The data was organized as the following format, where the sub-pixel level disparity images are saved as **.tiff** format, and the pixel level disparity images are saved as **.png** format.

```
PlantStereo

├── PlantStereo2021

│          ├── tomato

│          │          ├── training

│          │          │         ├── left_view

│          │          │          │         ├── 000000.png

│          │          │          │         ├── 000001.png

│          │          │          │         ├── ......

│          │          │          ├── right_view

│          │          │          │         ├── ......

│          │          │          ├── disp

│          │          │          │         ├── ......

│          │          │          ├── disp_high_acc

│          │          │          │         ├── 000000.tiff

│          │          │          │         ├── ......

│          │          ├── testing

│          │          │          ├── left_view

│          │          │          ├── right_view

│          │          │          ├── disp

│          │          │          ├── disp_high_acc

│          ├── spinach

│          ├── ......
```



## Download

You can use the following links to download out PlantStereo dataset.

###### [Google Drive link](https://drive.google.com/file/d/171GHcniSTh3NvWbTXsHjIa3KeU3qu8tL/view?usp=sharing)

## Usage

- sample.py

To construct the dataset, you can run the code in sample.py in your terminal:

```python
conda activate <your_anaconda_virtual_environment>
python sample.py --num 0
```

We can registrate the image and transformate the coordinate through function mech_zed_alignment():

```python
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
```

- epipole_rectification.py

  After collecting the left, right and disparity images throuth sample.py, we can perform epipole rectification on left and right images through epipole_rectification.py:

  ```python
  python epipole_rectification.py
  ```

## Citation

If you use our PlantStereo dataset in your research, please cite this publication:

```tex
@article{wang2023plantstereo,
  title={PlantStereo: A High Quality Stereo Matching Dataset for Plant Reconstruction},
  author={Wang, Qingyu and Wu, Dihua and Liu, Wei and Lou, Mingzhao and Jiang, Huanyu and Ying, Yibin and Zhou, Mingchuan},
  journal={Agriculture},
  volume={13},
  number={2},
  pages={330},
  year={2023},
  publisher={Multidisciplinary Digital Publishing Institute}
}
```

## Acknowledgements

This project is mainly based on: [zed-python-api](https://github.com/stereolabs/zed-python-api) and [mecheye_python_interface](https://github.com/MechMindRobotics/mecheye_python_interface), thanks to the authors.

## Contact

If you have any questions, please do not hesitate to contact us through E-mail or issue, we will reply as soon as possible.

12013027@zju.edu.cn or mczhou@zju.edu.cn