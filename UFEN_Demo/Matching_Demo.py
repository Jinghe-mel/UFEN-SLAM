from argparse import ArgumentParser as AP
import cv2
import numpy as np
import torch
import os

from utils.feature_matching import point_match_bina
from models.Super_network import SuperPointFrontend

if __name__ == '__main__':
    ap = AP()
    ap.add_argument('--model1_weight_path', default='weights/superpoint_v1.pth', type=str,
                    help="The original SuperPoint weight or other weights to compare")
    ap.add_argument('--model2_weight_path', default='weights/UFEN_v1.pth', type=str, help="Your weights")
    ap.add_argument('--img1_path', default='inputs/img1.png', type=str)
    ap.add_argument('--img2_path', default='inputs/img2.png', type=str)
    ap.add_argument('--save_path', default='outputs/', type=str)
    ap.add_argument('--prefer_id', default=1, type=int, help="name for saving the output plot")
    ap.add_argument('--binary_desc', default=True, type=bool, help="binary descriptor")
    ap.add_argument('--draw_all_matching', default=False, type=bool, help="draw wrong matching")
    # feature paras
    ap.add_argument('--score', default=0.001, type=float, help="threshold for selecting points")
    ap.add_argument('--max_num', default=1024, type=int, help="maximum feature points")
    ap.add_argument('--nms_dist', default=4, type=int)
    ap.add_argument('--border_remove', default=4, type=int)
    ap.add_argument('--cell', default=8, type=int)
    ap.add_argument('--matching_score', default=0.5, type=float, help="threshold for finding matching")
    args = ap.parse_args()

    teacher_model = SuperPointFrontend(args, model_id=0)
    test_model = SuperPointFrontend(args, model_id=1)
    point_match_bina(args, model=teacher_model, frame1=args.img1_path, frame2=args.img2_path)
    point_match_bina(args, model=test_model, frame1=args.img1_path, frame2=args.img2_path)


