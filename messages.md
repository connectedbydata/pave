---
layout: default
title: Messages
permalink: /messages/
subtitle: Public voice, values and recommendations on AI governance
menus: [header]
---

<style>
  /* Presentation CTA Card */
  .messages-cta-card {
    background: linear-gradient(135deg, #496a40 0%, #2e4728 100%);
    color: #ffffff;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 10px 30px -10px rgba(73, 106, 64, 0.3);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    position: relative;
    overflow: hidden;
  }

  .messages-cta-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0) 70%);
    border-radius: 50%;
    pointer-events: none;
  }

  .messages-cta-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 35px -10px rgba(73, 106, 64, 0.4);
  }

  .messages-cta-content {
    max-width: 65%;
    z-index: 5;
  }

  .messages-cta-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    color: #ffffff !important;
  }

  .messages-cta-desc {
    font-size: 1rem;
    line-height: 1.5;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .messages-cta-action {
    flex-shrink: 0;
    z-index: 5;
  }

  .btn-launch-presentation {
    display: inline-flex;
    align-items: center;
    gap: 0.65rem;
    background-color: #ffffff;
    color: #496a40 !important;
    font-weight: 700;
    padding: 0.85rem 1.75rem;
    border-radius: 9999px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
    text-decoration: none !important;
  }

  .btn-launch-presentation:hover {
    background-color: #f3f7f2;
    transform: scale(1.03);
    text-decoration: none !important;
  }

  /* Grid layout for message sections */
  .messages-grid {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    margin-top: 2rem;
  }

  .messages-case-card {
    background-color: #ffffff;
    border: 1px solid rgba(73, 106, 64, 0.1);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(73, 106, 64, 0.03);
    transition: border-color 0.2s ease;
  }

  .messages-case-card:hover {
    border-color: rgba(73, 106, 64, 0.25);
  }

  .messages-case-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(73, 106, 64, 0.1);
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
  }

  .messages-case-title {
    font-size: 1.35rem;
    margin: 0;
    font-weight: 700;
  }

  .messages-case-title a {
    color: #1a2f16;
  }

  .messages-case-title a:hover {
    color: #496a40;
    text-decoration: none;
  }

  .messages-count-badge {
    font-size: 0.8rem;
    font-weight: 600;
    color: #496a40;
    background-color: #f3f7f2;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    border: 1px solid rgba(73, 106, 64, 0.15);
  }

  .messages-quotes-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .message-quote-item {
    position: relative;
    padding-left: 1.5rem;
    border-left: 3px solid rgba(73, 106, 64, 0.2);
  }

  .message-quote-body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.05rem;
    line-height: 1.6;
    color: #243f1f;
    margin: 0 0 0.5rem 0;
    font-style: italic;
    font-weight: 500;
  }

  .message-quote-meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .message-type-tag {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    letter-spacing: 0.03em;
    border: 1px solid transparent;
  }

  .message-type-tag.issue {
    background-color: #fef3c7;
    color: #b45309;
    border-color: #fde68a;
  }

  .message-type-tag.recommendation {
    background-color: #d1fae5;
    color: #065f46;
    border-color: #a7f3d0;
  }

  .message-type-tag.quote {
    background-color: #e0e7ff;
    color: #3730a3;
    border-color: #c7d2fe;
  }

  .message-credit {
    font-size: 0.85rem;
    color: #556c50;
    font-weight: 500;
  }

  @media (max-width: 768px) {
    .messages-cta-card {
      flex-direction: column;
      align-items: stretch;
      gap: 1.5rem;
      padding: 1.5rem;
    }
    .messages-cta-content {
      max-width: 100%;
    }
    .btn-launch-presentation {
      justify-content: center;
      width: 100%;
    }
    .messages-case-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
  }
</style>

<div class="page-body-container">
  <div class="wrapper">
    <p>
      The PAVE Case Book gathers messages, values, and recommendations voiced by members of the public, citizens assemblies, and civil society groups during participatory AI engagement projects. These messages highlight the hopes, concerns, and principles that communities wish to see applied to AI systems and their governance.
    </p>

    <!-- Presentation CTA Card -->
    <div class="messages-cta-card">
      <div class="messages-cta-content">
        <h2 class="messages-cta-title">Interactive Presentation Mode</h2>
        <p class="messages-cta-desc">
          Launch the fullscreen, autoplaying slideshow of messages. Designed for presentation displays, projectors, or focused reading.
        </p>
      </div>
      <div class="messages-cta-action">
        <a href="{{ '/messages/run/' | relative_url }}" class="btn-launch-presentation">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8 5v14l11-7z"/>
          </svg>
          <span>Launch Presentation</span>
        </a>
      </div>
    </div>

    <!-- Messages List Grouped by Case Study -->
    <h2 style="font-family: 'Outfit', sans-serif; font-weight: 700; margin-top: 2rem;">Messages by Case Study</h2>

    <div class="messages-grid">
      {% assign sorted_cases = site.cases | sort: "title" %}
      {% for case in sorted_cases %}
        {% if case.messages and case.messages.size > 0 %}
          <div class="messages-case-card">
            <div class="messages-case-header">
              <h3 class="messages-case-title">
                <a href="{{ case.url | relative_url }}">{{ case.title | escape }}</a>
              </h3>
              <span class="messages-count-badge">{{ case.messages.size }} message{% if case.messages.size > 1 %}s{% endif %}</span>
            </div>
            
            <div class="messages-quotes-list">
              {% for msg_slug in case.messages %}
                {% assign message = site.messages | where: "slug", msg_slug | first %}
                {% if message %}
                  <div class="message-quote-item">
                    <blockquote class="message-quote-body">
                      “{{ message.title }}”
                    </blockquote>
                    <div class="message-quote-meta">
                      <span class="message-type-tag {{ message.type | downcase }}">{{ message.type }}</span>
                      {% if message.additional-credit-line %}
                        <span class="message-credit">— {{ message.additional-credit-line }}</span>
                      {% endif %}
                    </div>
                  </div>
                {% endif %}
              {% endfor %}
            </div>
          </div>
        {% endif %}
      {% endfor %}
    </div>
  </div>
</div>
