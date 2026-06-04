---
layout: default
title: Slideshow
permalink: /slideshow/
menus: [header]
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

<style>
  /* 1. Hide default Jekyll theme header & footer on slideshow page for immersive view */
  .site-header, .site-footer {
    display: none !important;
  }
  .page-content {
    padding: 0 !important;
    margin: 0 !important;
    background: #000 !important;
  }
  .page-content .wrapper {
    max-width: none !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  body {
    overflow: hidden !important;
    background-color: #000 !important;
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
  }

  /* Top Banner (1/10 Height: 10vh) */
  .top-banner {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 10vh;
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-inline: 2rem;
    box-sizing: border-box;
    z-index: 100;
  }

  .banner-left {
    display: flex;
    align-items: center;
  }

  .pave-logo {
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: #ffffff;
  }

  .banner-middle {
    display: flex;
    align-items: center;
    max-width: 32%;
  }

  .banner-explanation {
    font-size: 0.85rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.3;
  }

  .banner-right {
    display: flex;
    align-items: center;
    gap: 1.25rem;
  }

  /* Stacked Controls and Dropdown Selector */
  .controls-and-selector {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.3rem;
  }

  /* Controls and Progress Bar */
  .controls-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: none;
    border: none;
    padding: 0;
    box-shadow: none;
  }

  .play-pause-btn {
    background: none;
    border: none;
    color: #ffffff;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.25rem;
    transition: transform 0.2s;
  }

  .play-pause-btn:hover {
    transform: scale(1.12);
  }

  .play-pause-btn svg {
    width: 1.25rem;
    height: 1.25rem;
  }

  .speed-control-group {
    display: flex;
    align-items: center;
  }

  .speed-select {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.4rem;
    border-radius: 6px;
    outline: none;
    cursor: pointer;
    transition: all 0.2s;
  }

  .speed-select:hover {
    background: rgba(255, 255, 255, 0.18);
    border-color: rgba(255, 255, 255, 0.35);
  }

  .speed-select option {
    background: #0f172a;
    color: #ffffff;
  }

  .progress-bar-container {
    width: 110px;
    height: 4px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 9999px;
    overflow: hidden;
  }

  .progress-bar-fill {
    height: 100%;
    width: 0%;
    background: #6366f1;
    border-radius: 9999px;
  }

  .slide-counter {
    font-family: 'Outfit', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.85);
    min-width: 50px;
    text-align: center;
  }

  /* Case selector styles */
  .case-select-group {
    display: flex;
    align-items: center;
  }

  .case-select {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.725rem;
    font-weight: 600;
    padding: 0.15rem 0.4rem;
    border-radius: 5px;
    outline: none;
    cursor: pointer;
    transition: all 0.2s;
    max-width: 280px;
    text-overflow: ellipsis;
  }

  .case-select:hover {
    background: rgba(255, 255, 255, 0.18);
    border-color: rgba(255, 255, 255, 0.35);
  }

  .case-select option {
    background: #0f172a;
    color: #ffffff;
  }

  /* Exit Button style */
  .exit-btn {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    text-decoration: none;
    transition: all 0.2s;
  }

  .exit-btn:hover {
    background: rgba(255, 255, 255, 0.22);
    transform: scale(1.05);
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
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-size: cover;
    background-position: center;
    position: relative;
    box-sizing: border-box;
  }

  .slide-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(15, 23, 42, 0.4) 0%, rgba(15, 23, 42, 0.6) 60%, rgba(15, 23, 42, 0.75) 100%);
    z-index: 1;
  }

  /* Defined Color Palettes for Slides without Images */
  .bg-palette-0 { background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); }
  .bg-palette-1 { background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); }
  .bg-palette-2 { background: linear-gradient(135deg, #0c4a6e 0%, #0f172a 100%); }
  .bg-palette-3 { background: linear-gradient(135deg, #7c2d12 0%, #4c1d95 100%); }
  .bg-palette-4 { background: linear-gradient(135deg, #450a0a 0%, #1e1b4b 100%); }
  .bg-palette-5 { background: linear-gradient(135deg, #111827 0%, #374151 100%); }

  /* Message content Area (aligned in the middle 65% of screen height) */
  .slide-content-upper {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    z-index: 10;
    padding-top: 10vh; /* Shifts text below top banner */
    padding-bottom: 25vh; /* Shifts text above bottom details */
  }

  .message-wrapper {
    max-width: 960px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    padding-inline: 2rem;
    text-align: center;
  }

  .message-type-badge {
    font-family: 'Outfit', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
  }

  .message-type-badge.type-issue {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #fca5a5;
  }

  .message-type-badge.type-recommendation {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: #86efac;
  }

  .message-type-badge.type-quote {
    background: rgba(168, 85, 247, 0.15);
    border: 1px solid rgba(168, 85, 247, 0.3);
    color: #d8b4fe;
  }

  .message-text {
    font-family: 'Outfit', sans-serif;
    font-size: 2.35rem;
    font-weight: 700;
    line-height: 1.35;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 4px 18px rgba(0, 0, 0, 0.5);
  }

  .message-text.quote-text {
    font-style: italic;
    font-weight: 500;
  }

  .message-credit {
    font-size: 0.95rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  /* 3. Fixed Bottom Case Details Container (25vh) */
  .fixed-details-container {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100vw;
    height: 25vh;
    z-index: 90;
    box-sizing: border-box;
    padding: 0 2rem 2rem 2rem;
  }

  .case-details-panel {
    position: absolute;
    inset: 0 2rem 2rem 2rem;
    display: grid;
    /* Three-column layout: 1/2 Column (Other Info), 1/4 Column (Participants), 1/4 Column (Map) */
    grid-template-columns: 2fr 1fr 1fr;
    gap: 2rem;
    padding: 1.25rem 2rem;
    border-radius: 24px;
    box-sizing: border-box;
  }

  /* Glassmorphism Panel styles */
  .glass-container-dark {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(20px) saturate(140%);
    -webkit-backdrop-filter: blur(20px) saturate(140%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
  }

  @supports not (backdrop-filter: blur(1px)) {
    .glass-container-dark {
      background: rgba(15, 23, 42, 0.95);
    }
  }

  /* Column 1: Other Info (First 1/2 Column: 50% Width) */
  .details-left {
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow-y: auto;
    scrollbar-width: none;
    padding-right: 0.5rem;
  }
  .details-left::-webkit-scrollbar {
    display: none;
  }

  .project-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 0.2rem 0;
  }

  .project-subtitle {
    font-size: 0.85rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.65);
    margin: 0 0 0.75rem 0;
    line-height: 1.35;
  }

  .methods-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .method-tag {
    font-size: 0.68rem;
    font-weight: 600;
    color: #ffffff;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 0.2rem 0.5rem;
    border-radius: 5px;
  }

  /* Column 2: Participant Info (Middle 1/4 Column: 25% Width) */
  .details-middle {
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-left: 1px solid rgba(255, 255, 255, 0.08);
    padding-left: 1.5rem;
    overflow-y: auto;
    scrollbar-width: none;
    padding-right: 0.5rem;
  }
  .details-middle::-webkit-scrollbar {
    display: none;
  }

  .recruitment-methods-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-bottom: 0.45rem;
  }

  .recruitment-tag {
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #a5b4fc;
    background: rgba(165, 180, 252, 0.1);
    border: 1px solid rgba(165, 180, 252, 0.25);
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
  }

  .stat-line {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.88rem;
    line-height: 1.35;
  }

  .stat-line.deliberation-info {
    margin-top: 0.35rem;
    margin-bottom: 0.35rem;
  }

  .stat-icon {
    font-size: 1.15rem;
    line-height: 1;
    margin-top: 0.05rem;
  }

  .stat-text strong {
    color: #cbd5e1;
  }

  .apply-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    margin-top: 0.35rem;
  }

  .apply-tag {
    font-size: 0.62rem;
    font-weight: 600;
    color: #86efac;
    background: rgba(134, 239, 172, 0.15);
    border: 1px solid rgba(134, 239, 172, 0.25);
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
  }

  /* Column 3: Leaflet Mini Map (Right 1/4 Column: 25% Width) */
  .details-right {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    border-left: 1px solid rgba(255, 255, 255, 0.08);
    padding-left: 1.5rem;
  }

  .case-mini-map {
    width: 100%;
    height: 100%;
    max-height: 130px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: #111827;
  }

  /* Navigation Controls */
  .nav-control {
    position: absolute;
    top: 36%;
    width: 3.5rem;
    height: 3.5rem;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2rem;
    cursor: pointer;
    z-index: 95;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    user-select: none;
  }

  .nav-control:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.35);
    transform: scale(1.06);
  }

  .prev-control { left: 2.5rem; }
  .next-control { right: 2.5rem; }

  /* 4. Responsive Styling */
  @media (max-width: 992px) {
    .case-details-panel {
      grid-template-columns: 1fr;
      gap: 1rem;
      padding: 1rem 1.5rem;
      overflow-y: auto;
    }
    .details-middle {
      border-left: none;
      padding-left: 0;
      padding-top: 1rem;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    .details-right {
      border-left: none;
      padding-left: 0;
      padding-top: 1rem;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      justify-content: flex-start;
    }
    .case-mini-map {
      max-height: 90px;
    }
    .fixed-details-container {
      height: 42vh;
      padding: 0 1.5rem 1.5rem 1.5rem;
    }
    .case-details-panel {
      inset: 0 1.5rem 1.5rem 1.5rem;
    }
    .slide-content-upper {
      padding-bottom: 42vh;
    }
    .message-text {
      font-size: 1.85rem;
    }
  }

  @media (max-width: 768px) {
    .top-banner {
      height: 15vh;
      flex-direction: column;
      justify-content: center;
      gap: 0.35rem;
      padding-inline: 1rem;
      padding-block: 0.5rem;
    }
    .banner-explanation {
      display: none; /* Hide explanation on phone screens to fit controls bar */
    }
    .banner-right {
      width: 100%;
      justify-content: space-between;
      gap: 0.5rem;
    }
    .controls-and-selector {
      margin-right: 0;
      flex: 1;
      justify-content: space-between;
      gap: 0.3rem;
      width: 100%;
    }
    .controls-bar {
      width: 100%;
      justify-content: space-between;
    }
    .case-select-group {
      width: 100%;
    }
    .case-select {
      width: 100%;
      max-width: none;
    }
    .progress-bar-container {
      width: auto;
      flex: 1;
    }
    .exit-btn {
      width: 1.75rem;
      height: 1.75rem;
      font-size: 0.8rem;
    }
    .slide-content-upper {
      padding-top: 16vh;
      padding-bottom: 42vh;
      padding-inline: 1rem;
    }
    .message-text {
      font-size: 1.45rem;
    }
    .fixed-details-container {
      height: 40vh;
      padding: 0 0.75rem 0.75rem 0.75rem;
    }
    .case-details-panel {
      inset: 0 0.75rem 0.75rem 0.75rem;
      padding: 0.75rem 1.25rem;
      border-radius: 18px;
    }
    .project-title {
      font-size: 1.15rem;
    }
    .stat-line {
      font-size: 0.8rem;
    }
    .nav-control {
      top: 28%;
      width: 2.75rem;
      height: 2.75rem;
      font-size: 1.6rem;
    }
    .prev-control { left: 0.5rem; }
    .next-control { right: 0.5rem; }
    .details-right {
      display: none; /* Hide map on small viewports */
    }
  }
</style>

<div class="slideshow-container" id="slideshow-container">
  <!-- Top Banner (1/10 height: 10vh) -->
  <div class="top-banner">
    <div class="banner-left">
      <span class="pave-logo">PAVE: Towards a Citizens Track on AI</span>
    </div>
    <div class="banner-middle">
      <span class="banner-explanation">Findings from participatory public engagement across the world</span>
    </div>
    <div class="banner-right">
      <!-- Stacked Controls and Dropdown Selector -->
      <div class="controls-and-selector">
        <!-- Controls Bar -->
        <div class="controls-bar">
          <button class="play-pause-btn" id="play-pause-btn" aria-label="Pause Autoplay">
            <svg class="pause-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
            </svg>
            <svg class="play-icon" viewBox="0 0 24 24" fill="currentColor" style="display: none;">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </button>

          <!-- Autoplay Speed Selector -->
          <div class="speed-control-group">
            <select id="speed-select" class="speed-select" aria-label="Autoplay Speed">
              <option value="14000">Slow (14s)</option>
              <option value="10000">Fast (10s)</option>
              <option value="7000" selected>Fastest (7s)</option>
            </select>
          </div>

          <div class="progress-bar-container">
            <div class="progress-bar-fill" id="progress-bar-fill"></div>
          </div>
          <div class="slide-counter" id="slide-counter">1 / 1</div>
        </div>

        <!-- Case Selection Dropdown (Under controls) -->
        <div class="case-select-group">
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

      <!-- Exit Button -->
      <a href="{{ '/' | relative_url }}" class="exit-btn" title="Exit Slideshow">✕</a>
    </div>
  </div>

  <!-- Slides Track -->
  <div class="slides-track" id="slides-track">
    {% assign slide_index = 0 %}
    {% assign case_index = 0 %}
    {% assign color_index = 0 %}
    
    {% for case in site.cases %}
      {% if case.messages %}
        {% for message_slug in case.messages %}
          {% assign message = site.messages | where: "slug", message_slug | first %}
          {% if message %}
            
            <!-- Slide Background Selection -->
            {% assign has_photo = false %}
            {% if case.photos-and-images and case.photos-and-images.size > 0 %}
              {% assign photo_url = case.photos-and-images.first.url | relative_url %}
              {% assign has_photo = true %}
            {% else %}
              {% assign palette_class = "bg-palette-" | append: color_index %}
              {% assign color_index = color_index | plus: 1 %}
              {% if color_index > 5 %}
                {% assign color_index = 0 %}
              {% endif %}
            {% endif %}

            <div class="slide-item {% if has_photo %}has-photo-bg{% else %}{{ palette_class }}{% endif %}" 
                 {% if has_photo %}style="background-image: url('{{ photo_url }}');"{% endif %}
                 data-slide-index="{{ slide_index }}"
                 data-case-index="{{ case_index }}">
              
              <!-- Dark Overlay for images -->
              {% if has_photo %}
              <div class="slide-overlay"></div>
              {% endif %}

              <!-- Upper 3/4: Message content -->
              <div class="slide-content-upper">
                <div class="message-wrapper">
                  <span class="message-type-badge type-{{ message.type | downcase }}">{{ message.type }}</span>
                  
                  {% if message.type == "Quote" %}
                  <blockquote class="message-text quote-text">“{{ message.title }}”</blockquote>
                  {% else %}
                  <p class="message-text">{{ message.title }}</p>
                  {% endif %}
                  
                  {% if message.additional-credit-line %}
                  <p class="message-credit">{{ message.additional-credit-line }}</p>
                  {% endif %}
                </div>
              </div>
            </div>
            {% assign slide_index = slide_index | plus: 1 %}
          {% endif %}
        {% endfor %}
        {% assign case_index = case_index | plus: 1 %}
      {% endif %}
    {% endfor %}
  </div>

  <!-- Fixed Case Details Container (positioned fixed at the bottom 25vh) -->
  <div class="fixed-details-container">
    {% assign inner_case_index = 0 %}
    {% for case in site.cases %}
      {% if case.messages %}
        
        <!-- Pre-calculate Stats & Tags in Liquid -->
        {% assign total_participants = 0 %}
        {% assign has_deliberation = false %}
        {% assign deliberating_people = 0 %}
        {% assign deliberating_hours = 0 %}
        {% assign do_apply_list = "" | split: "" %}
        {% assign recruitment_methods = "" | split: "" %}
        
        {% if case.participants %}
          {% for part_slug in case.participants %}
            {% assign participant = site.participants | where: "slug", part_slug | first %}
            {% if participant %}
              {% if participant.how-many-people-took-part %}
                {% assign num = participant.how-many-people-took-part | plus: 0 %}
                {% assign total_participants = total_participants | plus: num %}
              {% endif %}
              
              {% if participant.recruitment-method %}
                {% unless recruitment_methods contains participant.recruitment-method %}
                  {% assign recruitment_methods = recruitment_methods | push: participant.recruitment-method %}
                {% endunless %}
              {% endif %}
              
              {% assign is_delib = false %}
              {% for method in participant.which-of-the-following-methods-were-used-to %}
                {% if method == 'Deliberation' %}
                  {% assign is_delib = true %}
                {% endif %}
              {% endfor %}
              {% if is_delib %}
                {% assign has_deliberation = true %}
                {% assign p_count = participant.how-many-people-took-part | plus: 0 %}
                {% assign deliberating_people = deliberating_people | plus: p_count %}
                {% assign p_hours = participant.on-average-how-many-hours-did-each-participant | plus: 0 %}
                {% assign deliberating_hours = deliberating_hours | plus: p_hours %}
              {% endif %}
              
              {% if participant.do-any-of-the-following-apply %}
                {% for item in participant.do-any-of-the-following-apply %}
                  {% unless do_apply_list contains item %}
                    {% assign do_apply_list = do_apply_list | push: item %}
                  {% endunless %}
                {% endfor %}
              {% endif %}
            {% endif %}
          {% endfor %}
        {% endif %}

        {% assign unique_methods = "" | split: "" %}
        {% if case.participants %}
          {% for part_slug in case.participants %}
            {% assign part = site.participants | where: "slug", part_slug | first %}
            {% if part and part.which-of-the-following-methods-were-used-to %}
              {% for method in part.which-of-the-following-methods-were-used-to %}
                {% unless unique_methods contains method %}
                  {% assign unique_methods = unique_methods | push: method %}
                {% endunless %}
              {% endfor %}
            {% endif %}
          {% endfor %}
        {% endif %}

        <div class="case-details-panel glass-container-dark" id="case-panel-{{ inner_case_index }}" style="opacity: 0; pointer-events: none; transition: opacity 0.4s ease;">
          
          <!-- Column 1: Other Info (First 1/2 Column: 50% Width) -->
          <div class="details-left">
            <h2 class="project-title">{{ case.title | escape }}</h2>
            <p class="project-subtitle">Participatory engagement about {{ case.describe-the-subject-matter-in-your-own-words-one | escape }}</p>
            
            <!-- Engagement method tags -->
            {% if unique_methods.size > 0 %}
            <div class="methods-tags">
              {% for method in unique_methods %}
                <span class="method-tag">{{ method }}</span>
              {% endfor %}
            </div>
            {% endif %}
          </div>
          
          <!-- Column 2: Participant Info (Middle 1/4 Column: 25% Width) -->
          <div class="details-middle">
            <!-- Recruitment methods tags (above Overall NNN people took part) -->
            {% if recruitment_methods.size > 0 %}
            <div class="recruitment-methods-tags">
              {% for rm in recruitment_methods %}
                <span class="recruitment-tag">{{ rm }}</span>
              {% endfor %}
            </div>
            {% endif %}

            <div class="stat-line overall-participants">
              <span class="stat-icon">👥</span>
              <span class="stat-text">Overall <strong>{{ total_participants }}</strong> people took part.</span>
            </div>

            <!-- Deliberation stats and do-any-of-the-following-apply tags -->
            {% if has_deliberation %}
              <div class="stat-line deliberation-info">
                <span class="stat-icon">💭</span>
                <span class="stat-text"><strong>{{ deliberating_people }}</strong> people deliberated over <strong>{{ deliberating_hours }}</strong> hours to produce these findings.</span>
              </div>
              {% if do_apply_list.size > 0 %}
                <div class="apply-tags">
                  {% for item in do_apply_list %}
                    <span class="apply-tag">{{ item }}</span>
                  {% endfor %}
                </div>
              {% endif %}
            {% endif %}
          </div>
          
          <!-- Column 3: Leaflet Mini Map (Right 1/4 Column: 25% Width) -->
          <div class="details-right">
            <div id="case-mini-map-{{ inner_case_index }}" class="case-mini-map"></div>
          </div>
        </div>
        
        {% assign inner_case_index = inner_case_index | plus: 1 %}
      {% endif %}
    {% endfor %}
  </div>

  <!-- Next / Prev Controls -->
  <button class="nav-control prev-control" id="prev-btn" aria-label="Previous slide">‹</button>
  <button class="nav-control next-control" id="next-btn" aria-label="Next slide">›</button>
</div>

<!-- Leaflet Dynamic Maps Scripts Block -->
{% assign inner_case_index = 0 %}
{% for case in site.cases %}
  {% if case.messages %}
    <script>
      (function() {
        // Collect coordinates and titles for this case's map markers
        var markers = [
          // Lead Organisations
          {% if case.lead-organisations %}
            {% for org_slug in case.lead-organisations %}
              {% assign org = site.organisations | where: "slug", org_slug | first %}
              {% if org %}
                {% for loc_slug in org.main-location %}
                  {% assign loc = site.locations | where: "slug", loc_slug | first %}
                  {% if loc.latitude and loc.longitude %}
                    {
                      lat: {{ loc.latitude }},
                      lng: {{ loc.longitude }},
                      title: "{{ org.title | escape }} (Lead)",
                      color: "#1d4ed8",
                      radius: 7,
                      weight: 2
                    },
                  {% endif %}
                {% endfor %}
              {% endif %}
            {% endfor %}
          {% endif %}

          // Involved Organisations
          {% if case.involved-organisations %}
            {% for org_slug in case.involved-organisations %}
              {% assign org = site.organisations | where: "slug", org_slug | first %}
              {% if org %}
                {% for loc_slug in org.main-location %}
                  {% assign loc = site.locations | where: "slug", loc_slug | first %}
                  {% if loc.latitude and loc.longitude %}
                    {
                      lat: {{ loc.latitude }},
                      lng: {{ loc.longitude }},
                      title: "{{ org.title | escape }} (Involved)",
                      color: "#64748b",
                      radius: 4,
                      weight: 1
                    },
                  {% endif %}
                {% endfor %}
              {% endif %}
            {% endfor %}
          {% endif %}

          // Participants
          {% if case.participants %}
            {% for part_slug in case.participants %}
              {% assign part = site.participants | where: "slug", part_slug | first %}
              {% if part %}
                {% for loc_slug in part.locations %}
                  {% assign loc = site.locations | where: "slug", loc_slug | first %}
                  {% if loc.latitude and loc.longitude %}
                    {
                      lat: {{ loc.latitude }},
                      lng: {{ loc.longitude }},
                      title: "{{ part.title | escape }} (Participants)",
                      color: "#f97316",
                      radius: 5.5,
                      weight: 1.5
                    },
                  {% endif %}
                {% endfor %}
              {% endif %}
            {% endfor %}
          {% endif %}
        ];

        window.addEventListener('load', () => {
          const mapEl = document.getElementById('case-mini-map-{{ inner_case_index }}');
          if (mapEl && markers.length > 0) {
            var map = L.map('case-mini-map-{{ inner_case_index }}', {
              zoomControl: false,
              attributionControl: false
            }).setView([20, 0], 2);

            // Light theme CARTO basemap tiles
            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
              maxZoom: 20
            }).addTo(map);

            var bounds = L.latLngBounds();

            markers.forEach(function (m) {
              var marker = L.circleMarker([m.lat, m.lng], {
                radius: m.radius,
                fillColor: m.color,
                color: "#ffffff",
                weight: m.weight,
                opacity: 1,
                fillOpacity: 0.85
              }).addTo(map);

              marker.bindPopup("<strong style='font-family:Plus Jakarta Sans, sans-serif; font-size:11px;'>" + m.title + "</strong>");
              bounds.extend([m.lat, m.lng]);
            });

            // Adjust size and bounds center
            setTimeout(function () {
              map.invalidateSize();
              map.fitBounds(bounds, { padding: [15, 15], maxZoom: 10 });
            }, 200);

            // Cache map reference to allow dynamic resize triggers
            if (!window.caseMaps) window.caseMaps = {};
            window.caseMaps[{{ inner_case_index }}] = map;
          } else if (mapEl) {
            // Remove maps frame if empty
            mapEl.parentNode.style.display = 'none';
          }
        });
      })();
    </script>
    {% assign inner_case_index = inner_case_index | plus: 1 %}
  {% endif %}
{% endfor %}

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
  let slideDuration = parseInt(speedSelect.value); // Read value from speedSelect
  let lastTime = 0;
  let progress = 0;
  let animationFrameId = null;
  let isPlaying = true;
  let activeCaseIndex = -1;

  // Initialize Counter display
  slideCounter.innerText = `1 / ${totalSlides}`;

  function updateCasePanel(caseIndex) {
    // Sync the case dropdown value
    if (caseSelect) {
      caseSelect.value = caseIndex;
    }

    if (activeCaseIndex === caseIndex) return; // Case didn't change, panel stays completely fixed!
    activeCaseIndex = caseIndex;

    const panels = document.querySelectorAll('.case-details-panel');
    panels.forEach((panel, idx) => {
      if (idx === caseIndex) {
        panel.style.opacity = '1';
        panel.style.pointerEvents = 'auto';
        
        // Trigger invalidateSize to draw leaflet map perfectly
        if (window.caseMaps && window.caseMaps[caseIndex]) {
          setTimeout(() => {
            window.caseMaps[caseIndex].invalidateSize();
          }, 80);
        }
      } else {
        panel.style.opacity = '0';
        panel.style.pointerEvents = 'none';
      }
    });
  }

  function goToSlide(index) {
    currentIndex = index;
    if (currentIndex >= totalSlides) currentIndex = 0;
    if (currentIndex < 0) currentIndex = totalSlides - 1;
    
    // Transition slides track horizontally
    track.style.transform = `translateX(-${currentIndex * 100}vw)`;
    slideCounter.innerText = `${currentIndex + 1} / ${totalSlides}`;
    
    // Update case info panel (stays fixed if caseIndex is the same)
    const activeSlide = slides[currentIndex];
    const caseIndex = parseInt(activeSlide.dataset.caseIndex);
    updateCasePanel(caseIndex);

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

  // Initialize the first panel display
  if (slides[0]) {
    const initialCaseIndex = parseInt(slides[0].dataset.caseIndex);
    updateCasePanel(initialCaseIndex);
  }
});
</script>
