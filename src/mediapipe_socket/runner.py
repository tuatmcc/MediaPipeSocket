#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import cv2
import sys
from numpy import ndarray

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
    """
    MediaPipeSocketを実行するためのクラス
    変数を追加する場合は、__init__関数内で初期化すること
    """

    def __init__(self, args: ArgParser) -> None:
        self.argments: ArgParser = args

        cameras: list[int] = self.GetAvailableCameras()  # 使用可能なカメラのリスト
        if len(cameras) == 0:  # カメラが見つからない場合
            raise ValueError("No camera detected.")

        self.camera: cv2.VideoCapture = cv2.VideoCapture(cameras[0])  # カメラの取得

        self.capturingVisulalizer: Visualizer = Visualizer(
            self.argments.use_brect
        )  # キャプチャ結果表示用
        self.filter: PoseLandmarkComposition = PoseLandmarkComposition()
        self.model: MediaPipePose = MediaPipePose(
            model_complexity=self.argments.model_complexity,
            enable_segmentation=self.argments.enable_segmentation,
            min_detection_confidence=self.argments.min_detection_confidence,
            min_tracking_confidence=self.argments.min_tracking_confidence,
        )  # モデルの初期化
        self.introduce: Introduction | None = None  # 紹介動画制御
        self.debugger: Debugger | None = None  # デバッグ画像制御
        self.oscClient: Client = CreateClient(
            args.ip_address, args.port
        )  # OSCクライアント
        self.state: int = STATES.GAME  # 状態管理

        if not self.argments.no_intro:  # 紹介動画が有効
            self.CreateIntroduce()

        if not self.argments.no_debug:  # デバッグが有効
            self.CreateDebugger()

    def GetAvailableCameras(self) -> list[int]:
        """
        画像を取得可能なカメラのリストを取得する(最大10台まで)
        """

        cameras: list[int] = []

        if self.argments.device != -1:  # 特定のカメラを指定している場合
            return [self.argments.device]

        for camera_number in range(0, 10):
            try:
                cap = cv2.VideoCapture(camera_number)
                ret, _ = cap.read()
            except Exception:
                ret = False

            if ret:
                cameras.append(camera_number)

        return cameras

    def GetImage(self) -> ndarray:
        """
        カメラから画像を取得する
        デバッグモードの場合はデバッグ画像を取得する
        """

        if self.debugger is not None and self.state == STATES.DEBUG:
            # デバッガが有効かつデバッグモードの場合
            return self.debugger.GetImage()

        ret, image = self.camera.read()
        if not ret:
            raise ValueError("Failed to capture image.")

        image = cv2.flip(image, 1)
        return image

    def CreateIntroduce(self) -> None:
        path: str = self.argments.intro_video_path  # 紹介動画のパス
        if path == "":  # 紹介動画が指定されていない場合
            self.introduce = Introduction()
        else:
            self.introduce = Introduction(path)

    def CreateDebugger(self) -> None:
        path: str = self.argments.debug_image_folder  # デバッグ画像のパス
        if path == "":  # デバッグ画像が指定されていない場合
            self.debugger = Debugger()
        else:
            self.debugger = Debugger(path)

    def ApplyFilter(
        self, image: ndarray
    ) -> tuple[list[Landmark] | None, list[Landmark] | None]:
        landmarks: list[Landmark] | None = self.model.process(image)
        processed: list[Landmark] | None = copy.deepcopy(landmarks)

        if not self.argments.no_lpf:  # ローパスフィルタが有効
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
            # デバッグモードが有効でない場合は無視される
            self.state = STATES.DEBUG
        elif key == 114:  # R
            self.state = STATES.GAME
        else:
            pass

    def Frame(self) -> bool:
        """
        1フレーム分の処理を行う
        ESCキーが押された場合はFalseを返す
        """

        if self.introduce is not None:
            self.introduce.Update()

        image: ndarray = self.GetImage()
        copyImage: ndarray = image.copy()  # 表示用にコピー
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)  # RGBに変換
        landmarks, processed = self.ApplyFilter(image)
        self.SendData(processed) if processed is not None else None

        key: int = cv2.waitKey(1)
        self.ChangeState(key)

        match self.state:
            case STATES.DEBUG | STATES.GAME:
                if self.debugger is not None:
                    self.debugger.UpdateImageIndex(key)

                if landmarks is not None:
                    self.capturingVisulalizer.update(copyImage, landmarks, (0, 255, 0))

                if processed is not None and not self.argments.no_lpf:
                    self.capturingVisulalizer.update(copyImage, processed, (255, 0, 0))

            case STATES.QUIT:
                return False  # 終了

            case _:
                pass

        self.capturingVisulalizer.display_fps(copyImage)
        self.capturingVisulalizer.show()

        return True

    def Run(self) -> None:
        while True:
            ret = self.Frame()  # 1フレーム分の処理
            if not ret:
                self.camera.release()  # カメラの解放
                cv2.destroyAllWindows()
                sys.exit(0)
