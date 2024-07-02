#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import array, ndarray, array_equal

from PIL import Image
import cv2
import os

filenames: list[str] = os.listdir("./src/images/")


def loadDebugImages() -> list[ndarray]:
    images: list[ndarray] = []
    for name in filenames:
        cvrawData = cv2.imread(f"./src/images/{name}")
        print(cvrawData.shape)
        rawData = Image.open(f"./src/images/{name}")
        rawData = rawData.convert("RGB")
        rawData = array(rawData)
        # rawData = array(rawData[:, :, ::-1])
        # print(rawData.shape)
        # print(array_equal(rawData, cvrawData))
        images.append(rawData)
    return images


def changeImage(index: int, length: int, key: int) -> int:
    for i in range(length):
        if key == 48 + i:
            return i
        else:
            pass
    return index
