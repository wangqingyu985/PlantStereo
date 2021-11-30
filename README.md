# PlantStereo

This is the official implementation code for the paper "PlantStereo: A Stereo Matching Benchmark for Plant Surface Dense Reconstruction".

## Paper

PlantStereo: A Stereo Matching Benchmark for Plant Surface Dense Reconstruction

[](https://arxiv.org/submit/4051570/view)

Qingyu Wang, Baojian Ma, Wei Liu, Mingzhao Lou, Mingchuan Zhou*, Huanyu Jiang and Yibin Ying

College of Biosystems Engineering and Food Science, Zhejiang University.

## Example and Overview

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

###### Baidu Netdisk link



###### Google Drive link



## Contact

If you have any questions, please do not hesitate to contact us through E-mail!

12013027@zju.edu.cn or mczhou@zju.edu.cn