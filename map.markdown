---
layout: default
title: Map
permalink: /map/
menus: [header]
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css" />
<script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
/* Dashboard Top Statistics Bar Styles */
.dashboard-stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 992px) {
  .dashboard-stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 600px) {
  .dashboard-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.1);
  border-top: 3px solid #496a40;
  border-radius: 12px;
  padding: 1.25rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 12px 24px rgba(73, 106, 64, 0.1);
  border-color: rgba(73, 106, 64, 0.25);
}

.stat-card:nth-child(1) { border-top-color: #2196F3; }
.stat-card:nth-child(2) { border-top-color: #E91E63; }
.stat-card:nth-child(3) { border-top-color: #9C27B0; }
.stat-card:nth-child(4) { border-top-color: #FF9800; }
.stat-card:nth-child(5) { border-top-color: #4CAF50; }

.stat-icon-wrapper {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon-wrapper.cases-icon {
  background-color: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}
.stat-icon-wrapper.countries-icon {
  background-color: rgba(233, 30, 99, 0.1);
  color: #E91E63;
}
.stat-icon-wrapper.continents-icon {
  background-color: rgba(156, 39, 176, 0.1);
  color: #9C27B0;
}
.stat-icon-wrapper.participants-icon {
  background-color: rgba(255, 152, 0, 0.1);
  color: #FF9800;
}
.stat-icon-wrapper.earliest-icon {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.stat-icon-wrapper svg {
  width: 22px;
  height: 22px;
  fill: currentColor;
}

.stat-details {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-family: 'Outfit', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a2f16;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: #556c50;
  letter-spacing: 0.02em;
}

/* Map & Controls Styles */
.dashboard-controls {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  padding: 0.75rem 1.25rem;
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.08);
  border-radius: 12px;
  display: flex;
  gap: 1.5rem;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.01);
  flex-wrap: wrap;
}

.dashboard-controls strong {
  font-family: 'Outfit', sans-serif;
  font-weight: 600;
  color: #1a2f16;
  font-size: 0.9rem;
}

.dashboard-controls label {
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #496a40;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: color 0.15s ease;
}

.dashboard-controls label:hover {
  color: #1a2f16;
}

.dashboard-controls label.disabled {
  opacity: 0.5;
  pointer-events: none;
  cursor: not-allowed;
}

.dashboard-controls label.disabled input {
  cursor: not-allowed;
}

.dashboard-controls input[type="radio"],
.dashboard-controls input[type="checkbox"] {
  accent-color: #496a40;
  cursor: pointer;
}

/* Custom Marker Cluster Theme Overrides */
.marker-cluster div {
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
}

.dashboard-map-container {
  height: 600px;
  width: 100%;
  border: 1px solid rgba(73, 106, 64, 0.12);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(73, 106, 64, 0.04);
  overflow: hidden;
  margin-top: 0.5rem;
}

/* Charts Section Styles */
.dashboard-charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-top: 2rem;
  margin-bottom: 2rem;
}

@media (max-width: 860px) {
  .dashboard-charts-grid {
    grid-template-columns: 1fr;
  }
}

.chart-card {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 24px rgba(73, 106, 64, 0.03);
  display: flex;
  flex-direction: column;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.chart-card:hover {
  box-shadow: 0 12px 32px rgba(73, 106, 64, 0.08);
}

.chart-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1a2f16;
  margin-top: 0;
  margin-bottom: 1.25rem;
  border-bottom: 1px solid rgba(73, 106, 64, 0.08);
  padding-bottom: 0.75rem;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 300px;
}

.dashboard-legend-card {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.08);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-top: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.01);
}

.dashboard-legend-card h4 {
  font-family: 'Outfit', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #1a2f16;
}

.dashboard-legend-card p {
  margin: 0;
  font-size: 0.825rem;
  color: #556c50;
  line-height: 1.5;
}

.legend-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 6px;
}
</style>

<!-- Top Statistics Bar -->
<div class="dashboard-stats-grid">
  <!-- Card 1: Mapped Cases -->
  <div class="stat-card">
    <div class="stat-icon-wrapper cases-icon">
      <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
    </div>
    <div class="stat-details">
      <span class="stat-value" id="stat-cases">-</span>
      <span class="stat-label">Mapped Cases</span>
    </div>
  </div>
  
  <!-- Card 2: Countries -->
  <div class="stat-card">
    <div class="stat-icon-wrapper countries-icon">
      <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.53c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.4z"/></svg>
    </div>
    <div class="stat-details">
      <span class="stat-value" id="stat-countries">-</span>
      <span class="stat-label">Countries</span>
    </div>
  </div>

  <!-- Card 3: Continents -->
  <div class="stat-card">
    <div class="stat-icon-wrapper continents-icon">
      <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.53c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.4z"/></svg>
    </div>
    <div class="stat-details">
      <span class="stat-value" id="stat-continents">-</span>
      <span class="stat-label">Continents</span>
    </div>
  </div>

  <!-- Card 4: Participants -->
  <div class="stat-card">
    <div class="stat-icon-wrapper participants-icon">
      <svg viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 8 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
    </div>
    <div class="stat-details">
      <span class="stat-value" id="stat-participants">-</span>
      <span class="stat-label">Participants</span>
    </div>
  </div>

  <!-- Card 5: Earliest -->
  <div class="stat-card">
    <div class="stat-icon-wrapper earliest-icon">
      <svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>
    </div>
    <div class="stat-details">
      <span class="stat-value" id="stat-earliest">-</span>
      <span class="stat-label">Earliest Case</span>
    </div>
  </div>
</div>

<!-- Map View Mode Controls -->
<div class="dashboard-controls">
  <strong>View Mode:</strong>
  <label><input type="radio" name="map-view" value="points" checked> Point View (Orgs & Participants)</label>
  <label><input type="radio" name="map-view" value="heatmap"> Heat Map (Countries)</label>
  <span style="border-left: 1px solid rgba(73, 106, 64, 0.15); height: 20px; margin-inline: 0.5rem;"></span>
  <label id="cluster-toggle-label"><input type="checkbox" id="cluster-toggle" checked> Cluster Nearby Markers</label>
</div>

<!-- Map Container -->
<div id="map" class="dashboard-map-container"></div>

<!-- Case List Container (Dynamic) -->
<div id="case-list-container" class="chart-card" style="margin-top: 1.5rem; display: none;">
  <h3 id="selected-country-name" class="chart-title" style="margin-bottom: 0.75rem; border-bottom: none; padding-bottom: 0;">Cases in [Country]</h3>
  <ul id="case-list" style="margin: 0; padding-left: 1.25rem; color: #435b3f; line-height: 1.6;"></ul>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([20, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var pointLayer = L.layerGroup();
    var pointClusterGroup = L.markerClusterGroup();
    var heatmapLayer = L.layerGroup();

    // Data for markers
    var pointLocations = [
      {% for case in site.cases %}
        {% if case.curation-decision == "Do not include" %}{% continue %}{% endif %}
        {% for org_slug in case.lead-organisations %}
          {% assign org = site.organisations | where: "slug", org_slug | first %}
          {% if org %}
            {% for loc_slug in org.main-location %}
              {% assign loc = site.locations | where: "slug", loc_slug | first %}
              {% if loc.latitude and loc.longitude %}
              {
                lat: {{ loc.latitude }},
                lng: {{ loc.longitude }},
                title: "{{ org.title | escape }}",
                type: "Organisation",
                color: "#2196F3",
                case: "{{ case.title | escape }}",
                url: "{{ org.url | relative_url }}",
                caseUrl: "{{ case.url | relative_url }}"
              },
              {% endif %}
            {% endfor %}
          {% endif %}
        {% endfor %}
        {% for part_slug in case.participants %}
          {% assign part = site.participants | where: "slug", part_slug | first %}
          {% if part %}
            {% assign loc_titles = "" | split: "," %}
            {% for l_slug in part.locations %}
              {% assign l_item = site.locations | where: "slug", l_slug | first %}
              {% if l_item %}
                {% assign l_title_escaped = l_item.title | escape %}
                {% assign loc_titles = loc_titles | push: l_title_escaped %}
              {% endif %}
            {% endfor %}
            {% assign locations_list = loc_titles | join: ", " %}
            {% for loc_slug in part.locations %}
              {% assign loc = site.locations | where: "slug", loc_slug | first %}
              {% if loc.latitude and loc.longitude %}
              {
                lat: {{ loc.latitude }},
                lng: {{ loc.longitude }},
                title: "{{ part.title | escape }}",
                type: "Participants",
                color: "#FF9800",
                case: "{{ case.title | escape }}",
                caseUrl: "{{ case.url | relative_url }}",
                url: "{{ case.url | relative_url }}",
                count: "{{ part.how-many-people-took-part | escape }}",
                locationsList: "{{ locations_list }}"
              },
              {% endif %}
            {% endfor %}
          {% endif %}
        {% endfor %}
      {% endfor %}
    ];

    // Aggregated data for country highlighting
    var countryData = {};
    {% for case in site.cases %}
      {% if case.curation-decision == "Do not include" %}{% continue %}{% endif %}
      {% for org_slug in case.lead-organisations %}
        {% assign org = site.organisations | where: "slug", org_slug | first %}
        {% if org %}
          {% for loc_slug in org.main-location %}
            {% assign loc = site.locations | where: "slug", loc_slug | first %}
            {% if loc.country-code %}
              (function() {
                var code = "{{ loc.country-code }}";
                var name = "{{ loc.title | escape }}";
                var caseTitle = "{{ case.title | escape }}";
                var caseSlug = "{{ case.slug }}";
                var caseUrl = "{{ case.url | relative_url }}";
                if (!countryData[code]) { countryData[code] = { count: 0, cases: {}, name: name }; }
                if (!countryData[code].cases[caseSlug]) {
                  countryData[code].cases[caseSlug] = { title: caseTitle, url: caseUrl };
                  countryData[code].count++;
                }
              })();
            {% endif %}
          {% endfor %}
        {% endif %}
      {% endfor %}
      
      {% for part_slug in case.participants %}
        {% assign part = site.participants | where: "slug", part_slug | first %}
        {% if part %}
          {% for loc_slug in part.locations %}
            {% assign loc = site.locations | where: "slug", loc_slug | first %}
            {% if loc.country-code %}
              (function() {
                var code = "{{ loc.country-code }}";
                var name = "{{ loc.title | escape }}";
                var caseTitle = "{{ case.title | escape }}";
                var caseSlug = "{{ case.slug }}";
                var caseUrl = "{{ case.url | relative_url }}";
                if (!countryData[code]) { countryData[code] = { count: 0, cases: {}, name: name }; }
                if (!countryData[code].cases[caseSlug]) {
                  countryData[code].cases[caseSlug] = { title: caseTitle, url: caseUrl };
                  countryData[code].count++;
                }
              })();
            {% endif %}
          {% endfor %}
        {% endif %}
      {% endfor %}
    {% endfor %}

    // 1. Add markers to standard layer and cluster groups
    var bounds = L.latLngBounds();
    pointLocations.forEach(function(loc) {
        var marker = L.circleMarker([loc.lat, loc.lng], {
          radius: 8,
          fillColor: loc.color,
          color: "#fff",
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8
        });

        if (loc.type === "Participants") {
            var popupText = "";
            var countVal = loc.count ? loc.count.trim() : "";
            if (countVal !== "") {
                popupText = "<strong>" + countVal + "</strong> people took part in a participatory process on AI in <strong>" + loc.locationsList + "</strong> through <a href='" + loc.caseUrl + "'><strong>" + loc.case + "</strong></a>.";
            } else {
                popupText = "Participants took part in a participatory process on AI in <strong>" + loc.locationsList + "</strong> through <a href='" + loc.caseUrl + "'><strong>" + loc.case + "</strong></a>.";
            }
            marker.bindPopup(popupText);
        } else {
            marker.bindPopup("<strong>Lead Organisation:</strong> <a href='" + loc.url + "'><strong>" + loc.title + "</strong></a><br>" + 
                             "Lead organiser for <a href='" + loc.caseUrl + "'>" + loc.case + "</a>.");
        }
                         
        pointLayer.addLayer(marker);
        pointClusterGroup.addLayer(marker);
        bounds.extend([loc.lat, loc.lng]);
    });

    // 2. Load and style countries in heatmapLayer
    fetch('https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson')
      .then(res => res.json())
      .then(geojsonData => {
        L.geoJson(geojsonData, {
          style: function(feature) {
            var code = feature.properties.ISO_A2 || feature.properties.iso_a2;
            var data = countryData[code];
            return {
              fillColor: data ? '#E91E63' : 'transparent',
              weight: data ? 1 : 0,
              opacity: 1,
              color: 'white',
              fillOpacity: data ? Math.min(0.2 + (data.count * 0.2), 0.7) : 0
            };
          },
          onEachFeature: function(feature, layer) {
            var code = feature.properties.ISO_A2 || feature.properties.iso_a2;
            var data = countryData[code];
            if (data) {
              layer.on('click', function(e) {
                L.DomEvent.stopPropagation(e);
                displayCases(data);
              });
            }
          }
        }).addTo(heatmapLayer);
      });

    // Initial display selection based on Cluster checkbox
    var clusterToggle = document.getElementById('cluster-toggle');
    var clusterToggleLabel = document.getElementById('cluster-toggle-label');
    var currentPointsLayer = clusterToggle.checked ? pointClusterGroup : pointLayer;
    currentPointsLayer.addTo(map);

    // Toggle Logic
    document.querySelectorAll('input[name="map-view"]').forEach(function(radio) {
      radio.addEventListener('change', function() {
        if (this.value === 'points') {
          map.removeLayer(heatmapLayer);
          
          currentPointsLayer = clusterToggle.checked ? pointClusterGroup : pointLayer;
          map.addLayer(currentPointsLayer);
          
          clusterToggleLabel.classList.remove('disabled');
          clusterToggle.disabled = false;
          
          document.getElementById('case-list-container').style.display = 'none';
        } else {
          map.removeLayer(pointLayer);
          map.removeLayer(pointClusterGroup);
          map.addLayer(heatmapLayer);
          
          clusterToggleLabel.classList.add('disabled');
          clusterToggle.disabled = true;
        }
      });
    });

    clusterToggle.addEventListener('change', function() {
      var viewMode = document.querySelector('input[name="map-view"]:checked').value;
      if (viewMode === 'points') {
        map.removeLayer(pointLayer);
        map.removeLayer(pointClusterGroup);
        
        currentPointsLayer = this.checked ? pointClusterGroup : pointLayer;
        map.addLayer(currentPointsLayer);
      } else {
        currentPointsLayer = this.checked ? pointClusterGroup : pointLayer;
      }
    });

    function displayCases(data) {
      var container = document.getElementById('case-list-container');
      var title = document.getElementById('selected-country-name');
      var list = document.getElementById('case-list');
      
      title.innerText = "Cases in " + data.name;
      list.innerHTML = "";
      
      Object.values(data.cases).forEach(function(c) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = c.url;
        a.innerText = c.title;
        li.appendChild(a);
        list.appendChild(li);
      });
      
      container.style.display = "block";
      container.scrollIntoView({ behavior: 'smooth' });
    }

    if (pointLocations.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] });
    }

    // ==========================================
    // DASHBOARD COMPUTATIONS & CHARTS
    // ==========================================

    const countryToContinent = {
      // Africa
      'GH': 'Africa', 'KE': 'Africa', 'TG': 'Africa', 'NG': 'Africa', 'ZA': 'Africa', 'EG': 'Africa', 'MA': 'Africa', 'TZ': 'Africa', 'UG': 'Africa', 'DZ': 'Africa', 'ET': 'Africa',
      // Europe
      'AT': 'Europe', 'DE': 'Europe', 'GB': 'Europe', 'LT': 'Europe', 'IT': 'Europe', 'CH': 'Europe', 'FI': 'Europe',
      'FR': 'Europe', 'ES': 'Europe', 'NL': 'Europe', 'BE': 'Europe', 'SE': 'Europe', 'NO': 'Europe', 'DK': 'Europe',
      'PL': 'Europe', 'IE': 'Europe', 'PT': 'Europe', 'GR': 'Europe', 'CZ': 'Europe', 'HU': 'Europe', 'RO': 'Europe',
      // North America
      'CA': 'North America', 'US': 'North America', 'MX': 'North America', 'CU': 'North America', 'PR': 'North America',
      // South America
      'BO': 'South America', 'AR': 'South America', 'BR': 'South America', 'UY': 'South America', 'CO': 'South America', 'CL': 'South America', 'PE': 'South America', 'VE': 'South America', 'EC': 'South America',
      // Asia
      'JP': 'Asia', 'IN': 'Asia', 'CN': 'Asia', 'KR': 'Asia', 'SG': 'Asia', 'ID': 'Asia', 'MY': 'Asia', 'TH': 'Asia', 'VN': 'Asia', 'PH': 'Asia', 'PK': 'Asia', 'BD': 'Asia', 'TR': 'Asia', 'IL': 'Asia', 'SA': 'Asia',
      // Oceania
      'AU': 'Oceania', 'NZ': 'Oceania', 'FJ': 'Oceania', 'PG': 'Oceania'
    };

    // Load participants and cases arrays
    var allParticipants = [
      {% for part in site.participants %}
        {% assign linked_case_valid = false %}
        {% for case_slug in part.cases %}
          {% assign case_obj = site.cases | where: "slug", case_slug | first %}
          {% if case_obj and case_obj.curation-decision != "Do not include" %}
            {% assign linked_case_valid = true %}
          {% endif %}
        {% endfor %}
        {% if linked_case_valid == false %}{% continue %}{% endif %}
      {
        slug: {{ part.slug | jsonify }},
        title: {{ part.title | jsonify }},
        cases: {{ part.cases | jsonify }},
        howManyTookPart: "{{ part.how-many-people-took-part | escape }}",
        methods: {{ part.which-of-the-following-methods-were-used-to | jsonify }},
        locations: [
          {% for loc_slug in part.locations %}
            {% assign loc = site.locations | where: "slug", loc_slug | first %}
            {% if loc %}
            {
              slug: {{ loc.slug | jsonify }},
              name: {{ loc.name | default: loc.title | jsonify }},
              countryCode: {{ loc.country-code | jsonify }}
            },
            {% endif %}
          {% endfor %}
        ]
      },
      {% endfor %}
    ];

    var allCases = [
      {% for case in site.cases %}
      {% if case.curation-decision == "Do not include" %}{% continue %}{% endif %}
      {
        slug: {{ case.slug | jsonify }},
        title: {{ case.title | jsonify }},
        url: {{ case.url | relative_url | jsonify }},
        startYear: "{{ case.what-year-did-the-project-start | escape }}",
        concludeYear: "{{ case.what-year-did-the-project-conclude | escape }}"
      },
      {% endfor %}
    ];

    // Compute Stats
    var totalCases = allCases.length;
    var countriesSet = new Set();
    var continentsSet = new Set();
    var totalParticipants = 0;

    allParticipants.forEach(function(part) {
        // Sum participants count
        if (part.howManyTookPart) {
            var cleanedNum = part.howManyTookPart.replace(/,/g, '').trim();
            var num = parseInt(cleanedNum);
            if (!isNaN(num)) {
                totalParticipants += num;
            }
        }

        // Collect countries and continents
        if (part.locations && Array.isArray(part.locations)) {
            part.locations.forEach(function(loc) {
                if (loc.countryCode) {
                    var code = loc.countryCode.toUpperCase();
                    countriesSet.add(code);
                    
                    var continent = countryToContinent[code];
                    if (continent) {
                        continentsSet.add(continent);
                    }
                }
            });
        }
    });

    // Find Earliest Case Year
    var earliestYear = Infinity;
    allCases.forEach(function(c) {
        if (c.startYear) {
            var yr = parseInt(c.startYear);
            if (!isNaN(yr) && yr < earliestYear) {
                earliestYear = yr;
            }
        }
    });
    if (earliestYear === Infinity) {
        earliestYear = "N/A";
    }

    // Populate Top Stats DOM
    document.getElementById('stat-cases').innerText = totalCases;
    document.getElementById('stat-countries').innerText = countriesSet.size > 0 ? countriesSet.size : "-";
    document.getElementById('stat-continents').innerText = continentsSet.size > 0 ? continentsSet.size : "-";
    document.getElementById('stat-participants').innerText = totalParticipants > 0 ? totalParticipants.toLocaleString() : "-";
    document.getElementById('stat-earliest').innerText = earliestYear;

    // Calculate Methods used across cases
    var methodCounts = {};
    var caseMethods = {}; // caseSlug -> Set of methods used in this case

    allParticipants.forEach(function(part) {
        var methods = part.methods || [];
        var cases = part.cases || [];
        
        cases.forEach(function(caseSlug) {
            if (!caseMethods[caseSlug]) {
                caseMethods[caseSlug] = new Set();
            }
            methods.forEach(function(method) {
                caseMethods[caseSlug].add(method);
            });
        });
    });

    // Count cases per method
    Object.values(caseMethods).forEach(function(methodsSet) {
        methodsSet.forEach(function(method) {
            methodCounts[method] = (methodCounts[method] || 0) + 1;
        });
    });

    // Sort methods by frequency
    var sortedMethods = Object.keys(methodCounts).map(function(method) {
        return { name: method, count: methodCounts[method] };
    }).sort(function(a, b) {
        return b.count - a.count;
    });

    // Limit to 6 items + others
    var displayMethods = [];
    if (sortedMethods.length > 6) {
        displayMethods = sortedMethods.slice(0, 6);
        var remainingDistinctCount = sortedMethods.length - 6;
        if (remainingDistinctCount > 0) {
            displayMethods.push({ name: remainingDistinctCount + ' other methods', count: 0 });
        }
    } else {
        displayMethods = sortedMethods;
    }

    // Calculate Initiative Timeline
    var timelineCounts = {};
    allCases.forEach(function(c) {
        if (c.startYear) {
            var yr = parseInt(c.startYear);
            if (!isNaN(yr)) {
                timelineCounts[yr] = (timelineCounts[yr] || 0) + 1;
            }
        }
    });

    // Sort years chronologically
    var sortedYears = Object.keys(timelineCounts).map(Number).sort(function(a, b) {
        return a - b;
    });

    // Configure Chart.js Theme Defaults to match site fonts
    if (window.Chart) {
        Chart.defaults.font.family = "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
        Chart.defaults.color = '#556c50';

        // 1. Methods Used Chart
        var methodsCtx = document.getElementById('methods-chart').getContext('2d');
        var methodsLabels = displayMethods.map(function(item) { return item.name; });
        var methodsData = displayMethods.map(function(item) { return item.count; });

        new Chart(methodsCtx, {
            type: 'bar',
            data: {
                labels: methodsLabels,
                datasets: [{
                    label: 'Cases Using Method',
                    data: methodsData,
                    backgroundColor: 'rgba(73, 106, 64, 0.75)',
                    borderColor: '#496a40',
                    borderWidth: 1,
                    borderRadius: 6,
                    barThickness: 18
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#1a2f16',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        padding: 10,
                        cornerRadius: 8,
                        displayColors: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(73, 106, 64, 0.06)'
                        },
                        ticks: {
                            precision: 0
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });

        // 2. Timeline of Initiatives Chart
        var timelineCtx = document.getElementById('timeline-chart').getContext('2d');
        var timelineLabels = sortedYears;
        var timelineData = sortedYears.map(function(yr) { return timelineCounts[yr]; });

        var gradient = timelineCtx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(73, 106, 64, 0.35)');
        gradient.addColorStop(1, 'rgba(73, 106, 64, 0.00)');

        new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: timelineLabels,
                datasets: [{
                    label: 'Initiatives Started',
                    data: timelineData,
                    borderColor: '#496a40',
                    borderWidth: 3,
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.35,
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: '#496a40',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointHoverBackgroundColor: '#496a40',
                    pointHoverBorderColor: '#ffffff',
                    pointHoverBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#1a2f16',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        padding: 10,
                        cornerRadius: 8,
                        displayColors: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(73, 106, 64, 0.06)'
                        },
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
});
</script>

<!-- Bottom Dashboard Charts Section -->
<div class="dashboard-charts-grid">
  <!-- Chart Card 1: Methods -->
  <div class="chart-card">
    <h3 class="chart-title">Methods Used Across Cases</h3>
    <div class="chart-container">
      <canvas id="methods-chart"></canvas>
    </div>
  </div>
  
  <!-- Chart Card 2: Timeline -->
  <div class="chart-card">
    <h3 class="chart-title">Timeline of Initiatives</h3>
    <div class="chart-container">
      <canvas id="timeline-chart"></canvas>
    </div>
  </div>
</div>

<!-- Legend Card -->
<div class="dashboard-legend-card">
  <h4>Legend</h4>
  <p style="margin-bottom: 0.5rem;">
    <span class="legend-dot" style="background:#2196F3;"></span> Lead Organisations &nbsp;&nbsp;&nbsp;
    <span class="legend-dot" style="background:#FF9800;"></span> Participants &nbsp;&nbsp;&nbsp;
    <span class="legend-dot" style="background:#E91E63; opacity: 0.6;"></span> Countries with engagement (Heat-map)
  </p>
  <p><small style="color: #7a9476; font-style: italic;">Click on a highlighted country in Heat Map view mode to list its associated cases below the map.</small></p>
</div>

