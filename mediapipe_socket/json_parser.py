#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from mediapipe_wrapper import Landmark


def to_json(landmarks: list[Landmark]) -> str:
    """Convert NormalizedLandmarkList to json string."""

    return json.dumps(
        [
            {
                "x": landmark["x"],
                "y": landmark["y"],
                "z": landmark["z"],
                "visibility": landmark["visibility"],
            }
            for landmark in landmarks
        ]
    )
