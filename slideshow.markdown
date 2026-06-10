---
layout: default
title: Slideshow
permalink: /slideshow/
menus: [header]
show_banner: false
---

<style>
  /* 1. Hide default Jekyll theme header & footer on slideshow page for immersive view */
  .site-header, .site-footer {
    display: none !important;
  }
  .page-content {
    padding: 0 !important;
    margin: 0 !important;
    background: #496a40 !important;
  }
  .page-content .wrapper {
    max-width: none !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  body {
    overflow: hidden !important;
    background-color: #496a40 !important;
    margin: 0 !important;
  }

  /* 2. Slideshow Layout */
  .slideshow-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: linear-gradient(135deg, #496a40 0%, #375030 100%);
  }

  /* Top Minimalist Header Overlay (Controls) */
  .top-header-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 2rem;
    box-sizing: border-box;
    z-index: 100;
    pointer-events: none;
  }

  .top-header-overlay * {
    pointer-events: auto;
  }

  /* Back Link */
  .back-to-cases {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #ffffff !important;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 0.5rem 1.25rem;
    border-radius: 9999px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.2s ease;
  }

  .back-to-cases:visited {
    color: #ffffff !important;
  }

  .back-to-cases:hover {
    background: rgba(255, 255, 255, 0.18);
    transform: translateY(-1px);
  }

  .back-to-cases svg {
    transition: transform 0.2s ease;
  }

  .back-to-cases:hover svg {
    transform: translateX(-3px);
  }

  /* Controls Section */
  .right-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  /* Autoplay Capsule */
  .autoplay-capsule {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 0.45rem 1.25rem;
    border-radius: 9999px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    color: #ffffff;
  }

  .play-pause-btn {
    background: none;
    border: none;
    color: #ffffff;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.2rem;
    transition: transform 0.2s;
  }

  .play-pause-btn:hover {
    transform: scale(1.15);
  }

  .play-pause-btn svg {
    width: 1.15rem;
    height: 1.15rem;
  }

  .speed-select {
    background: transparent;
    border: none;
    color: #ffffff;
    font-family: inherit;
    font-size: 0.8rem;
    font-weight: 600;
    outline: none;
    cursor: pointer;
    padding-right: 1.25rem;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right center;
  }

  .speed-select option {
    background: #375030;
    color: #ffffff;
  }

  .progress-bar-container {
    width: 80px;
    height: 4px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 2px;
    overflow: hidden;
  }

  .progress-bar-fill {
    height: 100%;
    width: 0%;
    background: #ffffff;
    border-radius: 2px;
  }

  .slide-counter {
    font-family: 'Outfit', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    min-width: 45px;
    text-align: center;
  }

  /* Case Selector Capsule */
  .case-select-capsule {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 0.45rem 1.25rem;
    border-radius: 9999px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }

  .case-select {
    background: transparent;
    border: none;
    color: #ffffff;
    font-family: inherit;
    font-size: 0.8rem;
    font-weight: 600;
    outline: none;
    cursor: pointer;
    padding-right: 1.5rem;
    max-width: 250px;
    text-overflow: ellipsis;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right center;
  }

  .case-select option {
    background: #375030;
    color: #ffffff;
  }

  /* Static/Fixed Header Info & Logo (Stays static unless changing) */
  .fixed-top-header {
    position: absolute;
    top: 6.5rem;
    left: 4.5rem;
    right: 4.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    z-index: 90;
    pointer-events: none;
  }

  .fixed-top-header * {
    pointer-events: auto;
  }

  .slide-case-info {
    max-width: 65%;
    opacity: 1;
    transition: opacity 0.2s ease-in-out;
  }

  .slide-case-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff !important;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.01em;
  }

  .slide-case-subtitle {
    font-size: 0.95rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.85);
    margin: 0;
    line-height: 1.45;
  }

  .slide-pave-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3.5rem;
    height: 3.5rem;
    background: transparent;
  }

  .slide-pave-logo img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  /* Slides Track */
  .slides-track {
    display: flex;
    width: 100%;
    height: 100%;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .slide-item {
    width: 100vw;
    height: 100vh;
    flex-shrink: 0;
    position: relative;
    box-sizing: border-box;
    padding: 11rem 4.5rem 5rem 4.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    z-index: 1;
    overflow: hidden;
  }

  /* Fixed Background Layers (sit on container, never move with slides) */
  .bg-layer {
    position: absolute;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    transition: opacity 0.7s ease;
  }

  .bg-layer-halftone {
    position: absolute;
    bottom: -60vw;
    right: -60vw;
    top: auto;
    left: auto;
    width: 100vw;
    height: 100vw;
    background-image: url('{{ "/assets/images/halftone-circle.png" | relative_url }}');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    opacity: inherit;
  }

  /* Main Quote Content Area */
  .slide-quote-content {
    flex: 1;
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    max-width: 1100px;
    width: 100%;
    margin: 0 auto;
    z-index: 5;
    padding-bottom: 4rem;
  }

  .quote-header {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 0.85rem;
  }

  .quote-icon-open {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(3rem, 6vh, 5rem);
    color: #8fa68b;
    line-height: 1;
    font-weight: 700;
  }

  .quote-type {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(1.4rem, 2.5vh, 2rem);
    font-weight: 700;
    color: #8fa68b;
    letter-spacing: 0.02em;
  }

  .quote-body {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2rem, 4.5vh, 4rem);
    font-weight: 600;
    line-height: 1.45;
    color: #ffffff;
    margin-bottom: 1.5rem;
    text-align: left;
  }

  .quote-footer {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .quote-icon-close {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2.5rem, 5vh, 4rem);
    color: #8fa68b;
    line-height: 1;
    font-weight: 700;
    margin-top: 0.15rem;
  }

  .quote-credit {
    font-size: clamp(0.9rem, 1.8vh, 1.2rem);
    font-weight: 500;
    color: #8fa68b;
    line-height: 1.4;
  }

  /* Slide Navigation Controls (Bottom Right) */
  .nav-controls-container {
    position: absolute;
    bottom: 2.5rem;
    right: 3rem;
    display: flex;
    gap: 0.75rem;
    z-index: 100;
  }

  .nav-circle-btn {
    width: 2.85rem;
    height: 2.85rem;
    border-radius: 50%;
    background-color: #ffffff;
    color: #496a40;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .nav-circle-btn:hover {
    transform: scale(1.08);
    background-color: #f3f4f6;
  }

  .nav-circle-btn svg {
    width: 1.25rem;
    height: 1.25rem;
  }

  /* QR Code Widget (Bottom Left) */
  .qr-widget {
    position: absolute;
    bottom: 2rem;
    left: 3rem;
    z-index: 100;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    opacity: 1;
    transition: opacity 0.35s ease;
  }

  .qr-widget.fading {
    opacity: 0;
  }

  .qr-widget canvas {
    border-radius: 8px;
    display: block;
  }

  .qr-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.55);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* Responsive Styling */
  @media (max-width: 992px) {
    .slide-item {
      padding: 13rem 3rem 4rem 3rem;
    }
    .fixed-top-header {
      top: 6.5rem;
      left: 3rem;
      right: 3rem;
    }
    .slide-case-title {
      font-size: 1.8rem;
    }
    .quote-body {
      font-size: 1.75rem;
    }
  }

  @media (max-width: 768px) {
    .top-header-overlay {
      padding: 1rem;
      flex-direction: column;
      align-items: stretch;
      gap: 0.75rem;
    }
    .right-controls {
      justify-content: space-between;
      width: 100%;
    }
    .autoplay-capsule {
      flex: 1;
      justify-content: space-between;
      padding: 0.35rem 0.85rem;
      gap: 0.5rem;
    }
    .progress-bar-container {
      width: 60px;
    }
    .case-select-capsule {
      padding: 0.35rem 0.85rem;
    }
    .case-select {
      max-width: none;
      width: 100%;
    }
    .back-to-cases {
      align-self: flex-start;
      padding: 0.4rem 1rem;
      font-size: 0.8rem;
    }
    .fixed-top-header {
      top: 10rem;
      left: 1.5rem;
      right: 1.5rem;
      flex-direction: column-reverse;
      gap: 0.75rem;
    }
    .slide-item {
      padding: 18rem 1.5rem 6rem 1.5rem;
    }
    .slide-case-title {
      font-size: 1.45rem;
    }
    .slide-case-subtitle {
      font-size: 0.85rem;
    }
    .slide-pave-logo {
      width: 2.75rem;
      height: 2.75rem;
      align-self: flex-end;
    }
    .quote-type {
      font-size: 1.35rem;
    }
    .quote-icon-open {
      font-size: 2.6rem;
    }
    .quote-body {
      font-size: 1.35rem;
      line-height: 1.45;
    }
    .quote-icon-close {
      font-size: 2.2rem;
    }
    .quote-credit {
      font-size: 0.88rem;
    }
    .bg-layer-halftone {
      width: 120vw;
      height: 120vw;
      bottom: -72vw;
      right: -72vw;
    }
    .nav-controls-container {
      bottom: 1.5rem;
      right: 1.5rem;
    }
    .nav-circle-btn {
      width: 2.5rem;
      height: 2.5rem;
    }
  }
