#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from typing import List, Tuple

import cv2
from numpy import ndarray

from args import ArgParser
from client import Client
from debug import changeImage, loadDebugImages
from filters import PoseLandmarkComposition
from mediapipe_wrapper import Landmark, MediaPipePose
from visualizer import Visualizer


def getCamera(capDevice: int, capWidth: int, capHeight: int) -> cv2.VideoCapture:
    # カメラ
    cap = cv2.VideoCapture(capDevice)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, capWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, capHeight)
    return cap


def getImage(camera: cv2.VideoCapture) -> Tuple[ndarray, ndarray]:
    ret, image = camera.read()
    if not ret:
        raise ValueError("No camera detected.")

    image = cv2.flip(image, 1)
    debugImage = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    return image, debugImage


def applyFilter(
    pose: MediaPipePose,
    image: ndarray,
    filter: PoseLandmarkComposition | None,
    noLPF: bool,
) -> Tuple[List[Landmark] | None, List[Landmark] | None]:
    # 検出実施 #############################################################
    landmarks: list[Landmark] | None = pose.process(image)
    processed_landmarks: list[Landmark] | None = None

    if landmarks is None:
        return None, None
    else:
        processed_landmarks: list[Landmark] | None = copy.deepcopy(landmarks)

    if not noLPF:
        # フィルタ適用 #######################################################
        if filter is not None:
            processed_landmarks = filter.update(processed_landmarks)

    return landmarks, processed_landmarks


def sendData(data: list[Landmark], client: Client) -> None:
    converted: list[list[float]] = [
        [landmark["x"], landmark["y"], landmark["z"], landmark["visibility"]]
        for landmark in data
    ]
    client.Send(converted)


def draw(
    visualizer: Visualizer | None,
    debugImage: ndarray,
    landmarks: List[Landmark] | None,
    processed: List[Landmark],
    noLPF: bool,
) -> None:
    if visualizer is None:
        return None

    if landmarks is not None:
        # オリジナル
        visualizer.update(debugImage, landmarks, (0, 255, 0))

    if not noLPF:
        # フィルタ適用後
        visualizer.update(debugImage, processed, (255, 0, 0))

    visualizer.display_fps(debugImage)
    visualizer.show()


def changeMode(key: int) -> bool | None:
    if key == 100:  # D
        return True
    elif key == 114:  # R
        return False
    else:
        return None


def exitLoop(key: int) -> bool:
    # キー処理(ESC：終了) ############################################
    if key == 27:  # ESC
        print("exit")
        return True
    else:
        return False


def launchDebug(
    image: ndarray,
    visualizer: Visualizer | None,
    pose: MediaPipePose,
    filter: PoseLandmarkComposition | None,
    client: Client,
    noLPF: bool,
) -> None:
    debugImage: ndarray = image.copy()
    landmarks, processed = applyFilter(pose, image, filter, noLPF)

    if processed is not None:
        sendData(processed, client)
        draw(visualizer, debugImage, landmarks, processed, noLPF)


def launchCamera(
    camera: cv2.VideoCapture,
    visualizer: Visualizer | None,
    pose: MediaPipePose,
    filter: PoseLandmarkComposition | None,
    client: Client,
    noLPF: bool,
) -> None:
    # カメラキャプチャ #####################################################
    image, debugImage = getImage(camera)
    landmarks, processed_landmarks = applyFilter(pose, image, filter, noLPF)

    if processed_landmarks is not None:
        sendData(processed_landmarks, client)
        draw(visualizer, debugImage, landmarks, processed_landmarks, noLPF)


def run_mediapipe_socket(args: ArgParser) -> None:
    # 引数解析
    no_visualize: bool = args.no_visualize
    no_lpf: bool = args.no_lpf

    model_complexity: int = args.model_complexity
    min_detection_confidence: float = args.min_detection_confidence
    min_tracking_confidence: float = args.min_tracking_confidence
    enable_segmentation: bool = args.enable_segmentation
    use_brect: bool = args.use_brect

    # Load debug images
    debugImages: List[ndarray] = loadDebugImages()

    # UDP Client (for sending data)
    udpClient = Client(args.ip_address, args.port)

    # カメラ
    camera: cv2.VideoCapture = getCamera(args.device, args.width, args.height)

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

    debugging: bool = False
    index: int = 0

    while True:
        try:
            key = cv2.waitKey(1)

            if debugging:
                index = changeImage(index, len(debugImages), key)
                launchDebug(
                    debugImages[index], visualizer, pose, pose_filter, udpClient, no_lpf
                )
            else:
                launchCamera(camera, visualizer, pose, pose_filter, udpClient, no_lpf)

            mode = changeMode(key)
            if mode is None:
                pass
            else:
                debugging = mode

            # キー処理(ESC：終了) ############################################
            if exitLoop(key):
                break

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break
        except Exception as err:
            print(err)
            break

    camera.release()
