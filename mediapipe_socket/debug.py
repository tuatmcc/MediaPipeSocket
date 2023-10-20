#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from numpy import ndarray, array
from PIL import Image

import keyboard

filenames: List[str] = [
    #"T-pose"
]

def loadDebugImages() -> List[ndarray]:
    images: List[ndarray] = []
    for name in filenames:
        rawData = Image.open("./debugImage/{}.png".format(name))
        images.append(array(rawData))
    return images


def changeImage(debugImages: List[ndarray]) -> ndarray:
    for i in range(len(debugImages)):
        if keyboard.is_pressed("{i}"):
            return debugImages[i]
        else:
            pass
    return debugImages[-1]
