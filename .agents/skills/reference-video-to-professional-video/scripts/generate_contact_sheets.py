#!/usr/bin/env python3
"""
generate_contact_sheets.py - Visual Contact Sheet Generator for Batch Frame Inspection

Assembles extracted frames into high-density grid contact sheets (e.g. 4x4 or 3x3)
with embedded frame numbers and timestamp badges.

Enables agents and human directors to:
- Inspect video progression systematically in manageable batches.
- Detect exact animation onset, keyframe velocity, and visual changes.
- Identify UI component persistence versus momentary effects.

Usage:
    python generate_contact_sheets.py --frames-dir reference-assets/frames
    python generate_contact_sheets.py --frames-dir reference-assets/frames --grid 4x4 --thumb-width 400
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Any
from PIL import Image, ImageDraw, ImageFont

def create_contact_sheet(
    batch_frames: List[Dict[str, Any]],
    sheet_index: int,
    output_path: str,
    cols: int = 4,
    rows: int = 4,
    thumb_w: int = 380,
    pad: int = 12,
    badge_bg: tuple = (15, 23, 42, 220), # Slate 900
    badge_text_color: tuple = (255, 255, 255)
):
    """Render a single grid sheet containing the specified batch of frames."""
    if not batch_frames:
        return
        
    # Open first image to determine aspect ratio
    sample_img = Image.open(batch_frames[0]["path"])
    aspect = sample_img.height / sample_img.width
    thumb_h = int(thumb_w * aspect)
    
    # Calculate canvas dimensions
    canvas_w = (cols * thumb_w) + ((cols + 1) * pad)
    header_h = 50
    canvas_h = header_h + (rows * thumb_h) + ((rows + 1) * pad)
    
    # Create dark-themed canvas
    sheet = Image.new("RGB", (canvas_w, canvas_h), color=(20, 24, 33)) # Dark Slate
    draw = ImageDraw.Draw(sheet)
    
    # Header text
    start_tc = batch_frames[0].get("timecode", "00:00:00.000")
    end_tc = batch_frames[-1].get("timecode", "00:00:00.000")
    header_text = f"CONTACT SHEET #{sheet_index:02d} | Frames {batch_frames[0]['frame_number']} to {batch_frames[-1]['frame_number']} | Timecode: {start_tc} -> {end_tc}"
    draw.rectangle([(0, 0), (canvas_w, header_h)], fill=(10, 14, 23))
    draw.text((pad + 4, 16), header_text, fill=(226, 232, 240))
    
    for idx, item in enumerate(batch_frames):
        col = idx % cols
        row = idx // cols
        
        x = pad + (col * (thumb_w + pad))
        y = header_h + pad + (row * (thumb_h + pad))
        
        try:
            with Image.open(item["path"]) as img:
                thumb = img.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                sheet.paste(thumb, (x, y))
                
                # Draw border around thumbnail
                draw.rectangle([(x, y), (x + thumb_w - 1, y + thumb_h - 1)], outline=(51, 65, 85), width=1)
                
                # Draw timestamp badge
                label = f"#{item['frame_number']} | {item.get('timecode', '')}"
                badge_h = 22
                badge_w = min(180, thumb_w - 10)
                badge_x = x + 6
                badge_y = y + thumb_h - badge_h - 6
                
                draw.rectangle(
                    [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
                    fill=(15, 23, 42)
                )
                draw.text((badge_x + 6, badge_y + 4), label, fill=(56, 189, 248)) # Cyan text
        except Exception as e:
            print(f"Warning: Failed to load frame {item['path']}: {e}", file=sys.stderr)
            
    sheet.save(output_path, quality=92)
    print(f"Saved contact sheet: {output_path} ({len(batch_frames)} frames)")

def generate_contact_sheets(
    frames_dir: str,
    output_dir: str = None,
    cols: int = 4,
    rows: int = 4,
    thumb_width: int = 380
):
    """Scan frames directory and generate sequenced contact sheets."""
    if not os.path.isdir(frames_dir):
        raise NotADirectoryError(f"Frames directory not found: {frames_dir}")
        
    out_dir = output_dir or os.path.join(frames_dir, "contact_sheets")
    os.makedirs(out_dir, exist_ok=True)
    
    index_file = os.path.join(frames_dir, "index.json")
    frames_list = []
    
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            for item in manifest.get("frames", []):
                frame_path = os.path.join(frames_dir, item["filename"])
                if os.path.exists(frame_path):
                    frames_list.append({
                        "frame_number": item["frame_number"],
                        "timecode": item["timecode"],
                        "seconds": item["timestamp_seconds"],
                        "path": frame_path,
                        "filename": item["filename"]
                    })
    else:
        # Fallback to file listing
        extensions = (".png", ".jpg", ".jpeg", ".webp")
        files = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(extensions)])
        for idx, f in enumerate(files, start=1):
            frames_list.append({
                "frame_number": idx,
                "timecode": f"Frame {idx}",
                "seconds": 0.0,
                "path": os.path.join(frames_dir, f),
                "filename": f
            })
            
    if not frames_list:
        print(f"No frames found in directory: {frames_dir}", file=sys.stderr)
        return
        
    batch_size = cols * rows
    total_batches = (len(frames_list) + batch_size - 1) // batch_size
    print(f"Total frames: {len(frames_list)}. Grid: {cols}x{rows} ({batch_size} per sheet). Generating {total_batches} sheet(s)...")
    
    manifest_sheets = []
    for sheet_idx in range(1, total_batches + 1):
        batch = frames_list[(sheet_idx - 1) * batch_size : sheet_idx * batch_size]
        out_name = f"contact_sheet_{sheet_idx:02d}.jpg"
        out_path = os.path.join(out_dir, out_name)
        create_contact_sheet(
            batch_frames=batch,
            sheet_index=sheet_idx,
            output_path=out_path,
            cols=cols,
            rows=rows,
            thumb_w=thumb_width
        )
        manifest_sheets.append({
            "sheet_index": sheet_idx,
            "filename": out_name,
            "path": out_path.replace("\\", "/"),
            "start_frame": batch[0]["frame_number"],
            "end_frame": batch[-1]["frame_number"],
            "start_timecode": batch[0].get("timecode", ""),
            "end_timecode": batch[-1].get("timecode", "")
        })
        
    # Write summary manifest
    summary_path = os.path.join(out_dir, "sheets_index.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_sheets": total_batches,
            "batch_size": batch_size,
            "sheets": manifest_sheets
        }, f, indent=2)
    print(f"\n[Finished] All {total_batches} contact sheets generated at: {out_dir}")

def main():
    parser = argparse.ArgumentParser(description="Generate contact sheets for structured visual frame analysis.")
    parser.add_argument("--frames-dir", "-d", default="reference-assets/frames", help="Directory containing extracted frames or index.json")
    parser.add_argument("--output-dir", "-o", default=None, help="Directory to save contact sheets (defaults to frames_dir/contact_sheets)")
    parser.add_argument("--grid", default="4x4", help="Grid dimension as COLSxROWS (e.g. 4x4, 3x3, 5x4)")
    parser.add_argument("--thumb-width", type=int, default=380, help="Width in pixels for each thumbnail (default: 380)")
    
    args = parser.parse_args()
    
    try:
        cols, rows = map(int, args.grid.lower().split("x"))
    except ValueError:
        print("Invalid grid format. Must be e.g. 4x4 or 3x3", file=sys.stderr)
        sys.exit(1)
        
    generate_contact_sheets(
        frames_dir=args.frames_dir,
        output_dir=args.output_dir,
        cols=cols,
        rows=rows,
        thumb_width=args.thumb_width
    )

if __name__ == "__main__":
    main()
