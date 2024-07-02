#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import array, ndarray

from PIL import Image
import cv2
import os

filenames: list[str] = os.listdir("./src/images/")


def loadDebugImages() -> list[ndarray]:
    images: list[ndarray] = []
    for name in filenames:
        cvrawData = cv2.imread(f"./src/images/{name}")
        cvrawData = cv2.cvtColor(cvrawData, cv2.COLOR_BGR2RGB)

        print(cvrawData.shape)
        rawData = Image.open(f"./src/images/{name}")
        rawData = rawData.convert("RGB")
        rawData = array(rawData)
        print(rawData.shape)
        images.append(cvrawData)
    return images


def changeImage(index: int, length: int, key: int) -> int:
    for i in range(length):
        if key == 48 + i:
            return i
        else:
            pass
    return index
