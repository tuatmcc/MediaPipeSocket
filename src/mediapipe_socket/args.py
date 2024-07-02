#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tap as typed_argment_parser


HOST_ADDRESS: str = "127.0.0.1"


class ArgParser(typed_argment_parser.Tap):
    """Typed Argument parser."""

    no_visualize: bool = False  # enable visualizations
    no_lpf: bool = False  # enable low pass filter
    no_debug: bool = False  # enable debug mode
    no_intro: bool = True  # enable intro
    device: int = -1  # camera device number
    width: int = 640  # camera capture width
    height: int = 480  # camera capture height
    ip_address: str = HOST_ADDRESS  # ip address to send messages to
    port: int = 8080  # target UDP port
    model_complexity: int = 1  # model complexity (0, 1(default), 2)
    min_detection_confidence: float = 0.5  # min_detection_confidence
    min_tracking_confidence: float = 0.5  # min_tracking_confidence
    enable_segmentation: bool = False  # enable segmentation
    segmentation_score_th: float = 0.5  # segmentation_score_threshold
    use_brect: bool = False  # use bounding rect
    intro_video_path: str = ""  # introduce video path
    debug_image_folder: str = ""  # debug image folder


def ParseArgs() -> ArgParser:
    """Get arguments from command line. Default values are used if not specified."""

    parser = ArgParser()

    parsed = parser.parse_args()

    return parsed
