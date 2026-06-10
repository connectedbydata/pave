---
layout: default
title: Videos
show_banner: false
permalink: /videos/
menus: [header]
---

<!-- Import Modern Premium Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

{% assign video_count = 0 %}
{% for res in site.resources %}
  {% if res.select == "Video" %}
    {% assign video_count = video_count | plus: 1 %}
  {% endif %}
{% endfor %}

<div class="video-gallery-container cases-index-page">
  <div class="browse-header-row">
    <h1 class="browse-title" id="main-cases-title">
      <span class="cases-count-num">{{ video_count }}</span> project videos
    </h1>
  </div>

  {% include filters_panel.html %}

  <!-- Status Bar -->
  <div class="browse-status-bar">
    <span class="cases-count-label">Showing <span class="cases-count-num">{{ video_count }}</span> videos</span>
  </div>

  <!-- Video Grid List -->
  <main class="video-grid" id="video-grid">
    {% for res in site.resources %}
      {% if res.select == "Video" %}
        <!-- Retrieve case metadata for current resource -->
        {% assign res_focus = "" | split: "||" %}
        {% assign res_methods = "" | split: "||" %}
        {% assign res_goals = "" | split: "||" %}
        {% assign res_locations = "" | split: "||" %}
        {% assign res_cases = "" | split: "||" %}

        {% for case_slug in res.cases %}
          {% for c in site.cases %}
            {% if c.slug == case_slug %}
              {% assign res_cases = res_cases | push: c.title %}
              <!-- Focus -->
              {% if c.what-form-of-ai-is-the-project-about %}
                {% for val in c.what-form-of-ai-is-the-project-about %}
                  {% assign res_focus = res_focus | push: val %}
                {% endfor %}
              {% endif %}
              <!-- Goals -->
              {% if c.project-goals %}
                {% for val in c.project-goals %}
                  {% assign res_goals = res_goals | push: val %}
                {% endfor %}
              {% endif %}
              <!-- Methods & Locations from participants -->
              {% if c.participants %}
                {% for part_slug in c.participants %}
                  {% assign part = site.participants | where: "slug", part_slug | first %}
                  {% if part %}
                    {% if part.which-of-the-following-methods-were-used-to %}
                      {% for method in part.which-of-the-following-methods-were-used-to %}
                        {% assign res_methods = res_methods | push: method %}
                      {% endfor %}
                    {% endif %}
                    {% if part.locations %}
                      {% for loc_slug in part.locations %}
                        {% assign loc = site.locations | where: "slug", loc_slug | first %}
                        {% if loc and loc.country-code %}
                          {% assign res_locations = res_locations | push: loc.country-code %}
                        {% endif %}
                      {% endfor %}
                    {% endif %}
                  {% endif %}
                {% endfor %}
              {% endif %}
            {% endif %}
          {% endfor %}
        {% endfor %}

        {% assign res_focus_uniq = res_focus | uniq %}
        {% assign res_methods_uniq = res_methods | uniq %}
        {% assign res_goals_uniq = res_goals | uniq %}
        {% assign res_locations_uniq = res_locations | uniq %}
        {% assign res_cases_uniq = res_cases | uniq %}

        <article class="video-card" 
                 data-focus="{{ res_focus_uniq | join: '||' | downcase }}" 
                 data-methods="{{ res_methods_uniq | join: '||' | downcase }}"
                 data-goals="{{ res_goals_uniq | join: '||' | downcase }}"
                 data-locations="{{ res_locations_uniq | join: '||' | downcase }}"
                 data-url="{{ res.external_url | escape }}">
          
          <!-- Card Thumbnail Area -->
          <div class="video-cover-wrapper">
            <div class="video-cover-container" id="cover-{{ res.slug }}">
              <!-- Spinner displayed during lazy loads -->
              <div class="video-spinner"></div>
              
              <!-- CURATED COVER ELEMENT (Loaded by JS) -->
              <div class="video-media-target"></div>

              <!-- Premium Hover & Play Overlay -->
              <div class="play-overlay">
                <div class="play-btn-circle">
                  <svg class="play-svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z"></path>
                  </svg>
                  <svg class="external-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="display: none;">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                    <polyline points="15 3 21 3 21 9"></polyline>
                    <line x1="10" y1="14" x2="21" y2="3"></line>
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Card Content Area -->
          <div class="video-card-body">
            <div class="video-case-link">
              {% for case_name in res_cases_uniq %}
                <span class="case-tag-badge">{{ case_name }}</span>
              {% endfor %}
            </div>

            <h2 class="video-title">{{ res.title | escape }}</h2>

            <p class="video-description">
              {% if res.short-description %}
                {{ res.short-description | escape }}
              {% else %}
                <!-- Fallback to case description or nice default -->
                {% assign fallback_desc = "" %}
                {% for case_slug in res.cases %}
                  {% for c in site.cases %}
                    {% if c.slug == case_slug %}
                      {% assign fallback_desc = c.provide-a-brief-description-of-the-project | truncatewords: 25 %}
                    {% endif %}
                  {% endfor %}
                {% endfor %}
                {% if fallback_desc != "" %}
                  {{ fallback_desc | escape }}
                {% else %}
                  Explore key highlights and media coverage from this case study engagement.
                {% endif %}
              {% endif %}
            </p>

            <!-- Specs block -->
            <div class="card-specs">
              {% if res_focus_uniq.size > 0 %}
                <div class="spec-row">
                  <span class="spec-label">Focus</span>
                  <span class="spec-value">{{ res_focus_uniq | join: ', ' }}</span>
                </div>
              {% endif %}

              {% if res_methods_uniq.size > 0 %}
                <div class="spec-row">
                  <span class="spec-label">Methods</span>
                  <span class="spec-value">{{ res_methods_uniq | join: ', ' }}</span>
                </div>
              {% endif %}

              {% if res_locations_uniq.size > 0 %}
                <div class="spec-row">
                  <span class="spec-label">Locations</span>
                  <span class="spec-value">
                    {% for code in res_locations_uniq %}
                      {% include country_name.html code=code %}{% unless forloop.last %}, {% endunless %}
                    {% endfor %}
                  </span>
                </div>
              {% endif %}
            </div>
          </div>

          <!-- Hidden case details content parsed on modal open -->
          <div class="video-case-details-source" style="display: none;">
            {% for case_slug in res.cases %}
              {% for c in site.cases %}
                {% if c.slug == case_slug %}
                  <div class="modal-case-info">
                    <span class="modal-case-badge">CASE STUDY</span>
                    <h3 class="modal-case-title">{{ c.title | escape }}</h3>
                    {% if c.provide-a-brief-description-of-the-project %}
                      <p class="modal-case-desc">{{ c.provide-a-brief-description-of-the-project | strip_html | truncatewords: 50 | escape }}</p>
                    {% endif %}
                    <div class="modal-case-fields">
                      {% if c.how-was-the-project-initiated %}
                        <div class="modal-meta-item">
                          <span class="modal-meta-label">Initiation:</span>
                          <span class="modal-meta-val">{{ c.how-was-the-project-initiated | join: ", " }}</span>
                        </div>
                      {% endif %}
                      {% if c.what-form-of-ai-is-the-project-about %}
                        <div class="modal-meta-item">
                          <span class="modal-meta-label">AI Focus:</span>
                          <span class="modal-meta-val">{{ c.what-form-of-ai-is-the-project-about | join: ", " }}</span>
                        </div>
                      {% endif %}
                      {% if c.geographic-scope %}
                        <div class="modal-meta-item">
                          <span class="modal-meta-label">Locations:</span>
                          <span class="modal-meta-val">
                            {% assign loc_titles = "" | split: "," %}
                            {% for loc_slug in c.geographic-scope %}
                              {% assign loc_item = site.locations | where: "slug", loc_slug | first %}
                              {% if loc_item %}
                                {% assign loc_titles = loc_titles | push: loc_item.title %}
                              {% endif %}
                            {% endfor %}
                            {{ loc_titles | join: ", " }}
                          </span>
                        </div>
                      {% endif %}
                    </div>
                    <a href="{{ c.url | relative_url }}" class="modal-view-case-btn" target="_blank">
                      <span>View Full Case Study</span>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                      </svg>
                    </a>
                  </div>
                {% endif %}
              {% endfor %}
            {% endfor %}
          </div>
        </article>
      {% endif %}
    {% endfor %}

    <!-- Empty State -->
    <div id="no-results-msg" class="no-results-message gallery-empty-state" style="display: none;">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="8" y1="12" x2="16" y2="12"></line>
      </svg>
      <h3>No matches found</h3>
      <p>Try clearing your active filters or selecting different options.</p>
    </div>
  </main>

  <!-- Cinema Immersive Full-Screen Video Modal -->
  <div id="video-modal" class="video-modal" aria-hidden="true" role="dialog" aria-label="Video Player">
    <div class="modal-backdrop" id="modal-backdrop"></div>
    <div class="modal-content-container">
      <button id="modal-close-btn" class="modal-close-btn" aria-label="Close video player">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <div class="modal-split-layout">
        <div class="modal-video-side">
          <div class="modal-video-wrapper">
            <iframe id="modal-video-iframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
          </div>
        </div>
        <div class="modal-details-side">
          <div id="modal-case-details-content">
            <!-- Populated via Javascript -->
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Custom High-Aesthetic styling (Vanilla CSS) -->
<style>
/* Variable and Premium Typography Setup */
.video-gallery-container {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  max-width: 100%;
  margin: 0 auto;
  padding: 1.5rem 0.5rem;
  color: #1e293b;
}

