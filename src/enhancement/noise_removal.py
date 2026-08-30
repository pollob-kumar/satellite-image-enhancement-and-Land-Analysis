"""
noise_removal.py
Denoising routines applied to raw satellite imagery, which is
commonly affected by sensor and atmospheric noise.
"""

import cv2


def denoise_median(image, ksize=5):
    """Fast, effective against impulse (salt-and-pepper) noise."""
    return cv2.medianBlur(image, ksize)


def denoise_nlm(image, h=10, template_window=7, search_window=21):
    """
    Non-Local Means denoising - preserves fine texture/edges better
    than simple blurring, good for vegetation texture detail.
    """
    if len(image.shape) == 2:
        return cv2.fastNlMeansDenoising(image, None, h, template_window, search_window)
    return cv2.fastNlMeansDenoisingColored(
        image, None, h, h, template_window, search_window
    )


def denoise_bilateral(image, d=9, sigma_color=75, sigma_space=75):
    """Edge-preserving smoothing, good general-purpose satellite denoiser."""
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)
