/**
 * GeoEnhance Studio - Client Application Logic
 * Interactive DIP Satellite Image Enhancement Platform
 */

// Application State
const state = {
  algorithms: [],
  samples: [],
  selectedSampleId: null,
  customImageB64: null,
  currentCategory: "spatial_smoothing",
  currentFilter: "gaussian",
  currentParams: {},
  viewMode: "split", // 'split' | 'sideBySide' | 'enhanced' | 'original'
  zoomLevel: 1.0,
  autoApply: true,
  histChannel: "gray",
  histogramData: null,
  pipelineSteps: [],
  isDraggingSlider: false,
  debounceTimer: null,
};

// Chart.js Instance
let histogramChart = null;

// DOM Elements
const elements = {
  sampleSelect: document.getElementById("sampleSelect"),
  imageUpload: document.getElementById("imageUpload"),
  autoApplyToggle: document.getElementById("autoApplyToggle"),
  downloadBtn: document.getElementById("downloadBtn"),
  exportReportBtn: document.getElementById("exportReportBtn"),
  
  tabSingle: document.getElementById("tabSingle"),
  tabPipeline: document.getElementById("tabPipeline"),
  singleFilterPanel: document.getElementById("singleFilterPanel"),
  pipelinePanel: document.getElementById("pipelinePanel"),

  categoryContainer: document.getElementById("categoryContainer"),
  filterContainer: document.getElementById("filterContainer"),
  filterDescription: document.getElementById("filterDescription"),
  parametersContainer: document.getElementById("parametersContainer"),
  resetParamsBtn: document.getElementById("resetParamsBtn"),
  applyFilterBtn: document.getElementById("applyFilterBtn"),

  pipelineStepsList: document.getElementById("pipelineStepsList"),
  addPipelineStepBtn: document.getElementById("addPipelineStepBtn"),
  runPipelineBtn: document.getElementById("runPipelineBtn"),

  systemStatus: document.getElementById("systemStatus"),
  processingTimeBadge: document.getElementById("processingTimeBadge"),

  // Viewport
  viewSplitSlider: document.getElementById("viewSplitSlider"),
  viewSideBySide: document.getElementById("viewSideBySide"),
  viewEnhancedOnly: document.getElementById("viewEnhancedOnly"),
  viewOriginalOnly: document.getElementById("viewOriginalOnly"),
  
  imgDimensions: document.getElementById("imgDimensions"),
  imgActiveFilter: document.getElementById("imgActiveFilter"),

  zoomInBtn: document.getElementById("zoomInBtn"),
  zoomOutBtn: document.getElementById("zoomOutBtn"),
  zoomResetBtn: document.getElementById("zoomResetBtn"),
  zoomLevelText: document.getElementById("zoomLevelText"),
  fullscreenBtn: document.getElementById("fullscreenBtn"),

  loadingOverlay: document.getElementById("loadingOverlay"),
  splitSliderWrapper: document.getElementById("splitSliderWrapper"),
  splitOriginalClip: document.getElementById("splitOriginalClip"),
  sliderHandle: document.getElementById("sliderHandle"),
  imgEnhanced: document.getElementById("imgEnhanced"),
  imgOriginal: document.getElementById("imgOriginal"),

  sideBySideWrapper: document.getElementById("sideBySideWrapper"),
  imgSideOriginal: document.getElementById("imgSideOriginal"),
  imgSideEnhanced: document.getElementById("imgSideEnhanced"),

  // Metrics
  metricPSNR: document.getElementById("metricPSNR"),
  metricSSIM: document.getElementById("metricSSIM"),
  metricMSE: document.getElementById("metricMSE"),
  metricEntropy: document.getElementById("metricEntropy"),
  metricEntropyDelta: document.getElementById("metricEntropyDelta"),
  metricRatingBadge: document.getElementById("metricRatingBadge"),

  // Right analytics
  rightAnalyticsTitle: document.getElementById("rightAnalyticsTitle"),
  fftSpectrumView: document.getElementById("fftSpectrumView"),
  landCoverStatsView: document.getElementById("landCoverStatsView"),
  fftOriginalImg: document.getElementById("fftOriginalImg"),
  fftEnhancedImg: document.getElementById("fftEnhancedImg"),
  vegCoveragePct: document.getElementById("vegCoveragePct"),
  waterCoveragePct: document.getElementById("waterCoveragePct"),
  urbanCoveragePct: document.getElementById("urbanCoveragePct"),
  vegBar: document.getElementById("vegBar"),
  waterBar: document.getElementById("waterBar"),
  urbanBar: document.getElementById("urbanBar"),
};

