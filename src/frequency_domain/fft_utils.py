"""
fft_utils.py
Core FFT helper functions shared by the low-pass and high-pass
frequency-domain filters.
"""

import numpy as np


def compute_fft(gray_image):
    """
    Compute the centered 2D FFT of a grayscale image.
    Returns the shifted frequency spectrum (complex array).
    """
    f = np.fft.fft2(gray_image.astype(np.float32))
    f_shift = np.fft.fftshift(f)
    return f_shift


def compute_magnitude_spectrum(f_shift):
    """Log-scaled magnitude spectrum, useful for visualization."""
    magnitude = 20 * np.log(np.abs(f_shift) + 1)
    magnitude = np.clip(magnitude, 0, 255)
    return magnitude.astype(np.uint8)


def inverse_fft(f_shift):
    """Reconstruct a spatial-domain image from a shifted FFT."""
    f_ishift = np.fft.ifftshift(f_shift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    img_back = np.clip(img_back, 0, 255)
    return img_back.astype(np.uint8)


def distance_grid(shape):
    """
    Return a grid of distances from the center of the frequency plane.
    Used to build ideal / Butterworth / Gaussian filter masks.
    """
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    dist = np.sqrt((y - crow) ** 2 + (x - ccol) ** 2)
    return dist