@media (min-width: 1200px) {
  .site-header .wrapper,
  .site-footer .wrapper,
  .page-content .wrapper {
    max-width: 80% !important;
    transition: max-width 0.3s ease;
  }
}

/* Base header layout */
.gallery-header {
  margin-block-end: 2.5rem;
  text-align: left;
}
.header-badge {
  display: inline-block;
  font-family: 'Outfit', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #6366f1;
  background: rgba(99, 102, 241, 0.08);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  margin-bottom: 0.75rem;
  border: 1px solid rgba(99, 102, 241, 0.15);
}
.gallery-header h1 {
  font-family: 'Outfit', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.15;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.gallery-header .subtitle {
  font-size: 1.05rem;
  color: #64748b;
  margin: 0;
  max-width: 600px;
  line-height: 1.5;
}

/* Glassmorphic Filter Box */
.filter-section {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(226, 232, 240, 0.8);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 20px;
  padding: 1.75rem;
  margin-bottom: 3rem;
  box-shadow: 0 4px 20px rgba(148, 163, 184, 0.05), 0 10px 40px rgba(148, 163, 184, 0.03);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  transition: all 0.3s ease;
}

.filter-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
  padding-bottom: 1rem;
}
.filter-title-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.filter-icon {
  width: 18px;
  height: 18px;
  color: #4f46e5;
}
.filter-title-group h3 {
  font-family: 'Outfit', sans-serif;
  font-size: 1.15rem;
  font-weight: 600;
  margin: 0;
  color: #0f172a;
}

