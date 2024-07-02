#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import ndarray
import cv2
import os


class Debugger:
    def __init__(self, imageFolder: str = "./src/images/") -> None:
        self.index: int = 0
        self.images: list[ndarray] = []
        self.LoadDebugImages(imageFolder)

    def GetImage(self) -> ndarray:
        return self.images[self.index]

    def LoadDebugImages(self, folder: str):
        images: list[str] = os.listdir(folder)
        for image in images:
            cvrawData = cv2.imread(f"./src/images/{image}")
            self.images.append(cvrawData)

    def UpdateImageIndex(self, key: int) -> None:
        for i in range(len(self.images)):
            if key == 48 + i:
                self.index = i
                break
