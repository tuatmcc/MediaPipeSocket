#!usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from matplotlib import pyplot as plt
from numpy import cos, pi, sin

# from typing import List


class SimpleFilter:
    """
    一次遅れ系を用いたリアルタイムフィルタ
    """

    def __init__(
        self, sample_size: int, time_constant: float, dt: float, init_value: float = 0.0
    ):
        """
        :param sample_size: サンプル数
        :param time_constant: 時定数
        :param dt: サンプリング周期
        :param init_value: 初期値
        """
        self.sample_size = sample_size
        self.tconst = time_constant
        self.dt = dt
        # self.stored_outputs: List[float] = [init_value] * sample_size
        self.prev = init_value
        self.now = time.time()

    def update(self, input: float) -> float:
        """
        フィルタを更新し、出力値を返す
        :param input: 入力値
        :return: 出力値
        """
        output = (1 - self.dt / self.tconst) * self.prev + (
            self.dt / self.tconst
        ) * input
        # self.stored_outputs = self.stored_outputs[1:] + [output]
        self.prev = output
        return output


def test():
    filter = SimpleFilter(10, 0.2, 0.05, 1)
    timer = range(100)
    x = []
    y = []
    for i in timer:
        xi = sin(i * pi / 20) + cos(i * pi * 5)
        x.append(xi)
        y.append(filter.update(xi))
        print(f"{xi} -> {y[-1]}")

    plt.plot(timer, x, linestyle="solid", color="red")
    plt.plot(timer, y, linestyle="solid", color="blue")
    plt.show()


test()
