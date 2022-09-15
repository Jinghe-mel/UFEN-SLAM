## UFEN-SLAM

# 1. Introduction

UFEN is an underwater feature extraction and matching network.
We use in-air RGBD data to generate synthetic underwater images and employ these as the medium to distil knowledge from a teacher model [SuperPoint](https://github.com/magicleap/SuperPointPretrainedNetwork).

We embed UFEN into the [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3) framework to replace the ORB feature. The code of UFEN-SLAM will be public shortly.

We also built a new underwater dataset in different water turbidities with groundtruth measurements named EASI.
