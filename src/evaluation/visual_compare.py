"""
visual_compare.py
Plotting helpers for visually analyzing before/after enhancement
results (used in the report and evaluation notebook).
"""

import cv2
import matplotlib.pyplot as plt


def _to_rgb(image):
    if len(image.shape) == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def show_before_after(original, enhanced, titles=("Original", "Enhanced"), save_path=None):
    """Side-by-side comparison plot."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(_to_rgb(original), cmap="gray" if len(original.shape) == 2 else None)
    axes[0].set_title(titles[0])
    axes[0].axis("off")

    axes[1].imshow(_to_rgb(enhanced), cmap="gray" if len(enhanced.shape) == 2 else None)
    axes[1].set_title(titles[1])
    axes[1].axis("off")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_histogram_comparison(original_gray, enhanced_gray, save_path=None):
    """Overlay histograms of the original vs enhanced grayscale images."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(original_gray.ravel(), bins=256, range=(0, 255), alpha=0.5, label="Original")
    ax.hist(enhanced_gray.ravel(), bins=256, range=(0, 255), alpha=0.5, label="Enhanced")
    ax.set_title("Pixel Intensity Histogram Comparison")
    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Frequency")
    ax.legend()

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_magnitude_spectrum(magnitude_spectrum, title="Magnitude Spectrum", save_path=None):
    """Display the frequency-domain magnitude spectrum of an image."""
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(magnitude_spectrum, cmap="gray")
    ax.set_title(title)
    ax.axis("off")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
