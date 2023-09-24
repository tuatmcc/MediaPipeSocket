#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def get_args() -> argparse.Namespace:
    """Get arguments from command line. Default values are used if not specified."""

    parser = argparse.ArgumentParser()
    # Camera
    parser.add_argument("--device", help="Camera Device Index", type=int, default=0)
    parser.add_argument("--width", help="Camera Capture Width", type=int, default=640)
    parser.add_argument(
        "--height", help="Camera Caputure Height", type=int, default=480
    )
    # Socket
    parser.add_argument("--port", help="Target UDP Port", type=int, default=5000)
    # MediaPipe
    parser.add_argument(
        "--model_complexity",
        help="model_complexity(0,1(default),2)",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--min_detection_confidence",
        help="min_detection_confidence",
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "--min_tracking_confidence",
        help="min_tracking_confidence",
        type=float,
        default=0.5,
    )
    parser.add_argument("--enable_segmentation", action="store_true")
    parser.add_argument(
        "--segmentation_score_th",
        help="segmentation_score_threshold",
        type=float,
        default=0.5,
    )
    parser.add_argument("--use_brect", action="store_true")

    return parser.parse_args()
