"""
test_filters.py
Basic sanity tests: every filter should return an array of the same
shape/dtype family as its input, and should not crash on a synthetic image.

Run with:
    python -m pytest tests/
"""

import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.spatial_domain.smoothing import mean_filter, gaussian_filter, median_filter, bilateral_filter
from src.spatial_domain.sharpening import laplacian_sharpen, unsharp_mask, high_boost_filter
from src.frequency_domain.low_pass_filter import ideal_lowpass, gaussian_lowpass, butterworth_lowpass
from src.frequency_domain.high_pass_filter import ideal_highpass, gaussian_highpass, butterworth_highpass
from src.enhancement.contrast_enhancement import histogram_equalization, clahe_equalization, gamma_correction
from src.evaluation.metrics import mse, psnr, compute_ssim, entropy


def _sample_color_image():
    rng = np.random.default_rng(42)
    return rng.integers(0, 255, size=(64, 64, 3), dtype=np.uint8)


def _sample_gray_image():
    rng = np.random.default_rng(42)
    return rng.integers(0, 255, size=(64, 64), dtype=np.uint8)


def test_spatial_smoothing_shapes():
    img = _sample_color_image()
    for fn in [mean_filter, gaussian_filter, median_filter, bilateral_filter]:
        out = fn(img)
        assert out.shape == img.shape


def test_spatial_sharpening_shapes():
    img = _sample_color_image()
    assert laplacian_sharpen(img).shape == img.shape
    assert unsharp_mask(img).shape == img.shape
    assert high_boost_filter(img).shape == img.shape


def test_frequency_filters_shapes():
    gray = _sample_gray_image()
    for fn in [ideal_lowpass, gaussian_lowpass, butterworth_lowpass,
               ideal_highpass, gaussian_highpass, butterworth_highpass]:
        out = fn(gray)
        assert out.shape == gray.shape


def test_contrast_enhancement():
    gray = _sample_gray_image()
    color = _sample_color_image()
    assert histogram_equalization(gray).shape == gray.shape
    assert clahe_equalization(color).shape == color.shape
    assert gamma_correction(color).shape == color.shape


def test_metrics_identity():
    img = _sample_gray_image()
    assert mse(img, img) == 0
    assert psnr(img, img) == float("inf")
    assert compute_ssim(img, img) == 1.0
    assert entropy(img) > 0
