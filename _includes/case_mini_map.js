// 2. Premium Widescreen Mini Map Loader (Leaflet + CARTO basemap)
var mapMarkers = [
  // Lead Organisations (bold blue dot)
  {% if page.fld05RupsUvpbg8vU %}
    {% for org_slug in page.fld05RupsUvpbg8vU %}
      {% assign org = site.organisations | where: "slug", org_slug | first %}
      {% if org %}
        {% for loc_slug in org.fldjNFI2YXLQ2PapK %}
          {% assign loc = site.locations | where: "slug", loc_slug | first %}
          {% if loc.fldWtvMukYmq1IuWq and loc.fldCdYZ8Ay6f6ulq1 %}
            {
              lat: {{ loc.fldWtvMukYmq1IuWq }},
              lng: {{ loc.fldCdYZ8Ay6f6ulq1 }},
              title: "{{ org.title | escape }} (Lead)",
              color: "#1d4ed8", /* Bold blue */
              radius: 7,
              weight: 2
            },
          {% endif %}
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endif %}

  // Involved Organisations (small grey dots)
  {% if page.fldxJ934AvP0LGna0 %}
    {% for org_slug in page.fldxJ934AvP0LGna0 %}
      {% assign org = site.organisations | where: "slug", org_slug | first %}
      {% if org %}
        {% for loc_slug in org.fldjNFI2YXLQ2PapK %}
          {% assign loc = site.locations | where: "slug", loc_slug | first %}
          {% if loc.fldWtvMukYmq1IuWq and loc.fldCdYZ8Ay6f6ulq1 %}
            {
              lat: {{ loc.fldWtvMukYmq1IuWq }},
              lng: {{ loc.fldCdYZ8Ay6f6ulq1 }},
              title: "{{ org.title | escape }} (Involved)",
              color: "#64748b", /* Grey */
              radius: 4,
              weight: 1
            },
          {% endif %}
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endif %}

  // Participants (orange dots)
  {% if page.fldAQhKPRBSYGsJwD %}
    {% for part_slug in page.fldAQhKPRBSYGsJwD %}
      {% assign part = site.participants | where: "slug", part_slug | first %}
      {% if part %}
        {% for loc_slug in part.fld0BFLjrsMUNnQAv %}
          {% assign loc = site.locations | where: "slug", loc_slug | first %}
          {% if loc.fldWtvMukYmq1IuWq and loc.fldCdYZ8Ay6f6ulq1 %}
            {
              lat: {{ loc.fldWtvMukYmq1IuWq }},
              lng: {{ loc.fldCdYZ8Ay6f6ulq1 }},
              title: "{{ part.title | escape }} (Participants)",
              color: "#f97316", /* Orange */
              radius: 5.5,
              weight: 1.5
            },
          {% endif %}
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endif %}
];

const mapContainer = document.getElementById('case-mini-map');
if (mapContainer && mapMarkers.length > 0) {
  // Initialise map
  var miniMap = L.map('case-mini-map', {
    zoomControl: false,
    attributionControl: false
  }).setView([20, 0], 2);

  // Premium Carto Light Basemap
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 20
  }).addTo(miniMap);

  var bounds = L.latLngBounds();

  mapMarkers.forEach(function (m) {
    var marker = L.circleMarker([m.lat, m.lng], {
      radius: m.radius,
      fillColor: m.color,
      color: "#ffffff",
      weight: m.weight,
      opacity: 1,
      fillOpacity: 0.85
    }).addTo(miniMap);

    marker.bindPopup("<strong style='font-family:Plus Jakarta Sans, sans-serif; font-size:11px;'>" + m.title + "</strong>");
    bounds.extend([m.lat, m.lng]);
  });

  // Ensure map tiles and dimensions are correctly initialized and centered in responsive grid panels
  setTimeout(function () {
    miniMap.invalidateSize();
    miniMap.fitBounds(bounds, { padding: [15, 15], maxZoom: 10 });
  }, 150);
} else if (mapContainer) {
  // If no locations are mapped for this case study, remove map slot
  mapContainer.style.display = 'none';
}
