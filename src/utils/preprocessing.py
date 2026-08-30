"""
preprocessing.py
Basic preprocessing steps applied before enhancement/filtering.
"""

import cv2
import numpy as np


def to_grayscale(image):
    """Convert a BGR image to single-channel grayscale (no-op if already gray)."""
    if len(image.shape) == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def resize_image(image, width=None, height=None):
    """
    Resize while preserving aspect ratio if only one dimension is given.
    If both are None, the original image is returned unchanged.
    """
    if width is None and height is None:
        return image

    h, w = image.shape[:2]

    if width is not None and height is None:
        ratio = width / float(w)
        height = int(h * ratio)
    elif height is not None and width is None:
        ratio = height / float(h)
        width = int(w * ratio)

    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)


def normalize_image(image):
    """Scale pixel values to the 0-255 uint8 range."""
    norm = cv2.normalize(image.astype("float32"), None, 0, 255, cv2.NORM_MINMAX)
    return norm.astype(np.uint8)


def add_synthetic_noise(image, noise_type="gaussian", amount=25):
    """
    Add synthetic noise/blur to a clean image so the pipeline can be
    demonstrated end-to-end even without a naturally degraded dataset.

    noise_type : "gaussian" | "salt_pepper" | "blur"
    """
    img = image.astype(np.float32)

    if noise_type == "gaussian":
        noise = np.random.normal(0, amount, img.shape).astype(np.float32)
        noisy = img + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)

    if noise_type == "salt_pepper":
        noisy = img.copy()
        prob = amount / 1000.0
        rnd = np.random.rand(*img.shape[:2])
        noisy[rnd < prob / 2] = 0
        noisy[rnd > 1 - prob / 2] = 255
        return noisy.astype(np.uint8)

    if noise_type == "blur":
        k = max(3, amount // 5 | 1)  # odd kernel size
        return cv2.GaussianBlur(image, (k, k), 0)

    raise ValueError(f"Unknown noise_type: {noise_type}")
