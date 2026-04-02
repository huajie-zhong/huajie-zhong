#!/usr/bin/env python3
"""Generate a styled SVG tracklist for the GitHub profile README."""

from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "tracklist.svg"

TRACKS = [
    {"num": "01", "title": "Perfect Match", "desc": "matchmaking for Cornell students", "status": "released", "url": "https://github.com/Perfect-Match-Org/perfect-match-web"},
    {"num": "02", "title": "EzModel", "desc": "visual DB schema + CRUD API gen", "status": "released", "url": "https://github.com/Bug-Bugger/EzModel"},
    {"num": "03", "title": "Tabime", "desc": "plan hangouts, effortlessly", "status": "released", "url": "https://github.com/Bug-Bugger/Tabime"},
    {"num": "04", "title": "CuffedOrNot", "desc": "the relationship quiz", "status": "released", "url": "https://github.com/Perfect-Match-Org/cuffedornot"},
    {"num": "05", "title": "Campus Meal Pick", "desc": "AI-powered eatery suggestions", "status": "released", "url": "https://github.com/Shengle-Dai/Campus-Meal-Pick"},
    {"num": "06", "title": "Escoffier", "desc": "a cooking companion app", "status": "recording", "url": ""},
]


def generate_tracklist():
    row_height = 52
    padding_top = 65
    total_height = padding_top + len(TRACKS) * row_height + 40

    rows_svg = ""
    for i, track in enumerate(TRACKS):
        y = padding_top + i * row_height
        is_recording = track["status"] == "recording"

        # Alternating subtle row background
        if i % 2 == 0:
            rows_svg += f'  <rect x="0" y="{y}" width="700" height="{row_height}" fill="#3d5a8a" opacity="0.04"/>\n'

        # Left accent bar
        accent_color = "#c0392b" if is_recording else "#5a7ab0"
        rows_svg += f'  <rect x="0" y="{y}" width="3" height="{row_height}" fill="{accent_color}" opacity="0.5" rx="1"/>\n'

        # Track number
        num_opacity = "0.3" if is_recording else "0.45"
        rows_svg += f'  <text x="28" y="{y + 32}" font-family="\'Fira Code\', \'Cascadia Code\', monospace" font-size="13" fill="#5a7ab0" opacity="{num_opacity}" text-anchor="middle">{track["num"]}</text>\n'

        # Track title
        title_color = "#d0d8e8" if not is_recording else "#b0b8c8"
        rows_svg += f'  <text x="55" y="{y + 30}" font-family="\'Segoe UI\', \'SF Pro Display\', -apple-system, sans-serif" font-size="15" font-weight="600" fill="{title_color}">{track["title"]}</text>\n'

        # Dotted line connecting title to description
        title_approx_width = len(track["title"]) * 9 + 55
        dot_start = title_approx_width + 10
        dot_end = 430
        if dot_start < dot_end:
            rows_svg += f'  <line x1="{dot_start}" y1="{y + 27}" x2="{dot_end}" y2="{y + 27}" stroke="#2a3a5c" stroke-width="1" stroke-dasharray="2,6" opacity="0.5"/>\n'

        # Description / status
        if is_recording:
            rows_svg += f'  <text x="440" y="{y + 30}" font-family="\'Fira Code\', monospace" font-size="11" fill="#c0392b" opacity="0.7">recording</text>\n'
            # Animated recording dot
            rows_svg += f'''  <circle cx="510" cy="{y + 26}" r="4" fill="#c0392b">
    <animate attributeName="opacity" values="0.9;0.2;0.9" dur="1.5s" repeatCount="indefinite"/>
  </circle>
'''
        else:
            rows_svg += f'  <text x="440" y="{y + 30}" font-family="\'Segoe UI\', sans-serif" font-size="12" fill="#6078a0" opacity="0.7">{track["desc"]}</text>\n'

        # Subtle separator line
        if i < len(TRACKS) - 1:
            rows_svg += f'  <line x1="20" y1="{y + row_height}" x2="680" y2="{y + row_height}" stroke="#2a3a5c" stroke-opacity="0.15" stroke-width="1"/>\n'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="{total_height}" viewBox="0 0 700 {total_height}">
  <defs>
    <linearGradient id="headerLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#3d5a8a;stop-opacity:0"/>
      <stop offset="50%" style="stop-color:#5a7ab0;stop-opacity:0.4"/>
      <stop offset="100%" style="stop-color:#3d5a8a;stop-opacity:0"/>
    </linearGradient>
  </defs>

  <!-- Header -->
  <text x="28" y="30" font-family="'Fira Code', 'Cascadia Code', monospace" font-size="11" fill="#4a6080" letter-spacing="4">TRACKLIST</text>
  <text x="672" y="30" font-family="'Fira Code', monospace" font-size="10" fill="#2a3a5c" text-anchor="end">06 tracks</text>

  <!-- Header underline -->
  <rect x="0" y="42" width="700" height="1" fill="url(#headerLine)"/>

  <!-- Track rows -->
{rows_svg}
  <!-- Bottom line -->
  <rect x="0" y="{total_height - 10}" width="700" height="1" fill="url(#headerLine)" opacity="0.5"/>

</svg>'''
    return svg


def main():
    svg = generate_tracklist()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated tracklist SVG")


if __name__ == "__main__":
    main()
