---
layout: page
title: Cases
permalink: /cases/
---

<div class="cases-index">
  {% assign sorted_cases = site.cases | sort: "title" %}
  {% for case in sorted_cases %}
    <article class="case-entry" style="margin-bottom: 2rem; border-bottom: 1px solid #eee; padding-bottom: 1.5rem;">
      <header>
        <h2 style="margin-bottom: 0.5rem;">
          <a href="{{ case.url | relative_url }}">{{ case.title | escape }}</a>
        </h2>
        <p class="case-meta" style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">
          {% if case.fldKttntgUGpSigJs %}
            {{ case.fldKttntgUGpSigJs }}
            {% if case.fldwgrONWjl5apN0a %} - {{ case.fldwgrONWjl5apN0a }}{% endif %}
          {% endif %}
        </p>
      </header>

      {% if case.fld0oykyuwbVPbW0H %}
        <div class="case-description">
          {{ case.fld0oykyuwbVPbW0H | truncatewords: 50 | newline_to_br }}
        </div>
      {% endif %}

      <p style="margin-top: 1rem;">
        <a href="{{ case.url | relative_url }}" class="btn">Read more &rarr;</a>
      </p>
    </article>
  {% endfor %}
</div>
