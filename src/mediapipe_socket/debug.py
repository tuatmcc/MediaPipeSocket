#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import ndarray
import cv2
import os


class Debugger:
    """
    デバッグ画像の管理を行うクラス
    """

    def __init__(self, imageFolder: str = "./src/images/") -> None:
        """
        imageFolder: デバッグ画像が格納されているフォルダのパス(pyproject.tomlからの相対パス)
        """
        self.index: int = 0  # 現在表示している画像のインデックス
        self.images: list[ndarray] = []
        self.LoadDebugImages(imageFolder)

    def GetImage(self) -> ndarray:
        """
        設定されているインデックスの画像を取得する
        """
        return self.images[self.index]

    def LoadDebugImages(self, folder: str):
        images: list[str] = os.listdir(folder)
        for image in images:
            cvrawData = cv2.imread(f"./src/images/{image}")
            self.images.append(cvrawData)

    def UpdateImageIndex(self, key: int) -> None:
        for i in range(len(self.images)):
            if (
                key == 48 + i
            ):  # 0~9のキーが押されたらその番号の画像を表示(48は0のASCIIコード)
                self.index = i
                break