</style>

<div class="slideshow-container" id="slideshow-container">
  <!-- Top Minimalist Header Overlay -->
  <div class="top-header-overlay">
    <!-- Back to Cases -->
    <a href="{{ '/' | relative_url }}" class="back-to-cases" title="Back to Case Studies">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"></line>
        <polyline points="12 19 5 12 12 5"></polyline>
      </svg>
      <span>All Cases</span>
    </a>

    <!-- Controls capsule & case selector -->
    <div class="right-controls">
      <!-- Autoplay capsule -->
      <div class="autoplay-capsule">
        <button class="play-pause-btn" id="play-pause-btn" aria-label="Pause Autoplay">
          <svg class="pause-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
          </svg>
          <svg class="play-icon" viewBox="0 0 24 24" fill="currentColor" style="display: none;">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </button>

        <select id="speed-select" class="speed-select" aria-label="Autoplay Speed">
          <option value="14000">Slow (14s)</option>
          <option value="10000">Medium (10s)</option>
          <option value="7000" selected>Fast (7s)</option>
        </select>

        <div class="progress-bar-container">
          <div class="progress-bar-fill" id="progress-bar-fill"></div>
        </div>

        <div class="slide-counter" id="slide-counter">1 / 1</div>
      </div>

      <!-- Case Selection Capsule -->
      <div class="case-select-capsule">
        <select id="case-select" class="case-select" aria-label="Select Case Study">
          {% assign opt_case_index = 0 %}
          {% for case in site.cases %}
            {% if case.messages %}
              <option value="{{ opt_case_index }}">{{ case.title | escape }}</option>
              {% assign opt_case_index = opt_case_index | plus: 1 %}
            {% endif %}
          {% endfor %}
        </select>
      </div>
    </div>
  </div>

  <!-- Fixed Top Header (Static Case Title/Subtitle & PAVE Logo) -->
  <div class="fixed-top-header">
    <div class="slide-case-info" id="fixed-case-info">
      <h2 class="slide-case-title" id="fixed-case-title"></h2>
      <p class="slide-case-subtitle" id="fixed-case-subtitle"></p>
    </div>
    <div class="slide-pave-logo">
      <img src="{{ '/assets/images/adobe_component_6.png' | relative_url }}" alt="PAVE Logo">
    </div>
  </div>

  <!-- Fixed Background Layers (A/B for cross-fade, never move with slides) -->
  <div class="bg-layer" id="bg-layer-a" style="opacity: 0.28;">
    <div class="bg-layer-halftone"></div>
  </div>
  <div class="bg-layer" id="bg-layer-b" style="opacity: 0;">
    <div class="bg-layer-halftone"></div>
  </div>

  <!-- Slides Track -->
  <div class="slides-track" id="slides-track">
    {% assign slide_index = 0 %}
    {% assign case_index = 0 %}
    
    {% for case in site.cases %}
      {% if case.messages %}
        {% for message_slug in case.messages %}
          {% assign message = site.messages | where: "slug", message_slug | first %}
          {% if message %}

            <div class="slide-item" 
                 data-slide-index="{{ slide_index }}"
                 data-case-index="{{ case_index }}"
                 data-case-title="{{ case.title | escape }} ({{case.what-year-did-the-project-start}} - {{case.what-year-did-the-project-conclude}})"
                 data-case-subtitle="Participatory engagement about {{ case.describe-the-subject-matter-in-your-own-words-one | escape }}"
                 data-case-url="{{ '/c/' | append: case.airtable_id | append: '/' | absolute_url }}">

              <!-- Center: Quote / Recommendation Body -->
              <div class="slide-quote-content">
                <div class="quote-header">
                  <span class="quote-icon-open">“</span>
                  <span class="quote-type">{{ message.type }}</span>
                </div>
                <div class="quote-body">
                  {{ message.title }}
                </div>
                {% if message.additional-credit-line %}
                  <div class="quote-footer">
                    <span class="quote-icon-close">”</span>
                    <span class="quote-credit">{{ message.additional-credit-line }}</span>
                  </div>
                {% endif %}
              </div>
            </div>

            {% assign slide_index = slide_index | plus: 1 %}
          {% endif %}
        {% endfor %}
        {% assign case_index = case_index | plus: 1 %}
      {% endif %}
    {% endfor %}
  </div>

  <!-- QR Code Widget (Bottom Left) -->
  <div class="qr-widget" id="qr-widget">
    <div id="qr-code"></div>
    <span class="qr-label">Scan to view case</span>
  </div>

  <!-- Navigation Controls (Bottom Right) -->
  <div class="nav-controls-container">
    <button class="nav-circle-btn" id="prev-btn" aria-label="Previous slide">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"></line>
        <polyline points="12 19 5 12 12 5"></polyline>
      </svg>
    </button>
    <button class="nav-circle-btn" id="next-btn" aria-label="Next slide">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="5" y1="12" x2="19" y2="12"></line>
        <polyline points="12 5 19 12 12 19"></polyline>
      </svg>
    </button>
  </div>