// Initialize Application
async function initApp() {
  lucide.createIcons();
  setupEventListeners();
  initHistogramChart();

  try {
    setStatus("Loading registry...", "loading");
    // Fetch algorithms and samples
    const [algoRes, sampleRes] = await Promise.all([
      fetch("/api/algorithms").then((r) => r.json()),
      fetch("/api/samples").then((r) => r.json()),
    ]);

    state.algorithms = algoRes.algorithms || [];
    state.samples = sampleRes.samples || [];

    populateSamples();
    renderCategories();

    // Select first sample and apply default filter
    if (state.samples.length > 0) {
      state.selectedSampleId = state.samples[0].filename;
      elements.sampleSelect.value = state.selectedSampleId;
    }

    selectCategory(state.currentCategory);
    await processCurrent();
    setStatus("Ready", "ready");
  } catch (err) {
    console.error("Initialization error:", err);
    setStatus("Error loading application", "error");
  }
}

// Set Status Bar
function setStatus(message, type = "ready") {
  if (type === "loading") {
    elements.systemStatus.className = "flex items-center text-cyan-400";
    elements.systemStatus.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-cyan-400 mr-1.5 animate-ping"></span>${message}`;
    elements.loadingOverlay.classList.remove("hidden");
  } else if (type === "error") {
    elements.systemStatus.className = "flex items-center text-rose-400";
    elements.systemStatus.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-rose-400 mr-1.5"></span>${message}`;
    elements.loadingOverlay.classList.add("hidden");
  } else {
    elements.systemStatus.className = "flex items-center text-emerald-400";
    elements.systemStatus.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5"></span>${message}`;
    elements.loadingOverlay.classList.add("hidden");
  }
}

// Populate Sample Dropdown
function populateSamples() {
  elements.sampleSelect.innerHTML = "";
  state.samples.forEach((sample) => {
    const opt = document.createElement("option");
    opt.value = sample.filename;
    opt.textContent = `${sample.category}: ${sample.filename}`;
    elements.sampleSelect.appendChild(opt);
  });
}

// Render Categories
function renderCategories() {
  elements.categoryContainer.innerHTML = "";
  state.algorithms.forEach((cat) => {
    const btn = document.createElement("button");
    btn.className = `category-btn w-full text-left px-2.5 py-1.5 rounded-lg border border-slate-700/60 bg-surface-800/60 hover:bg-surface-700/80 text-xs font-semibold flex items-center justify-between transition ${
      state.currentCategory === cat.id ? "active" : "text-slate-300"
    }`;
    btn.innerHTML = `
      <span class="truncate">${cat.name}</span>
      <span class="text-[10px] text-slate-400 ml-1 font-mono">${cat.filters.length}</span>
    `;
    btn.onclick = () => selectCategory(cat.id);
    elements.categoryContainer.appendChild(btn);
  });
}

// Select Category
function selectCategory(catId) {
  state.currentCategory = catId;
  renderCategories();

  const category = state.algorithms.find((c) => c.id === catId);
  if (!category) return;

  // Populate Filters
  elements.filterContainer.innerHTML = "";
  category.filters.forEach((filter, idx) => {
    const btn = document.createElement("button");
    const isSelected = idx === 0 || filter.id === state.currentFilter;
    btn.className = `filter-btn w-full text-left px-2.5 py-1.5 rounded-md border border-slate-700/50 bg-surface-900/60 hover:bg-surface-800 text-xs font-medium flex items-center justify-between transition ${
      isSelected ? "active" : "text-slate-300"
    }`;
    btn.innerHTML = `
      <span class="truncate">${filter.name}</span>
      <i data-lucide="chevron-right" class="w-3 h-3 text-slate-500"></i>
    `;
    btn.onclick = () => selectFilter(filter.id);
    elements.filterContainer.appendChild(btn);
  });

  lucide.createIcons();

  // Select first filter of new category
  const firstFilter = category.filters[0];
  if (firstFilter) {
    selectFilter(firstFilter.id);
  }
}

