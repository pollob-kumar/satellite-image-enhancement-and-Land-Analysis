"""
web_service.py
Core processing engine adapting the DIP algorithms for the web interface.
Handles image decoding/encoding, dynamic filter dispatching, metric evaluation,
FFT spectrum extraction, histogram generation, and land cover statistics.
"""

import base64
import io
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np

# Import DIP project modules
from src.spatial_domain.smoothing import (
    mean_filter,
    gaussian_filter,
    median_filter,
    bilateral_filter,
)
from src.spatial_domain.sharpening import (
    laplacian_sharpen,
    unsharp_mask,
    high_boost_filter,
)
from src.frequency_domain.fft_utils import (
    compute_fft,
    compute_magnitude_spectrum,
    distance_grid,
)
from src.frequency_domain.low_pass_filter import (
    ideal_lowpass,
    gaussian_lowpass,
    butterworth_lowpass,
)
from src.frequency_domain.high_pass_filter import (
    ideal_highpass,
    gaussian_highpass,
    butterworth_highpass,
)
from src.enhancement.contrast_enhancement import (
    histogram_equalization,
    clahe_equalization,
    gamma_correction,
    linear_contrast_stretch,
)
from src.enhancement.noise_removal import (
    denoise_median,
    denoise_nlm,
    denoise_bilateral,
)
from src.enhancement.feature_highlight import (
    highlight_vegetation,
    highlight_water,
    highlight_urban,
    combined_land_cover_map,
)
from src.evaluation.metrics import evaluate_all, mse, psnr, compute_ssim, entropy


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DATA_DIR = DATA_DIR / "raw"


def list_sample_images() -> List[Dict[str, Any]]:
    """Return available sample satellite images in data/raw."""
    samples = []
    if not RAW_DATA_DIR.exists():
        return samples

    for entry in RAW_DATA_DIR.iterdir():
        if entry.is_file() and entry.suffix.lower() in [".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"]:
            category = "General"
            name_lower = entry.name.lower()
            if "urban" in name_lower:
                category = "Urban / Built-up Area"
            elif "vegetation" in name_lower or "forest" in name_lower or "photo" in name_lower:
                category = "Vegetation / Forest"
            elif "water" in name_lower or "ocean" in name_lower:
                category = "Water Bodies / Coastal"

            samples.append({
                "id": entry.name,
                "filename": entry.name,
                "category": category,
                "size_kb": round(entry.stat().st_size / 1024, 1),
            })
    return samples


def get_sample_image_path(filename: str) -> Optional[Path]:
    """Resolve sample image path safely."""
    target = RAW_DATA_DIR / filename
    if target.exists() and target.is_file():
        return target
    return None


def load_image_from_bytes(data: bytes) -> np.ndarray:
    """Decode raw bytes into OpenCV BGR image array."""
    nparr = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Failed to decode image from provided data.")
    return image


def load_image_from_base64(b64_str: str) -> np.ndarray:
    """Decode base64 string (with or without data URI prefix) into OpenCV image."""
    if "," in b64_str:
        b64_str = b64_str.split(",", 1)[1]
    decoded_bytes = base64.b64decode(b64_str)
    return load_image_from_bytes(decoded_bytes)


def encode_image_to_base64(image: np.ndarray, format: str = "png") -> str:
    """Encode OpenCV image array to base64 string with MIME header."""
    ext = f".{format}"
    success, buffer = cv2.imencode(ext, image)
    if not success:
        raise ValueError(f"Failed to encode image to {format}.")
    b64_str = base64.b64encode(buffer).decode("utf-8")
    mime = "image/jpeg" if format.lower() in ["jpg", "jpeg"] else "image/png"
    return f"data:{mime};base64,{b64_str}"


def calculate_histograms(image: np.ndarray) -> Dict[str, List[int]]:
    """Compute 256-bin histograms for B, G, R and Grayscale/Luminance."""
    histograms: Dict[str, List[int]] = {}
    
    if len(image.shape) == 3:
        # BGR channels
        for i, color_name in enumerate(["blue", "green", "red"]):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            histograms[color_name] = hist.flatten().astype(int).tolist()
        
        # Luminance / Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])
        histograms["gray"] = hist_gray.flatten().astype(int).tolist()
    else:
        hist_gray = cv2.calcHist([image], [0], None, [256], [0, 256])
        histograms["gray"] = hist_gray.flatten().astype(int).tolist()
        histograms["red"] = histograms["gray"]
        histograms["green"] = histograms["gray"]
        histograms["blue"] = histograms["gray"]

    return histograms


