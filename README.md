# Satellite Image Enhancement for Land Analysis

**Course:** Digital Image Processing Sessional

## Objective
Enhance satellite imagery affected by noise, blur, or low contrast, and improve
visibility of land features (vegetation, water bodies, urban areas) using
spatial-domain and frequency-domain filtering techniques.

## Folder Structure(Short Version)
```
Satellite-Image-Enhancement/
├── data/               # raw / processed / reference images
├── src/                # all source code (see below)
├── notebooks/          # exploratory experiments
├── results/            # output figures + metrics_output.csv
├── docs/                # report and slides
└── tests/               # unit tests
```
## Folder Structure
```
Satellite-Image-Enhancement/
│
├── README.md                      # প্রজেক্ট overview, objective, কীভাবে রান করবে
├── requirements.txt                # opencv-python, numpy, matplotlib, scikit-image ইত্যাদি
│
├── data/
│   ├── raw/                        # অরিজিনাল (noisy/blurry/low-contrast) satellite images
│   ├── processed/                  # enhance করার পর সেভ করা images
│   └── reference/                  # (যদি থাকে) ground-truth / clean images, comparison এর জন্য
│
├── src/
│   ├── main.py                     # main pipeline চালানোর entry point
│   │
│   ├── spatial_domain/
│   │   ├── smoothing.py            # mean, gaussian, median filter
│   │   └── sharpening.py           # laplacian, unsharp masking, high-boost
│   │
│   ├── frequency_domain/
│   │   ├── fft_utils.py            # DFT/FFT, shift, magnitude spectrum
│   │   ├── low_pass_filter.py      # ideal/butterworth/gaussian LPF (denoise)
│   │   └── high_pass_filter.py     # HPF (edge/feature enhancement)
│   │
│   ├── enhancement/
│   │   ├── contrast_enhancement.py # histogram equalization, CLAHE
│   │   ├── noise_removal.py        # denoising techniques
│   │   └── feature_highlight.py    # vegetation/water/urban area highlighting (NDVI-like logic, color mapping)
│   │
│   ├── evaluation/
│   │   ├── metrics.py              # PSNR, MSE, SSIM, entropy calculation
│   │   └── visual_compare.py       # before/after plotting, histogram plotting
│   │
│   └── utils/
│       ├── io_utils.py             # image load/save helper
│       └── preprocessing.py        # grayscale conversion, resizing, normalization
│
├── notebooks/
│   └── experiments.ipynb           # interactive টেস্টিং ও visualization এর জন্য
│
├── results/
│   ├── figures/                    # before-after images, spectrum plots, histograms
│   └── metrics_output.csv          # quantitative results (PSNR/SSIM table)
│
├── docs/
│   ├── report.pdf                  # sessional report
│   └── presentation.pptx           # (যদি লাগে) slide
│
└── tests/
    └── test_filters.py             # ইউনিট টেস্ট (optional কিন্তু ভালো প্র্যাকটিস)
```

### `src/` modules
| Folder | Purpose |
|---|---|
| `spatial_domain/` | Mean, Gaussian, median, bilateral smoothing; Laplacian, unsharp mask, high-boost sharpening |
| `frequency_domain/` | FFT utilities; ideal / Gaussian / Butterworth low-pass & high-pass filters |
| `enhancement/` | Histogram equalization / CLAHE / gamma contrast; denoising; vegetation-water-urban highlighting |
| `evaluation/` | PSNR, MSE, SSIM, entropy metrics; before/after and histogram plotting |
| `utils/` | Image I/O, grayscale/resize/normalize, synthetic noise generator for demos |

## Setup
```bash
pip install -r requirements.txt
```

## Running the Web Application (Interactive Studio)
Launch the interactive web application:
```bash
python app.py
```
Then open your browser and navigate to: **`http://127.0.0.1:8000`**

### Web Studio Features:
- **Algorithm & Filter Hierarchy**: Select Spatial, Frequency, Contrast, Noise Removal, or Land Feature analysis domains and test any specific filter.
- **Live Parameter Controls**: Interactive sliders for kernel sizes, sigma, cutoff frequencies, filter orders, and clip limits.
- **Interactive Split Slider**: Before-and-after 20/20 comparison swipe slider.
- **Quality Metrics HUD**: Real-time calculation of PSNR, SSIM, MSE, and Shannon Entropy.
- **Intensity Histograms**: Dynamic RGB and luminance histograms powered by Chart.js.
- **2D FFT Frequency Spectrum**: Fourier spectrum visualization (Inferno colormap) showing frequency components.
- **Multi-Step Pipeline Builder**: Chain multiple filters sequentially (e.g., Denoise → CLAHE → Unsharp Mask → Land Classification).
- **Export**: Instant PNG download and CSV metrics report generation.

## CLI Usage (Alternative)
1. Place a satellite image in `data/raw/`, e.g. `data/raw/sample.jpg`.
2. Run the full pipeline:
```bash
python -m src.main --input data/raw/sample.jpg
```

   Add `--simulate_degradation` if your source image is already clean and you
   want to demonstrate noise/blur correction:
```bash
python -m src.main --input data/raw/sample.jpg --simulate_degradation
```
3. Outputs:
   - Enhanced image, LPF/HPF results, land-cover map → `data/processed/`
   - Before/after and histogram figures → `results/figures/`
   - Quantitative metrics table → `results/metrics_output.csv`

## Pipeline Summary
1. **Load** raw image (`utils/io_utils.py`)
2. **Denoise** — Non-Local Means (`enhancement/noise_removal.py`)
3. **Contrast enhance** — CLAHE (`enhancement/contrast_enhancement.py`)
4. **Sharpen** — Unsharp masking (`spatial_domain/sharpening.py`)
5. **Frequency-domain analysis** — FFT spectrum, Gaussian LPF/HPF (`frequency_domain/`)
6. **Feature highlighting** — vegetation (green) / water (blue) / urban (red) overlay (`enhancement/feature_highlight.py`)
7. **Evaluation** — PSNR, SSIM, MSE, entropy (`evaluation/metrics.py`)

## Tests
```bash
python -m pytest tests/
```

## Learning Outcomes Covered
- Frequency domain filters → `src/frequency_domain/`
- Spatial domain filters → `src/spatial_domain/`
- Smoothing & sharpening → both domains implemented
- Quantitative + visual analysis → `src/evaluation/`
- Remote sensing challenges (noise, blur, low contrast, land-cover distinction) → addressed end-to-end in `src/main.py`
