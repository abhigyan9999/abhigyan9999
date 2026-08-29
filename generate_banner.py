"""
Banner Generator for GitHub Profile: abhigyan9999 (Abhigyan Vishwakarma)
"""

import os
import sys
import numpy as np
from PIL import Image, ImageOps, ImageFilter

PROFILE_DATA = {
    "handle": "abhigyan9999",
    "name": "Abhigyan Vishwakarma",
    "role": "Full-Stack Developer",
    "origin": "India",
    "education": "Computer Science / Dev",
    "status": "Building + Shipping + Learning",
    "toolchain": "VS Code, Git, Postman, Figma",
    "core_lang": "JavaScript, TypeScript, Python",
    "core_frontend": "React, Next.js, HTML5, TailwindCSS",
    "core_backend": "Node.js, Express.js, REST APIs",
    "core_database": "MongoDB, PostgreSQL, MySQL",
    "core_infra": "Git, Docker, Vercel, Netlify",
    "grid_mail": "abhigyan@example.com",
    "grid_portfolio": "github.com/abhigyan9999",
    "grid_linkedin": "in/abhigyan-vishwakarma",
    "grid_github": "github.com/abhigyan9999",
}

THEME_COLORS = {
    "dark": {
        "bg": "#0A101F",
        "terminal_bg": "#0D1527",
        "border": "#1E293B",
        "title_bar": "#131C31",
        "chrome": "#22D3EE",
        "chrome_dim": "#0891B2",
        "text_label": "#94A3B8",
        "text_value": "#F8FAFC",
        "dots": "#334155",
        "accent": "#10B981",
        "portrait": "#A78BFA",
        "live_red": "#EF4444",
        "pill_bg": "#7C3AED",
        "pill_text": "#FFFFFF",
    },
    "light": {
        "bg": "#F8FAFC",
        "terminal_bg": "#FFFFFF",
        "border": "#CBD5E1",
        "title_bar": "#F1F5F9",
        "chrome": "#0891B2",
        "chrome_dim": "#0E7490",
        "text_label": "#64748B",
        "text_value": "#0F172A",
        "dots": "#E2E8F0",
        "accent": "#059669",
        "portrait": "#7C3AED",
        "live_red": "#DC2626",
        "pill_bg": "#6366F1",
        "pill_text": "#FFFFFF",
    }
}

def dither_image(image_path, target_size=(300, 340), is_dark=True):
    if os.path.exists(image_path):
        img = Image.open(image_path).convert("L")
        img = ImageOps.fit(img, target_size, method=Image.Resampling.LANCZOS)
        img = ImageOps.autocontrast(img, cutoff=1)
        img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
        dithered = img.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
        arr = np.array(dithered)
        return arr if is_dark else ~arr
    return generate_placeholder_matrix(target_size)

def generate_placeholder_matrix(target_size=(300, 340)):
    w, h = target_size
    cx, cy = w // 2, h // 2
    y, x = np.ogrid[:h, :w]
    head_mask = ((x - cx)**2 / (55**2) + (y - (cy - 35))**2 / (70**2)) <= 1
    body_mask = ((x - cx)**2 / (110**2) + (y - (cy + 110))**2 / (90**2)) <= 1
    combined = head_mask | body_mask
    noise = (np.sin(x / 3.0) * np.cos(y / 3.0) > -0.2)
    return combined & noise

def matrix_to_svg_paths(matrix, offset_x=45, offset_y=110, scale=1.0, color="#A78BFA"):
    h, w = matrix.shape
    path_data = []
    for row in range(h):
        in_run = False
        start_col = 0
        for col in range(w):
            val = matrix[row, col]
            if val and not in_run:
                in_run = True
                start_col = col
            elif not val and in_run:
                in_run = False
                x1 = offset_x + start_col * scale
                y1 = offset_y + row * scale
                run_len = (col - start_col) * scale
                path_data.append(f"M{x1:.1f} {y1:.1f}h{run_len:.1f}")
        if in_run:
            x1 = offset_x + start_col * scale
            y1 = offset_y + row * scale
            run_len = (w - start_col) * scale
            path_data.append(f"M{x1:.1f} {y1:.1f}h{run_len:.1f}")
            
    d_str = " ".join(path_data)
    return f'<path d="{d_str}" stroke="{color}" stroke-width="{scale:.1f}" shape-rendering="crispEdges" />'

