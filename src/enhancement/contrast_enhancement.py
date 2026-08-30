"""
contrast_enhancement.py
Techniques to improve low-contrast satellite imagery, common due to
atmospheric haze or sensor limitations.
"""

import cv2
import numpy as np


def histogram_equalization(gray_image):
    """Global histogram equalization."""
    return cv2.equalizeHist(gray_image)


def clahe_equalization(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    """
    Contrast Limited Adaptive Histogram Equalization (CLAHE).
    Works locally, avoiding over-amplification of noise in flat regions
    like water bodies - generally the best choice for satellite images.
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    if len(image.shape) == 2:
        return clahe.apply(image)

    # Apply CLAHE on the L channel in LAB space to preserve color balance
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_eq = clahe.apply(l)
    merged = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def gamma_correction(image, gamma=1.2):
    """Gamma correction - brightens (gamma<1) or darkens (gamma>1) an image."""
    inv_gamma = 1.0 / gamma
    table = np.array(
        [((i / 255.0) ** inv_gamma) * 255 for i in range(256)]
    ).astype(np.uint8)
    return cv2.LUT(image, table)


def linear_contrast_stretch(gray_image):
    """Simple min-max contrast stretching."""
    min_val, max_val = np.min(gray_image), np.max(gray_image)
    if max_val == min_val:
        return gray_image
    stretched = (gray_image.astype(np.float32) - min_val) * (255.0 / (max_val - min_val))
    return np.clip(stretched, 0, 255).astype(np.uint8)
