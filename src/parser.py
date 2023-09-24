#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# type: ignore

import json

from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList


def to_json(landmark_list: NormalizedLandmarkList) -> str:
    """Convert NormalizedLandmarkList to json string."""

    return json.dumps(
        [
            {
                "id": index,
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility,
            }
            for index, landmark in enumerate(landmark_list.landmark)
        ]
    )
