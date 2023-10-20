#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from numpy import ndarray, array
from PIL import Image

import keyboard

filenames: List[str] = [
    "T-pose",
    "X-pose"
]

def loadDebugImages() -> List[ndarray]:
    images: List[ndarray] = []
    for name in filenames:
        rawData = Image.open("mediapipe_socket/debugImages/{}.png".format(name))
        rawData = rawData.convert("RGB")
        images.append(array(rawData))
    return images


def changeImage(index: int, length: int) -> int:
    for i in range(length):
        if keyboard.is_pressed(str(i)):
            return i
        else:
            pass
    return index
