#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from typing import List, Tuple

import cv2
from numpy import ndarray

# from args import ArgParser
# from client import Client
# from debug import changeImage, loadDebugImages
# from filters import PoseLandmarkComposition
# from introduce import getFrame, loadVideoFiles, showVideoFrame
# from mediapipe_wrapper import Landmark, MediaPipePose
# from visualizer import Visualizer

from args import ArgParser
from client import Client, CreateClient
from debug import Debugger
from introduce import Introduction
from visualizer import Visualizer
from filters import PoseLandmarkComposition
from mediapipe_wrapper import Landmark, MediaPipePose


class STATES:
    DEBUG: int = 0
    GAME: int = 1
    QUIT: int = 2


class MediaPipeSocketRunner:
    def __init__(self, args: ArgParser) -> None:
        self.argments: ArgParser = args

        self.cam1 = cv2.VideoCapture(self.argments.device)
        self.cam1.set(cv2.CAP_PROP_FRAME_WIDTH, self.argments.width)
        self.cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, self.argments.height)

        self.cam2: cv2.VideoCapture | None = None
        if self.argments.secondary_device != -1:
            print("Secondary camera detected.")
            self.cam2 = cv2.VideoCapture(self.argments.secondary_device)
            self.cam2.set(cv2.CAP_PROP_FRAME_WIDTH, self.argments.width)
            self.cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, self.argments.height)

        self.capturingVisulalizer: Visualizer = Visualizer(self.argments.use_brect)
        self.filter: PoseLandmarkComposition = PoseLandmarkComposition()
        self.model: MediaPipePose = MediaPipePose(
            model_complexity=self.argments.model_complexity,
            enable_segmentation=self.argments.enable_segmentation,
            min_detection_confidence=self.argments.min_detection_confidence,
            min_tracking_confidence=self.argments.min_tracking_confidence,
        )
        self.introduce: Introduction | None = None
        self.debugger: Debugger | None = None
        self.oscClient: Client = CreateClient(args.ip_address, args.port)
        self.state: int = STATES.GAME

        self.GetCameras()
        if not self.argments.no_intro:
            self.CreateIntroduce()
        if not self.argments.no_debug:
            self.CreateDebugger()

    def GetCameras(self) -> None:
        self.cam1 = cv2.VideoCapture(self.argments.device)
        self.cam1.set(cv2.CAP_PROP_FRAME_WIDTH, self.argments.width)
        self.cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, self.argments.height)

        if self.argments.secondary_device != -1:
            self.cam2 = cv2.VideoCapture(self.argments.secondary_device)
            self.cam2.set(cv2.CAP_PROP_FRAME_WIDTH, self.argments.width)
            self.cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, self.argments.height)

    def GetImage(self) -> ndarray:
        if self.debugger is not None and self.state == STATES.DEBUG:
            return self.debugger.GetImage()

        ret, image = self.cam1.read()
        if not ret:
            raise ValueError("No camera detected.")

        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        return image

    def CreateIntroduce(self) -> None:
        path: str = self.argments.intro_video_path
        if path == "":
            self.introduce = Introduction()
        else:
            self.introduce = Introduction(path)

    def CreateDebugger(self) -> None:
        path: str = self.argments.debug_image_folder
        if path == "":
            self.debugger = Debugger()
        else:
            self.debugger = Debugger(path)

    def ApplyFilter(
        self, image: ndarray
    ) -> Tuple[List[Landmark] | None, List[Landmark] | None]:
        landmarks: list[Landmark] | None = self.model.process(image)
        processed: list[Landmark] | None = copy.deepcopy(landmarks)

        if not self.argments.no_lpf:
            processed = self.filter.update(processed) if processed is not None else None

        return landmarks, processed

    def SendData(self, data: list[Landmark]) -> None:
        converted: list[list[float]] = [
            [landmark["x"], landmark["y"], landmark["z"], landmark["visibility"]]
            for landmark in data
        ]
        self.oscClient.Send(converted)

    def ChangeState(self, key: int) -> None:
        if key == 27:  # ESC
            self.state = STATES.QUIT
        elif not self.argments.no_debug and key == 100:  # D
            self.state = STATES.DEBUG
        elif key == 114:  # R
            self.state = STATES.GAME
        else:
            pass

    def Frame(self) -> bool:
        key: int = cv2.waitKey(1)
        if self.introduce is not None:
            self.introduce.Update()

        image: ndarray = self.GetImage()
        copyImage: ndarray = image.copy()
        landmarks, processed = self.ApplyFilter(image)
        self.SendData(processed) if processed is not None else None

        match self.state:
            case STATES.DEBUG | STATES.GAME:
                if self.debugger is not None:
                    self.debugger.UpdateImageIndex(key)

                if landmarks is not None:
                    self.capturingVisulalizer.update(copyImage, landmarks, (0, 255, 0))

                if processed is not None and not self.argments.no_lpf:
                    self.capturingVisulalizer.update(copyImage, processed, (255, 0, 0))

            case STATES.QUIT:
                return False

            case _:
                pass

        self.capturingVisulalizer.display_fps(copyImage)
        self.capturingVisulalizer.show()
        return True

    def Run(self) -> None:
        while True:
            try:
                if not self.Frame():
                    break
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                break
            except Exception as err:
                print(err)
                break

        self.cam1.release()
        if self.cam2 is not None:
            self.cam2.release()
