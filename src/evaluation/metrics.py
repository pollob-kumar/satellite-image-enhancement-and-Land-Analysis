"""
metrics.py
Quantitative image-quality metrics used to objectively evaluate
enhancement results against the original (or a reference) image.
"""

import numpy as np
from skimage.metrics import structural_similarity as ssim


def mse(image_a, image_b):
    """Mean Squared Error - lower is more similar."""
    a = image_a.astype(np.float64)
    b = image_b.astype(np.float64)
    return float(np.mean((a - b) ** 2))


def psnr(image_a, image_b, max_pixel=255.0):
    """Peak Signal-to-Noise Ratio (dB) - higher indicates less distortion."""
    err = mse(image_a, image_b)
    if err == 0:
        return float("inf")
    return float(20 * np.log10(max_pixel / np.sqrt(err)))


def compute_ssim(image_a, image_b):
    """
    Structural Similarity Index (0 to 1) - higher means more
    structurally similar. Works on grayscale images.
    """
    if len(image_a.shape) == 3:
        import cv2
        image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    if len(image_b.shape) == 3:
        import cv2
        image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(image_a, image_b, full=True)
    return float(score)


def entropy(gray_image):
    """
    Shannon entropy - measures information content/detail.
    Higher entropy after enhancement generally indicates more
    recovered detail (useful when no reference image exists).
    """
    hist = np.histogram(gray_image, bins=256, range=(0, 255))[0]
    hist = hist / hist.sum()
    hist = hist[hist > 0]
    return float(-np.sum(hist * np.log2(hist)))


def evaluate_all(original, enhanced):
    """Convenience wrapper returning a dict of all metrics."""
    import cv2
    gray_enh = enhanced if len(enhanced.shape) == 2 else cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)

    return {
        "MSE": mse(original, enhanced),
        "PSNR": psnr(original, enhanced),
        "SSIM": compute_ssim(original, enhanced),
        "Entropy": entropy(gray_enh),
    }
