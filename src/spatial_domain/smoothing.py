"""
smoothing.py
Spatial-domain smoothing (low-pass) filters used to suppress noise
in satellite imagery before feature analysis.
"""

import cv2


def mean_filter(image, ksize=5):
    """Simple averaging (box) filter."""
    return cv2.blur(image, (ksize, ksize))


def gaussian_filter(image, ksize=5, sigma=1.0):
    """Gaussian smoothing - better edge preservation than mean filter."""
    ksize = ksize if ksize % 2 == 1 else ksize + 1
    return cv2.GaussianBlur(image, (ksize, ksize), sigma)


def median_filter(image, ksize=5):
    """
    Median filter - highly effective against salt-and-pepper noise,
    common in satellite sensor imagery.
    """
    ksize = ksize if ksize % 2 == 1 else ksize + 1
    return cv2.medianBlur(image, ksize)


def bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """
    Edge-preserving smoothing - denoises flat regions (e.g. water bodies)
    while keeping boundaries (e.g. coastlines, roads) sharp.
    """
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)
