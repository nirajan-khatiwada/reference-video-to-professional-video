#!/usr/bin/env python3
"""
other_helpers.py - Visual Identity & Design Token Utilities for Antigravity

Provides essential helper utilities for reference video reproduction:
1. palette: Extracts dominant color palette (Primary, Surface, Background, Accent)
2. crop: Extracts reusable UI component bounding boxes into reference-assets/
3. tokens: Generates production-ready TypeScript DesignTokens.ts for Remotion

Usage:
    # Extract dominant color palette:
    python other_helpers.py palette --input reference-assets/frames/frame_00001.png
    
    # Crop UI component from a frame:
    python other_helpers.py crop --image reference-assets/frames/frame_00001.png --box 100 200 400 300 --output reference-assets/components/navbar.png
    
    # Generate TypeScript design tokens:
    python other_helpers.py tokens --colors '#0f172a,#3b82f6,#10b981,#f8fafc' --output src/designTokens.ts
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Tuple, Any
from PIL import Image

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB integers to hex code."""
    return f"#{r:02x}{g:02x}{b:02x}"

def luminance(r: int, g: int, b: int) -> float:
    """Calculate perceived luminance (0.0 to 1.0)."""
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0

def extract_dominant_colors(image_path: str, max_colors: int = 6) -> List[Dict[str, Any]]:
    """Extract dominant colors from an image using PIL color quantization."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
        
    with Image.open(image_path) as img:
        # Resize to 200x200 to accelerate quantization and smooth high frequency noise
        small = img.convert("RGB").resize((200, 200), Image.Resampling.BILINEAR)
        quantized = small.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
        palette_bytes = quantized.getpalette()[:max_colors * 3]
        
        # Count frequency of each color
        color_counts = quantized.getcolors() or []
        color_counts.sort(key=lambda x: x[0], reverse=True)
        
        extracted = []
        for count, idx in color_counts:
            r = palette_bytes[idx * 3]
            g = palette_bytes[idx * 3 + 1]
            b = palette_bytes[idx * 3 + 2]
            hex_val = rgb_to_hex(r, g, b)
            lum = luminance(r, g, b)
            
            # Suggest semantic role
            if lum < 0.15:
                role = "Background (Dark)"
            elif lum > 0.85:
                role = "Background (Light) / Text"
            else:
                role = "Brand / Accent"
                
            extracted.append({
                "hex": hex_val,
                "rgb": [r, g, b],
                "luminance": round(lum, 2),
                "frequency": count,
                "suggested_role": role
            })
            
    return extracted

def crop_component(image_path: str, box: Tuple[int, int, int, int], output_path: str):
    """
    Crop region of interest from frame.
    box format: (x, y, width, height)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
        
    x, y, w, h = box
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    with Image.open(image_path) as img:
        crop_box = (x, y, x + w, y + h)
        cropped = img.crop(crop_box)
        cropped.save(output_path)
        print(f"[Cropped UI Component] Saved {w}x{h} region to: {output_path}")

def generate_typescript_tokens(colors: List[str], output_path: str, app_name: str = "App"):
    """Generate production-ready TypeScript design tokens for Remotion."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    c_primary = colors[0] if len(colors) > 0 else "#2563EB"
    c_secondary = colors[1] if len(colors) > 1 else "#3B82F6"
    c_accent = colors[2] if len(colors) > 2 else "#10B981"
    c_bg = colors[3] if len(colors) > 3 else "#0F172A"
    c_surface = colors[4] if len(colors) > 4 else "#1E293B"
    c_text = colors[5] if len(colors) > 5 else "#F8FAFC"
    
    ts_code = f"""// DesignTokens.ts - Generated Visual Design System for {app_name}
// Consistent tokens to preserve app identity across all Remotion scenes

export const DESIGN_TOKENS = {{
  colors: {{
    primary: '{c_primary}',
    secondary: '{c_secondary}',
    accent: '{c_accent}',
    background: '{c_bg}',
    surface: '{c_surface}',
    textPrimary: '{c_text}',
    textMuted: '#94A3B8',
    border: '#334155',
  }},
  typography: {{
    fontFamilyDisplay: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    fontFamilyCode: '"JetBrains Mono", Menlo, Monaco, Consolas, monospace',
    display: {{
      fontSize: 56,
      fontWeight: 800,
      letterSpacing: '-0.02em',
      lineHeight: 1.15,
    }},
    heading: {{
      fontSize: 38,
      fontWeight: 700,
      letterSpacing: '-0.01em',
      lineHeight: 1.25,
    }},
    subheading: {{
      fontSize: 24,
      fontWeight: 500,
      lineHeight: 1.4,
    }},
    body: {{
      fontSize: 18,
      fontWeight: 400,
      lineHeight: 1.5,
    }},
  }},
  radii: {{
    sm: 6,
    md: 12,
    lg: 20,
    full: 9999,
  }},
  shadows: {{
    card: '0 20px 40px -15px rgba(0, 0, 0, 0.5)',
    glow: '0 0 30px rgba(37, 99, 235, 0.35)',
  }},
  motion: {{
    springConfig: {{
      damping: 15,
      mass: 0.8,
      stiffness: 100,
    }},
    fadeDurationFrames: 15,
    transitionDurationFrames: 24,
  }},
}} as const;
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ts_code)
    print(f"[Design Tokens Generated] TypeScript tokens written to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Visual identity and design token utilities.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Palette parser
    p_pal = subparsers.add_parser("palette", help="Extract dominant colors from an image")
    p_pal.add_argument("--input", "-i", required=True, help="Path to input image frame")
    p_pal.add_argument("--colors", "-n", type=int, default=6, help="Number of dominant colors (default: 6)")
    p_pal.add_argument("--output-json", "-o", default=None, help="Optional JSON output path")
    
    # Crop parser
    p_crop = subparsers.add_parser("crop", help="Crop a region of interest (UI component) from a frame")
    p_crop.add_argument("--image", "-i", required=True, help="Source frame image")
    p_crop.add_argument("--box", "-b", nargs=4, type=int, required=True, metavar=("X", "Y", "W", "H"), help="Crop box: X Y Width Height")
    p_crop.add_argument("--output", "-o", required=True, help="Destination cropped image path")
    
    # Tokens parser
    p_tok = subparsers.add_parser("tokens", help="Generate TypeScript design tokens file")
    p_tok.add_argument("--colors", "-c", required=True, help="Comma-separated hex colors (e.g. #0f172a,#3b82f6,#10b981)")
    p_tok.add_argument("--output", "-o", default="src/designTokens.ts", help="Output TypeScript path")
    p_tok.add_argument("--app-name", default="App", help="Application name for token header")
    
    args = parser.parse_args()
    
    if args.command == "palette":
        colors = extract_dominant_colors(args.input, max_colors=args.colors)
        print("\n" + "=" * 54)
        print(" EXTRACTED COLOR PALETTE")
        print("=" * 54)
        for idx, c in enumerate(colors, start=1):
            print(f" {idx}. {c['hex']}  (RGB: {c['rgb']})  Luminance: {c['luminance']}  [{c['suggested_role']}]")
        print("=" * 54)
        if args.output_json:
            with open(args.output_json, "w", encoding="utf-8") as f:
                json.dump(colors, f, indent=2)
            print(f"Saved palette JSON to: {args.output_json}")
            
    elif args.command == "crop":
        crop_component(args.image, tuple(args.box), args.output)
        
    elif args.command == "tokens":
        hex_list = [c.strip() for c in args.colors.split(",") if c.strip()]
        generate_typescript_tokens(hex_list, args.output, app_name=args.app_name)

if __name__ == "__main__":
    main()