def get_fft_spectrum(image: np.ndarray) -> str:
    """Compute centered 2D FFT magnitude spectrum and return as base64 image."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Downsample if too large for FFT speed in web UI
    h, w = gray.shape[:2]
    if max(h, w) > 1024:
        scale = 1024 / max(h, w)
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    f_shift = compute_fft(gray)
    mag = compute_magnitude_spectrum(f_shift)
    # Apply colormap (INFERNO) for intuitive visualization
    colored_mag = cv2.applyColorMap(mag, cv2.COLORMAP_INFERNO)
    return encode_image_to_base64(colored_mag, format="png")


def apply_frequency_filter_multichannel(image: np.ndarray, filter_func, **params) -> np.ndarray:
    """Apply a frequency domain filter per channel for color images or directly for grayscale."""
    if len(image.shape) == 2:
        return filter_func(image, **params)
    
    # Process each BGR channel in frequency domain
    channels = cv2.split(image)
    filtered_channels = [filter_func(ch, **params) for ch in channels]
    return cv2.merge(filtered_channels)


def run_filter(image: np.ndarray, category: str, filter_name: str, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Dispatch filter execution based on category and filter name.
    Returns (enhanced_image, extra_data).
    """
    extra_data: Dict[str, Any] = {}
    
    def get_int(key, default):
        try:
            return int(params.get(key, default))
        except (TypeError, ValueError):
            return default
    
    def get_float(key, default):
        try:
            return float(params.get(key, default))
        except (TypeError, ValueError):
            return default

    # --- 1. SPATIAL DOMAIN SMOOTHING ---
    if category == "spatial_smoothing":
        if filter_name == "mean":
            ksize = get_int("ksize", 5)
            enhanced = mean_filter(image, ksize=ksize)
        elif filter_name == "gaussian":
            ksize = get_int("ksize", 5)
            sigma = get_float("sigma", 1.0)
            enhanced = gaussian_filter(image, ksize=ksize, sigma=sigma)
        elif filter_name == "median":
            ksize = get_int("ksize", 5)
            enhanced = median_filter(image, ksize=ksize)
        elif filter_name == "bilateral":
            d = get_int("d", 9)
            sigma_color = get_float("sigma_color", 75.0)
            sigma_space = get_float("sigma_space", 75.0)
            enhanced = bilateral_filter(image, d=d, sigma_color=sigma_color, sigma_space=sigma_space)
        else:
            raise ValueError(f"Unknown smoothing filter: {filter_name}")

    # --- 2. SPATIAL DOMAIN SHARPENING ---
    elif category == "spatial_sharpening":
        if filter_name == "laplacian":
            ksize = get_int("ksize", 3)
            # Laplacian ksize must be 1, 3, 5, 7
            if ksize % 2 == 0:
                ksize += 1
            enhanced = laplacian_sharpen(image, ksize=ksize)
        elif filter_name == "unsharp_mask":
            ksize = get_int("ksize", 5)
            sigma = get_float("sigma", 1.0)
            amount = get_float("amount", 1.5)
            threshold = get_int("threshold", 0)
            enhanced = unsharp_mask(image, ksize=ksize, sigma=sigma, amount=amount, threshold=threshold)
        elif filter_name == "high_boost":
            ksize = get_int("ksize", 5)
            sigma = get_float("sigma", 1.0)
            boost_factor = get_float("boost_factor", 1.5)
            enhanced = high_boost_filter(image, ksize=ksize, sigma=sigma, boost_factor=boost_factor)
        else:
            raise ValueError(f"Unknown sharpening filter: {filter_name}")

    # --- 3. FREQUENCY DOMAIN LOW-PASS ---
    elif category == "frequency_lowpass":
        cutoff = get_float("cutoff", 30.0)
        if filter_name == "ideal_lowpass":
            enhanced = apply_frequency_filter_multichannel(image, ideal_lowpass, cutoff=cutoff)
        elif filter_name == "gaussian_lowpass":
            enhanced = apply_frequency_filter_multichannel(image, gaussian_lowpass, cutoff=cutoff)
        elif filter_name == "butterworth_lowpass":
            order = get_int("order", 2)
            enhanced = apply_frequency_filter_multichannel(image, butterworth_lowpass, cutoff=cutoff, order=order)
        else:
            raise ValueError(f"Unknown frequency low-pass filter: {filter_name}")

    # --- 4. FREQUENCY DOMAIN HIGH-PASS ---
    elif category == "frequency_highpass":
        cutoff = get_float("cutoff", 30.0)
        if filter_name == "ideal_highpass":
            enhanced = apply_frequency_filter_multichannel(image, ideal_highpass, cutoff=cutoff)
        elif filter_name == "gaussian_highpass":
            enhanced = apply_frequency_filter_multichannel(image, gaussian_highpass, cutoff=cutoff)
        elif filter_name == "butterworth_highpass":
            order = get_int("order", 2)
            enhanced = apply_frequency_filter_multichannel(image, butterworth_highpass, cutoff=cutoff, order=order)
        else:
            raise ValueError(f"Unknown frequency high-pass filter: {filter_name}")

    # --- 5. CONTRAST ENHANCEMENT ---
    elif category == "contrast_enhancement":
        if filter_name == "histogram_equalization":
            if len(image.shape) == 3:
                ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
                ycrcb[:, :, 0] = histogram_equalization(ycrcb[:, :, 0])
                enhanced = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
            else:
                enhanced = histogram_equalization(image)
        elif filter_name == "clahe":
            clip_limit = get_float("clip_limit", 2.0)
            tile_grid = get_int("tile_grid_size", 8)
            enhanced = clahe_equalization(image, clip_limit=clip_limit, tile_grid_size=(tile_grid, tile_grid))
        elif filter_name == "gamma_correction":
            gamma = get_float("gamma", 1.2)
            enhanced = gamma_correction(image, gamma=gamma)
        elif filter_name == "linear_contrast_stretch":
            if len(image.shape) == 3:
                channels = cv2.split(image)
                stretched_channels = [linear_contrast_stretch(ch) for ch in channels]
                enhanced = cv2.merge(stretched_channels)
            else:
                enhanced = linear_contrast_stretch(image)
        else:
            raise ValueError(f"Unknown contrast enhancement: {filter_name}")

    # --- 6. NOISE REMOVAL ---
    elif category == "noise_removal":
        if filter_name == "median_denoise":
            ksize = get_int("ksize", 5)
            enhanced = denoise_median(image, ksize=ksize)
        elif filter_name == "nlm_denoise":
            h = get_float("h", 10.0)
            template_w = get_int("template_window", 7)
            search_w = get_int("search_window", 21)
            enhanced = denoise_nlm(image, h=h, template_window=template_w, search_window=search_w)
        elif filter_name == "bilateral_denoise":
            d = get_int("d", 9)
            sigma_color = get_float("sigma_color", 75.0)
            sigma_space = get_float("sigma_space", 75.0)
            enhanced = denoise_bilateral(image, d=d, sigma_color=sigma_color, sigma_space=sigma_space)
        else:
            raise ValueError(f"Unknown noise removal filter: {filter_name}")

    # --- 7. LAND FEATURE HIGHLIGHTING ---
    elif category == "feature_highlight":
        total_pixels = image.shape[0] * image.shape[1]
        
        if filter_name == "vegetation":
            enhanced, mask = highlight_vegetation(image)
            veg_pct = round((np.count_nonzero(mask) / total_pixels) * 100, 2)
            extra_data["land_stats"] = {"vegetation_pct": veg_pct}
            extra_data["mask_preview"] = encode_image_to_base64(mask, format="png")
        elif filter_name == "water":
            enhanced, mask = highlight_water(image)
            water_pct = round((np.count_nonzero(mask) / total_pixels) * 100, 2)
            extra_data["land_stats"] = {"water_pct": water_pct}
            extra_data["mask_preview"] = encode_image_to_base64(mask, format="png")
        elif filter_name == "urban":
            sat_max = get_int("saturation_max", 60)
            val_min = get_int("value_min", 100)
            enhanced, mask = highlight_urban(image, saturation_max=sat_max, value_min=val_min)
            urban_pct = round((np.count_nonzero(mask) / total_pixels) * 100, 2)
            extra_data["land_stats"] = {"urban_pct": urban_pct}
            extra_data["mask_preview"] = encode_image_to_base64(mask, format="png")
        elif filter_name == "combined_land_cover":
            enhanced, masks = combined_land_cover_map(image)
            veg_pct = round((np.count_nonzero(masks["vegetation"]) / total_pixels) * 100, 2)
            water_pct = round((np.count_nonzero(masks["water"]) / total_pixels) * 100, 2)
            urban_pct = round((np.count_nonzero(masks["urban"]) / total_pixels) * 100, 2)
            other_pct = max(0.0, round(100.0 - (veg_pct + water_pct + urban_pct), 2))
            extra_data["land_stats"] = {
                "vegetation_pct": veg_pct,
                "water_pct": water_pct,
                "urban_pct": urban_pct,
                "other_pct": other_pct,
            }
        else:
            raise ValueError(f"Unknown feature highlight filter: {filter_name}")

    else:
        raise ValueError(f"Unknown category: {category}")

    return enhanced, extra_data