// Select Specific Filter
function selectFilter(filterId) {
  state.currentFilter = filterId;

  // Highlight active filter button
  const category = state.algorithms.find((c) => c.id === state.currentCategory);
  if (!category) return;

  const filter = category.filters.find((f) => f.id === filterId);
  if (!filter) return;

  // Update description
  elements.filterDescription.textContent = filter.description;

  // Update filter buttons styling
  const buttons = elements.filterContainer.querySelectorAll(".filter-btn");
  category.filters.forEach((f, idx) => {
    if (f.id === filterId) {
      buttons[idx]?.classList.add("active");
    } else {
      buttons[idx]?.classList.remove("active");
    }
  });

  // Render Parameters
  renderParameters(filter);

  // Trigger processing
  if (state.autoApply) {
    triggerDebouncedProcess();
  }
}

// Render Parameters Sliders
function renderParameters(filter) {
  elements.parametersContainer.innerHTML = "";
  state.currentParams = {};

  if (!filter.params || filter.params.length === 0) {
    elements.parametersContainer.innerHTML =
      '<p class="text-xs text-slate-500 italic text-center py-2">No adjustable parameters for this filter.</p>';
    return;
  }

  filter.params.forEach((param) => {
    state.currentParams[param.id] = param.default;

    const group = document.createElement("div");
    group.className = "space-y-1";

    const labelRow = document.createElement("div");
    labelRow.className = "flex justify-between items-center text-[11px]";
    labelRow.innerHTML = `
      <span class="text-slate-300 font-medium">${param.label}</span>
      <span id="val_${param.id}" class="font-mono text-cyan-300 bg-surface-800 px-1.5 py-0.2 rounded border border-slate-700 font-bold">${param.default}</span>
    `;

    const slider = document.createElement("input");
    slider.type = "range";
    slider.min = param.min;
    slider.max = param.max;
    slider.step = param.step;
    slider.value = param.default;
    slider.className = "w-full cursor-pointer";

    slider.oninput = (e) => {
      const val = parseFloat(e.target.value);
      state.currentParams[param.id] = val;
      const valBadge = document.getElementById(`val_${param.id}`);
      if (valBadge) valBadge.textContent = val;

      if (state.autoApply) {
        triggerDebouncedProcess();
      }
    };

    group.appendChild(labelRow);
    group.appendChild(slider);
    elements.parametersContainer.appendChild(group);
  });
}

// Reset Parameters to Defaults
function resetParamsToDefaults() {
  const category = state.algorithms.find((c) => c.id === state.currentCategory);
  if (!category) return;
  const filter = category.filters.find((f) => f.id === state.currentFilter);
  if (!filter) return;

  renderParameters(filter);
  if (state.autoApply) {
    triggerDebouncedProcess();
  }
}

// Debounced Process Request
function triggerDebouncedProcess() {
  clearTimeout(state.debounceTimer);
  state.debounceTimer = setTimeout(() => {
    processCurrent();
  }, 120);
}

// Main Process Request to Backend
async function processCurrent() {
  try {
    setStatus("Processing...", "loading");
    
    const payload = {
      sample_id: state.customImageB64 ? null : state.selectedSampleId,
      image_b64: state.customImageB64 || null,
      category: state.currentCategory,
      filter_name: state.currentFilter,
      params: state.currentParams,
      compute_fft: true,
    };

    const res = await fetch("/api/process", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!data.success) {
      throw new Error(data.error || "Failed to process image.");
    }

    updateUIWithResult(data);
    setStatus("Ready", "ready");
  } catch (err) {
    console.error("Processing failed:", err);
    setStatus("Processing error: " + err.message, "error");
  }
}

