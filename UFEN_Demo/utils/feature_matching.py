import numpy as np
import torch
import os
import cv2
from utils.utils import output_process


def image_process(input_image):
    CUDA_WORK = torch.cuda.is_available()
    device = torch.device("cuda" if CUDA_WORK else "cpu")
    input_image = cv2.imread(input_image)

    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    img = input_image.astype('float32') / 255.0
    H, W = img.shape[0], img.shape[1]
    inp = torch.from_numpy(img).to(device)
    inp = torch.autograd.Variable(inp).view(1, 1, H, W)
    out = (np.dstack((img, img, img)) * 255.).astype('uint8')
    return inp, out


def point_match_bina(args, model, frame1, frame2):
    img1, gray1 = image_process(frame1)
    img2, gray2 = image_process(frame2)

    semi1, coarse_desc1 = model.run(img1)
    semi2, coarse_desc2 = model.run(img2)

    pts1, desc1, _ = output_process(coarse_desc1, semi1, args)
    pts2, desc2, _ = output_process(coarse_desc2, semi2, args)

    b_desc1 = (desc1 + ((desc1 >= 0).astype(desc1.dtype) - desc1)) * 2.0 - 1.0
    b_desc1 = b_desc1.T
    b_desc2 = (desc2 + ((desc2 >= 0).astype(desc2.dtype) - desc2)) * 2.0 - 1.0
    b_desc2 = b_desc2.T

    b_desc1[b_desc1 < 0] = 0
    b_desc1 = b_desc1.astype(np.uint8)
    b_desc2[b_desc2 < 0] = 0
    b_desc2 = b_desc2.astype(np.uint8)

    cv_kpts1 = [cv2.KeyPoint(pts1[0][i], pts1[1][i], 1)
                for i in range(pts1.shape[1])]
    cv_kpts2 = [cv2.KeyPoint(pts2[0][i], pts2[1][i], 1)
                for i in range(pts2.shape[1])]

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(b_desc1, b_desc2)
    matches = [m for m in matches if m.distance < 255 * (1 - args.matching_score)]
    matches = sorted(matches, key=lambda x: x.distance)
    src_pts = np.float32([cv_kpts1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
    dst_pts = np.float32([cv_kpts2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)
    M, mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.RANSAC, 10)
    matchesMask = mask.ravel().tolist()
    r_match = []
    f_match = []
    for i in range(0, len(matchesMask)):
        if matchesMask[i] == 0:
            f_matches = matches[i]
            f_match.append(f_matches)
        else:
            r_matches = matches[i]
            r_match.append(r_matches)

    draw_matches = r_match
    if args.draw_all_matching:
        draw_matches = matches
    img_out = cv2.drawMatches(gray1, cv_kpts1, gray2, cv_kpts2, draw_matches,
                              None, matchColor=(0, 255, 255), singlePointColor=(255, 255, 255), flags=2)
    if model.model_id == 0:
        save_path = os.path.join(args.save_path, '%02d' % args.prefer_id + "_model1" + ".png")
    else:
        save_path = os.path.join(args.save_path, '%02d' % args.prefer_id + "_model2" + ".png")
    cv2.imwrite(save_path, img_out)

    num_pt = int((pts1.shape[1] + pts2.shape[1]) / 2)
    print(f"model id: {model.model_id}, feature num: {num_pt}, matching num: {len(r_match)}, "
          f"correct rate: {len(r_match) / len(matches):.2f}")
