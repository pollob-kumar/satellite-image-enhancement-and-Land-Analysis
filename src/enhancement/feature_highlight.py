"""
feature_highlight.py
Highlights land-cover features (vegetation, water, urban/built-up areas)
in enhanced satellite imagery using color-based segmentation in the
HSV color space. This works on standard RGB satellite images; if a
near-infrared (NIR) band is available, `pseudo_ndvi` can be swapped
for a true NDVI computation.

NOTE: Thresholds are reasonable defaults for RGB imagery and may need
tuning per dataset/sensor.
"""

import cv2
import numpy as np


def _hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def highlight_vegetation(image, lower_green=(25, 40, 40), upper_green=(95, 255, 255)):
    """Mask + highlight vegetation regions (greenish hues) in bright green."""
    hsv = _hsv(image)
    mask = cv2.inRange(hsv, np.array(lower_green), np.array(upper_green))

    overlay = image.copy()
    overlay[mask > 0] = [0, 255, 0]  # BGR bright green
    result = cv2.addWeighted(image, 0.6, overlay, 0.4, 0)
    return result, mask


def highlight_water(image, lower_blue=(90, 30, 30), upper_blue=(135, 255, 255)):
    """Mask + highlight water bodies (bluish hues) in bright blue."""
    hsv = _hsv(image)
    mask = cv2.inRange(hsv, np.array(lower_blue), np.array(upper_blue))

    overlay = image.copy()
    overlay[mask > 0] = [255, 0, 0]  # BGR bright blue
    result = cv2.addWeighted(image, 0.6, overlay, 0.4, 0)
    return result, mask


def highlight_urban(image, saturation_max=60, value_min=100):
    """
    Urban/built-up areas tend to be low-saturation, mid-to-high brightness
    (concrete, roads, rooftops). Highlighted in red.
    """
    hsv = _hsv(image)
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    mask = ((s < saturation_max) & (v > value_min)).astype(np.uint8) * 255

    overlay = image.copy()
    overlay[mask > 0] = [0, 0, 255]  # BGR bright red
    result = cv2.addWeighted(image, 0.6, overlay, 0.4, 0)
    return result, mask


def combined_land_cover_map(image):
    """
    Produce a single composite map with vegetation (green), water (blue),
    and urban (red) regions overlaid together for visual land analysis.
    """
    _, veg_mask = highlight_vegetation(image)
    _, water_mask = highlight_water(image)
    _, urban_mask = highlight_urban(image)

    composite = image.copy()
    composite[veg_mask > 0] = [0, 255, 0]
    composite[water_mask > 0] = [255, 0, 0]
    composite[urban_mask > 0] = [0, 0, 255]

    blended = cv2.addWeighted(image, 0.5, composite, 0.5, 0)
    return blended, {"vegetation": veg_mask, "water": water_mask, "urban": urban_mask}
