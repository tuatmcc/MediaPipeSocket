#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple, List
import copy

import cv2
import keyboard
from numpy import ndarray

from args import ArgParser
from debug import loadDebugImages, changeImage
from filters import PoseLandmarkComposition
from json_parser import to_json
from mediapipe_wrapper import Landmark, MediaPipePose
from udp_client import UDPClient, HOST_ADDRESS
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


def applyFilter(pose: MediaPipePose, image: ndarray, filter: PoseLandmarkComposition | None, noLPF: bool) -> Tuple[List[Landmark] | None, List[Landmark] | None]:
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


def sendData(data: List[Landmark], client: UDPClient) -> None:
    message = to_json(data).encode("utf-8")
    client.send(message)


def draw(visualizer: Visualizer | None, debugImage: ndarray, landmarks: List[Landmark] | None, processed: List[Landmark], noLPF: bool) -> None:
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


def exitLoop(keyCode: int) -> bool:
    # キー処理(ESC：終了) ############################################
    key = cv2.waitKey(1)
    if key == keyCode:  # ESC
        print("exit")
        return True
    else:
        return False


def launchDebug(images: List[ndarray], visualizer: Visualizer | None, pose: MediaPipePose, filter: PoseLandmarkComposition | None, noLPF: bool) -> None:
    image: ndarray = changeImage(images)
    landmarks, processed = applyFilter(pose, copy.deepcopy(image), filter, noLPF)

    if processed is not None:
        #sendData(processed_landmarks, udpClient)
        draw(visualizer, image, landmarks, processed, noLPF)


def launchCamera(camera: cv2.VideoCapture, visualizer: Visualizer | None, pose: MediaPipePose, filter: PoseLandmarkComposition | None, noLPF: bool) -> None:
    # カメラキャプチャ #####################################################
    image, debugImage = getImage(camera)
    landmarks, processed_landmarks = applyFilter(pose, image, filter, noLPF)

    if processed_landmarks is not None:
        #sendData(processed_landmarks, udpClient)
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
    udpClient = UDPClient(HOST_ADDRESS, args.port)

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

    while True:
        try:
            if debugging:
                launchDebug(debugImages, visualizer, pose, pose_filter, no_lpf)
            else:
                launchCamera(camera, visualizer, pose, pose_filter, no_lpf)

            # キー処理(ESC：終了) ############################################
            if exitLoop(27):
                break

            if keyboard.is_pressed("F1"):
                debugging = True
            elif keyboard.is_pressed("F2"):
                debugging = False
            else:
                pass

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break
        except Exception as err:
            print(err)
            break

    camera.release()
