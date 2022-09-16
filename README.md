# UFEN-SLAM

## 1. Introduction

UFEN is an underwater feature extraction and matching network.
We use in-air RGBD data to generate synthetic underwater images and employ these as the medium to distil knowledge from a teacher model [SuperPoint](https://github.com/magicleap/SuperPointPretrainedNetwork).

Refer to [GCNv2](https://github.com/jiexiong2016/GCNv2_SLAM), We embed UFEN into the [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3) framework to replace the ORB feature. The code of UFEN-SLAM will be public shortly.

We also built a new underwater dataset in different water turbidities with groundtruth measurements named EASI.
The link of EASI can be found in [EASI Dataset](https://github.com/Jinghe-mel/UFEN-SLAM/tree/main/EASI%20Dataset).

## 2. Demo

![](Others/ORB1.gif)
