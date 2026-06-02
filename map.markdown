---
layout: default
title: Map of Engagement
permalink: /map/
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

<div id="map-controls" style="margin-top: 20px; padding: 10px; background: #f0f0f0; border: 1px solid #ccc; border-radius: 4px; display: flex; gap: 20px; align-items: center;">
  <strong>View Mode:</strong>
  <label style="cursor: pointer;"><input type="radio" name="map-view" value="points" checked> Point View (Orgs & Participants)</label>
  <label style="cursor: pointer;"><input type="radio" name="map-view" value="heatmap"> Heat Map (Countries)</label>
</div>

<div id="map" style="height: 600px; width: 100%; margin-top: 10px; border: 1px solid #ccc;"></div>

<div id="case-list-container" style="margin-top: 20px; display: none;">
  <h3 id="selected-country-name">Cases in [Country]</h3>
  <ul id="case-list"></ul>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([20, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var pointLayer = L.layerGroup().addTo(map);
    var heatmapLayer = L.layerGroup();

    // Data for markers
    var pointLocations = [
      {% for case in site.cases %}
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
                url: "{{ org.url | relative_url }}"
              },
              {% endif %}
            {% endfor %}
          {% endif %}
        {% endfor %}
        {% for part_slug in case.participants %}
          {% assign part = site.participants | where: "slug", part_slug | first %}
          {% if part %}
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
                url: "{{ case.url | relative_url }}"
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

    // 1. Add markers to pointLayer
    var bounds = L.latLngBounds();
    pointLocations.forEach(function(loc) {
        var marker = L.circleMarker([loc.lat, loc.lng], {
          radius: 8,
          fillColor: loc.color,
          color: "#fff",
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8
        }).addTo(pointLayer);

        marker.bindPopup("<strong>" + loc.title + "</strong><br>" + 
                         "Type: " + loc.type + "<br>" +
                         "Case: <a href='" + loc.url + "'>" + loc.case + "</a>");
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

    // Toggle Logic
    document.querySelectorAll('input[name="map-view"]').forEach(function(radio) {
      radio.addEventListener('change', function() {
        if (this.value === 'points') {
          map.removeLayer(heatmapLayer);
          map.addLayer(pointLayer);
          document.getElementById('case-list-container').style.display = 'none';
        } else {
          map.removeLayer(pointLayer);
          map.addLayer(heatmapLayer);
        }
      });
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
});
</script>

<div class="map-legend" style="margin-top: 20px; padding: 15px; background: #f9f9f9; border: 1px solid #ddd; border-radius: 4px;">
  <h4>Legend</h4>
  <p>
    <span style="display:inline-block; width:12px; height:12px; background:#2196F3; border-radius:50%; margin-right:5px;"></span> Lead Organisations<br>
    <span style="display:inline-block; width:12px; height:12px; background:#FF9800; border-radius:50%; margin-right:5px;"></span> Participants<br>
    <span style="display:inline-block; width:12px; height:12px; background:#E91E63; opacity: 0.5; margin-right:5px;"></span> Countries with engagement (Heat-map)
  </p>
  <p><small>Click on a highlighted country to see the associated cases below.</small></p>
</div>
