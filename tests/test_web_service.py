"""
test_web_service.py
Integration tests for the web service engine and FastAPI endpoints.
"""

import os
import sys
import numpy as np
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, ALGORITHMS_REGISTRY
from src.web_service import (
    process_image_request,
    run_pipeline,
    list_sample_images,
    calculate_histograms,
    get_fft_spectrum,
)


def create_synthetic_satellite_image():
    """Create a synthetic 128x128 3-channel test image."""
    img = np.zeros((128, 128, 3), dtype=np.uint8)
    # Vegetation zone (greenish)
    img[:64, :64] = [30, 150, 40]
    # Water zone (bluish)
    img[64:, :64] = [180, 100, 20]
    # Urban zone (grey/concrete)
    img[:64, 64:] = [120, 120, 120]
    # Road / edge feature
    img[64:, 64:] = [200, 200, 200]
    return img


def test_list_samples():
    samples = list_sample_images()
    assert len(samples) >= 3


def test_calculate_histograms():
    img = create_synthetic_satellite_image()
    hists = calculate_histograms(img)
    assert "red" in hists and "green" in hists and "blue" in hists and "gray" in hists
    assert len(hists["red"]) == 256


def test_get_fft_spectrum():
    img = create_synthetic_satellite_image()
    spectrum_b64 = get_fft_spectrum(img)
    assert spectrum_b64.startswith("data:image/png;base64,")


def test_all_algorithms_in_registry():
    img = create_synthetic_satellite_image()
    for category_info in ALGORITHMS_REGISTRY:
        cat_id = category_info["id"]
        for filter_info in category_info["filters"]:
            filt_id = filter_info["id"]
            params = {p["id"]: p["default"] for p in filter_info.get("params", [])}
            
            result = process_image_request(
                original_image=img,
                category=cat_id,
                filter_name=filt_id,
                params=params,
                compute_fft_flag=True,
            )
            
            assert result["success"] is True
            assert result["enhanced_image"].startswith("data:image/png;base64,")
            assert "metrics" in result
            assert "PSNR" in result["metrics"]
            assert "SSIM" in result["metrics"]


def test_pipeline_execution():
    img = create_synthetic_satellite_image()
    steps = [
        {"category": "noise_removal", "filter": "median_denoise", "params": {"ksize": 3}},
        {"category": "contrast_enhancement", "filter": "clahe", "params": {"clip_limit": 2.0, "tile_grid_size": 8}},
        {"category": "spatial_sharpening", "filter": "unsharp_mask", "params": {"amount": 1.2, "sigma": 1.0}},
    ]
    
    result = run_pipeline(img, steps)
    assert result["success"] is True
    assert len(result["steps"]) == 3
    assert result["final_image"].startswith("data:image/png;base64,")


def test_fastapi_endpoints():
    client = TestClient(app)
    
    # 1. Root index
    res = client.get("/")
    assert res.status_code == 200
    
    # 2. Algorithms registry
    res = client.get("/api/algorithms")
    assert res.status_code == 200
    assert "algorithms" in res.json()
    
    # 3. Samples list
    res = client.get("/api/samples")
    assert res.status_code == 200
    assert len(res.json()["samples"]) >= 1
    
    # 4. Process endpoint with first sample
    sample_filename = res.json()["samples"][0]["filename"]
    res = client.post("/api/process", json={
        "sample_id": sample_filename,
        "category": "spatial_smoothing",
        "filter_name": "gaussian",
        "params": {"ksize": 5, "sigma": 1.5},
        "compute_fft": True,
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "enhanced_image" in data
    assert "metrics" in data