def process_image_request(
    original_image: np.ndarray,
    category: str,
    filter_name: str,
    params: Dict[str, Any],
    compute_fft_flag: bool = True,
) -> Dict[str, Any]:
    """
    Main processing entry point. Executes filter, calculates metrics,
    histograms, FFT spectra, and formats JSON response.
    """
    start_time = time.perf_counter()
    
    enhanced_image, extra_data = run_filter(original_image, category, filter_name, params)
    
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
    
    # Quantitative metrics
    metrics = evaluate_all(original_image, enhanced_image)
    gray_orig = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY) if len(original_image.shape) == 3 else original_image
    metrics["Original_Entropy"] = entropy(gray_orig)
    metrics["Entropy_Gain"] = round(metrics["Entropy"] - metrics["Original_Entropy"], 4)
    metrics["Execution_Time_ms"] = elapsed_ms
    
    # Format metrics
    metrics["PSNR"] = round(metrics["PSNR"], 2) if metrics["PSNR"] != float("inf") else 999.0
    metrics["SSIM"] = round(metrics["SSIM"], 4)
    metrics["MSE"] = round(metrics["MSE"], 2)
    metrics["Entropy"] = round(metrics["Entropy"], 4)
    metrics["Original_Entropy"] = round(metrics["Original_Entropy"], 4)

    # Histograms
    hist_orig = calculate_histograms(original_image)
    hist_enh = calculate_histograms(enhanced_image)

    # FFT Spectrums
    fft_data = {}
    if compute_fft_flag:
        fft_data["original_fft"] = get_fft_spectrum(original_image)
        fft_data["enhanced_fft"] = get_fft_spectrum(enhanced_image)

    enhanced_b64 = encode_image_to_base64(enhanced_image, format="png")
    original_b64 = encode_image_to_base64(original_image, format="png")
    
    response = {
        "success": True,
        "category": category,
        "filter": filter_name,
        "execution_time_ms": elapsed_ms,
        "original_image": original_b64,
        "enhanced_image": enhanced_b64,
        "metrics": metrics,
        "histograms": {
            "original": hist_orig,
            "enhanced": hist_enh,
        },
        "fft": fft_data,
        "extra": extra_data,
        "image_info": {
            "width": original_image.shape[1],
            "height": original_image.shape[0],
            "channels": original_image.shape[2] if len(original_image.shape) == 3 else 1,
        }
    }
    
    return response


