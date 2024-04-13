#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from numpy import array, ndarray
from PIL import Image

filenames: List[str] = ["T-pose.png", "X-pose.png"]


def loadDebugImages() -> List[ndarray]:
    images: list[ndarray] = []
    for name in filenames:
        rawData = Image.open("mediapipe_socket/debugImages/{}".format(name))
        rawData = rawData.convert("RGB")
        images.append(array(rawData))
    return images


def changeImage(index: int, length: int, key: int) -> int:
    for i in range(length):
        if key == 48 + i:
            return i
        else:
            pass
    return index
