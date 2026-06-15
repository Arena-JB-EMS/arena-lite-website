/**
 * ARENA SITE CONFIG LOADER v1.0.0
 * S104 — 2026-06-15
 *
 * Fetches dynamic config from ARENA_SITE_CONFIG GAS Web App
 * and injects values into the DOM via data attributes.
 *
 * HOW IT WORKS:
 *   1. On DOMContentLoaded, fetches JSON from ARENA_CONFIG_URL
 *   2. For each element with data-config="key":
 *      → Sets element.textContent to config[key]
 *   3. For each element with data-config-href-key="key":
 *      → Looks for companion data-config-href-prefix attribute
 *      → Sets href to `${prefix}${config[key]}`
 *   4. If a key is missing from config, element is hidden (display:none)
 *   5. If the fetch fails entirely, ALL config-dependent elements are hidden
 *
 * SETUP AFTER GAS DEPLOYMENT:
 *   Replace 'PASTE_GAS_DEPLOYMENT_URL_HERE' below with your /exec URL.
 *   That URL is stable — it only changes if you create a new deployment.
 *
 * HTML USAGE:
 *
 *   Plain text injection:
 *     <span data-config="phone">01618702916</span>
 *
 *   Link with dynamic href + text:
 *     <a href="tel:01618702916"
 *        data-config="phone"
 *        data-config-href-prefix="tel:"
 *        data-config-href-key="phone">01618702916</a>
 *
 *   Email link (text = email address, href = mailto:email):
 *     <a href="mailto:j.baguley@thearenahub.co.uk"
 *        data-config="email_dpo"
 *        data-config-href-prefix="mailto:"
 *        data-config-href-key="email_dpo">j.baguley@thearenahub.co.uk</a>
 *
 *   Social link (href only, no text change):
 *     <a href="https://linkedin.com/company/the-arena-hub"
 *        data-config-href-prefix=""
 *        data-config-href-key="social_linkedin">LinkedIn</a>
 *
 * AVAILABLE CONFIG KEYS (managed in ARENA_SITE_CONFIG sheet):
 *   CONTACT: phone, email_dpo, email_pilot, email_sales, email_support,
 *            email_compliance, email_schools, email_safeguarding,
 *            email_data_protection, email_info, email_scn
 *   LEGAL:   company_name, company_number, duns_number, director_name,
 *            director_title, dpa_reference
 *   PRICING: pilot_price, pilot_duration
 *   SOCIAL:  social_linkedin, social_facebook, social_instagram, social_substack
 */

(function () {
  'use strict';

  // ── CONFIGURATION ──────────────────────────────────────────────────────────
  var ARENA_CONFIG_URL = 'https://script.google.com/macros/s/AKfycbxphfIOhEweH4m3WeF8lAVffSPbAB9uUXH-1t0qfYnWPV_G9NHxdbCrcMZHLm6gXROabA/exec';
  // ────────────────────────────────────────────────────────────────────────────

  var ATTR_TEXT       = 'data-config';
  var ATTR_HREF       = 'data-config-href-key';
  var ATTR_PREFIX     = 'data-config-href-prefix';
  var ATTR_EMAIL_SWAP = 'data-config-href-email-key'; // swaps only email in mailto:email?subject=...

  /**
   * Main entry — called after DOM is ready.
   */
  function init() {
    if (!ARENA_CONFIG_URL || ARENA_CONFIG_URL === 'PASTE_GAS_DEPLOYMENT_URL_HERE') {
      console.warn('[ArenaConfig] No config URL set. Keeping static fallback values visible.');
      return;
    }

    fetch(ARENA_CONFIG_URL)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (payload) {
        if (!payload.ok || !payload.config) throw new Error('Invalid payload');
        applyConfig(payload.config);
      })
      .catch(function (err) {
        console.warn('[ArenaConfig] Fetch failed — hiding config-dependent elements.', err.message);
        hideAll();
      });
  }

  /**
   * Walk the DOM and inject config values.
   */
  function applyConfig(cfg) {
    // Text injection — elements with data-config="key"
    var textEls = document.querySelectorAll('[' + ATTR_TEXT + ']');
    for (var i = 0; i < textEls.length; i++) {
      var el  = textEls[i];
      var key = el.getAttribute(ATTR_TEXT);
      if (cfg.hasOwnProperty(key)) {
        el.textContent = cfg[key];
      } else {
        el.style.display = 'none';
      }
    }

    // Href injection — elements with data-config-href-key="key"
    var hrefEls = document.querySelectorAll('[' + ATTR_HREF + ']');
    for (var j = 0; j < hrefEls.length; j++) {
      var hEl    = hrefEls[j];
      var hKey   = hEl.getAttribute(ATTR_HREF);
      var prefix = hEl.getAttribute(ATTR_PREFIX) || '';
      if (cfg.hasOwnProperty(hKey)) {
        hEl.setAttribute('href', prefix + cfg[hKey]);
      } else {
        hEl.style.display = 'none';
      }
    }

    // Email-swap injection — elements with data-config-href-email-key="key"
    // Replaces only the email address portion of an existing mailto: href,
    // preserving any ?subject=... query parameters.
    var emailSwapEls = document.querySelectorAll('[' + ATTR_EMAIL_SWAP + ']');
    for (var k = 0; k < emailSwapEls.length; k++) {
      var eEl  = emailSwapEls[k];
      var eKey = eEl.getAttribute(ATTR_EMAIL_SWAP);
      if (cfg.hasOwnProperty(eKey)) {
        var existing = eEl.getAttribute('href') || '';
        var updated  = existing.replace(/mailto:[^?#]*/i, 'mailto:' + cfg[