def run_pipeline(original_image: np.ndarray, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute a sequential multi-stage enhancement pipeline."""
    start_time = time.perf_counter()
    current_image = original_image.copy()
    step_results = []

    for i, step in enumerate(steps):
        category = step.get("category", "")
        filter_name = step.get("filter", "")
        params = step.get("params", {})
        
        current_image, extra = run_filter(current_image, category, filter_name, params)
        step_results.append({
            "step_index": i + 1,
            "category": category,
            "filter": filter_name,
            "image_preview": encode_image_to_base64(current_image, format="png"),
        })

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
    metrics = evaluate_all(original_image, current_image)
    gray_orig = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY) if len(original_image.shape) == 3 else original_image
    metrics["Original_Entropy"] = entropy(gray_orig)
    metrics["Entropy_Gain"] = round(metrics["Entropy"] - metrics["Original_Entropy"], 4)
    metrics["Execution_Time_ms"] = elapsed_ms
    
    metrics["PSNR"] = round(metrics["PSNR"], 2) if metrics["PSNR"] != float("inf") else 999.0
    metrics["SSIM"] = round(metrics["SSIM"], 4)
    metrics["MSE"] = round(metrics["MSE"], 2)
    metrics["Entropy"] = round(metrics["Entropy"], 4)

    return {
        "success": True,
        "execution_time_ms": elapsed_ms,
        "original_image": encode_image_to_base64(original_image, format="png"),
        "final_image": encode_image_to_base64(current_image, format="png"),
        "metrics": metrics,
        "histograms": {
            "original": calculate_histograms(original_image),
            "enhanced": calculate_histograms(current_image),
        },
        "fft": {
            "original_fft": get_fft_spectrum(original_image),
            "enhanced_fft": get_fft_spectrum(current_image),
        },
        "steps": step_results,
        "image_info": {
            "width": original_image.shape[1],
            "height": original_image.shape[0],
            "channels": original_image.shape[2] if len(original_image.shape) == 3 else 1,
        }
    }
