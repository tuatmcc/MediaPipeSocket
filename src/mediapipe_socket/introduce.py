#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
from numpy import ndarray

from visualizer import Visualizer


class Introduction:
    def __init__(
        self, videoPath: str = "./mediapipe_socket/videos/example.mp4"
    ) -> None:
        self.visualizer = Visualizer(False)
        self.video = cv2.VideoCapture(videoPath)

    def Frame(self) -> ndarray:
        ret, frame = self.video.read()
        if not ret:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video.read()
        return frame

    def Update(self) -> None:
        frame = self.Frame()
        self.visualizer.image_output = frame
        self.visualizer.show()

    def __del__(self) -> None:
        self.video.release()
        cv2.destroyAllWindows()
