#!usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import copy

import cv2
import numpy
from mediapipe.python.solution_base import NamedTuple
from mediapipe.python.solutions import pose as mp_pose
from numpy import ndarray

from args import get_args
from json_parser import to_json
from udp_client import UdpClient
from visualize import calc_bounding_rect, draw_bounding_rect, draw_landmarks


def main() -> None:
    # 引数解析
    args: argparse.Namespace = get_args()
    debug: bool = args.debug
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

    while True:
        try:
            # カメラキャプチャ #####################################################
            ret, image = cap.read()
            if not ret:
                break
            image: ndarray = cv2.flip(image, 1)  # ミラー表示
            debug_image: ndarray = copy.deepcopy(image)

            # 検出実施 #############################################################
            image: ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result: NamedTuple = pose.process(image)

            # 描画 ################################################################
            if debug:
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
                    # 外接矩形の計算
                    brect = calc_bounding_rect(debug_image, result.pose_landmarks)
                    # 描画
                    debug_image = draw_landmarks(
                        debug_image,
                        result.pose_landmarks,
                        # upper_body_only,
                    )
                    debug_image = draw_bounding_rect(use_brect, debug_image, brect)

            # UDP送信 ##############################################################
            if result.pose_landmarks is not None:
                udpClient.send(
                    to_json(result.pose_landmarks).encode(), ("localhost", target_port)
                )

            # キー処理(ESC：終了) #################################################
            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break

            # 画面反映 #############################################################
            if debug:
                cv2.imshow("MediaPipe Pose Demo", debug_image)
        except Exception as e:
            print(e)
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
