#!/usr/bin/env python3
"""Generate styled SVG tracklists (dark + light) for the GitHub profile README."""

from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

TRACKS = [
    {"num": "01", "title": "Perfect Match", "desc": "matchmaking for Cornell students", "status": "released", "url": "https://github.com/Perfect-Match-Org/perfect-match-web"},
    {"num": "02", "title": "EzModel", "desc": "visual DB schema + CRUD API gen", "status": "released", "url": "https://github.com/Bug-Bugger/EzModel"},
    {"num": "03", "title": "Tabime", "desc": "plan hangouts, effortlessly", "status": "released", "url": "https://github.com/Bug-Bugger/Tabime"},
    {"num": "04", "title": "CuffedOrNot", "desc": "the relationship quiz", "status": "released", "url": "https://github.com/Perfect-Match-Org/cuffedornot"},
    {"num": "05", "title": "Campus Meal Pick", "desc": "AI-powered eatery suggestions", "status": "released", "url": "https://github.com/Shengle-Dai/Campus-Meal-Pick"},
    {"num": "06", "title": "Escoffier", "desc": "a cooking companion app", "status": "recording", "url": ""},
]

# Key/Jun Maeda palette
PALETTES = {
    "dark": {
        "row_bg": "#7b9ed4",
        "accent": "#7b9ed4",
        "accent_recording": "#d4a87c",
        "text_title": "#e4e0ec",
        "text_title_recording": "#c0b8d0",
        "text_num": "#7b9ed4",
        "text_desc": "#7882a0",
        "line_color": "#2a3050",
        "header_text": "#7882a0",
        "header_sub": "#4a5068",
        "dot_line": "#2a3050",
        "recording_text": "#d4a87c",
        "line_grad_mid": "#a89cc8",
        "line_grad_edge": "#7b9ed4",
    },
    "light": {
        "row_bg": "#5a7caa",
        "accent": "#5a7caa",
        "accent_recording": "#b08050",
        "text_title": "#2a2a3a",
        "text_title_recording": "#4a4a5a",
        "text_num": "#5a7caa",
        "text_desc": "#6a6a80",
        "line_color": "#c8c0d0",
        "header_text": "#6a6a80",
        "header_sub": "#8a8a98",
        "dot_line": "#c8c0d0",
        "recording_text": "#b08050",
        "line_grad_mid": "#8070a0",
        "line_grad_edge": "#5a7caa",
    },
}


def generate_tracklist(theme="dark"):
    p = PALETTES[theme]
    row_height = 52
    padding_top = 65
    total_height = padding_top + len(TRACKS) * row_height + 40

    rows_svg = ""
    for i, track in enumerate(TRACKS):
        y = padding_top + i * row_height
        is_recording = track["status"] == "recording"

        # Alternating subtle row background
        if i % 2 == 0:
            rows_svg += f'  <rect x="0" y="{y}" width="700" height="{row_height}" fill="{p["row_bg"]}" opacity="0.04"/>\n'

        # Left accent bar
        accent_color = p["accent_recording"] if is_recording else p["accent"]
        rows_svg += f'  <rect x="0" y="{y}" width="3" height="{row_height}" fill="{accent_color}" opacity="0.5" rx="1"/>\n'

        # Track number
        num_opacity = "0.3" if is_recording else "0.45"
        rows_svg += f'  <text x="28" y="{y + 32}" font-family="\'Fira Code\', \'Cascadia Code\', monospace" font-size="13" fill="{p["text_num"]}" opacity="{num_opacity}" text-anchor="middle">{track["num"]}</text>\n'

        # Track title
        title_color = p["text_title_recording"] if is_recording else p["text_title"]
        rows_svg += f'  <text x="55" y="{y + 30}" font-family="\'Segoe UI\', \'SF Pro Display\', -apple-system, sans-serif" font-size="15" font-weight="600" fill="{title_color}">{track["title"]}</text>\n'

        # Dotted line connecting title to description
        title_approx_width = len(track["title"]) * 9 + 55
        dot_start = title_approx_width + 10
        dot_end = 430
        if dot_start < dot_end:
            rows_svg += f'  <line x1="{dot_start}" y1="{y + 27}" x2="{dot_end}" y2="{y + 27}" stroke="{p["dot_line"]}" stroke-width="1" stroke-dasharray="2,6" opacity="0.5"/>\n'

        # Description / status
        if is_recording:
            rows_svg += f'  <text x="440" y="{y + 30}" font-family="\'Fira Code\', monospace" font-size="11" fill="{p["recording_text"]}" opacity="0.7">recording</text>\n'
            rows_svg += f'''  <circle cx="510" cy="{y + 26}" r="4" fill="{p["recording_text"]}">
    <animate attributeName="opacity" values="0.9;0.2;0.9" dur="1.5s" repeatCount="indefinite"/>
  </circle>
'''
        else:
            rows_svg += f'  <text x="440" y="{y + 30}" font-family="\'Segoe UI\', sans-serif" font-size="12" fill="{p["text_desc"]}" opacity="0.7">{track["desc"]}</text>\n'

        # Subtle separator line
        if i < len(TRACKS) - 1:
            rows_svg += f'  <line x1="20" y1="{y + row_height}" x2="680" y2="{y + row_height}" stroke="{p["line_color"]}" stroke-opacity="0.15" stroke-width="1"/>\n'

    track_count = f"{len(TRACKS):02d} tracks"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="{total_height}" viewBox="0 0 700 {total_height}">
  <defs>
    <linearGradient id="headerLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{p["line_grad_edge"]};stop-opacity:0"/>
      <stop offset="50%" style="stop-color:{p["line_grad_mid"]};stop-opacity:0.4"/>
      <stop offset="100%" style="stop-color:{p["line_grad_edge"]};stop-opacity:0"/>
    </linearGradient>
  </defs>

  <!-- Header -->
  <text x="28" y="30" font-family="'Fira Code', 'Cascadia Code', monospace" font-size="11" fill="{p["header_text"]}" letter-spacing="4">TRACKLIST</text>
  <text x="672" y="30" font-family="'Fira Code', monospace" font-size="10" fill="{p["header_sub"]}" text-anchor="end">{track_count}</text>

  <!-- Header underline -->
  <rect x="0" y="42" width="700" height="1" fill="url(#headerLine)"/>

  <!-- Track rows -->
{rows_svg}
  <!-- Bottom line -->
  <rect x="0" y="{total_height - 10}" width="700" height="1" fill="url(#headerLine)" opacity="0.5"/>

</svg>'''
    return svg


def main():
    for theme in ("dark", "light"):
        svg = generate_tracklist(theme)
        output_file = OUTPUT_DIR / f"tracklist-{theme}.svg"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated tracklist-{theme}.svg")


if __name__ == "__main__":
    main()
