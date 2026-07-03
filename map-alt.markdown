---
layout: default
title: Interactive Map & Filters
permalink: /map-alt/
menus: [header]
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css" />
<script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>

<style>
/* Page Layout */
.map-alt-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 2rem;
  margin-top: 1.5rem;
  margin-bottom: 3rem;
}

@media (max-width: 992px) {
  .map-alt-layout {
    grid-template-columns: 1fr;
  }
}

/* Sidebar Styling */
.map-sidebar {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
  align-self: start;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(73, 106, 64, 0.1);
  padding-bottom: 0.75rem;
}

.sidebar-header h2 {
  font-size: 1.25rem;
  margin: 0;
  font-weight: 700;
  color: #1a2f16;
}

.reset-btn {
  background: none;
  border: none;
  color: #496a40;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  transition: color 0.15s ease;
  text-decoration: underline;
}

.reset-btn:hover {
  color: #1a2f16;
}

/* Filter Sections */
.filter-section {
  margin-bottom: 1.5rem;
}

.filter-section:last-child {
  margin-bottom: 0;
}

.filter-section h3 {
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #556c50;
  margin-top: 0;
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Scrollbar for touchscreen and overflow scrollable facets */
.scrollable-facet {
  max-height: 210px; /* 5 items * 42px height */
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding-right: 6px;
  background: #fafbfa;
  border: 1px solid rgba(73, 106, 64, 0.05);
  border-radius: 10px;
  padding: 6px;
}

.scrollable-facet::-webkit-scrollbar {
  width: 6px;
}
.scrollable-facet::-webkit-scrollbar-track {
  background: rgba(73, 106, 64, 0.03);
  border-radius: 3px;
}
.scrollable-facet::-webkit-scrollbar-thumb {
  background: rgba(73, 106, 64, 0.25);
  border-radius: 3px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #243f1f;
  cursor: pointer;
  line-height: 1.4;
  user-select: none;
  padding: 8px 10px;
  border-radius: 8px;
  min-height: 40px; /* Touch target optimized */
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.filter-label:hover {
  background-color: rgba(73, 106, 64, 0.04);
}

.filter-label:active {
  background-color: rgba(73, 106, 64, 0.12); /* Touch response feedback */
}

.filter-label.active-checked {
  background-color: rgba(73, 106, 64, 0.08);
  border-color: rgba(73, 106, 64, 0.15);
  font-weight: 600;
}

.filter-label.zero-count {
  opacity: 0.45;
}

.filter-label.zero-count input {
  cursor: not-allowed;
}

.filter-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  accent-color: #496a40;
  cursor: pointer;
  flex-shrink: 0;
  margin: 0;
}

.filter-count {
  color: #7a9476;
  font-size: 0.75rem;
  margin-left: auto;
  font-weight: 500;
}

/* Dual Range Slider Styling */
.slider-wrapper {
  position: relative;
  width: 100%;
  height: 20px;
  margin-top: 15px;
  margin-bottom: 25px;
}

.slider-track {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 5px;
  background-color: rgba(73, 106, 64, 0.1);
  border-radius: 5px;
  transform: translateY(-50%);
  z-index: 1;
}

.slider-highlight {
  position: absolute;
  top: 50%;
  height: 5px;
  background-color: #496a40;
  border-radius: 5px;
  transform: translateY(-50%);
  z-index: 2;
}

.slider-wrapper input[type="range"] {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  background: none;
  pointer-events: none;
  -webkit-appearance: none;
  appearance: none;
  transform: translateY(-50%);
  z-index: 3;
  margin: 0;
}

.slider-wrapper input[type="range"]::-webkit-slider-thumb {
  height: 18px;
  width: 18px;
  border-radius: 50%;
  background-color: #496a40;
  border: 2px solid #ffffff;
  cursor: pointer;
  pointer-events: auto;
  -webkit-appearance: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
  transition: transform 0.1s ease;
}

.slider-wrapper input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.slider-wrapper input[type="range"]::-moz-range-thumb {
  height: 14px;
  width: 14px;
  border-radius: 50%;
  background-color: #496a40;
  border: 2px solid #ffffff;
  cursor: pointer;
  pointer-events: auto;
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
  transition: transform 0.1s ease;
}

.slider-wrapper input[type="range"]::-moz-range-thumb:hover {
  transform: scale(1.15);
}

.slider-values {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  font-weight: 600;
  color: #496a40;
}

/* Statistics Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.08);
  border-top: 3px solid #496a40;
  border-radius: 12px;
  padding: 1rem 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.01);
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(73, 106, 64, 0.08);
}

/* Distinct card tops to look beautiful and premium */
.stat-card:nth-child(1) { border-top-color: #496a40; }
.stat-card:nth-child(2) { border-top-color: #2196F3; }
.stat-card:nth-child(3) { border-top-color: #9C27B0; }
.stat-card:nth-child(4) { border-top-color: #FF9800; }
.stat-card:nth-child(5) { border-top-color: #E91E63; }

.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card:nth-child(1) .stat-icon { background: rgba(73, 106, 64, 0.08); color: #496a40; }
.stat-card:nth-child(2) .stat-icon { background: rgba(33, 150, 243, 0.08); color: #2196F3; }
.stat-card:nth-child(3) .stat-icon { background: rgba(156, 39, 176, 0.08); color: #9C27B0; }
.stat-card:nth-child(4) .stat-icon { background: rgba(255, 152, 0, 0.08); color: #FF9800; }
.stat-card:nth-child(5) .stat-icon { background: rgba(233, 30, 99, 0.08); color: #E91E63; }

.stat-icon svg {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-family: 'Outfit', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #1a2f16;
  line-height: 1.2;
}

.stat-label-text {
  font-size: 0.725rem;
  font-weight: 600;
  text-transform: uppercase;
  color: #556c50;
  letter-spacing: 0.02em;
}

/* Map Styling */
.map-alt-container {
  height: 550px;
  width: 100%;
  border: 1px solid rgba(73, 106, 64, 0.12);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.02);
  overflow: hidden;
  margin-bottom: 2rem;
  z-index: 10;
}

/* Dynamic Case Listing Section */
.cases-list-section {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.01);
}

.cases-list-section h2 {
  font-size: 1.25rem;
  margin-top: 0;
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(73, 106, 64, 0.08);
  padding-bottom: 0.5rem;
}

.cases-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  max-height: 500px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.case-item-card {
  border: 1px solid rgba(73, 106, 64, 0.06);
  border-radius: 10px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.15s ease;
  background: #fbfcfb;
}

.case-item-card:hover {
  border-color: rgba(73, 106, 64, 0.2);
  background: #ffffff;
  transform: translateX(3px);
}

.case-item-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex-grow: 1;
}

.case-item-title {
  font-weight: 700;
  font-size: 1rem;
  color: #1a2f16;
}

.case-item-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.775rem;
  color: #7a9476;
  flex-wrap: wrap;
}

.case-item-meta span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.tag-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15rem 0.45rem;
  border-radius: 9999px;
  background-color: rgba(73, 106, 64, 0.08);
  color: #496a40;
}

.case-item-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
  min-width: 120px;
}

.case-stat-num {
  font-family: 'Outfit', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #496a40;
}

.case-stat-lbl {
  font-size: 0.675rem;
  text-transform: uppercase;
  color: #7a9476;
}

/* Map Controls Bar (Segmented control button group + cluster checkbox) */
.map-controls-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -1rem; /* push it close under the map container */
  margin-bottom: 2rem;
  padding: 0.75rem 1rem;
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.1);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.01);
  flex-wrap: wrap;
  gap: 1rem;
}

.view-mode-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.view-mode-toggle span {
  font-size: 0.8rem;
  font-weight: 700;
  color: #556c50;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-right: 0.25rem;
}

.view-mode-toggle label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #496a40;
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid rgba(73, 106, 64, 0.15);
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 36px;
}

.view-mode-toggle label:hover {
  background-color: rgba(73, 106, 64, 0.04);
}

.view-mode-toggle label.active-toggle {
  background-color: #496a40;
  color: #ffffff;
  border-color: #496a40;
}

.view-mode-toggle input[type="radio"] {
  display: none; /* hide standard radio circles */
}

.cluster-toggle-wrapper label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #496a40;
  cursor: pointer;
  user-select: none;
  min-height: 36px;
}