def build_svg(data, mode="dark", photo_path="photo.jpg"):
    colors = THEME_COLORS[mode]
    is_dark = (mode == "dark")
    matrix = dither_image(photo_path, target_size=(300, 340), is_dark=is_dark)
    portrait_path = matrix_to_svg_paths(matrix, offset_x=45, offset_y=125, scale=1.05, color=colors["portrait"])
    
    info_rows = [
        ("Subject", data["name"]),
        ("Role", data["role"]),
        ("Origin", data["origin"]),
        ("Education", data["education"]),
        ("Status", data["status"]),
        ("ToolChain", data["toolchain"]),
        ("Core.Lang", data["core_lang"]),
        ("Core.Frontend", data["core_frontend"]),
        ("Core.Backend", data["core_backend"]),
        ("Core.Database", data["core_database"]),
        ("Core.Infra", data["core_infra"]),
        ("Grid.Mail", data["grid_mail"]),
        ("Grid.Portfolio", data["grid_portfolio"]),
        ("Grid.LinkedIn", data["grid_linkedin"]),
        ("Grid.GitHub", data["grid_github"]),
    ]
    
    info_svg_lines = []
    start_y = 135
    line_gap = 26
    col_x = 425
    value_right_x = 1135
    
    for i, (label, val) in enumerate(info_rows):
        cur_y = start_y + i * line_gap
        dots = ". " * 45
        info_svg_lines.append(f"""
    <!-- Row {i+1}: {label} -->
    <text x="{col_x}" y="{cur_y}" font-family="monospace" font-size="13" font-weight="600" fill="{colors['text_label']}">{label}</text>
    <text x="{col_x + 130}" y="{cur_y}" font-family="monospace" font-size="12" fill="{colors['dots']}">{dots}</text>
    <text x="{value_right_x}" y="{cur_y}" text-anchor="end" font-family="monospace" font-size="13" fill="{colors['text_value']}">{val}</text>
        """)
        
    info_content = "\n".join(info_svg_lines)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="1180" height="610">
  <defs>
    <style>
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
      }}
      .live-dot {{
        animation: pulse 1.8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
      }}
      text {{
        user-select: none;
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="1180" height="610" rx="12" fill="{colors['bg']}" />
  <rect x="2" y="2" width="1176" height="606" rx="10" fill="{colors['terminal_bg']}" stroke="{colors['border']}" stroke-width="1.5" />

  <!-- Terminal Title Bar -->
  <path d="M2 12 C2 6.477 6.477 2 12 2 L1168 2 C1173.523 2 1178 6.477 1178 12 L1178 46 L2 46 Z" fill="{colors['title_bar']}" stroke="{colors['border']}" stroke-width="1.5" />
  
  <!-- Window Controls -->
  <circle cx="24" cy="24" r="6" fill="#EF4444" />
  <circle cx="44" cy="24" r="6" fill="#F59E0B" />
  <circle cx="64" cy="24" r="6" fill="#10B981" />

  <!-- Terminal Title -->
  <text x="590" y="29" text-anchor="middle" font-family="monospace" font-size="13" font-weight="600" fill="{colors['text_label']}">profile.sh --live</text>

  <!-- LIVE Badge & Pill -->
  <g transform="translate(980, 14)">
    <rect width="68" height="20" rx="4" fill="{colors['bg']}" stroke="{colors['border']}" stroke-width="1" />
    <circle cx="12" cy="10" r="4" fill="{colors['live_red']}" class="live-dot" />
    <text x="24" y="14" font-family="monospace" font-size="10" font-weight="700" fill="{colors['live_red']}">LIVE</text>
  </g>
  <g transform="translate(1055, 14)">
    <rect width="115" height="20" rx="10" fill="{colors['pill_bg']}" />
    <text x="57" y="14" text-anchor="middle" font-family="monospace" font-size="10" font-weight="700" fill="{colors['pill_text']}">@{data['handle']}</text>
  </g>

  <!-- Section Separator Line -->
  <line x1="395" y1="58" x2="395" y2="590" stroke="{colors['border']}" stroke-width="1.5" stroke-dasharray="4 4" />

  <!-- LEFT PANEL: VISUAL.MAP -->
  <text x="45" y="85" font-family="monospace" font-size="13" font-weight="700" fill="{colors['chrome']}">// VISUAL.MAP</text>
  <rect x="35" y="105" width="335" height="380" rx="6" fill="none" stroke="{colors['border']}" stroke-width="1" />
  
  <!-- Dithered Portrait -->
  <g transform="translate(0, 0)">
    {portrait_path}
  </g>

  <!-- Status readout below portrait -->
  <text x="45" y="525" font-family="monospace" font-size="11" fill="{colors['text_label']}">RENDER: 1-BIT DITHER</text>
  <text x="45" y="545" font-family="monospace" font-size="11" fill="{colors['accent']}">STATUS: ACTIVE_FEED</text>

  <!-- RIGHT PANEL: SYSTEM.INFO -->
  <text x="425" y="85" font-family="monospace" font-size="13" font-weight="700" fill="{colors['chrome']}">// SYSTEM.INFO</text>
  
  <!-- Info Rows -->
  {info_content}
</svg>"""
    return svg

def main():
    dark_svg = build_svg(PROFILE_DATA, mode="dark", photo_path="photo.jpg")
    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
        
    light_svg = build_svg(PROFILE_DATA, mode="light", photo_path="photo.jpg")
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
        
    print("[OK] SVGs successfully generated for abhigyan9999.")

if __name__ == "__main__":
    main()
