#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import array, ndarray

# from PIL import Image
from cv2 import imread
import os

filenames: list[str] = os.listdir("./src/images")


def loadDebugImages() -> list[ndarray]:
    images: list[ndarray] = []
    for name in filenames:
        rawData = imread(f"./src/images/{name}")
        images.append(array(rawData))
    return images


def changeImage(index: int, length: int, key: int) -> int:
    for i in range(length):
        if key == 48 + i:
            return i
        else:
            pass
    return index
