# Satellite Image Enhancement Studio — Walkthrough

## Summary of Completed Work
We have built a web application for the **Satellite Image Enhancement for Land Analysis** project. The platform connects the Digital Image Processing (DIP) algorithms (Spatial & Frequency domain filtering, Contrast Enhancement, Noise Removal, Feature Highlighting, Quantitative Metrics) to an interactive, modern user interface.

---

## Key Modules Implemented

### 1. Web Service Adapter Engine ([`src/web_service.py`](file:///d:/antigravity/Satellite-Image-Enhancement/src/web_service.py))
- **Dynamic Filter Execution**: Integrates all DIP algorithms from `spatial_domain/`, `frequency_domain/`, `enhancement/`, and `evaluation/`.
- **2D Fourier Spectrum Visualizer**: Computes 2D FFT shifted magnitude spectra with Inferno colormapping for frequency analysis.
- **Multichannel Histogram Generation**: Computes 256-bin intensity distributions for Red, Green, Blue, and Luminance channels.
- **Quantitative Metrics Calculation**: Computes live PSNR, SSIM, MSE, Shannon Entropy, and Shannon Entropy Gain.
- **Land Cover Area Statistics**: Segments and calculates % coverage of vegetation, water bodies, and urban terrain.

### 2. FastAPI Application Server ([`app.py`](file:///d:/antigravity/Satellite-Image-Enhancement/app.py))
- Serves the Single-Page Application (SPA) at `http://127.0.0.1:8000`.
- API endpoints:
  - `GET /api/algorithms`: Schema of all domains, filters, descriptions, and dynamic slider parameter ranges.
  - `GET /api/samples`: Lists bundled satellite images (`urban_area_Adelaide`, `vegetation`, `water_bodies`).
  - `POST /api/process`: Executes filters with dynamic parameters on custom uploads or bundled samples.
  - `POST /api/pipeline`: Executes multi-stage sequential processing pipelines.

### 3. Modern Frontend User Interface
- **HTML Canvas & Controls** ([`static/index.html`](file:///d:/antigravity/Satellite-Image-Enhancement/static/index.html)): Clean dark theme with Tailwind CSS, Lucide icons, and Chart.js.
- **Styling** ([`static/css/style.css`](file:///d:/antigravity/Satellite-Image-Enhancement/static/css/style.css)): Custom glowing split slider, range sliders, dot-grid canvas, glassmorphic panels.
- **Application Logic** ([`static/js/app.js`](file:///d:/antigravity/Satellite-Image-Enhancement/static/js/app.js)):
  - **Interactive 20/20 Split Slider**: Smooth drag-and-swipe comparison between Original and Enhanced images.
  - **Live Auto-Apply & Debounce**: Instant visual feedback as sliders are adjusted.
  - **Histograms Overlay**: Chart.js rendering of Original vs Enhanced pixel distributions.
  - **Multi-Step Pipeline Builder**: Build and execute multi-stage enhancement chains.
  - **Export System**: Download enhanced images (PNG) and export CSV metrics summary reports.

---

## Validation & Automated Tests
We added an integration test suite ([`tests/test_web_service.py`](file:///d:/antigravity/Satellite-Image-Enhancement/tests/test_web_service.py)) and executed `pytest`:
```bash
python -m pytest tests/
```
**Result**: 11 out of 11 tests passed successfully in 6.52s.

---

## How to Launch the Web Application

To run the web studio on your machine:

1. Open your terminal in the project directory:
   ```bash
   python app.py
   ```
2. Open your browser and go to:
   ```text
   http://127.0.0.1:8000
   ```