.cluster-toggle-wrapper input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #496a40;
  cursor: pointer;
  margin: 0;
}
</style>

<div class="map-alt-layout">
  <!-- Left Side Filters -->
  <aside class="map-sidebar">
    <div class="sidebar-header">
      <h2>Filters</h2>
      <button class="reset-btn" id="reset-all-btn">Reset All</button>
    </div>

    <!-- Modality Filter -->
    <div class="filter-section">
      <h3>Modality</h3>
      <div class="checkbox-group" id="modality-filters">
        <label class="filter-label"><input type="checkbox" value="Offline"> Offline <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Online"> Online <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Hybrid"> Hybrid <span class="filter-count">(0)</span></label>
      </div>
    </div>

    <!-- Level of engagement Filter -->
    <div class="filter-section">
      <h3>Level of Engagement</h3>
      <div class="checkbox-group" id="level-filters">
        <label class="filter-label"><input type="checkbox" value="Community"> Community <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="National"> National <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Professional"> Professional <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Global"> Global <span class="filter-count">(0)</span></label>
      </div>
    </div>

    <!-- Time slider Filter -->
    <div class="filter-section">
      <h3>Average Time (Hours)</h3>
      <div class="slider-wrapper">
        <div class="slider-track"></div>
        <div class="slider-highlight" id="slider-highlight"></div>
        <input type="range" id="hours-min" min="0" max="120" value="0">
        <input type="range" id="hours-max" min="0" max="120" value="120">
      </div>
      <div class="slider-values">
        <span>Min: <span id="hours-min-lbl">0h</span></span>
        <span>Max: <span id="hours-max-lbl">120h</span></span>
      </div>
    </div>

    <!-- Theme Filter -->
    <div class="filter-section">
      <h3>Theme</h3>
      <div class="checkbox-group scrollable-facet" id="theme-filters">
        <label class="filter-label"><input type="checkbox" value="Artificial Intelligence"> Artificial Intelligence <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Education"> Education <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Environment"> Environment <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Healthcare"> Healthcare <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Infrastructure"> Infrastructure <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Safety"> Safety <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Work"> Work <span class="filter-count">(0)</span></label>
        <label class="filter-label"><input type="checkbox" value="Youth"> Youth <span class="filter-count">(0)</span></label>
      </div>
    </div>

    <!-- Dynamic Methods Filter -->
    <div class="filter-section">
      <h3>Methods</h3>
      <div class="checkbox-group scrollable-facet" id="methods-filters">
        <!-- Dynamically populated and sorted -->
      </div>
    </div>
  </aside>

  <!-- Right Side Map & Stats -->
  <main class="map-main">
    <!-- Top Statistics Bar -->
    <div class="stats-grid">
      <!-- Mapped Cases Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-cases">0</span>
          <span class="stat-label-text">Participatory Processes</span>
        </div>
      </div>
      
      <!-- Countries Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.53c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.4z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-countries">0</span>
          <span class="stat-label-text">Countries</span>
        </div>
      </div>

      <!-- Continents Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.53c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.4z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-continents">0</span>
          <span class="stat-label-text">Continents</span>
        </div>
      </div>

      <!-- Total Engaged Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 8 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-participants">0</span>
          <span class="stat-label-text">Participants Engaged</span>
        </div>
      </div>

      <!-- Messages Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 11H7V9h2v2zm4 0h-2V9h2v2zm4 0h-2V9h2v2z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-messages">0</span>
          <span class="stat-label-text">Recommendations & Issues</span>
        </div>
      </div>
    </div>

    <!-- Map Area -->
    <div id="map" class="map-alt-container"></div>

    <!-- Map Controls Bar (Touch friendly under the map) -->
    <div class="map-controls-bar">
      <div class="view-mode-toggle">
        <span>Show on Map:</span>
        <label class="control-btn active-toggle">
          <input type="radio" name="map-layer-view" value="both" checked> Both
        </label>
        <label class="control-btn">
          <input type="radio" name="map-layer-view" value="participants"> Participant Locations
        </label>
        <label class="control-btn">
          <input type="radio" name="map-layer-view" value="organisations"> Organisation Locations
        </label>
      </div>
      <div class="cluster-toggle-wrapper">
        <label>
          <input type="checkbox" id="map-cluster-toggle" checked> Cluster markers
        </label>
      </div>
    </div>

    <!-- Filtered Cases List Section -->
    <div class="cases-list-section">
      <h2 id="cases-count-header">Cases Mapped</h2>
      <div class="cases-grid" id="cases-grid-list">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </main>
