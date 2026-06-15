#!/usr/bin/env python3
"""
patch_html_config_lite.py — S104 — 2026-06-15
Injects arena-config.js data attributes into Arena Lite website HTML files.

Run from the arena-lite-com/ directory:
    python3 patch_html_config_lite.py

Uses the same GAS endpoint and arena-config.js as the main site.
New keys used here: email_legal, email_hello (added to sheet via addMissingKeys())
"""

import shutil
import sys
from pathlib import Path

BASE    = Path(__file__).parent
DRY_RUN = '--dry-run' in sys.argv

SCRIPT_TAG    = '<script src="arena-config.js"></script>'
SCRIPT_MARKER = 'src="arena-config.js"'

TARGET_PAGES = ['dpa.html', 'privacy.html', 'terms.html', 'login.html', 'success.html']

def patch(filepath, replacements):
    p = Path(filepath)
    if not p.exists():
        print(f"  SKIP (not found): {p.name}")
        return
    original = p.read_text(encoding='utf-8')
    content  = original
    for old, new in replacements:
        if old not in content:
            print(f"  WARN [{p.name}]: not found — '{old[:70].strip()}'")
            continue
        count   = content.count(old)
        content = content.replace(old, new)
        print(f"  OK   [{p.name}]: {count}x — '{old[:70].strip()}'")
    if content == original:
        print(f"  INFO [{p.name}]: no changes")
        return
    if not DRY_RUN:
        shutil.copy2(p, p.with_suffix(p.suffix + '.bak'))
        p.write_text(content, encoding='utf-8')
        print(f"  SAVED: {p.name}")
    else:
        print(f"  DRY-RUN: {p.name}")


print("\n=== STEP 1: Injecting arena-config.js script tag ===")
for fname in TARGET_PAGES:
    p = BASE / fname
    if not p.exists():
        print(f"  SKIP: {fname}")
        continue
    content = p.read_text(encoding='utf-8')
    if SCRIPT_MARKER in content:
        print(f"  ALREADY PRESENT: {fname}")
        continue
    if '</body>' not in content:
        print(f"  WARN: no </body> in {fname}")
        continue
    new_content = content.replace('</body>', f'  {SCRIPT_TAG}\n</body>', 1)
    if not DRY_RUN:
        shutil.copy2(p, p.with_suffix('.html.bak'))
        p.write_text(new_content, encoding='utf-8')
        print(f"  INJECTED: {fname}")
    else:
        print(f"  DRY-RUN: {fname}")


print("\n=== STEP 2: Injecting data-config attributes ===")

# ─── dpa.html ────────────────────────────────────────────────────────────────
print("\n[dpa.html]")
patch(BASE / 'dpa.html', [

    # Signatory block — Company No + DUNS + Email
    (
        'Company No. CH#1708605<br>\n      D-U-N-S: 234652645<br>\n      Email: <a href="mailto:compliance@thearenahub.co.uk">compliance@thearenahub.co.uk</a></p>',
        'Company No. CH#<span data-config="company_number">1708605</span><br>\n      D-U-N-S: <span data-config="duns_number">234652645</span><br>\n      Email: <a href="mailto:compliance@thearenahub.co.uk" data-config="email_compliance" data-config-href-prefix="mailto:" data-config-href-key="email_compliance">compliance@thearenahub.co.uk</a></p>'
    ),

    # Inline compliance email (DPIA available from)
    (
        '<a href="mailto:compliance@thearenahub.co.uk">compliance@thearenahub.co.uk</a>)</p>',
        '<a href="mailto:compliance@thearenahub.co.uk" data-config="email_compliance" data-config-href-prefix="mailto:" data-config-href-key="email_compliance">compliance@thearenahub.co.uk</a>)</p>'
    ),

    # developmentMode paragraph compliance email
    (
        '(contactable at <a href="mailto:compliance@thearenahub.co.uk">compliance@thearenahub.co.uk</a>)',
        '(contactable at <a href="mailto:compliance@thearenahub.co.uk" data-config="email_compliance" data-config-href-prefix="mailto:" data-config-href-key="email_compliance">compliance@thearenahub.co.uk</a>)'
    ),

    # Signatory footer block
    (
        '<strong>The Arena Hub Ltd</strong> &nbsp;·&nbsp; CH#1708605 &nbsp;·&nbsp; Registered in England &amp; Wales</p>\n  <p>Email: <a href="mailto:compliance@thearenahub.co.uk">compliance@thearenahub.co.uk</a></p>\n  <p>Tel: <a href="tel:01618702916">01618702916</a></p>',
        '<strong><span data-config="company_name">The Arena Hub Ltd</span></strong> &nbsp;·&nbsp; CH#<span data-config="company_number">1708605</span> &nbsp;·&nbsp; Registered in England &amp; Wales</p>\n  <p>Email: <a href="mailto:compliance@thearenahub.co.uk" data-config="email_compliance" data-config-href-prefix="mailto:" data-config-href-key="email_compliance">compliance@thearenahub.co.uk</a></p>\n  <p>Tel: <a href="tel:01618702916" data-config="phone" data-config-href-prefix="tel:" data-config-href-key="phone">01618702916</a></p>'
    ),

    # Footer copyright
    (
        '&copy; 2026 The Arena Hub Ltd. All rights reserved. Registered in England and Wales. CH#1708605',
        '&copy; 2026 <span data-config="company_name">The Arena Hub Ltd</span>. All rights reserved. Registered in England and Wales. CH#<span data-config="company_number">1708605</span>'
    ),
])


