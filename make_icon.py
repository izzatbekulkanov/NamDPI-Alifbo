# -*- coding: utf-8 -*-
"""
NamDPI alifbo - Professional Icon Generator
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_namdpi_icon(path="app_icon.ico"):
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []

    for w, h in sizes:
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 1. Elegant rounded square with deep academic navy gradient
        r = int(w * 0.22)
        pad = max(1, int(w * 0.03))
        
        # Outer border / subtle glow
        draw.rounded_rectangle(
            [pad, pad, w - pad - 1, h - pad - 1],
            radius=r,
            fill=(15, 23, 42, 255),      # Slate 900
            outline=(6, 182, 212, 230),   # Cyan 500
            width=max(1, int(w * 0.035))
        )

        # Inner subtle gradient card
        inner_pad = max(2, int(w * 0.08))
        draw.rounded_rectangle(
            [inner_pad, inner_pad, w - inner_pad - 1, h - inner_pad - 1],
            radius=int(r * 0.75),
            fill=(30, 41, 59, 255),      # Slate 800
            outline=(51, 65, 85, 255),   # Slate 700
            width=max(1, int(w * 0.02))
        )

        # 2. Main Central Symbol: "Ö" and "Ў" stylized monogram
        # Central circle for 'Ö'
        cx, cy = w // 2, int(h * 0.55)
        radius = int(w * 0.22)
        thickness = max(1, int(w * 0.075))
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=(6, 182, 212, 255), # Cyan
            width=thickness
        )

        # Two dots above O for Ö (golden academic accents)
        dot_r = max(1, int(w * 0.038))
        dot_y = cy - radius - int(w * 0.11)
        dot_offset = int(w * 0.11)
        draw.ellipse(
            [cx - dot_offset - dot_r, dot_y - dot_r, cx - dot_offset + dot_r, dot_y + dot_r],
            fill=(245, 158, 11, 255) # Amber/Gold
        )
        draw.ellipse(
            [cx + dot_offset - dot_r, dot_y - dot_r, cx + dot_offset + dot_r, dot_y + dot_r],
            fill=(245, 158, 11, 255)
        )

        # Subtle bottom arch / accent
        arch_y = cy + radius + int(w * 0.05)
        if w >= 48:
            arch_w = int(w * 0.2)
            draw.line(
                [cx - arch_w, arch_y, cx + arch_w, arch_y],
                fill=(245, 158, 11, 200),
                width=max(1, int(w * 0.025))
            )

        images.append(img)

    images[0].save(path, format="ICO", sizes=[(im.width, im.height) for im in images])
    print(f"Professional icon saved successfully to {path}")

if __name__ == '__main__':
    create_namdpi_icon("I:\\translate\\app_icon.ico")