// Update Viewport and Analytics with Backend Result
function updateUIWithResult(data) {
  // 1. Update Images
  elements.imgOriginal.src = data.original_image;
  elements.imgEnhanced.src = data.enhanced_image;
  elements.imgSideOriginal.src = data.original_image;
  elements.imgSideEnhanced.src = data.enhanced_image;

  // 2. Metadata info
  if (data.image_info) {
    elements.imgDimensions.textContent = `${data.image_info.width} × ${data.image_info.height} px`;
  }
  elements.imgActiveFilter.textContent = `${data.category} / ${data.filter}`;
  elements.processingTimeBadge.textContent = `${data.execution_time_ms} ms`;

  // 3. Quantitative Metrics
  const m = data.metrics || {};
  elements.metricPSNR.textContent = m.PSNR ?? "--";
  elements.metricSSIM.textContent = m.SSIM ?? "--";
  elements.metricMSE.textContent = m.MSE ?? "--";
  elements.metricEntropy.textContent = m.Entropy ?? "--";

  const entropyGain = m.Entropy_Gain ?? 0;
  const sign = entropyGain >= 0 ? "+" : "";
  elements.metricEntropyDelta.textContent = `(${sign}${entropyGain})`;
  elements.metricEntropyDelta.className =
    entropyGain >= 0
      ? "text-[10px] text-emerald-400 font-mono"
      : "text-[10px] text-rose-400 font-mono";

  // Quality Assessment Badge
  if (m.PSNR > 35) {
    elements.metricRatingBadge.textContent = "High Fidelity";
    elements.metricRatingBadge.className =
      "text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
  } else if (m.PSNR > 25) {
    elements.metricRatingBadge.textContent = "Moderate Shift";
    elements.metricRatingBadge.className =
      "text-[10px] font-bold px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/40";
  } else {
    elements.metricRatingBadge.textContent = "Heavy Transform";
    elements.metricRatingBadge.className =
      "text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/40";
  }

  // 4. Update Histograms
  if (data.histograms) {
    state.histogramData = data.histograms;
    updateHistogramChart();
  }

  // 5. Right Analytics (FFT or Land Cover)
  if (data.extra && data.extra.land_stats) {
    // Show Land Cover View
    elements.rightAnalyticsTitle.textContent = "Land Cover Breakdown";
    elements.fftSpectrumView.classList.add("hidden");
    elements.landCoverStatsView.classList.remove("hidden");
    elements.landCoverStatsView.classList.add("flex");

    const stats = data.extra.land_stats;
    const veg = stats.vegetation_pct ?? 0;
    const water = stats.water_pct ?? 0;
    const urban = stats.urban_pct ?? 0;

    elements.vegCoveragePct.textContent = `${veg}%`;
    elements.waterCoveragePct.textContent = `${water}%`;
    elements.urbanCoveragePct.textContent = `${urban}%`;

    elements.vegBar.style.width = `${veg}%`;
    elements.waterBar.style.width = `${water}%`;
    elements.urbanBar.style.width = `${urban}%`;
  } else {
    // Show FFT Spectrum View
    elements.rightAnalyticsTitle.textContent = "2D FFT Frequency Spectrum";
    elements.landCoverStatsView.classList.add("hidden");
    elements.landCoverStatsView.classList.remove("flex");
    elements.fftSpectrumView.classList.remove("hidden");

    if (data.fft) {
      elements.fftOriginalImg.src = data.fft.original_fft || "";
      elements.fftEnhancedImg.src = data.fft.enhanced_fft || "";
    }
  }
}

// Chart.js Histogram Setup
function initHistogramChart() {
  const ctx = document.getElementById("histogramChart").getContext("2d");
  const labels = Array.from({ length: 256 }, (_, i) => i);

  histogramChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Original",
          data: [],
          borderColor: "rgba(148, 163, 184, 0.6)",
          borderWidth: 1.5,
          borderDash: [3, 3],
          pointRadius: 0,
          fill: false,
        },
        {
          label: "Enhanced",
          data: [],
          borderColor: "rgb(6, 182, 212)",
          backgroundColor: "rgba(6, 182, 212, 0.15)",
          borderWidth: 2,
          pointRadius: 0,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 250 },
      plugins: {
        legend: { display: false },
        tooltip: {
          mode: "index",
          intersect: false,
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          titleFont: { size: 10 },
          bodyFont: { size: 10 },
        },
      },
      scales: {
        x: {
          display: true,
          grid: { display: false },
          ticks: { color: "#64748b", font: { size: 8 }, maxTicksLimit: 8 },
        },
        y: {
          display: false,
          grid: { color: "rgba(51, 65, 85, 0.3)" },
        },
      },
    },
  });
}

