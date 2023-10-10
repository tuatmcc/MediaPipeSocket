#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import NamedTuple, TypedDict

from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList
from mediapipe.python.solutions import pose as mp_pose
from numpy import ndarray

Landmark = TypedDict(
    "Landmark",
    {
        "x": float,
        "y": float,
        "z": float,
        "visibility": float,
    },
)


class MediaPipePose(mp_pose.Pose):
    def process(self, image: ndarray) -> list[Landmark] | None:
        """Process an RGB image and return the pose landmarks."""
        result: NamedTuple = super().process(image)
        if result.pose_landmarks is None:  # type: ignore
            return None
        else:
            pose_landmarks: NormalizedLandmarkList = result.pose_landmarks  # type: ignore
            return self.__to_landmarks(pose_landmarks)

    def __to_landmarks(self, pose_landmarks: NormalizedLandmarkList) -> list[Landmark]:
        return [
            {
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility,
            }
            for landmark in pose_landmarks.landmark  # type: ignore
        ]
