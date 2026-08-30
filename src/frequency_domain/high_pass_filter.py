"""
high_pass_filter.py
Frequency-domain high-pass filters (HPF) - emphasize edges/details
such as roads, building outlines, and field boundaries.
"""

import numpy as np
from src.frequency_domain.fft_utils import compute_fft, inverse_fft, distance_grid


def ideal_highpass(gray_image, cutoff=30):
    """Ideal HPF - hard cutoff, keeps frequencies above the cutoff radius."""
    f_shift = compute_fft(gray_image)
    dist = distance_grid(gray_image.shape)

    mask = (dist > cutoff).astype(np.float32)
    filtered_shift = f_shift * mask

    return inverse_fft(filtered_shift)


def gaussian_highpass(gray_image, cutoff=30):
    """Gaussian HPF - smooth complement of the Gaussian LPF."""
    f_shift = compute_fft(gray_image)
    dist = distance_grid(gray_image.shape)

    mask = 1 - np.exp(-(dist ** 2) / (2 * (cutoff ** 2)))
    filtered_shift = f_shift * mask

    return inverse_fft(filtered_shift)


def butterworth_highpass(gray_image, cutoff=30, order=2):
    """Butterworth HPF - complement of the Butterworth LPF."""
    f_shift = compute_fft(gray_image)
    dist = distance_grid(gray_image.shape)

    # avoid divide-by-zero at the DC component
    dist[dist == 0] = 1e-6
    mask = 1 / (1 + (cutoff / dist) ** (2 * order))
    filtered_shift = f_shift * mask

    return inverse_fft(filtered_shift)
