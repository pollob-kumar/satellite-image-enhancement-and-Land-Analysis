"""
io_utils.py
Helper functions for loading and saving images.
"""

import os
import cv2


def load_image(path, color_mode="color"):
    """
    Load an image from disk.

    Parameters
    ----------
    path : str
        Path to the image file.
    color_mode : str
        "color" -> loads as BGR (3-channel)
        "gray"  -> loads as single-channel grayscale

    Returns
    -------
    numpy.ndarray
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")

    flag = cv2.IMREAD_COLOR if color_mode == "color" else cv2.IMREAD_GRAYSCALE
    img = cv2.imread(path, flag)

    if img is None:
        raise ValueError(f"Failed to read image (unsupported format?): {path}")

    return img


def save_image(image, path):
    """
    Save an image to disk, creating parent directories if needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    success = cv2.imwrite(path, image)
    if not success:
        raise IOError(f"Failed to save image to: {path}")
    return path


def list_images(folder, extensions=(".png", ".jpg", ".jpeg", ".tif", ".tiff")):
    """
    Return a sorted list of full paths to image files in a folder.
    """
    files = [
        os.path.join(folder, f)
        for f in sorted(os.listdir(folder))
        if f.lower().endswith(extensions)
    ]
    return files
