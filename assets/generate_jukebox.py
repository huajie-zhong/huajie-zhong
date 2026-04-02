#!/usr/bin/env python3
"""Generate a styled SVG 'Track of the Day' card for the GitHub profile README."""

import json
import random
import hashlib
from datetime import datetime, timezone
from pathlib import Path

TRACKS_FILE = Path(__file__).parent / "tracks.json"
OUTPUT_FILE = Path(__file__).parent / "jukebox.svg"

# Color palette — anime game inspired gradients
PALETTES = [
    {"bg1": "#08090e", "bg2": "#0c0f1a", "accent": "#5a7ab0", "accent2": "#3d5a8a", "text": "#d0d8e8", "sub": "#6078a0", "glow": "#4a6a9a"},
    {"bg1": "#0a0c14", "bg2": "#0e1220", "accent": "#8098c0", "accent2": "#5a7ab0", "text": "#d8dde8", "sub": "#5a6a88", "glow": "#6888b0"},
    {"bg1": "#090b12", "bg2": "#0d1018", "accent": "#a0b4d0", "accent2": "#7898c0", "text": "#d0d8e8", "sub": "#4a6080", "glow": "#8098c0"},
    {"bg1": "#080a10", "bg2": "#0c101c", "accent": "#6888b0", "accent2": "#4a6a9a", "text": "#c8d0e0", "sub": "#5a7090", "glow": "#5a7ab0"},
    {"bg1": "#0a0d16", "bg2": "#0e1220", "accent": "#90a8c8", "accent2": "#6888b0", "text": "#d4dae6", "sub": "#5a6a88", "glow": "#7898c0"},
]


def get_daily_seed():
    """Use today's date as seed for deterministic daily randomness."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return int(hashlib.md5(today.encode()).hexdigest(), 16)


def generate_waveform_bars(count=32, seed=0):
    """Generate random waveform bar heights."""
    rng = random.Random(seed)
    bars = []
    for i in range(count):
        # Create a natural-looking waveform with peaks and valleys
        base = rng.random()
        # Add some structure — peaks tend to cluster
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

    # Truncate long titles/artists for display
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
    palette = rng.choice(PALETTES)

    svg = generate_svg(track, palette, seed)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Generated jukebox card: {track['title']} by {track['artist']}")


if __name__ == "__main__":
    main()
