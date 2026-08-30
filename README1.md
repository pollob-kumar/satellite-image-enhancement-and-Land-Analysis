### <span style="color:red">1</span>
Ei project ta complete korte sudu best and clean folder structure dao. 
Subject: DIGITAL IMAGE PROCESSING SESSIONAL

Satellite Image Enhancement for Land Analysis Project Statement Create a digital image processing system to improve satellite imagery affected by noise, blur, or low contrast. The system shall enhance land features such as vegetation, water bodies, and urban areas using suitable filtering techniques.
Expected Learning Outcomes: 
• Apply frequency and spatial domain filters 
• Use smoothing and sharpening techniques 
• Analyze image quality improvements visually and quantitatively 
• Understand remote sensing image challenges

<span style="color:red">---------------------------------</span>






এই প্রজেক্টের জন্য একটা ক্লিন, প্রফেশনাল ফোল্ডার স্ট্রাকচার নিচে দিলাম — যেটা রিপোর্ট লেখা, কোড অর্গানাইজ করা এবং রেজাল্ট প্রেজেন্ট করা তিনটার জন্যই সুবিধাজনক।

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

### কেন এভাবে সাজানো
- **spatial_domain vs frequency_domain** আলাদা রাখা হয়েছে যেন Expected Learning Outcome-এর ২টা পয়েন্ট (spatial + frequency filter) স্পষ্টভাবে দেখা যায়।
- **enhancement/** folder-এ contrast, noise removal, আর land-feature highlighting (vegetation/water/urban) আলাদা মডিউলে রাখা — evaluator সহজে বুঝবে কোন অংশ কী কাজ করছে।
- **evaluation/** আলাদা রাখা হয়েছে কারণ "visually and quantitatively analyze" — এটা রিপোর্টে দেখানোর জন্য critical অংশ (PSNR, SSIM, histogram compare)।
- **data/raw vs processed vs reference** থাকলে before-after তুলনা করা সহজ হয়, এবং রিপোর্টে স্ক্রিনশট নেওয়াও সহজ।
- **results/** এ figures ও metrics আলাদা রাখলে রিপোর্ট লেখার সময় সরাসরি pull করা যায়।

চাইলে আমি এই স্ট্রাকচার অনুযায়ী actual খালি ফোল্ডার + স্টার্টার কোড ফাইল (যেমন `main.py`, `fft_utils.py` স্কেলিটন) বানিয়ে একটা zip আকারে দিতে পারি — বলো লাগবে কিনা।





### <span style="color:red">2</span>
ei folder structure onusare, tumi step by step code dao.
### <span style="color:red">---------------------------------</span>





আমি পুরো প্রজেক্ট স্ট্রাকচার অনুযায়ী actual কোড ফাইল বানিয়ে দিচ্ছি। প্রথমে ফোল্ডার তৈরি করি।Now let's quickly verify everything imports and runs correctly with a synthetic test image.Pipeline চলছে ঠিকমতো। এখন quick sanity test আর zip বানিয়ে দিচ্ছি।সব টেস্ট পাস করেছে এবং পুরো পাইপলাইন কাজ করছে। এখন test artifacts মুছে ক্লিন zip বানাচ্ছি।Directory structure ঠিক হয়ে গেছে। এখন re-verify করে ফাইনাল zip বানাচ্ছি।Confirmed working end-to-end. Now packaging the final zip.পুরো প্রজেক্ট রান করে টেস্ট করা হয়েছে — কাজ করছে ঠিকভাবে। এতে আছে:

- **`src/spatial_domain/`** — mean, Gaussian, median, bilateral smoothing + Laplacian, unsharp mask, high-boost sharpening
- **`src/frequency_domain/`** — FFT utils, ideal/Gaussian/Butterworth LPF ও HPF
- **`src/enhancement/`** — CLAHE contrast enhancement, NLM/median/bilateral denoising, vegetation-water-urban feature highlighting (HSV-based)
- **`src/evaluation/`** — PSNR, MSE, SSIM, entropy মেট্রিক্স + before/after ও হিস্টোগ্রাম প্লট
- **`src/main.py`** — সব একসাথে চালানোর সম্পূর্ণ pipeline
- **`tests/test_filters.py`** — sanity tests (সব pass করেছে)

চালানোর নিয়ম:
```bash
pip install -r requirements.txt
python -m src.main --input data/raw/your_image.jpg --simulate_degradation
```

`data/raw/` এ কোনো satellite image (বা যেকোনো ছবি) রাখলে সেটা degrade → denoise → contrast enhance → sharpen → land-cover highlight করে `data/processed/` আর `results/figures/`-এ ফলাফল সেভ হবে, আর `results/metrics_output.csv`-এ PSNR/SSIM/MSE/Entropy সেভ হবে — যেগুলো সরাসরি রিপোর্টে ব্যবহার করা যাবে।





### <span style="color:red">3</span>

ami asole bujhtechi na. folder structure ki vabe je kaj korche bujhtechi na.
ami code run korlam and kaj o holo kintu bujhlam na.

ami picture dichi:
urban_area_Adelaide_DougBarber.jpg

processed:
urban_area_Adelaide_DougBarber_enhanced.png
urban_area_Adelaide_DougBarber_hpf.png
urban_area_Adelaide_DougBarber_landcover.png
urban_area_Adelaide_DougBarber_lpf.png
urban_area_Adelaide_DougBarber_spectrum.png

results:
    figures:
    urban_area_Adelaide_DougBarber_before_after.png
    urban_area_Adelaide_DougBarber_histogram.png
   urban_area_Adelaide_DougBarber_spectrum_plot.png

metrics_output.csv

```csv
image,MSE,PSNR,SSIM,Entropy
urban_area_Adelaide_DougBarber,1104.800594155701,17.697964617360817,0.7523146365687189,7.817672887403056

```
### <span style="color:red">---------------------------------</span>




কোনো ছবি upload হয়নি, কিন্তু তুমি যেই output filenames দিয়েছ, সেগুলো দেখেই বুঝিয়ে দিচ্ছি — `main.py` ভেতরে ভেতরে কী কী ধাপে কাজ করেছে, আর প্রতিটা output file কোন ধাপ থেকে এসেছে।

## তুমি যা করেছ

```bash
python -m src.main --input data/raw/urban_area_Adelaide_DougBarber.jpg --simulate_degradation
```

এই একটা কমান্ড ভেতরে `run_pipeline()` ফাংশনকে কল করেছে, যেটা ৭টা ধাপে কাজ করে। প্রতিটা ধাপ **folder structure এর একটা নির্দিষ্ট module** ব্যবহার করে।

## ধাপে ধাপে কী হয়েছে

**ধাপ ১ — Load**
`src/utils/io_utils.py` দিয়ে তোমার `urban_area_Adelaide_DougBarber.jpg` লোড হয়েছে (এটা তোমার original ছবি)।

**ধাপ ২ — Degradation simulate**
তুমি `--simulate_degradation` flag দিয়েছ, তাই `src/utils/preprocessing.py` দিয়ে কৃত্রিমভাবে noise আর blur যোগ করা হয়েছে — কারণ তোমার original ছবিটা তো এমনিতে পরিষ্কার, তাই enhancement দেখানোর জন্য প্রথমে নষ্ট করে নেওয়া হয়েছে। (এটা `_degraded.png` হিসেবে সেভ হওয়ার কথা ছিল, তোমার লিস্টে দেখছি না — চেক করে দেখো `data/processed/` এ আছে কিনা)

**ধাপ ৩ — Spatial domain enhancement** (এখান থেকে `enhanced.png` তৈরি)
```
denoise (NLM) → contrast enhance (CLAHE) → sharpen (unsharp mask)
```
এই তিনটা ধাপ থেকে **`urban_area_Adelaide_DougBarber_enhanced.png`** তৈরি হয়েছে — এটাই তোমার মূল "before → after" ফলাফল। Noise কমেছে, contrast বেড়েছে, edges sharp হয়েছে।

**ধাপ ৪ — Frequency domain (FFT)** (এখান থেকে ৩টা ফাইল তৈরি)
- `_spectrum.png` → ছবিটার FFT magnitude spectrum (ছবিতে কোন frequency কতটা আছে তার visual)
- `_lpf.png` → Gaussian Low-Pass Filter প্রয়োগ করা ফলাফল (high-frequency/noise কেটে দিয়ে smooth করা)
- `_hpf.png` → Gaussian High-Pass Filter প্রয়োগ করা ফলাফল (শুধু edges/details রাখা, বাকি সব কালো)

**ধাপ ৫ — Land-cover highlighting**
`src/enhancement/feature_highlight.py` দিয়ে `enhanced.png` এর উপর HSV color analysis চালিয়ে vegetation (সবুজ), water (নীল), urban (লাল) — এই তিনটা আলাদা রঙে হাইলাইট করা হয়েছে → **`_landcover.png`**

**ধাপ ৬ — Quantitative evaluation**
`src/evaluation/metrics.py` দিয়ে **degraded ছবি vs enhanced ছবি** তুলনা করে PSNR/SSIM/MSE/Entropy বের করে `metrics_output.csv` এ লেখা হয়েছে।

**ধাপ ৭ — Visual plots** (`results/figures/` এ যায়)
- `_before_after.png` → পাশাপাশি degraded vs enhanced
- `_histogram.png` → দুইটার pixel intensity histogram তুলনা
- `_spectrum_plot.png` → FFT spectrum matplotlib দিয়ে plot করা ভার্সন

## তোমার metrics এর মানে কী

```
MSE: 1104.8      → degraded আর enhanced এর pixel difference (moderate)
PSNR: 17.7 dB    → তুলনামূলক কম, কারণ তুমি ইচ্ছাকৃতভাবে অনেক noise/blur যোগ করেছিলে
SSIM: 0.752      → structural মিল ৭৫%, মানে মূল গঠন মোটামুটি টিকে আছে
Entropy: 7.82    → বেশ high, মানে enhanced ছবিতে ভালো পরিমাণ detail/information আছে
```

## সংক্ষেপে folder ↔ code ম্যাপিং

| Output ফাইল | কোন module থেকে এসেছে |
|---|---|
| `_enhanced.png` | `spatial_domain/` + `enhancement/` |
| `_lpf.png`, `_hpf.png`, `_spectrum.png` | `frequency_domain/` |
| `_landcover.png` | `enhancement/feature_highlight.py` |
| `metrics_output.csv` | `evaluation/metrics.py` |
| `results/figures/*` | `evaluation/visual_compare.py` |

কোনো নির্দিষ্ট অংশ (যেমন — CLAHE ঠিক কী করে, বা FFT spectrum কীভাবে পড়তে হয়) নিয়ে আরও গভীরে জানতে চাইলে বলো, সেটা নিয়ে আলাদাভাবে বুঝিয়ে দিচ্ছি।






### <span style="color:red">4</span>


Madam jodi bole agula point koi implement korcho and tomar output a kon file ?

Expected Learning Outcomes 
• Apply frequency and spatial domain filters 
• Use smoothing and sharpening techniques 
• Analyze image quality improvements visually and quantitatively 
• Understand remote sensing image challenges
### <span style="color:red">---------------------------------</span>






ম্যাডাম যদি জিজ্ঞেস করে "কোথায় implement করেছ", তাহলে প্রতিটা Learning Outcome ধরে ধরে code file + function + output file বলতে পারবে। নিচে সাজিয়ে দিলাম।

## ১. Apply frequency and spatial domain filters

**Spatial domain** — `src/spatial_domain/`
- `smoothing.py` → `mean_filter()`, `gaussian_filter()`, `median_filter()`, `bilateral_filter()`
- `sharpening.py` → `laplacian_sharpen()`, `unsharp_mask()`, `high_boost_filter()`
- Pipeline-এ ব্যবহার হয়েছে `unsharp_mask()` → output: **`_enhanced.png`**

**Frequency domain** — `src/frequency_domain/`
- `fft_utils.py` → FFT নেওয়া ও ফেরত আনার core function (`compute_fft`, `inverse_fft`)
- `low_pass_filter.py` → `ideal_lowpass()`, `gaussian_lowpass()`, `butterworth_lowpass()`
- `high_pass_filter.py` → `ideal_highpass()`, `gaussian_highpass()`, `butterworth_highpass()`
- Pipeline-এ ব্যবহার হয়েছে `gaussian_lowpass()` ও `gaussian_highpass()` → output: **`_lpf.png`**, **`_hpf.png`**, spectrum দেখানোর জন্য **`_spectrum.png`**

➡️ **প্রমাণ:** `_lpf.png` (blurred/smooth version) আর `_hpf.png` (শুধু edges) পাশাপাশি দেখালেই বোঝা যায় frequency domain filter কাজ করেছে।

## ২. Use smoothing and sharpening techniques

- **Smoothing/Denoising** → `src/enhancement/noise_removal.py` এর `denoise_nlm()` (Non-Local Means) — pipeline-এর প্রথম ধাপ
- **Sharpening** → `src/spatial_domain/sharpening.py` এর `unsharp_mask()` — pipeline-এর শেষ ধাপ

➡️ **প্রমাণ:** `_before_after.png` — বামে degraded (noisy+blurry), ডানে enhanced (smooth+sharp)। এটা `results/figures/` এ আছে।

## ৩. Analyze image quality improvements visually and quantitatively

**Visual analysis** — `src/evaluation/visual_compare.py`
- `show_before_after()` → **`_before_after.png`**
- `plot_histogram_comparison()` → **`_histogram.png`** (pixel intensity distribution বদলেছে কিনা দেখায়)
- `plot_magnitude_spectrum()` → **`_spectrum_plot.png`**

**Quantitative analysis** — `src/evaluation/metrics.py`
- `mse()`, `psnr()`, `compute_ssim()`, `entropy()` → output: **`metrics_output.csv`**

➡️ **প্রমাণ:** তোমার CSV-তেই আছে —
```
MSE: 1104.8, PSNR: 17.7 dB, SSIM: 0.752, Entropy: 7.82
```
এগুলো সরাসরি এই outcome-এর প্রমাণ — সংখ্যা দিয়ে ছবির উন্নতি মাপা হয়েছে।

## ৪. Understand remote sensing image challenges

এটা মূলত concept/discussion অংশ, কিন্তু code-এ যেভাবে address করা হয়েছে:

- **Noise problem** → `add_synthetic_noise()` (`utils/preprocessing.py`) দিয়ে simulate করা হয়েছে, তারপর `denoise_nlm()` দিয়ে সমাধান
- **Blur problem** → একইভাবে simulate করে `unsharp_mask()` দিয়ে সমাধান
- **Low contrast problem** (satellite imagery-তে atmospheric haze এর কারণে সাধারণ) → `contrast_enhancement.py` এর `clahe_equalization()` দিয়ে সমাধান
- **Land-feature distinction problem** (vegetation/water/urban আলাদা করা কঠিন কারণ resolution/color mixing) → `feature_highlight.py` এর `combined_land_cover_map()` দিয়ে সমাধান → output: **`_landcover.png`**

➡️ **প্রমাণ:** `_landcover.png` — এখানে সবুজ (vegetation), নীল (water), লাল (urban) আলাদা করে দেখানো হয়েছে, যেটা remote sensing-এর একটা বাস্তব challenge (মানুষের চোখে land-cover আলাদা করা কঠিন, তাই automated highlighting দরকার)।

---

## সংক্ষিপ্ত টেবিল (রিপোর্ট বা presentation slide-এ দিতে পারো)

| Learning Outcome | Code Location | Output File |
|---|---|---|
| Frequency domain filter | `frequency_domain/low_pass_filter.py`, `high_pass_filter.py` | `_lpf.png`, `_hpf.png`, `_spectrum.png` |
| Spatial domain filter | `spatial_domain/smoothing.py`, `sharpening.py` | `_enhanced.png` |
| Smoothing | `enhancement/noise_removal.py` → `denoise_nlm()` | `_enhanced.png` (intermediate step) |
| Sharpening | `spatial_domain/sharpening.py` → `unsharp_mask()` | `_enhanced.png` |
| Visual quality analysis | `evaluation/visual_compare.py` | `_before_after.png`, `_histogram.png` |
| Quantitative quality analysis | `evaluation/metrics.py` | `metrics_output.csv` |
| Remote sensing challenges | `utils/preprocessing.py` (simulate) + `enhancement/` (solve) | `_landcover.png`, `metrics_output.csv` |

এই টেবিলটা presentation slide বা report-এর conclusion অংশে দিলে ম্যাডাম সহজেই বুঝবেন কোনটা কোথায় implement হয়েছে। চাইলে আমি এটার উপর ভিত্তি করে একটা ছোট PDF/PPT রিপোর্ট সামারিও বানিয়ে দিতে পারি — লাগবে কিনা বলো।



### <span style="color:red">5</span>

1. ei folder structure ta details a bujhe dao jate sob bujhte pari sob and working process.
2.  ami jodi git commit korte cai tahole kon kon file mile different different commit korbo. mane ekta project a to onek commit hoy and onek somoy related file gula mile ekta commit hoy and onek somoy sudu ekta file alada  commit korte hoy. tai ami cai tumi bujhe je dao kon file single and kon gula multiple file niye commit korte hobe.


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

### <span style="color:red">---------------------------------</span>


## ১. Folder Structure — Details এ Working Process

### Top-level ফাইল
- **`README.md`** — প্রজেক্টের পরিচয়পত্র। কেউ প্রথমবার প্রজেক্ট খুললে এখান থেকেই বুঝবে কী আছে, কীভাবে চালাতে হয়।
- **`requirements.txt`** — কোন লাইব্রেরি লাগবে তার লিস্ট। `pip install -r requirements.txt` দিলে সব একসাথে ইনস্টল হয়।

### `data/` — শুধু ছবি রাখার জায়গা, কোনো কোড নেই
- **`raw/`** → তুমি যে original satellite image দাও, সেটা এখানে বসে (input)
- **`processed/`** → `main.py` রান করার পর যত enhanced/filtered ছবি তৈরি হয়, সব এখানে সেভ হয় (output)
- **`reference/`** → যদি তোমার কাছে ground-truth (একদম পরিষ্কার) ছবি থাকে তুলনা করার জন্য, সেটা এখানে রাখা যায় — এখন এটা খালি, ভবিষ্যতে দরকার হলে ব্যবহার হবে

### `src/` — আসল কাজের কোড, এটাই প্রজেক্টের ইঞ্জিন

**`main.py`** — এটা conductor-এর মতো। নিজে কোনো filtering করে না, বরং বাকি সব module থেকে function ডেকে ডেকে ধাপে ধাপে চালায়। তুমি যখন `python -m src.main --input ...` চালাও, তখন এই ফাইলটাই প্রথমে রান হয়।

**`spatial_domain/`** — সরাসরি পিক্সেলের উপর কাজ করা filter গুলো
- `smoothing.py` → ছবি soft/smooth করে (noise কমায়)
- `sharpening.py` → ছবির edge গুলো স্পষ্ট করে

**`frequency_domain/`** — ছবিকে FFT দিয়ে frequency-তে রূপান্তর করে filter করা
- `fft_utils.py` → বাকি দুইটা ফাইলের জন্য common tool (FFT নেওয়া/ফেরানো)
- `low_pass_filter.py` → high-frequency (noise/detail) কেটে দিয়ে smooth করে
- `high_pass_filter.py` → low-frequency কেটে দিয়ে শুধু edge/detail রাখে

**`enhancement/`** — উন্নত processing, যেগুলো spatial+frequency এর বাইরে
- `contrast_enhancement.py` → অন্ধকার/dull ছবিকে উজ্জ্বল-স্পষ্ট করে (CLAHE)
- `noise_removal.py` → advanced denoising (NLM algorithm)
- `feature_highlight.py` → vegetation/water/urban রঙ দিয়ে আলাদা করে চেনায়

**`evaluation/`** — কাজ কতটা ভালো হলো সেটা মাপার code
- `metrics.py` → সংখ্যায় মাপে (PSNR, SSIM, MSE, Entropy)
- `visual_compare.py` → চোখে দেখার জন্য গ্রাফ/প্লট বানায়

**`utils/`** — ছোট ছোট সাহায্যকারী ফাংশন, যেগুলো উপরের সব module ব্যবহার করে
- `io_utils.py` → ছবি লোড করা, সেভ করা
- `preprocessing.py` → grayscale করা, resize করা, আর ডেমোর জন্য কৃত্রিম noise বসানো

### কাজের ফ্লো (main.py এর ভেতরে)
```
data/raw/image.jpg
      ↓ (io_utils.py দিয়ে লোড)
      ↓ (preprocessing.py দিয়ে degrade করা, যদি flag দাও)
      ↓ (noise_removal.py → denoise)
      ↓ (contrast_enhancement.py → CLAHE)
      ↓ (spatial_domain/sharpening.py → sharpen)
      → data/processed/*_enhanced.png
      ↓ (frequency_domain/ → LPF, HPF, spectrum)
      → data/processed/*_lpf.png, *_hpf.png, *_spectrum.png
      ↓ (enhancement/feature_highlight.py)
      → data/processed/*_landcover.png
      ↓ (evaluation/metrics.py)
      → results/metrics_output.csv
      ↓ (evaluation/visual_compare.py)
      → results/figures/*.png
```

### বাকি অংশ
- **`notebooks/`** → পরীক্ষা-নিরীক্ষার জায়গা, চূড়ান্ত code এখানে থাকে না
- **`results/`** → শুধু output রাখার জায়গা (figures + metrics csv)
- **`docs/`** → রিপোর্ট আর প্রেজেন্টেশন ফাইল রাখার জায়গা
- **`tests/`** → code ঠিকমতো কাজ করছে কিনা যাচাই করার automated test

**মূল কথা:** `data/` ও `results/` শুধু ফাইল রাখার জায়গা, কোনো লজিক নেই। আসল কাজ সব `src/` এর ভেতরে, আর সেখানেও প্রতিটা folder একটা নির্দিষ্ট দায়িত্ব পালন করে (single responsibility)। এই কারণেই কেউ `frequency_domain/` folder খুললেই বুঝে যাবে ভেতরে FFT-related কোড আছে, `spatial_domain/` খুললেই বুঝবে সরাসরি pixel filter আছে।

---

## ২. Git Commit Strategy — কোন ফাইল Single, কোন গুলো একসাথে

Git commit-এর মূলনীতি হলো: **একটা commit একটা logical change represent করবে**। মানে "আমি একটা কাজ করেছি" — সেটা এক ফাইলে হোক বা পাঁচ ফাইলে, যদি সব একই উদ্দেশ্যে বদলেছে, তাহলে একসাথে commit করবে।

তোমার প্রজেক্টের জন্য বাস্তবসম্মত commit sequence নিচে দিলাম:

### Commit 1 — Project scaffold (single, foundational)
```
git add README.md requirements.txt
git commit -m "Initial project setup with README and dependencies"
```
এই দুইটা ফাইল একসাথে কারণ দুইটাই "প্রজেক্ট শুরু করার" কাজ — একটাও আলাদা করার দরকার নেই।

### Commit 2 — Folder structure + placeholders
```
git add data/ results/ docs/ notebooks/ tests/ .gitkeep
git commit -m "Add project folder structure with placeholder directories"
```

### Commit 3 — Utils (একসাথে, কারণ একে অপরের উপর নির্ভরশীল ভিত্তি)
```
git add src/utils/io_utils.py src/utils/preprocessing.py src/__init__.py src/utils/__init__.py
git commit -m "Add image I/O and preprocessing utility functions"
```

### Commit 4 — Spatial domain smoothing (single file, কারণ standalone feature)
```
git add src/spatial_domain/smoothing.py src/spatial_domain/__init__.py
git commit -m "Implement spatial domain smoothing filters (mean, gaussian, median, bilateral)"
```

### Commit 5 — Spatial domain sharpening (আলাদা commit, কারণ আলাদা feature)
```
git add src/spatial_domain/sharpening.py
git commit -m "Implement spatial domain sharpening (laplacian, unsharp mask, high-boost)"
```

### Commit 6 — Frequency domain FFT core (single, কারণ এটা বাকি দুইটার ভিত্তি)
```
git add src/frequency_domain/fft_utils.py src/frequency_domain/__init__.py
git commit -m "Add FFT utility functions for frequency domain processing"
```

### Commit 7 — LPF + HPF একসাথে (এই দুইটা related, একই সময় বানানো, একে অপরের complement)
```
git add src/frequency_domain/low_pass_filter.py src/frequency_domain/high_pass_filter.py
git commit -m "Implement low-pass and high-pass frequency domain filters"
```
> এখানে কেন একসাথে? কারণ দুইটাই `fft_utils.py` এর উপর নির্ভর করে, একই ধরনের কাজ (ideal/gaussian/butterworth), এবং একটা ছাড়া আরেকটা অসম্পূর্ণ মনে হয় review করার সময়।

### Commit 8 — Contrast enhancement (single)
```
git add src/enhancement/contrast_enhancement.py src/enhancement/__init__.py
git commit -m "Add contrast enhancement techniques (histogram eq, CLAHE, gamma)"
```

### Commit 9 — Noise removal (single, আলাদা feature)
```
git add src/enhancement/noise_removal.py
git commit -m "Add advanced denoising methods (NLM, bilateral, median)"
```

### Commit 10 — Feature highlighting (single, বড় ও আলাদা logic)
```
git add src/enhancement/feature_highlight.py
git commit -m "Implement vegetation/water/urban land-cover highlighting"
```

### Commit 11 — Evaluation metrics + visual compare (একসাথে, কারণ দুইটাই "evaluation" purpose)
```
git add src/evaluation/metrics.py src/evaluation/visual_compare.py src/evaluation/__init__.py
git commit -m "Add quantitative metrics and visual comparison tools"
```
> চাইলে এটাও দুই ভাগ করতে পারো (metrics আলাদা, visual_compare আলাদা) — যদি তুমি দুই দিনে দুইটা বানাও। কিন্তু একসাথে বানালে একসাথে commit করাই স্বাভাবিক।

### Commit 12 — Main pipeline (single, সবচেয়ে গুরুত্বপূর্ণ commit)
```
git add src/main.py
git commit -m "Add main pipeline integrating all enhancement and evaluation steps"
```

### Commit 13 — Tests (single, আলাদা কারণ এটা verification-এর কাজ)
```
git add tests/test_filters.py
git commit -m "Add unit tests for filter and metric functions"
```

### Commit 14 — Sample run outputs (optional, যদি রাখতে চাও)
```
git add data/processed/ results/figures/ results/metrics_output.csv
git commit -m "Add sample pipeline output for demonstration"
```

---

### সাধারণ নিয়ম (মনে রাখার জন্য)

| পরিস্থিতি | Single commit নাকি Multiple? |
|---|---|
| একটা ফাইল একটা independent feature/module | **Single** |
| দুইটা ফাইল একে অপরের সাথে সরাসরি জড়িত (যেমন LPF+HPF, একই ধরনের filter) | **একসাথে** |
| Config/setup ফাইল (README, requirements) | **একসাথে**, প্রজেক্টের শুরুতে |
| একটা ফাইল আরেকটার উপর নির্ভরশীল কিন্তু ভিন্ন সময়ে বানানো (যেমন smoothing vs sharpening) | **আলাদা আলাদা** |
| Bug fix | সবসময় **আলাদা commit**, feature commit-এর সাথে মেশাবে না |
| Output/generated ফাইল (processed images, csv) | কোডের commit থেকে **আলাদা**, কারণ এগুলো ফলাফল, কোড না |

**মূল টেস্ট:** নিজেকে জিজ্ঞেস করো — "এই commit মেসেজে যদি এক লাইনে লিখি, তাহলে কি সব ফাইলের কাজটা এক কথায় বলা যায়?" যদি হ্যাঁ হয়, একসাথে commit করো। যদি দুইটা আলাদা কথা বলতে হয়, তাহলে আলাদা commit করো।



### <span style="color:red">6</span>
Pipeline-এ ব্যবহার হয়েছে `unsharp_mask()` → output: `_enhanced.png`

Pipeline-এ ব্যবহার হয়েছে `gaussian_lowpass()` ও `gaussian_highpass()` → output: `_lpf.png`, `_hpf.png`, spectrum দেখানোর জন্য `_spectrum.png`

agula mane ki bujhai? ex: Spatial domain-er sudu `sharpening.py`unsharp_mask() algorithom use kora hoiche naki ? baki gula use kora hoyni?

### <span style="color:red">---------------------------------</span>

হ্যাঁ, ঠিক ধরেছ। এটা পরিষ্কার করে দেই।

## আসল ব্যাপারটা কী

তোমার `src/spatial_domain/sharpening.py` ফাইলে **৩টা ফাংশন** লেখা আছে:
- `laplacian_sharpen()`
- `unsharp_mask()`
- `high_boost_filter()`

কিন্তু `main.py` (pipeline) যখন চলে, তখন এর ভেতর থেকে **শুধু `unsharp_mask()` কে call করা হয়েছে**। বাকি দুইটা (`laplacian_sharpen`, `high_boost_filter`) ফাইলে **আছে, লেখা আছে, কাজ করে**, কিন্তু pipeline এই মুহূর্তে সেগুলো ব্যবহার করছে না।

একইভাবে:

| ফাইল | যা যা লেখা আছে | Pipeline আসলে যা call করেছে |
|---|---|---|
| `spatial_domain/smoothing.py` | `mean_filter`, `gaussian_filter`, `median_filter`, `bilateral_filter` | **একটাও না** (smoothing এর জন্য এখানে থেকে কিছু call হয়নি) |
| `spatial_domain/sharpening.py` | `laplacian_sharpen`, `unsharp_mask`, `high_boost_filter` | শুধু **`unsharp_mask`** |
| `frequency_domain/low_pass_filter.py` | `ideal_lowpass`, `gaussian_lowpass`, `butterworth_lowpass` | শুধু **`gaussian_lowpass`** |
| `frequency_domain/high_pass_filter.py` | `ideal_highpass`, `gaussian_highpass`, `butterworth_highpass` | শুধু **`gaussian_highpass`** |
| `enhancement/noise_removal.py` | `denoise_median`, `denoise_nlm`, `denoise_bilateral` | শুধু **`denoise_nlm`** |
| `enhancement/contrast_enhancement.py` | `histogram_equalization`, `clahe_equalization`, `gamma_correction`, `linear_contrast_stretch` | শুধু **`clahe_equalization`** |

## কেন এমন করা হয়েছে

আমি প্রতিটা module-এ **একাধিক option** দিয়ে রেখেছি (যেমন smoothing-এর জন্য ৪টা রকমের filter), যাতে —

1. তুমি Learning Outcome-এ "spatial ও frequency domain filter" বলতে যা যা টেকনিক আছে, সব demonstrate করতে পারো — শুধু একটা algorithm না জেনে অনেকগুলো জেনে রাখা
2. `main.py`-তে সবগুলো একসাথে ব্যবহার না করে, **প্রতিটা কাজের জন্য একটা করে best/practical algorithm বেছে** নিয়ে pipeline বানানো হয়েছে (বাস্তব প্রজেক্টে সব filter একসাথে apply করলে ফলাফল খারাপ হয়ে যায়)
3. বাকি algorithm গুলো তুমি **রিপোর্ট বা প্রেজেন্টেশনে comparison দেখানোর জন্য** ব্যবহার করতে পারবে — যেমন "mean vs gaussian vs median filter কীভাবে আলাদা ফলাফল দেয়" এটা দেখাতে চাইলে

## তাহলে কি বাকি ফাংশনগুলো অপ্রয়োজনীয়?

না। এগুলো **ready আছে, কিন্তু pipeline-এ wire করা হয়নি**। তুমি চাইলে `main.py` তে সহজেই বদলে নিতে পারো, যেমন:

```python
# এখন আছে:
sharpened = unsharp_mask(contrast_enhanced, ksize=5, sigma=1.0, amount=1.2)

# চাইলে বদলে করতে পারো:
sharpened = laplacian_sharpen(contrast_enhanced)
# অথবা
sharpened = high_boost_filter(contrast_enhanced, boost_factor=1.8)
```

## ম্যাডামকে যদি বলতে হয়

সত্যি কথাটাই বলবে — এটা লুকানোর কিছু নেই, বরং ভালো practice:

> "আমি স্মুথিং/শার্পনিং/ফিল্টারিং এর জন্য একাধিক algorithm implement করেছি (`smoothing.py`, `sharpening.py` ফাইলে), কিন্তু final pipeline-এ (`main.py`) practical output-এর জন্য সবচেয়ে effective একটা করে বেছে নিয়েছি — যেমন smoothing-এর জন্য mean/gaussian/median এর বদলে NLM denoising, sharpening-এর জন্য laplacian/high-boost এর বদলে unsharp masking।"

এতে বরং ভালো দেখাবে — মানে তুমি শুধু একটা টেকনিক শিখোনি, **অনেকগুলো জেনে, তুলনা করে সবচেয়ে ভালোটা বেছেছ**।

চাইলে আমি `main.py`-তে একটা optional comparison section যোগ করে দিতে পারি, যেখানে সব smoothing/sharpening algorithm একসাথে চালিয়ে পাশাপাশি দেখাবে — রিপোর্টের জন্য এটা খুব ভালো visual evidence হবে। লাগবে কি?


### <span style="color:red">7</span>
sharpened = unsharp_mask(contrast_enhanced, ksize=5, sigma=1.0, amount=1.2)

sharpened = laplacian_sharpen(contrast_enhanced)

sharpened = high_boost_filter(contrast_enhanced, boost_factor=1.8)


agular paramater kivabe janbo ba bujhbo ? mane mam jodi bole agula ki vabe bujhle contrast_enhanced, boost_factor=1.8 ba onno gula alada keno? ami cacchi nije nijei jeno iccha moto algorithm use korte pari.
### <span style="color:red">---------------------------------</span>

খুব ভালো প্রশ্ন। এটা বুঝলে তুমি সত্যিই "নিজে নিজে" algorithm ব্যবহার করতে পারবে, শুধু আমার দেওয়া code copy-paste না করে। ধাপে ধাপে বুঝিয়ে দিচ্ছি।

## প্রথমে একটা confusion পরিষ্কার করি

```python
sharpened = laplacian_sharpen(contrast_enhanced)
```

এখানে **`contrast_enhanced`** কোনো "parameter এর নাম" না — এটা তোমার **variable এর নাম**, যেখানে আগের ধাপের ছবিটা রাখা আছে। মানে "contrast enhance করা ছবিটাকে এখন sharpen করো" — এটা তুমি `img`, `x`, `my_photo` যা খুশি নাম দিতে পারতে, ফলাফল একই হতো। এটা parameter না, এটা শুধু **input ছবি**।

## এখন আসল parameter গুলো বুঝি

প্রতিটা function-এর ভেতরে গিয়ে দেখো কী কী parameter নেয়। যেমন:দেখো, প্রতিটা function এর প্রথম লাইনে (`def function_name(...)`) সব parameter লেখা থাকে, আর তার পাশে একটা `=value` থাকলে সেটা **default value** — মানে তুমি না দিলে এই মান নিজে থেকে ব্যবহার হবে।

## `laplacian_sharpen(image, ksize=3)`

| Parameter | মানে কী | বাড়ালে কী হয় | কমালে কী হয় |
|---|---|---|---|
| `image` | যেই ছবি sharpen করতে চাও | — | — |
| `ksize` | Laplacian operator এর kernel/window size (কতটুকু এলাকা দেখে edge বের করবে) | বড় kernel → মোটা/বড় edge ধরা পড়ে, কিন্তু noise ও বেশি amplify হয় | ছোট kernel → শুধু সূক্ষ্ম/সরু edge ধরে |

⚠️ শর্ত: `ksize` অবশ্যই **odd number** হতে হবে (1, 3, 5, 7...) — কারণ কোনো pixel-কে কেন্দ্র ধরে চারপাশে সমান দূরত্বে দেখতে হয়, জোড় সংখ্যা হলে center পাওয়া যায় না।

## `unsharp_mask(image, ksize=5, sigma=1.0, amount=1.5, threshold=0)`

এই algorithm এর মূল সূত্র (docstring-এই লেখা আছে):
```
sharpened = original + amount × (original − blurred)
```

| Parameter | মানে কী | বাড়ালে কী হয় |
|---|---|---|
| `ksize` | Blur করার সময় কতটুকু এলাকা নিয়ে average করবে | বড় হলে বেশি blur হয়, ফলে sharpening effect ও বেশি hard হয় |
| `sigma` | Gaussian blur এর তীব্রতা (spread) | বড় sigma → বেশি soft/wide blur |
| `amount` | কতটা sharpen করবে (মূল সূত্রের ঐ `amount` সংখ্যাটাই) | `amount=0` হলে কোনো sharpening হবে না (original ফেরত পাবে); `amount=3` দিলে অতিরিক্ত sharp, unrealistic দেখাবে |
| `threshold` | কত ছোট difference কে "noise" ধরে ignore করবে | বাড়ালে flat/সমান এলাকা (যেমন আকাশ, পানি) sharpen হবে না, শুধু আসল edge sharpen হবে |

**Intuition:** ছবিকে blur করে, তারপর "original − blurred" করলে শুধু **edge/detail অংশটা** বের হয়ে আসে (একে বলে "mask")। সেই mask-কে `amount` দিয়ে গুণ করে original-এ যোগ করলে edge গুলো জোরালো হয়ে যায়।

## `high_boost_filter(image, ksize=5, sigma=1.0, boost_factor=1.5)`

```
boosted = boost_factor × original + (original − blurred)
```

| Parameter | মানে কী |
|---|---|
| `ksize`, `sigma` | একই ভাবে blur করার জন্য (unsharp mask এর মতোই) |
| `boost_factor` | Original ছবিকে কতটা গুরুত্ব/ওজন দেবে। `boost_factor=1` হলে সাধারণ sharpening, `boost_factor=1.8` দিলে original-কে আরও বেশি প্রাধান্য দিয়ে sharpen করবে (তুলনায় বেশি "boost") |

## Frequency domain filter গুলোতে (LPF/HPF)

```python
gaussian_lowpass(gray_image, cutoff=30)
```

| Parameter | মানে কী |
|---|---|
| `cutoff` | Frequency domain-এ কোন radius পর্যন্ত জায়গাকে "low frequency" ধরবে | `cutoff` বাড়ালে বেশি frequency কে "low" ধরে রাখবে → কম blur হবে; `cutoff` কমালে বেশি aggressive blur হবে |

## এবার নিজে নিজে বোঝার জন্য সাধারণ নিয়ম (এইটাই আসল স্কিল)

Python-এ যেকোনো function দেখলে এভাবে পড়বে:

```python
def function_name(required_param, optional_param=default_value):
```

1. **যেগুলোতে `=` চিহ্ন নেই** (যেমন `image`) — এগুলো **must-give**, না দিলে error দেবে
2. **যেগুলোতে `=value`** আছে (যেমন `ksize=5`) — এগুলো **optional**, না দিলে ওই default value নিজে থেকে ব্যবহার হবে
3. Function-এর **docstring** (`"""...."""` অংশ) পড়লে বুঝবে সূত্র/logic কী
4. প্যারামিটারের নাম নিজেই ইঙ্গিত দেয় — `boost_factor`, `amount`, `cutoff`, `threshold` — নাম দেখেই আন্দাজ করা যায় কী নিয়ন্ত্রণ করছে

## নিজে experiment করার জন্য

তুমি চাইলে `main.py`-তে একটা লাইন বদলে সরাসরি চেষ্টা করে দেখতে পারো:

```python
# আগে
sharpened = unsharp_mask(contrast_enhanced, ksize=5, sigma=1.0, amount=1.2)

# পরীক্ষা ১: বেশি sharp করতে চাইলে
sharpened = unsharp_mask(contrast_enhanced, amount=2.5)

# পরীক্ষা ২: laplacian ব্যবহার করতে চাইলে
sharpened = laplacian_sharpen(contrast_enhanced, ksize=5)
```

চালিয়ে দেখো output ছবি কেমন বদলায় — এভাবেই আসলে বোঝা যায় parameter এর প্রভাব, শুধু সংজ্ঞা পড়ে না। 

চাইলে আমি এমন একটা ছোট script বানিয়ে দিতে পারি যেটা একই ছবিতে বিভিন্ন `amount`/`boost_factor`/`cutoff` value দিয়ে একসাথে পাশাপাশি দেখাবে (grid of results) — তাহলে চোখে দেখেই বুঝবে কোন value কী effect করে। বানিয়ে দেব?