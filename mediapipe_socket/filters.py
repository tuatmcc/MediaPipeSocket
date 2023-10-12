#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import TypedDict

from mediapipe_wrapper import Landmark
from scipy.ndimage import gaussian_filter


class GaussianFilter:
    """
    ガウシアンフィルタ
    """

    def __init__(self, sample_size: int, sigma: float, init_value: float = 0.0):
        """
        :param sample_size: サンプル数
        :param sigma: ガウス分布の標準偏差
        :param init_value: 初期値
        """
        self.sample_size = sample_size
        self.sigma = sigma
        self.stored_inputs: list[float] = [init_value] * sample_size
        self.prev = init_value

    def update(self, input: float) -> float:
        """
        フィルタを更新し、出力値を返す
        :param input: 入力値
        :return: 出力値
        """
        self.stored_inputs = self.stored_inputs[1:] + [input]
        output = gaussian_filter(self.stored_inputs, sigma=self.sigma)[-1]
        return output


class LandmarkComposiion(TypedDict):
    """
    ランドマークの各座標についてガウシアンフィルタを保持するクラス
    """

    x: GaussianFilter
    y: GaussianFilter
    z: GaussianFilter
    visibility: GaussianFilter


class PoseLandmarkComposition:
    """
    MediaPipePoseの出力値(33個のランドマーク)について、各座標についてガウシアンフィルタを保持するクラス
    """

    def __init__(self):
        self.filters: list[LandmarkComposiion] = [
            {
                "x": GaussianFilter(200, 4, 0.0),
                "y": GaussianFilter(200, 4, 0.0),
                "z": GaussianFilter(200, 4, 0.0),
                "visibility": GaussianFilter(200, 4, 0.0),
            }
            for _ in range(33)
        ]

    def update(self, landmarks: list[Landmark]) -> list[Landmark]:
        """
        フィルタを更新し、出力値を返す
        """
        for i, landmark in enumerate(landmarks):  # type: ignore
            landmarks[i]["x"] = self.filters[i]["x"].update(landmark["x"])
            landmarks[i]["y"] = self.filters[i]["y"].update(landmark["y"])
            landmarks[i]["z"] = self.filters[i]["z"].update(landmark["z"])
            landmarks[i]["visibility"] = self.filters[i]["visibility"].update(
                landmark["visibility"]
            )
        return landmarks
