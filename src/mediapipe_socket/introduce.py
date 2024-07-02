#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
from numpy import ndarray

from visualizer import Visualizer

filenames: list[str] = ["example.mp4"]


def loadVideoFiles() -> list[cv2.VideoCapture]:
    videos: list[cv2.VideoCapture] = []
    pathbase: str = "videos/{}"
    for name in filenames:
        fmtpath = pathbase.format(name)
        cap = cv2.VideoCapture(fmtpath)
        videos.append(cap)
    return videos


def getFrame(videos: list[cv2.VideoCapture], index: int) -> tuple[ndarray, int]:
    ret, frame = videos[index].read()
    if not ret:
        videos[index].set(cv2.CAP_PROP_POS_FRAMES, 0)
        index += 1

        if index > len(videos) - 1:
            index = 0

        ret, frame = videos[index].read()

    return frame, index


def showVideoFrame(frame: ndarray, visualizer: Visualizer) -> None:
    visualizer.image_output = frame
    visualizer.show()
