#!usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import copy
from parser import to_json

import cv2
import numpy as numpy
from mediapipe.python.solutions import pose as mp_pose

from args import get_args
from udp_client import UdpClient
from visualize import calc_bounding_rect, draw_bounding_rect, draw_landmarks


def main() -> None:
    # 引数解析
    args: argparse.Namespace = get_args()
    cap_device: str = args.device
    cap_width: int = args.width
    cap_height: int = args.height
    target_port: int = args.port
    model_complexity: int = args.model_complexity
    min_detection_confidence: float = args.min_detection_confidence
    min_tracking_confidence: float = args.min_tracking_confidence
    enable_segmentation: bool = args.enable_segmentation
    segmentation_score_th: float = args.segmentation_score_th
    use_brect: bool = args.use_brect

    # UDP Client
    udpClient = UdpClient(5007)
    # カメラ
    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード #############################################################
    pose = mp_pose.Pose(
        model_complexity=model_complexity,
        enable_segmentation=enable_segmentation,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    cnt: int = 0
    while True:
        # カメラキャプチャ #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv2.flip(image, 1)  # ミラー表示
        debug_image = copy.deepcopy(image)

        # 検出実施 #############################################################
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = pose.process(image)

        # 描画 ################################################################
        if enable_segmentation and result.segmentation_mask is not None:
            # セグメンテーション
            mask = (
                numpy.stack((result.segmentation_mask,) * 3, axis=-1)
                > segmentation_score_th
            )
            bg_resize_image = numpy.zeros(image.shape, dtype=numpy.uint8)
            bg_resize_image[:] = (0, 255, 0)
            debug_image = numpy.where(mask, debug_image, bg_resize_image)
        if result.pose_landmarks is not None:
            if (cnt % 10) == 0:
                # print(to_json(results.pose_landmarks))
                udpClient.send(
                    to_json(result.pose_landmarks).encode(), ("localhost", target_port)
                )
            # 外接矩形の計算
            brect = calc_bounding_rect(debug_image, result.pose_landmarks)
            # 描画
            debug_image = draw_landmarks(
                debug_image,
                result.pose_landmarks,
                # upper_body_only,
            )
            debug_image = draw_bounding_rect(use_brect, debug_image, brect)

        # キー処理(ESC：終了) #################################################
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break

        # 画面反映 #############################################################
        cv2.imshow("MediaPipe Pose Demo", debug_image)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