// Update Histogram Chart based on selected channel
function updateHistogramChart() {
  if (!histogramChart || !state.histogramData) return;

  const ch = state.histChannel;
  const origData = state.histogramData.original[ch] || [];
  const enhData = state.histogramData.enhanced[ch] || [];

  let enhColor = "rgb(6, 182, 212)";
  let enhBg = "rgba(6, 182, 212, 0.15)";

  if (ch === "red") {
    enhColor = "rgb(239, 68, 68)";
    enhBg = "rgba(239, 68, 68, 0.15)";
  } else if (ch === "green") {
    enhColor = "rgb(16, 185, 129)";
    enhBg = "rgba(16, 185, 129, 0.15)";
  } else if (ch === "blue") {
    enhColor = "rgb(59, 130, 246)";
    enhBg = "rgba(59, 130, 246, 0.15)";
  }

  histogramChart.data.datasets[0].data = origData;
  histogramChart.data.datasets[1].data = enhData;
  histogramChart.data.datasets[1].borderColor = enhColor;
  histogramChart.data.datasets[1].backgroundColor = enhBg;

  histogramChart.update();
}

// Setup Event Listeners
function setupEventListeners() {
  // Sample Switch
  elements.sampleSelect.addEventListener("change", (e) => {
    state.selectedSampleId = e.target.value;
    state.customImageB64 = null;
    processCurrent();
  });

  // Custom Image Upload
  elements.imageUpload.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      state.customImageB64 = event.target.result;
      processCurrent();
    };
    reader.readAsDataURL(file);
  });

  // Auto-apply toggle
  elements.autoApplyToggle.addEventListener("change", (e) => {
    state.autoApply = e.target.checked;
  });

  // Apply button
  elements.applyFilterBtn.addEventListener("click", () => {
    processCurrent();
  });

  // Reset params button
  elements.resetParamsBtn.addEventListener("click", () => {
    resetParamsToDefaults();
  });

  // Download Enhanced Image
  elements.downloadBtn.addEventListener("click", () => {
    if (!elements.imgEnhanced.src) return;
    const a = document.createElement("a");
    a.href = elements.imgEnhanced.src;
    a.download = `enhanced_${state.currentCategory}_${state.currentFilter}.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  });

  // Export Metrics Report
  elements.exportReportBtn.addEventListener("click", exportMetricsReport);

  // Tabs
  elements.tabSingle.addEventListener("click", () => {
    elements.tabSingle.className =
      "flex-1 py-2 text-xs font-bold rounded-lg flex items-center justify-center space-x-1.5 text-cyan-400 bg-surface-800 shadow-sm border border-slate-700/60 transition";
    elements.tabPipeline.className =
      "flex-1 py-2 text-xs font-semibold rounded-lg flex items-center justify-center space-x-1.5 text-slate-400 hover:text-slate-200 transition";
    elements.singleFilterPanel.classList.remove("hidden");
    elements.pipelinePanel.classList.add("hidden");
  });

  elements.tabPipeline.addEventListener("click", () => {
    elements.tabPipeline.className =
      "flex-1 py-2 text-xs font-bold rounded-lg flex items-center justify-center space-x-1.5 text-indigo-400 bg-surface-800 shadow-sm border border-slate-700/60 transition";
    elements.tabSingle.className =
      "flex-1 py-2 text-xs font-semibold rounded-lg flex items-center justify-center space-x-1.5 text-slate-400 hover:text-slate-200 transition";
    elements.singleFilterPanel.classList.add("hidden");
    elements.pipelinePanel.classList.remove("hidden");
  });

  // View Mode Switchers
  elements.viewSplitSlider.addEventListener("click", () => setViewMode("split"));
  elements.viewSideBySide.addEventListener("click", () => setViewMode("sideBySide"));
  elements.viewEnhancedOnly.addEventListener("click", () => setViewMode("enhanced"));
  elements.viewOriginalOnly.addEventListener("click", () => setViewMode("original"));

  // Zoom Controls
  elements.zoomInBtn.addEventListener("click", () => adjustZoom(0.2));
  elements.zoomOutBtn.addEventListener("click", () => adjustZoom(-0.2));
  elements.zoomResetBtn.addEventListener("click", () => resetZoom());

  // Fullscreen
  elements.fullscreenBtn.addEventListener("click", toggleFullscreen);

  // Histogram Channel Buttons
  document.querySelectorAll(".hist-chan-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      document.querySelectorAll(".hist-chan-btn").forEach((b) => b.classList.remove("active-hist"));
      e.target.classList.add("active-hist");
      state.histChannel = e.target.getAttribute("data-channel");
      updateHistogramChart();
    });
  });

  // Pipeline Step Handling
  elements.addPipelineStepBtn.addEventListener("click", addPipelineStep);
  elements.runPipelineBtn.addEventListener("click", executePipeline);

  // Setup Interactive Split Slider
  setupSplitSlider();
}

// Split Slider Drag & Move Logic
function setupSplitSlider() {
  const container = elements.splitSliderWrapper;
  const clip = elements.splitOriginalClip;
  const handle = elements.sliderHandle;

  function updateSliderPosition(clientX) {
    const rect = container.getBoundingClientRect();
    let offsetX = clientX - rect.left;
    let percentage = (offsetX / rect.width) * 100;
    percentage = Math.max(0, Math.min(100, percentage));

    clip.style.width = `${percentage}%`;
    handle.style.left = `${percentage}%`;
  }

  container.addEventListener("mousedown", (e) => {
    state.isDraggingSlider = true;
    updateSliderPosition(e.clientX);
  });

  window.addEventListener("mousemove", (e) => {
    if (!state.isDraggingSlider) return;
    updateSliderPosition(e.clientX);
  });

  window.addEventListener("mouseup", () => {
    state.isDraggingSlider = false;
  });

  // Touch support for mobile / tablets
  container.addEventListener("touchstart", (e) => {
    state.isDraggingSlider = true;
    updateSliderPosition(e.touches[0].clientX);
  });

  window.addEventListener("touchmove", (e) => {
    if (!state.isDraggingSlider) return;
    updateSliderPosition(e.touches[0].clientX);
  });

  window.addEventListener("touchend", () => {
    state.isDraggingSlider = false;
  });
}

// Set View Mode
function setViewMode(mode) {
  state.viewMode = mode;

  // Reset active classes
  [elements.viewSplitSlider, elements.viewSideBySide, elements.viewEnhancedOnly, elements.viewOriginalOnly].forEach(
    (b) => {
      b.className = "px-2.5 py-1 rounded text-slate-400 hover:text-slate-200 transition flex items-center space-x-1";
    }
  );

  if (mode === "split") {
    elements.viewSplitSlider.className =
      "px-2.5 py-1 rounded text-cyan-300 bg-surface-700/80 font-semibold transition flex items-center space-x-1";
    elements.splitSliderWrapper.classList.remove("hidden");
    elements.sideBySideWrapper.classList.add("hidden");
    elements.splitOriginalClip.style.width = "50%";
    elements.sliderHandle.style.display = "block";
    elements.sliderHandle.style.left = "50%";
  } else if (mode === "sideBySide") {
    elements.viewSideBySide.className =
      "px-2.5 py-1 rounded text-cyan-300 bg-surface-700/80 font-semibold transition flex items-center space-x-1";
    elements.splitSliderWrapper.classList.add("hidden");
    elements.sideBySideWrapper.classList.remove("hidden");
  } else if (mode === "enhanced") {
    elements.viewEnhancedOnly.className =
      "px-2.5 py-1 rounded text-cyan-300 bg-surface-700/80 font-semibold transition flex items-center space-x-1";
    elements.splitSliderWrapper.classList.remove("hidden");
    elements.sideBySideWrapper.classList.add("hidden");
    elements.splitOriginalClip.style.width = "0%";
    elements.sliderHandle.style.display = "none";
  } else if (mode === "original") {
    elements.viewOriginalOnly.className =
      "px-2.5 py-1 rounded text-cyan-300 bg-surface-700/80 font-semibold transition flex items-center space-x-1";
    elements.splitSliderWrapper.classList.remove("hidden");
    elements.sideBySideWrapper.classList.add("hidden");
    elements.splitOriginalClip.style.width = "100%";
    elements.sliderHandle.style.display = "none";
  }
}

// Zoom Handlers
function adjustZoom(delta) {
  state.zoomLevel = Math.max(0.4, Math.min(3.0, state.zoomLevel + delta));
  applyZoom();
}

function resetZoom() {
  state.zoomLevel = 1.0;
  applyZoom();
}

function applyZoom() {
  elements.zoomLevelText.textContent = `${Math.round(state.zoomLevel * 100)}%`;
  elements.splitSliderWrapper.style.transform = `scale(${state.zoomLevel})`;
  elements.splitSliderWrapper.style.transformOrigin = "center center";
  elements.sideBySideWrapper.style.transform = `scale(${state.zoomLevel})`;
  elements.sideBySideWrapper.style.transformOrigin = "center center";
}

// Fullscreen
function toggleFullscreen() {
  const elem = document.getElementById("canvasViewport");
  if (!document.fullscreenElement) {
    elem.requestFullscreen().catch((err) => alert(`Error: ${err.message}`));
  } else {
    document.exitFullscreen();
  }
}

// Export Metrics Report CSV
function exportMetricsReport() {
  const psnr = elements.metricPSNR.textContent;
  const ssim = elements.metricSSIM.textContent;
  const mse = elements.metricMSE.textContent;
  const entropy = elements.metricEntropy.textContent;
  const time = elements.processingTimeBadge.textContent;

  const csvContent =
    "data:text/csv;charset=utf-8," +
    "Metric,Value\n" +
    `Sample Image,${state.selectedSampleId || "Custom Upload"}\n` +
    `Category,${state.currentCategory}\n` +
    `Filter,${state.currentFilter}\n` +
    `Parameters,"${JSON.stringify(state.currentParams)}"\n` +
    `PSNR (dB),${psnr}\n` +
    `SSIM,${ssim}\n` +
    `MSE,${mse}\n` +
    `Shannon Entropy,${entropy}\n` +
    `Processing Time,${time}\n`;

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `metrics_${state.currentCategory}_${state.currentFilter}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Multi-Stage Pipeline Logic
function addPipelineStep() {
  const category = state.algorithms.find((c) => c.id === state.currentCategory) || state.algorithms[0];
  const filter = category.filters.find((f) => f.id === state.currentFilter) || category.filters[0];

  const step = {
    id: Date.now(),
    category: category.id,
    filter: filter.id,
    filterName: filter.name,
    params: { ...state.currentParams },
  };

  state.pipelineSteps.push(step);
  renderPipelineSteps();
}

function renderPipelineSteps() {
  elements.pipelineStepsList.innerHTML = "";
  if (state.pipelineSteps.length === 0) {
    elements.pipelineStepsList.innerHTML =
      '<p class="text-xs text-slate-500 italic text-center py-2">No steps in pipeline. Click "Add Step".</p>';
    return;
  }

  state.pipelineSteps.forEach((step, idx) => {
    const card = document.createElement("div");
    card.className =
      "bg-surface-800/80 p-2 rounded-lg border border-slate-700/60 flex items-center justify-between text-xs";
    card.innerHTML = `
      <div class="flex items-center space-x-2">
        <span class="w-5 h-5 rounded-full bg-cyan-500/20 text-cyan-400 font-bold flex items-center justify-center text-[10px]">
          ${idx + 1}
        </span>
        <div>
          <p class="font-bold text-slate-200">${step.filterName}</p>
          <p class="text-[10px] text-slate-400 font-mono">${JSON.stringify(step.params)}</p>
        </div>
      </div>
      <button class="text-rose-400 hover:text-rose-300 p-1" title="Remove step">
        <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
      </button>
    `;

    card.querySelector("button").onclick = () => {
      state.pipelineSteps.splice(idx, 1);
      renderPipelineSteps();
    };

    elements.pipelineStepsList.appendChild(card);
  });

  lucide.createIcons();
}

async function executePipeline() {
  if (state.pipelineSteps.length === 0) {
    alert("Please add at least one step to the pipeline.");
    return;
  }

  try {
    setStatus("Executing pipeline...", "loading");

    const payload = {
      sample_id: state.customImageB64 ? null : state.selectedSampleId,
      image_b64: state.customImageB64 || null,
      steps: state.pipelineSteps.map((s) => ({
        category: s.category,
        filter: s.filter,
        params: s.params,
      })),
    };

    const res = await fetch("/api/pipeline", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!data.success) {
      throw new Error(data.error || "Failed to execute pipeline.");
    }

    data.enhanced_image = data.final_image;
    data.category = "Pipeline";
    data.filter = `${state.pipelineSteps.length} Steps`;
    updateUIWithResult(data);
    setStatus("Pipeline Complete", "ready");
  } catch (err) {
    console.error("Pipeline failed:", err);
    setStatus("Pipeline error: " + err.message, "error");
  }
}

// Start application when DOM is ready
document.addEventListener("DOMContentLoaded", initApp);
