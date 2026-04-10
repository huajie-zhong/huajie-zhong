#!/usr/bin/env python3
"""Generate styled SVG 'Track of the Day' cards (dark + light) for the GitHub profile README."""

import json
import random
import hashlib
from datetime import datetime, timezone
from pathlib import Path

TRACKS_FILE = Path(__file__).parent / "tracks.json"
OUTPUT_DIR = Path(__file__).parent

PALETTES = {
    "dark": [
        {"bg1": "#0e1118", "bg2": "#131a24", "accent": "#7b9ed4", "accent2": "#a89cc8", "text": "#e4e0ec", "sub": "#7882a0", "glow": "#92b4e0"},
        {"bg1": "#0e1118", "bg2": "#151c28", "accent": "#92b4e0", "accent2": "#7b9ed4", "text": "#e4e0ec", "sub": "#7882a0", "glow": "#a89cc8"},
        {"bg1": "#0f1220", "bg2": "#131a24", "accent": "#a89cc8", "accent2": "#92b4e0", "text": "#e4e0ec", "sub": "#7882a0", "glow": "#7b9ed4"},
    ],
    "light": [
        {"bg1": "#f6f2ee", "bg2": "#eee8e2", "accent": "#5a7caa", "accent2": "#8070a0", "text": "#2a2a3a", "sub": "#6a6a80", "glow": "#5a7caa"},
        {"bg1": "#f4f0ec", "bg2": "#ede7e0", "accent": "#8070a0", "accent2": "#5a7caa", "text": "#2a2a3a", "sub": "#6a6a80", "glow": "#8070a0"},
        {"bg1": "#f6f2ee", "bg2": "#eee8e2", "accent": "#6a88b0", "accent2": "#7868a0", "text": "#2a2a3a", "sub": "#6a6a80", "glow": "#6a88b0"},
    ],
}


def get_daily_seed():
    """Use today's date as seed for deterministic daily randomness."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return int(hashlib.md5(today.encode()).hexdigest(), 16)


def generate_waveform_bars(count=32, seed=0):
    """Generate random waveform bar heights."""
    rng = random.Random(seed)
    bars = []
    for i in range(count):
        base = rng.random()
        height = 8 + base * 24
        bars.append(round(height, 1))
    return bars


def escape_xml(text):
    """Escape special XML characters."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def generate_svg(track, palette, seed):
    """Generate the jukebox SVG card."""
    title = escape_xml(track["title"])
    artist = escape_xml(track["artist"])
    bars = generate_waveform_bars(40, seed)
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")

    display_title = title if len(title) <= 35 else title[:32] + "..."
    display_artist = artist if len(artist) <= 45 else artist[:42] + "..."

    bar_svg = ""
    bar_width = 8
    bar_gap = 3
    total_bars = 40
    waveform_width = total_bars * (bar_width + bar_gap)
    waveform_x = (480 - waveform_width) / 2

    for i, h in enumerate(bars):
        x = waveform_x + i * (bar_width + bar_gap)
        y = 135 - h / 2
        opacity = 0.5 + (h / 32) * 0.5
        delay = i * 0.08
        bar_svg += f'''    <rect x="{x}" y="{y}" width="{bar_width}" height="{h}" rx="4" fill="{palette['accent']}" opacity="{opacity:.2f}">
      <animate attributeName="height" values="{h};{h*0.4};{h*1.2};{h*0.6};{h}" dur="{1.5 + (i % 5) * 0.3}s" repeatCount="indefinite" begin="{delay}s"/>
      <animate attributeName="y" values="{y};{135 - h*0.2};{135 - h*0.6};{135 - h*0.3};{y}" dur="{1.5 + (i % 5) * 0.3}s" repeatCount="indefinite" begin="{delay}s"/>
    </rect>
'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="240" viewBox="0 0 480 240">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{palette['bg1']}" />
      <stop offset="100%" style="stop-color:{palette['bg2']}" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{palette['accent2']}" />
      <stop offset="100%" style="stop-color:{palette['accent']}" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="480" height="240" rx="16" fill="url(#bg)" />
  <rect width="480" height="240" rx="16" fill="none" stroke="{palette['accent']}" stroke-opacity="0.15" stroke-width="1" />

  <!-- Vinyl disc icon -->
  <g>
    <circle cx="44" cy="42" r="18" fill="none" stroke="{palette['accent']}" stroke-opacity="0.3" stroke-width="1.5"/>
    <circle cx="44" cy="42" r="10" fill="none" stroke="{palette['accent']}" stroke-opacity="0.2" stroke-width="1"/>
    <circle cx="44" cy="42" r="3" fill="{palette['accent']}" opacity="0.5"/>
    <animateTransform attributeName="transform" type="rotate" from="0 44 42" to="360 44 42" dur="4s" repeatCount="indefinite"/>
  </g>

  <!-- Header -->
  <text x="72" y="38" font-family="'Segoe UI', 'SF Pro Display', -apple-system, sans-serif" font-size="11" font-weight="600" fill="{palette['sub']}" letter-spacing="3" text-transform="uppercase">TRACK OF THE DAY</text>
  <text x="72" y="54" font-family="'Segoe UI', sans-serif" font-size="10" fill="{palette['sub']}" opacity="0.5">{today}</text>

  <!-- Divider line -->
  <line x1="24" y1="68" x2="456" y2="68" stroke="url(#accentGrad)" stroke-opacity="0.2" stroke-width="1"/>

  <!-- Waveform visualizer -->
  <g filter="url(#glow)" opacity="0.9">
{bar_svg}  </g>

  <!-- Track info -->
  <text x="240" y="178" font-family="'Segoe UI', 'SF Pro Display', -apple-system, sans-serif" font-size="16" font-weight="700" fill="{palette['text']}" text-anchor="middle" letter-spacing="0.5">{display_title}</text>
  <text x="240" y="198" font-family="'Segoe UI', sans-serif" font-size="12" fill="{palette['sub']}" text-anchor="middle">{display_artist}</text>

  <!-- Bottom accent line -->
  <rect x="180" y="214" width="120" height="2" rx="1" fill="url(#accentGrad)" opacity="0.4"/>

</svg>'''

    return svg


def main():
    with open(TRACKS_FILE, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    seed = get_daily_seed()
    rng = random.Random(seed)

    track = rng.choice(tracks)

    for theme in ("dark", "light"):
        palette = random.Random(seed).choice(PALETTES[theme])
        svg = generate_svg(track, palette, seed)
        output_file = OUTPUT_DIR / f"jukebox-{theme}.svg"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated jukebox-{theme}.svg: {track['title']} by {track['artist']}")


if __name__ == "__main__":
    main()