.clear-filters-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(239, 68, 68, 0.06);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.15);
  padding: 0.35rem 0.8rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fadeIn 0.25s ease-out;
}
.clear-filters-btn svg {
  width: 12px;
  height: 12px;
}
.clear-filters-btn:hover {
  background: #dc2626;
  color: #ffffff;
  border-color: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
}

.filter-groups {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}
@media (min-width: 768px) {
  .filter-groups {
    grid-template-columns: 1fr 1fr;
  }
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.filter-group h4 {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  margin: 0;
}
.toggle-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

/* Glassmorphic Active Toggle Badges */
.filter-toggle {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #e2e8f0;
  padding: 0.4rem 0.9rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}
.filter-toggle:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #0f172a;
  transform: translateY(-1px);
}
.filter-toggle.active {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  color: #ffffff;
  border-color: #4f46e5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
  font-weight: 600;
}

/* CSS Grid for neat, uniform columns */
.video-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.75rem;
  transition: all 0.4s ease;
}
@media (min-width: 640px) {
  .video-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1024px) {
  .video-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Video Card Styling (Equal Height Layout) */
.video-card {
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.9);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  opacity: 1;
  transform: scale(1);
}
.video-card:hover {
  transform: translateY(-4px) scale(1.005);
  border-color: rgba(99, 102, 241, 0.25);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.03);
}

/* Card image / Video container styling */
.video-cover-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #0f172a;
}
.video-cover-container {
  width: 100%;
  height: 100%;
  position: relative;
  cursor: pointer;
  overflow: hidden;
}

.video-media-target {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.video-card:hover .video-media-target {
  transform: scale(1.05);
}

/* Video Loading Spinner */
.video-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 32px;
  height: 32px;
  margin-top: -16px;
  margin-left: -16px;
  border: 3px solid rgba(255,255,255,0.1);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 1s infinite linear;
  display: none;
  z-index: 2;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Overlay play button styling */
.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}
.video-card:hover .play-overlay {
  opacity: 1;
}

.play-btn-circle {
  width: 54px;
  height: 54px;
  background: rgba(255, 255, 255, 0.95);
  color: #4f46e5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  transform: scale(0.85);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.play-svg {
  width: 20px;
  height: 20px;
  margin-left: 2px; /* Center-align the play triangle */
}
.external-svg {
  width: 20px;
  height: 20px;
}
.video-card:hover .play-btn-circle {
  transform: scale(1.12);
  background: #4f46e5;
  color: #ffffff;
  box-shadow: 0 15px 30px rgba(79, 70, 229, 0.4);
}

