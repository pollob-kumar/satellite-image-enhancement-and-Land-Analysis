"""
app.py
FastAPI Web Application Server for Satellite Image Enhancement Studio.
Provides high-performance REST APIs and serves the modern single-page web UI.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import cv2
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.web_service import (
    get_sample_image_path,
    list_sample_images,
    load_image_from_base64,
    load_image_from_bytes,
    process_image_request,
    run_pipeline,
)

app = FastAPI(
    title="Satellite Image Enhancement Studio",
    description="Interactive Web Platform for Satellite Image Filtering and Land Analysis",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = PROJECT_ROOT / "static"
STATIC_DIR.mkdir(exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ProcessRequest(BaseModel):
    sample_id: Optional[str] = None
    image_b64: Optional[str] = None
    category: str
    filter_name: str
    params: Dict[str, Any] = Field(default_factory=dict)
    compute_fft: bool = True


class PipelineStep(BaseModel):
    category: str
    filter: str
    params: Dict[str, Any] = Field(default_factory=dict)


class PipelineRequest(BaseModel):
    sample_id: Optional[str] = None
    image_b64: Optional[str] = None
    steps: List[PipelineStep]


# Algorithm & Filter Schema registry for dynamic UI rendering
ALGORITHMS_REGISTRY = [
    {
        "id": "spatial_smoothing",
        "name": "Spatial Domain - Smoothing",
        "description": "Low-pass spatial filters to reduce sensor noise, atmospheric haze, and suppress granular variance.",
        "icon": "sparkles",
        "filters": [
            {
                "id": "gaussian",
                "name": "Gaussian Filter",
                "description": "Weighted 2D Gaussian kernel smoothing. Excellent balance of noise suppression and edge preservation.",
                "params": [
                    {"id": "ksize", "label": "Kernel Size (Odd)", "type": "slider", "min": 3, "max": 25, "step": 2, "default": 5},
                    {"id": "sigma", "label": "Gaussian Sigma (σ)", "type": "slider", "min": 0.1, "max": 10.0, "step": 0.1, "default": 1.5},
                ],
            },
            {
                "id": "bilateral",
                "name": "Bilateral Filter",
                "description": "Edge-preserving non-linear filter. Denoises flat regions (fields/water) while keeping boundaries (roads/coastlines) crisp.",
                "params": [
                    {"id": "d", "label": "Diameter (d)", "type": "slider", "min": 3, "max": 21, "step": 2, "default": 9},
                    {"id": "sigma_color", "label": "Sigma Color", "type": "slider", "min": 10, "max": 150, "step": 5, "default": 75},
                    {"id": "sigma_space", "label": "Sigma Space", "type": "slider", "min": 10, "max": 150, "step": 5, "default": 75},
                ],
            },
            {
                "id": "median",
                "name": "Median Filter",
                "description": "Replaces pixel with the neighborhood median. Highly effective against salt-and-pepper sensor dropout noise.",
                "params": [
                    {"id": "ksize", "label": "Kernel Size (Odd)", "type": "slider", "min": 3, "max": 21, "step": 2, "default": 5},
                ],
            },
            {
                "id": "mean",
                "name": "Mean / Box Filter",
                "description": "Simple neighborhood averaging. Fast general low-pass blurring.",
                "params": [
                    {"id": "ksize", "label": "Kernel Size", "type": "slider", "min": 3, "max": 25, "step": 2, "default": 5},
                ],
            },
        ],
    },
    {
        "id": "spatial_sharpening",
        "name": "Spatial Domain - Sharpening",
        "description": "High-pass spatial filters to highlight fine structural features, roads, building outlines, and land borders.",
        "icon": "zap",
        "filters": [
            {
                "id": "unsharp_mask",
                "name": "Unsharp Masking",
                "description": "Subtracts blurred image from original and adds scaled high frequencies. Enhances texture contrast.",
                "params": [
                    {"id": "ksize", "label": "Blur Kernel Size", "type": "slider", "min": 3, "max": 21, "step": 2, "default": 5},
                    {"id": "sigma", "label": "Blur Sigma (σ)", "type": "slider", "min": 0.5, "max": 5.0, "step": 0.1, "default": 1.0},
                    {"id": "amount", "label": "Sharpening Amount", "type": "slider", "min": 0.2, "max": 4.0, "step": 0.1, "default": 1.5},
                    {"id": "threshold", "label": "Contrast Threshold", "type": "slider", "min": 0, "max": 50, "step": 1, "default": 0},
                ],
            },
            {
                "id": "high_boost",
                "name": "High-Boost Filtering",
                "description": "Amplifies fine details while retaining an adjustable proportion of base low frequencies.",
                "params": [
                    {"id": "ksize", "label": "Kernel Size", "type": "slider", "min": 3, "max": 21, "step": 2, "default": 5},
                    {"id": "sigma", "label": "Sigma (σ)", "type": "slider", "min": 0.5, "max": 5.0, "step": 0.1, "default": 1.0},
                    {"id": "boost_factor", "label": "Boost Factor (A)", "type": "slider", "min": 1.0, "max": 3.5, "step": 0.1, "default": 1.5},
                ],
            },
            {
                "id": "laplacian",
                "name": "Laplacian Operator",
                "description": "Second-order derivative operator for accentuating rapid intensity transitions and sharp edges.",
                "params": [
                    {"id": "ksize", "label": "Laplacian Kernel Size", "type": "slider", "min": 1, "max": 7, "step": 2, "default": 3},
                ],
            },
        ],
    },
    {
        "id": "frequency_lowpass",
        "name": "Frequency Domain - Low-Pass",
        "description": "2D Fast Fourier Transform (FFT) low-pass filtering. Suppresses high-frequency noise in the frequency plane.",
        "icon": "activity",
        "filters": [
            {
                "id": "gaussian_lowpass",
                "name": "Gaussian Low-Pass Filter (GLPF)",
                "description": "Smooth frequency cutoff without ringing (Gibbs) artifacts.",
                "params": [
                    {"id": "cutoff", "label": "Cutoff Frequency (D₀)", "type": "slider", "min": 5, "max": 150, "step": 5, "default": 40},
                ],
            },
            {
                "id": "butterworth_lowpass",
                "name": "Butterworth Low-Pass Filter (BLPF)",
                "description": "Configurable frequency transition slope controlled by filter order n.",
                "params": [
                    {"id": "cutoff", "label": "Cutoff Frequency (D₀)", "type": "slider", "min": 5, "max": 150, "step": 5, "default": 40},
                    {"id": "order", "label": "Filter Order (n)", "type": "slider", "min": 1, "max": 8, "step": 1, "default": 2},
                ],
            },
            {
                "id": "ideal_lowpass",
                "name": "Ideal Low-Pass Filter (ILPF)",
                "description": "Hard frequency cutoff at radius D₀. Demonstrates classic sinc/ringing phenomenon.",
                "params": [
                    {"id": "cutoff", "label": "Cutoff Radius (D₀)", "type": "slider", "min": 5, "max": 150, "step": 5, "default": 40},
                ],
            },
        ],
    },
    {
        "id": "frequency_highpass",
        "name": "Frequency Domain - High-Pass",
        "description": "2D FFT high-pass filtering to extract prominent edges, building footprints, and coastline contours.",
        "icon": "layers",
        "filters": [
            {
                "id": "gaussian_highpass",
                "name": "Gaussian High-Pass Filter (GHPF)",
                "description": "Smooth frequency suppression of low frequencies. Produces clean edge maps.",
                "params": [
                    {"id": "cutoff", "label": "Cutoff Frequency (D₀)", "type": "slider", "min": 5, "max": 150, "step": 5, "default": 30},
                ],
            },
            {
                "id": "butterworth_highpass",
                "name": "Butterworth High-Pass Filter (BHPF)",
                "description": "Adjustable frequency roll-off to control edge sensitivity and gradient preservation.",
                "params": [
                    {"id": "cutoff", "label": "Cutoff Frequency (D₀)", "type": "slider", "min": 5, "max": 150, "step": 5, "default": 30},
                    {"id": "order", "label": "Filter Order (n)", "type": "slider", "min": 1, "max": 8, "step": 1, "default": 2},
                ],
            },
            {
                "id": "ideal_highpass",
                "name": "Ideal High-Pass Filter (IHPF)",
                "description": "Abrupt rejection of frequencies inside radius D₀.",
                "params": [
                    {"id": "cutoff", "label": "Cutoff Radius (D₀)", "type": "slider", "min": 5, "max": 150, "step": 5, "default": 30},
                ],
            },
        ],
    },
    {
        "id": "contrast_enhancement",
        "name": "Contrast Enhancement",
        "description": "Dynamic range adjustment for foggy, low-contrast, or sun-glare degraded satellite imagery.",
        "icon": "sun",
        "filters": [
            {
                "id": "clahe",
                "name": "CLAHE (Adaptive Equalization)",
                "description": "Contrast Limited Adaptive Histogram Equalization. Prevents over-amplification in uniform areas (e.g. sea/desert).",
                "params": [
                    {"id": "clip_limit", "label": "Clip Limit", "type": "slider", "min": 1.0, "max": 8.0, "step": 0.5, "default": 2.5},
                    {"id": "tile_grid_size", "label": "Grid Size (NxN)", "type": "slider", "min": 4, "max": 16, "step": 2, "default": 8},
                ],
            },
            {
                "id": "gamma_correction",
                "name": "Gamma Correction",
                "description": "Non-linear power-law transform. Gamma < 1 brightens shadows; Gamma > 1 darkens highlights.",
                "params": [
                    {"id": "gamma", "label": "Gamma Value (γ)", "type": "slider", "min": 0.2, "max": 3.0, "step": 0.1, "default": 1.2},
                ],
            },
            {
                "id": "histogram_equalization",
                "name": "Global Histogram Equalization",
                "description": "Flattens the overall intensity distribution to maximize global dynamic contrast.",
                "params": [],
            },
            {
                "id": "linear_contrast_stretch",
                "name": "Min-Max Contrast Stretch",
                "description": "Linearly maps the minimum and maximum image pixel intensities to full 0-255 range.",
                "params": [],
            },
        ],
    },
    {
        "id": "noise_removal",
        "name": "Noise Removal & Restoration",
        "description": "Advanced spatial and non-local restoration routines for sensor noise and atmospheric degradation.",
        "icon": "shield-check",
        "filters": [
            {
                "id": "nlm_denoise",
                "name": "Non-Local Means (NLM)",
                "description": "Averages similar pixel patches across the whole image. Preserves rich vegetation and crop textures.",
                "params": [
                    {"id": "h", "label": "Filter Strength (h)", "type": "slider", "min": 3.0, "max": 25.0, "step": 1.0, "default": 10.0},
                    {"id": "template_window", "label": "Template Window Size", "type": "slider", "min": 3, "max": 11, "step": 2, "default": 7},
                    {"id": "search_window", "label": "Search Window Size", "type": "slider", "min": 11, "max": 31, "step": 2, "default": 21},
                ],
            },
            {
                "id": "bilateral_denoise",
                "name": "Bilateral Denoising",
                "description": "Preserves sharp geographical transitions while smoothing flat terrain.",
                "params": [
                    {"id": "d", "label": "Diameter", "type": "slider", "min": 5, "max": 21, "step": 2, "default": 9},
                    {"id": "sigma_color", "label": "Sigma Color", "type": "slider", "min": 20, "max": 150, "step": 5, "default": 75},
                    {"id": "sigma_space", "label": "Sigma Space", "type": "slider", "min": 20, "max": 150, "step": 5, "default": 75},
                ],
            },
            {
                "id": "median_denoise",
                "name": "Impulse Noise Median Removal",
                "description": "Robust suppression of satellite transmission packet drop / dead pixel noise.",
                "params": [
                    {"id": "ksize", "label": "Kernel Size", "type": "slider", "min": 3, "max": 15, "step": 2, "default": 5},
                ],
            },
        ],
    },
    {
        "id": "feature_highlight",
        "name": "Land Feature Analysis & Highlighting",
        "description": "HSV color space segmentation and land cover classification for environmental mapping.",
        "icon": "map-pin",
        "filters": [
            {
                "id": "combined_land_cover",
                "name": "Combined Land-Cover Composite",
                "description": "Multi-class segmentation map: Vegetation (Green), Water Bodies (Blue), Urban / Built-up (Red).",
                "params": [],
            },
            {
                "id": "vegetation",
                "name": "Vegetation / Canopy Isolation",
                "description": "Segment and highlight green agricultural fields, forests, and canopy vegetation in bright green.",
                "params": [],
            },
            {
                "id": "water",
                "name": "Water Bodies / Coastal Isolation",
                "description": "Segment oceans, rivers, lakes, and reservoirs in vivid cyan/blue.",
                "params": [],
            },
            {
                "id": "urban",
                "name": "Urban / Built-up Areas",
                "description": "Segment low-saturation concrete, asphalt, rooftops, and transportation infrastructure in bright red.",
                "params": [
                    {"id": "saturation_max", "label": "Max Saturation Threshold", "type": "slider", "min": 20, "max": 120, "step": 5, "default": 60},
                    {"id": "value_min", "label": "Min Value / Brightness", "type": "slider", "min": 50, "max": 200, "step": 5, "default": 100},
                ],
            },
        ],
    },
]


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve main single-page interface."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h1>Satellite Image Enhancement Studio is starting...</h1>")


@app.get("/api/algorithms")
async def get_algorithms():
    """Return categorized algorithm and filter schema."""
    return {"algorithms": ALGORITHMS_REGISTRY}


@app.get("/api/samples")
async def get_samples():
    """List bundled sample raw satellite images."""
    return {"samples": list_sample_images()}


@app.get("/api/samples/{filename}")
async def get_sample_image(filename: str):
    """Retrieve raw sample image file."""
    path = get_sample_image_path(filename)
    if not path:
        raise HTTPException(status_code=404, detail="Sample image not found")
    return FileResponse(path)


def _resolve_input_image(sample_id: Optional[str], image_b64: Optional[str]):
    """Helper to resolve image from either sample_id or base64 payload."""
    if image_b64 and image_b64.strip():
        return load_image_from_base64(image_b64)
    if sample_id:
        path = get_sample_image_path(sample_id)
        if path:
            img = cv2.imread(str(path))
            if img is not None:
                return img
    # Fallback to first available sample
    samples = list_sample_images()
    if samples:
        path = get_sample_image_path(samples[0]["filename"])
        if path:
            return cv2.imread(str(path))
    raise HTTPException(status_code=400, detail="No valid input image provided or found.")


@app.post("/api/process")
async def process_image(req: ProcessRequest):
    """Execute selected algorithm and filter with parameters."""
    try:
        image = _resolve_input_image(req.sample_id, req.image_b64)
        result = process_image_request(
            original_image=image,
            category=req.category,
            filter_name=req.filter_name,
            params=req.params,
            compute_fft_flag=req.compute_fft,
        )
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


@app.post("/api/upload-process")
async def upload_and_process(
    file: UploadFile = File(...),
    category: str = Form(...),
    filter_name: str = Form(...),
    params_json: str = Form("{}"),
):
    """Process an uploaded image file directly with multipart form."""
    try:
        import json
        params = json.loads(params_json)
        contents = await file.read()
        image = load_image_from_bytes(contents)
        result = process_image_request(
            original_image=image,
            category=category,
            filter_name=filter_name,
            params=params,
            compute_fft_flag=True,
        )
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


@app.post("/api/pipeline")
async def process_pipeline(req: PipelineRequest):
    """Execute multi-step enhancement pipeline."""
    try:
        image = _resolve_input_image(req.sample_id, req.image_b64)
        steps_dicts = [{"category": s.category, "filter": s.filter, "params": s.params} for s in req.steps]
        result = run_pipeline(image, steps_dicts)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
