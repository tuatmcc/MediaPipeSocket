#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tap as typed_argment_parser


class ArgParser(typed_argment_parser.Tap):
    """Typed Argument parser."""

    no_visualize: bool = False  # enable visualizations
    no_lpf: bool = False  # enable low pass filter
    device: int = 0  # camera device index
    width: int = 640  # camera capture width
    height: int = 480  # camera capture height
    ip_address: string = "192.168.0.254" # ip address to send messages to
    port: int = 8080  # target UDP port
    model_complexity: int = 1  # model complexity (0, 1(default), 2)
    min_detection_confidence: float = 0.5  # min_detection_confidence
    min_tracking_confidence: float = 0.5  # min_tracking_confidence
    enable_segmentation: bool = False  # enable segmentation
    segmentation_score_th: float = 0.5  # segmentation_score_threshold
    use_brect: bool = False  # use bounding rect


def get_args() -> ArgParser:
    """Get arguments from command line. Default values are used if not specified."""

    parser = ArgParser()

    parsed = parser.parse_args()

    return parsed