/* Iframe layout matching */
.video-iframe {
  width: 100%;
  height: 100%;
  border: 0;
  z-index: 3;
  position: absolute;
  top: 0;
  left: 0;
  animation: fadeIn 0.4s ease;
}

/* Card details styling */
.video-card-body {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex-grow: 1; /* Stretch to fill card height */
}
.video-case-link {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
.case-tag-badge {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #4f46e5;
  background: rgba(79, 70, 229, 0.06);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  border: 1px solid rgba(79, 70, 229, 0.1);
}

.video-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.15rem;
  font-weight: 600;
  line-height: 1.35;
  margin: 0;
  color: #0f172a;
}
.video-description {
  font-size: 0.875rem;
  line-height: 1.45;
  color: #475569;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 4.35em; /* Lock description space for neat grid alignment */
}

/* Specs block styled like Cases */
.video-card .card-specs {
  margin-top: auto; /* Push specs and description to bottom and align */
  margin-bottom: 0.5rem;
  padding-block: 0.75rem;
  border-top: 1px solid #496a40 !important;
  border-bottom: 1px solid #496a40 !important;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.video-card .card-specs .spec-row {
  display: flex;
  font-size: 0.775rem !important;
  line-height: 1.4;
  gap: 0.5rem;
}
.video-card .card-specs .spec-row .spec-label {
  font-weight: 700;
  color: #000000 !important;
  text-transform: uppercase;
  min-width: 75px;
  flex-shrink: 0;
}
.video-card .card-specs .spec-row .spec-value {
  color: #496a40 !important;
}

/* Fade animation effects */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Empty State Styling */
.gallery-empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border: 1px dashed #cbd5e1;
  border-radius: 20px;
  animation: fadeIn 0.3s ease;
  width: 100%;
}
.gallery-empty-state svg {
  width: 48px;
  height: 48px;
  color: #94a3b8;
  margin-bottom: 1rem;
}
.gallery-empty-state h3 {
  font-family: 'Outfit', sans-serif;
  font-size: 1.25rem;
  margin: 0 0 0.5rem 0;
  color: #0f172a;
}
.gallery-empty-state p {
  color: #64748b;
  margin: 0;
  font-size: 0.9rem;
}

/* Adaptive transitions for display/hide card actions */
.video-card.hidden {
  opacity: 0;
  transform: scale(0.95);
  height: 0;
  margin-bottom: 0;
  border-width: 0;
  padding: 0;
  pointer-events: none;
  display: none; /* Instant layout hide for columns reflow */
}

/* Cinema Immersive Full-Screen Video Modal Styling */
.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.video-modal.active {
  opacity: 1;
  pointer-events: auto;
}
.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(10, 15, 30, 0.85);
  backdrop-filter: blur(12px) saturate(120%);
  -webkit-backdrop-filter: blur(12px) saturate(120%);
  transition: all 0.3s ease;
}
.modal-content-container {
  position: relative;
  width: 90vw;
  max-width: 1400px;
  height: 80vh;
  max-height: 800px;
  background: #0f172a;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7);
  transform: scale(0.94);
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 100000;
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.video-modal.active .modal-content-container {
  transform: scale(1);
}

/* Modal Split Screen Layout */
.modal-split-layout {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}
@media (min-width: 768px) {
  .modal-split-layout {
    flex-direction: row;
  }
}

.modal-video-side {
  flex: 3;
  background: #000000;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40vh;
}
@media (min-width: 768px) {
  .modal-video-side {
    min-height: auto;
  }
}

.modal-video-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}
.modal-video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

.modal-details-side {
  flex: 1;
  background: #0f172a;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: #f8fafc;
  overflow-y: auto;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
@media (min-width: 768px) {
  .modal-details-side {
    border-top: none;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
  }
}

/* Modal Details Elements Styling (Premium typography & contrast) */
.modal-case-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.modal-case-info:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
.modal-case-badge {
  display: inline-block;
  align-self: flex-start;
  font-family: 'Outfit', sans-serif;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #818cf8;
  background: rgba(129, 140, 248, 0.15);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  border: 1px solid rgba(129, 140, 248, 0.2);
}
.modal-case-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.3;
  margin: 0;
  color: #ffffff;
}
.modal-case-desc {
  font-size: 0.85rem;
  line-height: 1.5;
  color: #94a3b8;
  margin: 0;
}
.modal-case-fields {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.modal-meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}
.modal-meta-label {
  font-size: 0.65rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.modal-meta-val {
  font-size: 0.8rem;
  color: #cbd5e1;
}
.modal-view-case-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #4f46e5;
  color: #ffffff !important;
  font-size: 0.8rem;
  font-weight: 600;
  text-decoration: none !important;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  margin-top: 0.5rem;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}