</div>

<!-- QR Code Library -->
<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>

<!-- Slideshow Logic Engine -->
<script>
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('slideshow-container');
  const track = document.getElementById('slides-track');
  const slides = document.querySelectorAll('.slide-item');
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const playPauseBtn = document.getElementById('play-pause-btn');
  const playIcon = playPauseBtn.querySelector('.play-icon');
  const pauseIcon = playPauseBtn.querySelector('.pause-icon');
  const progressBarFill = document.getElementById('progress-bar-fill');
  const slideCounter = document.getElementById('slide-counter');
  const speedSelect = document.getElementById('speed-select');
  const caseSelect = document.getElementById('case-select');

  const totalSlides = slides.length;
  if (totalSlides === 0) return;

  let currentIndex = 0;
  let slideDuration = parseInt(speedSelect.value);
  let lastTime = 0;
  let progress = 0;
  let animationFrameId = null;
  let isPlaying = true;
  let currentCaseIndex = -1;

  // Background cross-fade layer references
  const bgLayerA = document.getElementById('bg-layer-a');
  const bgLayerB = document.getElementById('bg-layer-b');
  let activeBgLayer = 'a'; // 'a' starts visible

  // Cross-fade between fixed background layers on case change
  function crossFadeBackground() {
    // Both layers show the same halftone image right now.
    // If per-case background images are added via data-bg on slides,
    // set the inactive layer's image here before fading.
    const incoming = activeBgLayer === 'a' ? bgLayerB : bgLayerA;
    const outgoing = activeBgLayer === 'a' ? bgLayerA : bgLayerB;

    incoming.style.opacity = '0.28';
    outgoing.style.opacity = '0';
    activeBgLayer = activeBgLayer === 'a' ? 'b' : 'a';
  }

  // Initialize Counter display
  slideCounter.innerText = `1 / ${totalSlides}`;

  // QR Code widget
  const qrWidget = document.getElementById('qr-widget');
  const qrCodeEl = document.getElementById('qr-code');
  let qrInstance = null;
  let qrCurrentUrl = null;

  function updateQRCode(url) {
    if (!url || url === qrCurrentUrl) return;
    qrCurrentUrl = url;

    // Fade out
    qrWidget.classList.add('fading');
    setTimeout(() => {
      // Clear previous QR
      qrCodeEl.innerHTML = '';
      qrInstance = new QRCode(qrCodeEl, {
        text: url,
        width: 128,
        height: 128,
        colorDark: '#ffffff',
        colorLight: 'rgba(0,0,0,0)',
        correctLevel: QRCode.CorrectLevel.L
      });
      // Fade back in
      qrWidget.classList.remove('fading');
    }, 300);
  }

  function updateCaseSelect(caseIndex) {
    // Sync the case dropdown value
    if (caseSelect) {
      caseSelect.value = caseIndex;
    }
  }

  function goToSlide(index) {
    currentIndex = index;
    if (currentIndex >= totalSlides) currentIndex = 0;
    if (currentIndex < 0) currentIndex = totalSlides - 1;
    
    // Transition slides track horizontally
    track.style.transform = `translateX(-${currentIndex * 100}vw)`;
    slideCounter.innerText = `${currentIndex + 1} / ${totalSlides}`;
    
    // Update case info elements with transitions when case changes
    const activeSlide = slides[currentIndex];
    const caseIndex = parseInt(activeSlide.dataset.caseIndex);
    const title = activeSlide.dataset.caseTitle;
    const subtitle = activeSlide.dataset.caseSubtitle;

    const titleEl = document.getElementById('fixed-case-title');
    const subtitleEl = document.getElementById('fixed-case-subtitle');
    const caseInfoEl = document.getElementById('fixed-case-info');

    if (caseIndex !== currentCaseIndex) {
      currentCaseIndex = caseIndex;

      // Cross-fade the fixed background layer
      crossFadeBackground();

      // Update QR code for this case
      updateQRCode(activeSlide.dataset.caseUrl);

      // Fade out/in the case title block
      if (caseInfoEl) {
        caseInfoEl.style.opacity = '0';
        setTimeout(() => {
          if (titleEl) titleEl.textContent = title;
          if (subtitleEl) subtitleEl.textContent = subtitle;
          caseInfoEl.style.opacity = '1';
        }, 150);
      } else {
        if (titleEl) titleEl.textContent = title;
        if (subtitleEl) subtitleEl.textContent = subtitle;
      }
    }

    updateCaseSelect(caseIndex);

    // Reset timer progress
    lastTime = performance.now();
    progress = 0;
    progressBarFill.style.width = '0%';
  }

  function goToNextSlide() {
    goToSlide(currentIndex + 1);
  }

  function goToPrevSlide() {
    goToSlide(currentIndex - 1);
  }

  // Animation cycle loop using requestAnimationFrame
  function tick(timestamp) {
    if (!lastTime) lastTime = timestamp;
    
    if (isPlaying) {
      const elapsed = timestamp - lastTime;
      progress = (elapsed / slideDuration) * 100;
      
      if (progress >= 100) {
        progress = 0;
        lastTime = timestamp;
        goToNextSlide();
      }
      progressBarFill.style.width = `${progress}%`;
    } else {
      // Preserve elapsed calculation relative to progress when paused
      lastTime = timestamp - (progress / 100) * slideDuration;
    }
    
    animationFrameId = requestAnimationFrame(tick);
  }

  // Start autoplay timer
  animationFrameId = requestAnimationFrame(tick);

  function pauseAutoplay() {
    isPlaying = false;
    playIcon.style.display = 'block';
    pauseIcon.style.display = 'none';
  }

  function playAutoplay() {
    isPlaying = true;
    playIcon.style.display = 'none';
    pauseIcon.style.display = 'block';
    lastTime = performance.now();
  }

  // Controls bindings
  prevBtn.addEventListener('click', goToPrevSlide);
  nextBtn.addEventListener('click', goToNextSlide);

  playPauseBtn.addEventListener('click', () => {
    if (isPlaying) {
      pauseAutoplay();
    } else {
      playAutoplay();
    }
  });

  // Handle Autoplay Speed changes
  speedSelect.addEventListener('change', () => {
    slideDuration = parseInt(speedSelect.value);
    // Restart current progress cycle
    lastTime = performance.now();
    progress = 0;
    progressBarFill.style.width = '0%';
  });

  // Handle Case Dropdown selection changes
  if (caseSelect) {
    caseSelect.addEventListener('change', () => {
      const selectedCaseIndex = parseInt(caseSelect.value);
      // Find the first slide index for this case
      let targetSlideIndex = -1;
      for (let i = 0; i < slides.length; i++) {
        if (parseInt(slides[i].dataset.caseIndex) === selectedCaseIndex) {
          targetSlideIndex = i;
          break;
        }
      }
      if (targetSlideIndex !== -1) {
        goToSlide(targetSlideIndex);
      }
    });
  }

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
      goToNextSlide();
    } else if (e.key === 'ArrowLeft') {
      goToPrevSlide();
    } else if (e.key === ' ') {
      e.preventDefault(); // prevent space from scrolling page
      if (isPlaying) {
        pauseAutoplay();
      } else {
        playAutoplay();
      }
    }
  });

  // Swipe gestures support for mobile devices
  let touchStartX = 0;
  let touchEndX = 0;

  container.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  container.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, { passive: true });

  function handleSwipe() {
    const swipeThreshold = 55;
    if (touchStartX - touchEndX > swipeThreshold) {
      goToNextSlide();
    } else if (touchEndX - touchStartX > swipeThreshold) {
      goToPrevSlide();
    }
  }

  // Initialize the first dropdown value, fixed header content & QR code
  if (slides[0]) {
    const initialSlide = slides[0];
    const initialCaseIndex = parseInt(initialSlide.dataset.caseIndex);
    const initialTitle = initialSlide.dataset.caseTitle;
    const initialSubtitle = initialSlide.dataset.caseSubtitle;

    const titleEl = document.getElementById('fixed-case-title');
    const subtitleEl = document.getElementById('fixed-case-subtitle');

    if (titleEl) titleEl.textContent = initialTitle;
    if (subtitleEl) subtitleEl.textContent = initialSubtitle;
    currentCaseIndex = initialCaseIndex;

    updateCaseSelect(initialCaseIndex);
    updateQRCode(initialSlide.dataset.caseUrl);
  }
});
</script>
