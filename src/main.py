"""
main.py
End-to-end pipeline:
1. Load a raw satellite image
2. (Optional) simulate degradation for demo purposes
3. Denoise -> Contrast enhance -> Sharpen  (spatial domain)
4. Also demonstrate frequency-domain LPF/HPF
5. Highlight land-cover features (vegetation/water/urban)
6. Evaluate results quantitatively (PSNR/SSIM/Entropy)
7. Save processed images + figures + metrics report

Run from the project root:
    python -m src.main --input data/raw/sample.jpg
"""

import argparse
import os
import sys
import csv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2

from src.utils.io_utils import load_image, save_image
from src.utils.preprocessing import to_grayscale, add_synthetic_noise

from src.spatial_domain.smoothing import gaussian_filter, median_filter
from src.spatial_domain.sharpening import unsharp_mask

from src.frequency_domain.fft_utils import compute_fft, compute_magnitude_spectrum
from src.frequency_domain.low_pass_filter import gaussian_lowpass
from src.frequency_domain.high_pass_filter import gaussian_highpass

from src.enhancement.contrast_enhancement import clahe_equalization
from src.enhancement.noise_removal import denoise_nlm
from src.enhancement.feature_highlight import combined_land_cover_map

from src.evaluation.metrics import evaluate_all
from src.evaluation.visual_compare import (
    show_before_after,
    plot_histogram_comparison,
    plot_magnitude_spectrum,
)


def run_pipeline(input_path, output_dir="data/processed", figures_dir="results/figures",
                  simulate_degradation=False, show_plots=False):

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    basename = os.path.splitext(os.path.basename(input_path))[0]

    # 1. Load
    original = load_image(input_path, color_mode="color")

    # 2. Optional synthetic degradation (useful when demoing on clean images)
    working = original.copy()
    if simulate_degradation:
        working = add_synthetic_noise(working, noise_type="gaussian", amount=20)
        working = add_synthetic_noise(working, noise_type="blur", amount=15)
        save_image(working, os.path.join(output_dir, f"{basename}_degraded.png"))

    # 3. Spatial-domain enhancement pipeline
    denoised = denoise_nlm(working)
    contrast_enhanced = clahe_equalization(denoised)
    sharpened = unsharp_mask(contrast_enhanced, ksize=5, sigma=1.0, amount=1.2)

    save_image(sharpened, os.path.join(output_dir, f"{basename}_enhanced.png"))

    # 4. Frequency-domain demonstration (on grayscale)
    gray = to_grayscale(working)
    f_shift = compute_fft(gray)
    spectrum = compute_magnitude_spectrum(f_shift)
    lpf_result = gaussian_lowpass(gray, cutoff=40)
    hpf_result = gaussian_highpass(gray, cutoff=40)

    save_image(spectrum, os.path.join(output_dir, f"{basename}_spectrum.png"))
    save_image(lpf_result, os.path.join(output_dir, f"{basename}_lpf.png"))
    save_image(hpf_result, os.path.join(output_dir, f"{basename}_hpf.png"))

    # 5. Land-cover feature highlighting
    land_cover_map, masks = combined_land_cover_map(sharpened)
    save_image(land_cover_map, os.path.join(output_dir, f"{basename}_landcover.png"))

    # 6. Quantitative evaluation (vs the working/degraded input)
    metrics = evaluate_all(working, sharpened)
    print(f"\n[Metrics] {basename}")
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}")

    metrics_path = os.path.join("results", "metrics_output.csv")
    os.makedirs("results", exist_ok=True)
    file_exists = os.path.exists(metrics_path)
    with open(metrics_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["image", "MSE", "PSNR", "SSIM", "Entropy"])
        writer.writerow([basename, metrics["MSE"], metrics["PSNR"], metrics["SSIM"], metrics["Entropy"]])

    # 7. Visual comparisons (saved as figures)
    show_before_after(
        working, sharpened,
        titles=("Input", "Enhanced"),
        save_path=os.path.join(figures_dir, f"{basename}_before_after.png"),
    )
    plot_histogram_comparison(
        to_grayscale(working), to_grayscale(sharpened),
        save_path=os.path.join(figures_dir, f"{basename}_histogram.png"),
    )
    plot_magnitude_spectrum(
        spectrum, title=f"{basename} - FFT Magnitude Spectrum",
        save_path=os.path.join(figures_dir, f"{basename}_spectrum_plot.png"),
    )

    print(f"\nDone. Outputs saved in '{output_dir}' and '{figures_dir}'.")
    return {
        "enhanced": sharpened,
        "land_cover_map": land_cover_map,
        "metrics": metrics,
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Satellite Image Enhancement Pipeline")
    parser.add_argument("--input", required=True, help="Path to raw satellite image")
    parser.add_argument("--output_dir", default="data/processed")
    parser.add_argument("--figures_dir", default="results/figures")
    parser.add_argument("--simulate_degradation", action="store_true",
                         help="Add synthetic noise/blur before enhancing (for demo on clean images)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(
        input_path=args.input,
        output_dir=args.output_dir,
        figures_dir=args.figures_dir,
        simulate_degradation=args.simulate_degradation,
    )
