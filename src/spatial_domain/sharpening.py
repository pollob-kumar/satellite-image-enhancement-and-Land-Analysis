"""
sharpening.py
Spatial-domain sharpening (high-pass) techniques used to enhance
edges of urban structures, roads, and land boundaries.
"""

import cv2
import numpy as np


def laplacian_sharpen(image, ksize=3):
    """Sharpen using the Laplacian operator (edge enhancement)."""
    gray_input = len(image.shape) == 2
    lap = cv2.Laplacian(image, cv2.CV_64F, ksize=ksize)
    lap = cv2.convertScaleAbs(lap)

    if gray_input:
        sharpened = cv2.addWeighted(image, 1.0, lap, 1.0, 0)
    else:
        sharpened = cv2.addWeighted(image, 1.0, lap, 1.0, 0)

    return sharpened


def unsharp_mask(image, ksize=5, sigma=1.0, amount=1.5, threshold=0):
    """
    Classic unsharp masking: sharpened = original + amount * (original - blurred)
    """
    blurred = cv2.GaussianBlur(image, (ksize, ksize), sigma)
    sharpened = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)

    if threshold > 0:
        low_contrast_mask = np.absolute(image.astype(int) - blurred.astype(int)) < threshold
        sharpened = np.where(low_contrast_mask, image, sharpened)

    return np.clip(sharpened, 0, 255).astype(np.uint8)


def high_boost_filter(image, ksize=5, sigma=1.0, boost_factor=1.5):
    """
    High-boost filtering: amplifies high-frequency detail while retaining
    a controllable amount of the low-frequency (original) content.
    boost_factor > 1 increases sharpening strength.
    """
    blurred = cv2.GaussianBlur(image, (ksize, ksize), sigma)
    mask = cv2.subtract(image, blurred)
    boosted = cv2.addWeighted(image, boost_factor, mask, 1.0, 0)
    return np.clip(boosted, 0, 255).astype(np.uint8)
