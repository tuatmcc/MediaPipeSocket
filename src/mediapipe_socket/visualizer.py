#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import cv2
import numpy
from numpy import ndarray

from filters import GaussianFilter
from mediapipe_wrapper import Landmark


class Visualizer:
    def __init__(self, use_brect: bool, winname: str = "MediaPipe Pose Demo"):
        self.image_output: ndarray | None = None
        self.use_brect: bool = use_brect
        self.winname: str = winname
        self.last_frame_time: float = time.time()
        self.fps: GaussianFilter = GaussianFilter(30, 5)

        cv2.namedWindow(self.winname, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.winname, 1500, 750)

    def show(self) -> None:
        if self.image_output is None:
            return

        cv2.imshow(self.winname, self.image_output)
        self.image_output = None
        return

    def display_fps(self, image: ndarray) -> None:
        now = time.time()
        current_fps = self.fps.update(1 / (now - self.last_frame_time))
        self.last_frame_time = now
        image = cv2.putText(
            image,
            str(f"FPS: {current_fps:.2f}"),
            (0, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )
        self.image_output = image
        return

    def update(
        self,
        image: ndarray,
        landmarks: list[Landmark],
        color: tuple[int, int, int] = (0, 255, 0),
    ) -> None:
        # 描画
        self.image_output = self.__draw_bounding_rect(
            self.use_brect, image, landmarks, color=color
        )
        self.image_output = self.__draw_landmarks(
            self.image_output, landmarks, color=color
        )
        return

    def __draw_bounding_rect(
        self,
        use_brect: bool,
        image: ndarray,
        landmarks: list[Landmark],
        color=(0, 255, 0),
    ) -> ndarray:
        if use_brect:
            image_width, image_height = image.shape[1], image.shape[0]

            landmark_array = numpy.empty((0, 2), int)

            for _, landmark in enumerate(landmarks):
                landmark_x = min(int(landmark["x"] * image_width), image_width - 1)
                landmark_y = min(int(landmark["y"] * image_height), image_height - 1)

                landmark_point = [numpy.array((landmark_x, landmark_y))]

                landmark_array = numpy.append(landmark_array, landmark_point, axis=0)

            x, y, w, h = cv2.boundingRect(landmark_array)
            # 外接矩形
            cv2.rectangle(image, (x, y), (w, h), color, 2)

        return image

    def __draw_landmarks(
        self,
        image: ndarray,
        landmarks: list[Landmark],
        visibility_th=0.5,
        color=(0, 255, 0),
    ) -> ndarray:
        image_width, image_height = (
            image.shape[1],
            image.shape[0],
        )

        landmark_point = []

        for index, landmark in enumerate(landmarks):
            landmark_x = min(int(landmark["x"] * image_width), image_width - 1)
            landmark_y = min(int(landmark["y"] * image_height), image_height - 1)
            landmark_z = landmark["z"]
            landmark_point.append([landmark["visibility"], (landmark_x, landmark_y)])

            if landmark["visibility"] < visibility_th:
                continue

            if index == 0:  # 鼻
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 1:  # 右目：目頭
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 2:  # 右目：瞳
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 3:  # 右目：目尻
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 4:  # 左目：目頭
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 5:  # 左目：瞳
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 6:  # 左目：目尻
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 7:  # 右耳
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 8:  # 左耳
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 9:  # 口：左端
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 10:  # 口：左端
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 11:  # 右肩
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 12:  # 左肩
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 13:  # 右肘
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 14:  # 左肘
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 15:  # 右手首
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 16:  # 左手首
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 17:  # 右手1(外側端)
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 18:  # 左手1(外側端)
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 19:  # 右手2(先端)
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 20:  # 左手2(先端)
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 21:  # 右手3(内側端)
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 22:  # 左手3(内側端)
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 23:  # 腰(右側)
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 24:  # 腰(左側)
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 25:  # 右ひざ
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 26:  # 左ひざ
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 27:  # 右足首
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 28:  # 左足首
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 29:  # 右かかと
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 30:  # 左かかと
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 31:  # 右つま先
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)
            if index == 32:  # 左つま先
                cv2.circle(image, (landmark_x, landmark_y), 5, color, 2)

            cv2.putText(
                image,
                "z:" + str(round(landmark_z, 3)),
                (landmark_x - 10, landmark_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )

        if len(landmark_point) > 0:
            # 右目
            if (
                landmark_point[1][0] > visibility_th
                and landmark_point[2][0] > visibility_th
            ):
                cv2.line(image, landmark_point[1][1], landmark_point[2][1], color, 2)
            if (
                landmark_point[2][0] > visibility_th
                and landmark_point[3][0] > visibility_th
            ):
                cv2.line(image, landmark_point[2][1], landmark_point[3][1], color, 2)

            # 左目
            if (
                landmark_point[4][0] > visibility_th
                and landmark_point[5][0] > visibility_th
            ):
                cv2.line(image, landmark_point[4][1], landmark_point[5][1], color, 2)
            if (
                landmark_point[5][0] > visibility_th
                and landmark_point[6][0] > visibility_th
            ):
                cv2.line(image, landmark_point[5][1], landmark_point[6][1], color, 2)

            # 口
            if (
                landmark_point[9][0] > visibility_th
                and landmark_point[10][0] > visibility_th
            ):
                cv2.line(image, landmark_point[9][1], landmark_point[10][1], color, 2)

            # 肩
            if (
                landmark_point[11][0] > visibility_th
                and landmark_point[12][0] > visibility_th
            ):
                cv2.line(image, landmark_point[11][1], landmark_point[12][1], color, 2)

            # 右腕
            if (
                landmark_point[11][0] > visibility_th
                and landmark_point[13][0] > visibility_th
            ):
                cv2.line(image, landmark_point[11][1], landmark_point[13][1], color, 2)
            if (
                landmark_point[13][0] > visibility_th
                and landmark_point[15][0] > visibility_th
            ):
                cv2.line(image, landmark_point[13][1], landmark_point[15][1], color, 2)

            # 左腕
            if (
                landmark_point[12][0] > visibility_th
                and landmark_point[14][0] > visibility_th
            ):
                cv2.line(image, landmark_point[12][1], landmark_point[14][1], color, 2)
            if (
                landmark_point[14][0] > visibility_th
                and landmark_point[16][0] > visibility_th
            ):
                cv2.line(image, landmark_point[14][1], landmark_point[16][1], color, 2)

            # 右手
            if (
                landmark_point[15][0] > visibility_th
                and landmark_point[17][0] > visibility_th
            ):
                cv2.line(image, landmark_point[15][1], landmark_point[17][1], color, 2)
            if (
                landmark_point[17][0] > visibility_th
                and landmark_point[19][0] > visibility_th
            ):
                cv2.line(image, landmark_point[17][1], landmark_point[19][1], color, 2)
            if (
                landmark_point[19][0] > visibility_th
                and landmark_point[21][0] > visibility_th
            ):
                cv2.line(image, landmark_point[19][1], landmark_point[21][1], color, 2)
            if (
                landmark_point[21][0] > visibility_th
                and landmark_point[15][0] > visibility_th
            ):
                cv2.line(image, landmark_point[21][1], landmark_point[15][1], color, 2)

            # 左手
            if (
                landmark_point[16][0] > visibility_th
                and landmark_point[18][0] > visibility_th
            ):
                cv2.line(image, landmark_point[16][1], landmark_point[18][1], color, 2)
            if (
                landmark_point[18][0] > visibility_th
                and landmark_point[20][0] > visibility_th
            ):
                cv2.line(image, landmark_point[18][1], landmark_point[20][1], color, 2)
            if (
                landmark_point[20][0] > visibility_th
                and landmark_point[22][0] > visibility_th
            ):
                cv2.line(image, landmark_point[20][1], landmark_point[22][1], color, 2)
            if (
                landmark_point[22][0] > visibility_th
                and landmark_point[16][0] > visibility_th
            ):
                cv2.line(image, landmark_point[22][1], landmark_point[16][1], color, 2)

            # 胴体
            if (
                landmark_point[11][0] > visibility_th
                and landmark_point[23][0] > visibility_th
            ):
                cv2.line(image, landmark_point[11][1], landmark_point[23][1], color, 2)
            if (
                landmark_point[12][0] > visibility_th
                and landmark_point[24][0] > visibility_th
            ):
                cv2.line(image, landmark_point[12][1], landmark_point[24][1], color, 2)
            if (
                landmark_point[23][0] > visibility_th
                and landmark_point[24][0] > visibility_th
            ):
                cv2.line(image, landmark_point[23][1], landmark_point[24][1], color, 2)

            if len(landmark_point) > 25:
                # 右足
                if (
                    landmark_point[23][0] > visibility_th
                    and landmark_point[25][0] > visibility_th
                ):
                    cv2.line(
                        image, landmark_point[23][1], landmark_point[25][1], color, 2
                    )
                if (
                    landmark_point[25][0] > visibility_th
                    and landmark_point[27][0] > visibility_th
                ):
                    cv2.line(
                        image, landmark_point[25][1], landmark_point[27][1], color, 2
                    )
                if (
                    landmark_point[27][0] > visibility_th
                    and landmark_point[29][0] > visibility_th
                ):
                    cv2.line(
                        image, landmark_point[27][1], landmark_point[29][1], color, 2
                    )
                if (
                    landmark_point[29][0] > visibility_th
                    and landmark_point[31][0] > visibility_th
                ):
                    cv2.line(
                        image, landmark_point[29][1], landmark_point[31][1], color, 2
                    )

                # 左足
                if (
                    landmark_point[24][0] > visibility_th
                    and landmark_point[26][0] > visibility_th
                ):
                    cv2.line(
                        image, landmark_point[24][1], landmark_point[26][1], color, 2
                    )
                if (
                    landmark_point[26][0] > visibility_th
                    and landmark_point[28][0] > visibility_th
                ):
                    cv2.line(
                        image, landmark_point[26][1], landmark_point[28][1], color, 2
                    )
                if (
                    landmark_point[28][0] > visibility_th
                    and landmark_point[30][0] > visibility_th
                ):
                    cv2.line(
                        image, landmark_point[28][1], landmark_point[30][1], color, 2
                    )
                if (
                    landmark_point[30][0] > visibility_th
                    and landmark_point[32][0] > visibility_th
                ):
                    cv2.line(
                        image, landmark_point[30][1], landmark_point[32][1], color, 2
                    )
        return image
