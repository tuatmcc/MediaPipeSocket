#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

import cv2
from numpy import ndarray

from args import ArgParser
from filters import PoseLandmarkComposition
from json_parser import to_json
from mediapipe_wrapper import Landmark, MediaPipePose
from udp_client import UdpClient
from visualizer import Visualizer


def run_mediapipe_socket(args: ArgParser) -> None:
    # 引数解析
    no_visualize: bool = args.no_visualize
    no_lpf: bool = args.no_lpf
    cap_device = args.device
    cap_width: int = args.width
    cap_height: int = args.height
    target_port: int = args.port
    model_complexity: int = args.model_complexity
    min_detection_confidence: float = args.min_detection_confidence
    min_tracking_confidence: float = args.min_tracking_confidence
    enable_segmentation: bool = args.enable_segmentation
    use_brect: bool = args.use_brect

    # UDP Client (for sending data)
    udpClient = UdpClient()

    # カメラ
    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # ビジュアライザ
    visualizer = Visualizer(use_brect) if not no_visualize else None

    # ポーズ用のローパスフィルタ
    pose_filter = PoseLandmarkComposition() if not no_lpf else None

    # モデルロード
    pose = MediaPipePose(
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
                print("No Camera")
                break

            image: ndarray = cv2.flip(image, 1)  # ミラー表示
            debug_image: ndarray = copy.deepcopy(image)

            # 検出実施 #############################################################
            image: ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pose_landmarks: list[Landmark] | None = pose.process(image)

            if pose_landmarks is not None:
                # フィルタ適用 #######################################################
                processed_landmarks: list[Landmark] = copy.deepcopy(pose_landmarks)
                if not no_lpf and pose_filter is not None:
                    processed_landmarks = pose_filter.update(
                        copy.deepcopy(pose_landmarks)
                    )

                # UDP送信 ############################################################
                message = to_json(processed_landmarks).encode("utf-8")
                udpClient.send(
                    message,
                    ("localhost", target_port),
                )

                # 描画 ################################################################
                if not no_visualize and visualizer is not None:
                    # オリジナル
                    visualizer.update(
                        debug_image,
                        pose_landmarks,
                        color=(0, 255, 0),
                    )
                    if not no_lpf and pose_filter is not None:
                        # フィルタ適用後
                        visualizer.update(
                            debug_image,
                            processed_landmarks,
                            color=(0, 0, 255),
                        )
                    visualizer.display_fps(debug_image)
                    visualizer.show()

                    # キー処理(ESC：終了) ############################################
                    key = cv2.waitKey(1)
                    if key == 27:  # ESC
                        print("exit")
                        break

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break
        except Exception as err:
            print(err)
            break

    cap.release()