</div>

<script>
document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialise the Map
  const map = L.map('map').setView([20, 0], 2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  const markerClusterGroup = L.markerClusterGroup({
    showCoverageOnHover: false,
    maxClusterRadius: 40
  });

  const pointLayer = L.layerGroup();

  // Global variables to store loaded data
  let allCases = [];
  let methodCounts = {};
  
  // DOM References
  const methodsFiltersContainer = document.getElementById('methods-filters');
  const statsCases = document.getElementById('stats-cases');
  const statsCountries = document.getElementById('stats-countries');
  const statsContinents = document.getElementById('stats-continents');
  const statsParticipants = document.getElementById('stats-participants');
  const statsMessages = document.getElementById('stats-messages');
  const casesGridList = document.getElementById('cases-grid-list');
  const casesCountHeader = document.getElementById('cases-count-header');
  const resetBtn = document.getElementById('reset-all-btn');

  // Slider Elements
  const hoursMinInput = document.getElementById('hours-min');
  const hoursMaxInput = document.getElementById('hours-max');
  const hoursMinLbl = document.getElementById('hours-min-lbl');
  const hoursMaxLbl = document.getElementById('hours-max-lbl');
  const sliderHighlight = document.getElementById('slider-highlight');

  // 2. Fetch Aggregated Cases Data
  fetch('/assets/data/cases_aggregated.json')
    .then(response => response.json())
    .then(data => {
      allCases = data;
      
      // Determine max average hours dynamically to scale slider
      let maxHoursVal = 120;
      allCases.forEach(c => {
        if (c.average_hours > maxHoursVal) {
          maxHoursVal = Math.ceil(c.average_hours);
        }
      });
      hoursMinInput.max = maxHoursVal;
      hoursMaxInput.max = maxHoursVal;
      hoursMaxInput.value = maxHoursVal;
      hoursMaxLbl.innerText = maxHoursVal + 'h';

      // Compute methods occurrence frequency for sorting and counting
      computeMethodsFreq();

      // Listen for slider changes
      hoursMinInput.addEventListener('input', handleSliderInput);
      hoursMaxInput.addEventListener('input', handleSliderInput);
      
      // Listen for checkbox changes
      document.querySelectorAll('.filter-section input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateFiltersAndUI);
      });

      // Listen for view mode segmented control clicks
      document.querySelectorAll('input[name="map-layer-view"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
          // Toggle active-toggle class on labels
          document.querySelectorAll('.view-mode-toggle label').forEach(lbl => {
            if (lbl.contains(e.target)) {
              lbl.classList.add('active-toggle');
            } else {
              lbl.classList.remove('active-toggle');
            }
          });
          updateFiltersAndUI();
        });
      });

      // Listen for cluster checkbox
      document.getElementById('map-cluster-toggle').addEventListener('change', updateFiltersAndUI);

      // Update Slider Visual Track
      updateSliderTrack();

      // Initial filter run (draws everything)
      updateFiltersAndUI();
    })
    .catch(error => {
      console.error("Error loading aggregated cases:", error);
    });

  // Reset Button logic
  resetBtn.addEventListener('click', () => {
    // Uncheck all checkboxes
    document.querySelectorAll('.map-sidebar input[type="checkbox"]').forEach(cb => cb.checked = false);
    // Reset sliders
    hoursMinInput.value = hoursMinInput.min;
    hoursMaxInput.value = hoursMaxInput.max;
    
    // Reset map controls
    document.getElementById('map-cluster-toggle').checked = true;
    document.querySelector('input[name="map-layer-view"][value="both"]').checked = true;
    document.querySelectorAll('.view-mode-toggle label').forEach(lbl => {
      if (lbl.querySelector('input').value === 'both') {
        lbl.classList.add('active-toggle');
      } else {
        lbl.classList.remove('active-toggle');
      }
    });

    updateSliderTrack();
    updateFiltersAndUI();
  });

  // 3. Methods aggregation
  function computeMethodsFreq() {
    methodCounts = {};
    allCases.forEach(c => {
      if (c.methods && Array.isArray(c.methods)) {
        c.methods.forEach(m => {
          methodCounts[m] = (methodCounts[m] || 0) + 1;
        });
      }
    });
  }

  // 3a. Update Fixed Facet Labels (Modality, Level, Theme)
  function updateFixedFacetLabels(containerId, countMap) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const labels = container.querySelectorAll('.filter-label');
    labels.forEach(label => {
      const input = label.querySelector('input');
      const value = input.value;
      const count = countMap[value] || 0;
      
      const countSpan = label.querySelector('.filter-count');
      if (countSpan) {
        countSpan.innerText = '(' + count + ')';
      }
      
      if (input.checked) {
        label.classList.add('active-checked');
      } else {
        label.classList.remove('active-checked');
      }
      
      if (count === 0) {
        label.classList.add('zero-count');
      } else {
        label.classList.remove('zero-count');
      }
    });
  }

  // 3b. Render Methods checkboxes dynamically (sorted, count-filtered, touchscreen-optimized)
  function updateMethodsCheckboxes(activeCounts, selectedMethods) {
    const methodsToRender = [];
    const allMethodNames = new Set([...Object.keys(methodCounts), ...selectedMethods]);
    
    allMethodNames.forEach(m => {
      const count = activeCounts[m] || 0;
      const isChecked = selectedMethods.includes(m);
      // Hide methods with count 0 unless they are checked
      if (count > 0 || isChecked) {
        methodsToRender.push({ name: m, count: count, checked: isChecked });
      }
    });

    // Sort: checked ones first, then by count descending, then alphabetical
    methodsToRender.sort((a, b) => {
      if (a.checked !== b.checked) {
        return a.checked ? -1 : 1;
      }
      if (b.count !== a.count) {
        return b.count - a.count;
      }
      return a.name.localeCompare(b.name);
    });

    methodsFiltersContainer.innerHTML = '';
    methodsToRender.forEach(method => {
      const label = document.createElement('label');
      label.className = 'filter-label' + (method.checked ? ' active-checked' : '') + (method.count === 0 ? ' zero-count' : '');
      
      const input = document.createElement('input');
      input.type = 'checkbox';
      input.value = method.name;
      input.checked = method.checked;
      input.addEventListener('change', updateFiltersAndUI);

      const spanText = document.createTextNode(' ' + method.name);
      
      const countSpan = document.createElement('span');
      countSpan.className = 'filter-count';
      countSpan.innerText = '(' + method.count + ')';

      label.appendChild(input);
      label.appendChild(spanText);
      label.appendChild(countSpan);
      
      methodsFiltersContainer.appendChild(label);
    });

    // Adjust scrollable class dynamically
    if (methodsToRender.length > 5) {
      methodsFiltersContainer.classList.add('scrollable-facet');
    } else {
      methodsFiltersContainer.classList.remove('scrollable-facet');
    }
  }

  // 4. Slider track updating
  function handleSliderInput(e) {
    const valMin = parseInt(hoursMinInput.value);
    const valMax = parseInt(hoursMaxInput.value);

    // Prevent thumbs from crossing
    if (e.target.id === 'hours-min') {
      if (valMin > valMax - 1) {
        hoursMinInput.value = valMax - 1;
      }
    } else {
      if (valMax < valMin + 1) {
        hoursMaxInput.value = valMin + 1;
      }
    }

    updateSliderTrack();
    updateFiltersAndUI();
  }

  function updateSliderTrack() {
    const minVal = parseInt(hoursMinInput.value);
    const maxVal = parseInt(hoursMaxInput.value);
    const minLimit = parseInt(hoursMinInput.min) || 0;
    const maxLimit = parseInt(hoursMinInput.max) || 120;

    hoursMinLbl.innerText = minVal + 'h';
    hoursMaxLbl.innerText = maxVal + 'h';

    const range = maxLimit - minLimit;
    const percentLeft = range > 0 ? ((minVal - minLimit) / range) * 100 : 0;
    const percentRight = range > 0 ? 100 - (((maxVal - minLimit) / range) * 100) : 0;

    sliderHighlight.style.left = percentLeft + '%';
    sliderHighlight.style.right = percentRight + '%';
  }

  // 5. Filter application
  function updateFiltersAndUI() {
    // Collect active filter choices
    const selectedMods = Array.from(document.querySelectorAll('#modality-filters input:checked')).map(cb => cb.value);
    const selectedLevels = Array.from(document.querySelectorAll('#level-filters input:checked')).map(cb => cb.value);
    const selectedThemes = Array.from(document.querySelectorAll('#theme-filters input:checked')).map(cb => cb.value);
    const selectedMethods = Array.from(document.querySelectorAll('#methods-filters input:checked')).map(cb => cb.value);

    // Helpers to check match
    const matchesModality = (c, mods) => mods.length === 0 || (c.modalities && c.modalities.some(m => mods.includes(m)));
    const matchesLevel = (c, levels) => levels.length === 0 || levels.includes(c.level_of_engagement);
    const matchesTheme = (c, themes) => themes.length === 0 || (c.themes && c.themes.some(t => themes.includes(t)));
    const matchesMethod = (c, meths) => meths.length === 0 || (c.methods && c.methods.some(m => meths.includes(m)));
    const matchesHours = (c, minH, maxH) => c.average_hours >= minH && c.average_hours <= maxH;

    // --- DYNAMIC TIME SLIDER BOUNDS ---
    // Compute bounds based on checkboxes only
    const casesForHours = allCases.filter(c =>
      matchesModality(c, selectedMods) &&
      matchesLevel(c, selectedLevels) &&
      matchesTheme(c, selectedThemes) &&
      matchesMethod(c, selectedMethods)
    );

    let activeMin = Infinity;
    let activeMax = -Infinity;
    casesForHours.forEach(c => {
      if (c.average_hours < activeMin) activeMin = c.average_hours;
      if (c.average_hours > activeMax) activeMax = c.average_hours;
    });

    if (activeMin === Infinity) {
      activeMin = 0;
      activeMax = 120;
    } else {
      activeMin = Math.floor(activeMin);
      activeMax = Math.ceil(activeMax);
    }
    if (activeMin === activeMax) {
      activeMax = activeMin + 1;
    }

    const isMinAtLimit = (parseInt(hoursMinInput.value) === parseInt(hoursMinInput.min));
    const isMaxAtLimit = (parseInt(hoursMaxInput.value) === parseInt(hoursMaxInput.max));

    // Update input bounds
    hoursMinInput.min = activeMin;
    hoursMinInput.max = activeMax;
    hoursMaxInput.min = activeMin;
    hoursMaxInput.max = activeMax;

    // Adjust values
    if (isMinAtLimit) {
      hoursMinInput.value = activeMin;
    } else {
      hoursMinInput.value = Math.max(activeMin, Math.min(activeMax, parseInt(hoursMinInput.value)));
    }

    if (isMaxAtLimit) {
      hoursMaxInput.value = activeMax;
    } else {
      hoursMaxInput.value = Math.max(activeMin, Math.min(activeMax, parseInt(hoursMaxInput.value)));
    }

    if (parseInt(hoursMinInput.value) > parseInt(hoursMaxInput.value) - 1) {
      hoursMinInput.value = Math.max(activeMin, parseInt(hoursMaxInput.value) - 1);
    }

    updateSliderTrack();

    const minHours = parseInt(hoursMinInput.value);
    const maxHours = parseInt(hoursMaxInput.value);

    // Filter Cases Array (Matches all filters including new dynamic slider range)
    const filteredCases = allCases.filter(c => 
      matchesModality(c, selectedMods) &&
      matchesLevel(c, selectedLevels) &&
      matchesTheme(c, selectedThemes) &&
      matchesMethod(c, selectedMethods) &&
      matchesHours(c, minHours, maxHours)
    );

    // --- ORTHOGONAL FACET COUNTS ---

    // 1. Modality counts (ignore Modality filter)
    const casesForModality = allCases.filter(c =>
      matchesLevel(c, selectedLevels) &&
      matchesTheme(c, selectedThemes) &&
      matchesMethod(c, selectedMethods) &&
      matchesHours(c, minHours, maxHours)
    );
    const modalityCounts = { "Offline": 0, "Online": 0, "Hybrid": 0 };
    casesForModality.forEach(c => {
      if (c.modalities) {
        c.modalities.forEach(m => {
          if (m in modalityCounts) modalityCounts[m]++;
        });
      }
    });

    // 2. Level counts (ignore Level filter)
    const casesForLevel = allCases.filter(c =>
      matchesModality(c, selectedMods) &&
      matchesTheme(c, selectedThemes) &&
      matchesMethod(c, selectedMethods) &&
      matchesHours(c, minHours, maxHours)
    );
    const levelCounts = { "Community": 0, "National": 0, "Professional": 0, "Global": 0 };
    casesForLevel.forEach(c => {
      if (c.level_of_engagement in levelCounts) {
        levelCounts[c.level_of_engagement]++;
      }
    });

    // 3. Theme counts (ignore Theme filter)
    const casesForTheme = allCases.filter(c =>
      matchesModality(c, selectedMods) &&
      matchesLevel(c, selectedLevels) &&
      matchesMethod(c, selectedMethods) &&
      matchesHours(c, minHours, maxHours)
    );
    const themeCounts = {
      "Artificial Intelligence": 0, "Education": 0, "Environment": 0,
      "Healthcare": 0, "Infrastructure": 0, "Safety": 0, "Work": 0, "Youth": 0
    };
    casesForTheme.forEach(c => {
      if (c.themes) {
        c.themes.forEach(t => {
          if (t in themeCounts) themeCounts[t]++;
        });
      }
    });

    // 4. Method counts (ignore Method filter)
    const casesForMethod = allCases.filter(c =>
      matchesModality(c, selectedMods) &&
      matchesLevel(c, selectedLevels) &&
      matchesTheme(c, selectedThemes) &&
      matchesHours(c, minHours, maxHours)
    );
    const activeMethodCounts = {};
    casesForMethod.forEach(c => {
      if (c.methods) {
        c.methods.forEach(m => {
          activeMethodCounts[m] = (activeMethodCounts[m] || 0) + 1;
        });
      }
    });

    // Update checkbox labels & dynamic lists
    updateFixedFacetLabels('modality-filters', modalityCounts);
    updateFixedFacetLabels('level-filters', levelCounts);
    updateFixedFacetLabels('theme-filters', themeCounts);
    updateMethodsCheckboxes(activeMethodCounts, selectedMethods);

    // Update Stats, Map, and Case list
    updateStatistics(filteredCases);
    updateMapPoints(filteredCases);
    updateCaseListUI(filteredCases);
  }

  function updateStatistics(filteredCases) {
    const countriesSet = new Set();
    const continentsSet = new Set();
    let totalParticipantsCount = 0;
    let totalMessagesCount = 0;

    filteredCases.forEach(c => {
      if (c.countries) c.countries.forEach(co => countriesSet.add(co));
      if (c.continents) c.continents.forEach(con => continentsSet.add(con));
      totalParticipantsCount += c.total_participants || 0;
      totalMessagesCount += c.message_count || 0;
    });

    // Animate stats counter transitions for a premium look
    animateCounter(statsCases, filteredCases.length);
    animateCounter(statsCountries, countriesSet.size);
    animateCounter(statsContinents, continentsSet.size);
    animateCounter(statsParticipants, totalParticipantsCount);
    animateCounter(statsMessages, totalMessagesCount);
  }

  function animateCounter(element, targetValue) {
    const startVal = parseInt(element.innerText.replace(/,/g, '')) || 0;
    if (startVal === targetValue) {
      element.innerText = targetValue.toLocaleString();
      return;
    }
    
    const duration = 400; // ms
    const startTime = performance.now();

    function step(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Ease out cubic
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const currentVal = Math.floor(startVal + easeProgress * (targetValue - startVal));
      
      element.innerText = currentVal.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        element.innerText = targetValue.toLocaleString();
      }
    }
    requestAnimationFrame(step);
  }

  function updateMapPoints(filteredCases) {
    // Clear both layers
    markerClusterGroup.clearLayers();
    pointLayer.clearLayers();

    // Get current map settings
    const mapLayerView = document.querySelector('input[name="map-layer-view"]:checked')?.value || 'both';
    const clusterMarkers = document.getElementById('map-cluster-toggle').checked;

    const bounds = L.latLngBounds();
    let pointCount = 0;

    filteredCases.forEach(c => {
      if (c.points && Array.isArray(c.points)) {
        c.points.forEach(point => {
          // Filter point type
          if (mapLayerView === 'participants' && point.type !== 'Participants') return;
          if (mapLayerView === 'organisations' && point.type !== 'Organisation') return;

          const marker = L.circleMarker([point.lat, point.lng], {
            radius: 8,
            fillColor: point.color || '#496a40',
            color: '#fff',
            weight: 1.5,
            opacity: 1,
            fillOpacity: 0.85
          });

          // Bind relevant popup text
          let popupText = '';
          if (point.type === 'Participants') {
            const countVal = point.count ? String(point.count).trim() : '';
            const parsedCount = parseInt(countVal.replace(/,/g, ''));
            const countText = (!isNaN(parsedCount)) ? `<strong>${parsedCount.toLocaleString()}</strong> people` : 'Participants';
            
            const locations = point.locations_list ? point.locations_list.split(',').map(s => s.trim()).filter(Boolean) : [];
            
            if (locations.length > 5) {
              const markerCountry = point.location_name || '';
              const otherCountries = locations.filter(name => name !== markerCountry);
              const firstFourOthers = otherCountries.slice(0, 4);
              const remainingCount = otherCountries.length - firstFourOthers.length;
              const pluralSuffix = remainingCount === 1 ? 'country' : 'countries';
              
              const countriesText = `${markerCountry ? `<strong>${markerCountry}</strong>` : ''}${firstFourOthers.length > 0 ? `, ${firstFourOthers.map(c => `<strong>${c}</strong>`).join(', ')}` : ''}, and <strong>${remainingCount}</strong> more ${pluralSuffix}`;
              
              popupText = `${countText} took part in this process on AI in ${countriesText} through <a href="${c.url}"><strong>${c.title}</strong></a>.`;
            } else {
              popupText = `${countText} took part in a participatory process on AI in <strong>${point.locations_list}</strong> through <a href="${c.url}"><strong>${c.title}</strong></a>.`;
            }
          } else {
            popupText = `<strong>Lead Organisation:</strong> <a href="${point.url}"><strong>${point.title}</strong></a><br>Lead organiser for <a href="${c.url}">${c.title}</a>.`;
          }

          marker.bindPopup(popupText);
          
          if (clusterMarkers) {
            markerClusterGroup.addLayer(marker);
          } else {
            pointLayer.addLayer(marker);
          }
          
          bounds.extend([point.lat, point.lng]);
          pointCount++;
        });
      }
    });

    // Ensure only the active layer group is attached to the map
    map.removeLayer(markerClusterGroup);
    map.removeLayer(pointLayer);

    if (clusterMarkers) {
      map.addLayer(markerClusterGroup);
    } else {
      map.addLayer(pointLayer);
    }

    // Auto-fit bounds if we have points
    if (pointCount > 0) {
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 12 });
    }
  }

  function updateCaseListUI(filteredCases) {
    casesCountHeader.innerText = filteredCases.length + ' Participatory Processes Mapped';
    casesGridList.innerHTML = '';

    if (filteredCases.length === 0) {
      casesGridList.innerHTML = '<div style="color: #7a9476; text-align: center; padding: 2rem; font-style: italic;">No cases match the selected filters. Click "Reset All" to clear filters.</div>';
      return;
    }

    filteredCases.forEach(c => {
      const card = document.createElement('div');
      card.className = 'case-item-card';

      const details = document.createElement('div');
      details.className = 'case-item-details';

      const titleLink = document.createElement('a');
      titleLink.href = c.url;
      titleLink.className = 'case-item-title';
      titleLink.innerText = c.title;
      details.appendChild(titleLink);

      const meta = document.createElement('div');
      meta.className = 'case-item-meta';

      // Level badge
      if (c.level_of_engagement) {
        const levelSpan = document.createElement('span');
        levelSpan.innerHTML = `<span class="tag-badge">${c.level_of_engagement} Scope</span>`;
        meta.appendChild(levelSpan);
      }

      // Modalities list
      if (c.modalities && c.modalities.length > 0) {
        const modalitiesSpan = document.createElement('span');
        modalitiesSpan.innerText = 'Modality: ' + c.modalities.join(', ');
        meta.appendChild(modalitiesSpan);
      }

      // Themes tags
      if (c.themes && c.themes.length > 0) {
        const themesSpan = document.createElement('span');
        themesSpan.innerText = 'Theme: ' + c.themes.join(', ');
        meta.appendChild(themesSpan);
      }

      details.appendChild(meta);
      card.appendChild(details);

      const stats = document.createElement('div');
      stats.className = 'case-item-stats';

      if (c.total_participants > 0) {
        const pNum = document.createElement('div');
        pNum.className = 'case-stat-num';
        pNum.innerText = c.total_participants.toLocaleString();
        
        const pLbl = document.createElement('div');
        pLbl.className = 'case-stat-lbl';
        pLbl.innerText = 'Participants';
        
        stats.appendChild(pNum);
        stats.appendChild(pLbl);
      } else {
        const pNum = document.createElement('div');
        pNum.className = 'case-stat-num';
        pNum.style.color = '#7a9476';
        pNum.innerText = '-';
        
        const pLbl = document.createElement('div');
        pLbl.className = 'case-stat-lbl';
        pLbl.innerText = 'Participants';
        
        stats.appendChild(pNum);
        stats.appendChild(pLbl);
      }

      card.appendChild(stats);
      casesGridList.appendChild(card);
    });
  }
});
</script>