.modal-view-case-btn:hover {
  background: #6366f1;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.35);
}
.modal-view-case-btn svg {
  width: 14px;
  height: 14px;
}

.modal-close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 100001;
}
.modal-close-btn:hover {
  background: rgba(255, 255, 255, 0.28);
  transform: rotate(90deg) scale(1.05);
}
.modal-close-btn svg {
  width: 20px;
  height: 20px;
}
</style>

<!-- Custom JS Engine -->
<script>
document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.video-card');

  // Get Cinema Modal Elements
  const modal = document.getElementById('video-modal');
  const modalIframe = document.getElementById('modal-video-iframe');
  const modalClose = document.getElementById('modal-close-btn');
  const modalBackdrop = document.getElementById('modal-backdrop');
  const modalCaseDetails = document.getElementById('modal-case-details-content');

  // Helper: Open Modal function
  function openVideoModal(ytId, title, detailsHtml) {
    modalIframe.src = `https://www.youtube-nocookie.com/embed/${ytId}?autoplay=1&rel=0&modestbranding=1&cc_load_policy=1`;
    modalIframe.title = title;
    
    if (modalCaseDetails) {
      modalCaseDetails.innerHTML = detailsHtml;
    }
    
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden'; // prevent background scrolling
  }

  // Helper: Close Modal function
  function closeVideoModal() {
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
    modalIframe.src = ''; // completely halt video playback/audio
    
    if (modalCaseDetails) {
      modalCaseDetails.innerHTML = '';
    }
    
    document.body.style.overflow = '';
  }

  // Bind Cinema Modal close triggers
  modalClose.addEventListener('click', closeVideoModal);
  modalBackdrop.addEventListener('click', closeVideoModal);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeVideoModal();
    }
  });

  // Helper: Extract YouTube ID
  function getYouTubeId(url) {
    if (!url) return null;
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
  }

  // 1. Initial Video Player & Cover Setup
  cards.forEach(card => {
    const url = card.dataset.url;
    const coverWrapper = card.querySelector('.video-cover-container');
    const mediaTarget = card.querySelector('.video-media-target');
    const playCircle = card.querySelector('.play-btn-circle');
    const playSvg = card.querySelector('.play-svg');
    const externalSvg = card.querySelector('.external-svg');

    const ytId = getYouTubeId(url);

    if (ytId) {
      // Set high-res YouTube Thumbnail
      mediaTarget.style.backgroundImage = `url('https://img.youtube.com/vi/${ytId}/maxresdefault.jpg')`;
      
      // Dynamic overlay play click opens modern cinema modal
      coverWrapper.addEventListener('click', () => {
        const title = card.querySelector('.video-title').textContent;
        const desc = card.querySelector('.video-description').textContent.trim();
        const detailsSource = card.querySelector('.video-case-details-source');
        
        let detailsHtml = '';
        if (detailsSource && detailsSource.innerHTML.trim() !== '') {
          detailsHtml = detailsSource.innerHTML;
        } else {
          detailsHtml = `
            <div class="modal-case-info">
              <span class="modal-case-badge">VIDEO RESOURCE</span>
              <h3 class="modal-case-title">${title}</h3>
              <p class="modal-case-desc">${desc}</p>
            </div>
          `;
        }
        
        openVideoModal(ytId, title, detailsHtml);
      });

    } else {
      // Non-YouTube Links (Vimeo or Web pages)
      const hostname = new URL(url).hostname.replace('www.', '');
      
      // Gorgeous premium gradient fallback thumbnail
      mediaTarget.style.background = 'linear-gradient(135deg, #4f46e5 0%, #a855f7 100%)';
      
      // Add custom visual badge for external context
      const tagBadge = document.createElement('div');
      tagBadge.className = 'external-source-badge';
      tagBadge.textContent = hostname;
      tagBadge.style.cssText = `
        position: absolute;
        top: 12px;
        right: 12px;
        background: rgba(15, 23, 42, 0.8);
        color: #ffffff;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(4px);
        z-index: 2;
      `;
      coverWrapper.appendChild(tagBadge);

      // Display outbound external SVG instead of play
      playSvg.style.display = 'none';
      externalSvg.style.display = 'block';

      // Click launches the link in a new tab
      coverWrapper.addEventListener('click', () => {
        window.open(url, '_blank', 'noopener,noreferrer');
      });
    }
  });
});
</script>

{% include filters_script.html %}