# ─── privacy.html ─────────────────────────────────────────────────────────────
print("\n[privacy.html]")
patch(BASE / 'privacy.html', [

    # Intro — company number + phone + data-protection email
    (
        'Company No. CH#1708605. Tel: <a href="tel:01618702916">01618702916</a>. Our contact address for all data-related matters is <strong><a href="mailto:data-protection@thearenahub.co.uk">data-protection@thearenahub.co.uk</a></strong>.',
        'Company No. CH#<span data-config="company_number">1708605</span>. Tel: <a href="tel:01618702916" data-config="phone" data-config-href-prefix="tel:" data-config-href-key="phone">01618702916</a>. Our contact address for all data-related matters is <strong><a href="mailto:data-protection@thearenahub.co.uk" data-config="email_data_protection" data-config-href-prefix="mailto:" data-config-href-key="email_data_protection">data-protection@thearenahub.co.uk</a></strong>.'
    ),

    # Retention deletion request email
    (
        '<a href="mailto:data-protection@thearenahub.co.uk">data-protection@thearenahub.co.uk</a>. We will respond within 30 days.',
        '<a href="mailto:data-protection@thearenahub.co.uk" data-config="email_data_protection" data-config-href-prefix="mailto:" data-config-href-key="email_data_protection">data-protection@thearenahub.co.uk</a>. We will respond within 30 days.'
    ),

    # Rights email
    (
        '<a href="mailto:data-protection@thearenahub.co.uk">data-protection@thearenahub.co.uk</a>. We will respond within 30 days. If you are dissatisfied',
        '<a href="mailto:data-protection@thearenahub.co.uk" data-config="email_data_protection" data-config-href-prefix="mailto:" data-config-href-key="email_data_protection">data-protection@thearenahub.co.uk</a>. We will respond within 30 days. If you are dissatisfied'
    ),

    # Contact block email
    (
        'Email: <a href="mailto:data-protection@thearenahub.co.uk">data-protection@thearenahub.co.uk</a></p>',
        'Email: <a href="mailto:data-protection@thearenahub.co.uk" data-config="email_data_protection" data-config-href-prefix="mailto:" data-config-href-key="email_data_protection">data-protection@thearenahub.co.uk</a></p>'
    ),

    # Footer last-updated line
    (
        'The Arena Hub Ltd &nbsp;&bull;&nbsp; CH#1708605',
        '<span data-config="company_name">The Arena Hub Ltd</span> &nbsp;&bull;&nbsp; CH#<span data-config="company_number">1708605</span>'
    ),
])


# ─── terms.html ───────────────────────────────────────────────────────────────
print("\n[terms.html]")
patch(BASE / 'terms.html', [

    # Multi-seat legal email
    (
        '<a href="mailto:legal@thearenahub.co.uk">legal@thearenahub.co.uk</a> to discuss multi-seat arrangements.',
        '<a href="mailto:legal@thearenahub.co.uk" data-config="email_legal" data-config-href-prefix="mailto:" data-config-href-key="email_legal">legal@thearenahub.co.uk</a> to discuss multi-seat arrangements.'
    ),

    # Cancellation email
    (
        '<a href="mailto:legal@thearenahub.co.uk">legal@thearenahub.co.uk</a>. Cancellation takes effect',
        '<a href="mailto:legal@thearenahub.co.uk" data-config="email_legal" data-config-href-prefix="mailto:" data-config-href-key="email_legal">legal@thearenahub.co.uk</a>. Cancellation takes effect'
    ),

    # Contact block email
    (
        'Email: <a href="mailto:legal@thearenahub.co.uk">legal@thearenahub.co.uk</a></p>',
        'Email: <a href="mailto:legal@thearenahub.co.uk" data-config="email_legal" data-config-href-prefix="mailto:" data-config-href-key="email_legal">legal@thearenahub.co.uk</a></p>'
    ),

    # Company number in footer
    (
        'CH#1708605',
        'CH#<span data-config="company_number">1708605</span>'
    ),
])


# ─── login.html ───────────────────────────────────────────────────────────────
print("\n[login.html]")
patch(BASE / 'login.html', [
    (
        '<a href="mailto:support@thearenahub.co.uk">support@thearenahub.co.uk</a>',
        '<a href="mailto:support@thearenahub.co.uk" data-config="email_support" data-config-href-prefix="mailto:" data-config-href-key="email_support">support@thearenahub.co.uk</a>'
    ),
])


# ─── success.html ─────────────────────────────────────────────────────────────
print("\n[success.html]")
patch(BASE / 'success.html', [
    (
        '<a href="mailto:support@thearenahub.co.uk">support@thearenahub.co.uk</a>',
        '<a href="mailto:support@thearenahub.co.uk" data-config="email_support" data-config-href-prefix="mailto:" data-config-href-key="email_support">support@thearenahub.co.uk</a>'
    ),
])


print("\n=== LITE PATCH COMPLETE ===")
print("Next: run addMissingKeys() in GAS editor to add email_legal + email_hello to live sheet.")
print("Then commit arena-lite-com/ folder to Arena-JB-EMS repo.")
