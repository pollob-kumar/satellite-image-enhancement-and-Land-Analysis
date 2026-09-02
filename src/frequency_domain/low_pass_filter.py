"""
low_pass_filter.py
Frequency-domain low-pass filters (LPF) - suppress high-frequency
noise while retaining broad land-cover structure.
"""

import numpy as np
from src.frequency_domain.fft_utils import compute_fft, inverse_fft, distance_grid


def ideal_lowpass(gray_image, cutoff=30):
    """Ideal LPF - hard cutoff, can introduce ringing artifacts."""
    f_shift = compute_fft(gray_image)
    dist = distance_grid(gray_image.shape)

    mask = (dist <= cutoff).astype(np.float32)
    filtered_shift = f_shift * mask

    return inverse_fft(filtered_shift)


def gaussian_lowpass(gray_image, cutoff=30):
    """Gaussian LPF - smooth transition, no ringing artifacts."""
    f_shift = compute_fft(gray_image)
    dist = distance_grid(gray_image.shape)

    mask = np.exp(-(dist ** 2) / (2 * (cutoff ** 2)))
    filtered_shift = f_shift * mask

    return inverse_fft(filtered_shift)


def butterworth_lowpass(gray_image, cutoff=30, order=2):
    """Butterworth LPF - configurable roll-off between ideal and Gaussian."""
    f_shift = compute_fft(gray_image)
    dist = distance_grid(gray_image.shape)

    mask = 1 / (1 + (dist / cutoff) ** (2 * order))
    filtered_shift = f_shift * mask

    return inverse_fft(filtered_shift)
