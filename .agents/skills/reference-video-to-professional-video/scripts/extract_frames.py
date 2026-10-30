#!/usr/bin/env python3
"""
extract_frames.py - High-Fidelity Frame Extractor for Reference Video Analysis

Extracts frames from a reference video using FFmpeg:
- Preserves exact frame order and timestamps.
- Supports native fps extraction (every single frame) or sample rates (e.g. 1 fps, 2 fps, 4 fps).
- Generates an index.json file mapping every frame to its timecode and timestamp.
- Supports time windows (--start-time, --end-time) and frame limits.

Usage:
    # Extract all frames:
    python extract_frames.py input.mp4 --all --output-dir reference-assets/frames
    
    # Extract keyframes at 2 fps for visual inspection:
    python extract_frames.py input.mp4 --fps 2 --output-dir reference-assets/frames_2fps
"""

import sys
import os
import json
import subprocess
import argparse
from typing import Dict, Any, List

def format_timestamp(seconds: float) -> str:
    """Format seconds into HH-MM-SS.mmm for filenames."""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hrs:02d}-{mins:02d}-{secs:06.3f}".replace(".", "_")

def format_timecode(seconds: float) -> str:
    """Format seconds into standard timecode HH:MM:SS.mmm."""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:06.3f}"

def get_video_info(video_path: str) -> Dict[str, Any]:
    """Retrieve basic video duration and fps using ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate,avg_frame_rate,duration,width,height",
        "-show_entries", "format=duration",
        "-print_format", "json",
        video_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        data = json.loads(res.stdout)
        stream = data.get("streams", [{}])[0]
        fmt = data.get("format", {})
        
        from fractions import Fraction
        fps_str = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "30/1"
        try:
            fps = float(Fraction(fps_str)) if "/" in fps_str else float(fps_str)
        except ZeroDivisionError:
            fps = 30.0
            
        dur_str = stream.get("duration") or fmt.get("duration") or "0"
        duration = float(dur_str)
        
        return {
            "fps": fps,
            "duration": duration,
            "width": int(stream.get("width", 0)),
            "height": int(stream.get("height", 0))
        }
    except Exception as e:
        print(f"Warning: could not read ffprobe info ({e}), using default 30fps.", file=sys.stderr)
        return {"fps": 30.0, "duration": 0.0, "width": 0, "height": 0}

def extract_frames(
    video_path: str,
    output_dir: str,
    fps: float = None,
    extract_all: bool = False,
    start_time: float = None,
    end_time: float = None,
    max_frames: int = None,
    img_format: str = "png",
    include_timestamp_names: bool = False
) -> Dict[str, Any]:
    """Execute FFmpeg frame extraction and compile index.json."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    os.makedirs(output_dir, exist_ok=True)
    video_info = get_video_info(video_path)
    native_fps = video_info["fps"]
    
    # Build FFmpeg command
    cmd = ["ffmpeg", "-y"]
    
    if start_time is not None and start_time > 0:
        cmd.extend(["-ss", str(start_time)])
        
    cmd.extend(["-i", video_path])
    
    if end_time is not None:
        duration_window = end_time - (start_time or 0.0)
        if duration_window > 0:
            cmd.extend(["-t", str(duration_window)])
            
    # Filter configuration
    vf_filters = []
    effective_fps = native_fps
    
    if extract_all:
        effective_fps = native_fps
    elif fps is not None and fps > 0:
        vf_filters.append(f"fps={fps}")
        effective_fps = fps
    else:
        # Default sampling: 2 fps for efficient AI visual inspection
        vf_filters.append("fps=2")
        effective_fps = 2.0
        
    if vf_filters:
        cmd.extend(["-vf", ",".join(vf_filters)])
        
    if max_frames:
        cmd.extend(["-vframes", str(max_frames)])
        
    # Output pattern
    out_pattern = os.path.join(output_dir, f"frame_%05d.{img_format}")
    cmd.extend(["-q:v", "2", out_pattern])
    
    print(f"Executing extraction: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    # Scan created frames and compile index.json
    extracted_files = sorted([f for f in os.listdir(output_dir) if f.startswith("frame_") and f.endswith(f".{img_format}")])
    
    frames_index = []
    base_start = start_time or 0.0
    
    for idx, fname in enumerate(extracted_files, start=1):
        # Calculate timestamp based on extraction rate
        timestamp_sec = base_start + ((idx - 1) / effective_fps)
        timecode = format_timecode(timestamp_sec)
        
        frame_entry = {
            "frame_number": idx,
            "filename": fname,
            "relative_path": os.path.join(output_dir, fname).replace("\\", "/"),
            "timestamp_seconds": round(timestamp_sec, 3),
            "timecode": timecode,
        }
        frames_index.append(frame_entry)
        
    manifest = {
        "source_video": os.path.abspath(video_path),
        "total_extracted_frames": len(frames_index),
        "extraction_fps": effective_fps,
        "native_fps": native_fps,
        "video_resolution": f"{video_info['width']}x{video_info['height']}",
        "frames": frames_index
    }
    
    index_path = os.path.join(output_dir, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"\n[Extraction Completed] Successfully extracted {len(frames_index)} frames to '{output_dir}'.")
    print(f"[Index Saved] Frame metadata index written to '{index_path}'.")
    return manifest

def main():
    parser = argparse.ArgumentParser(description="Extract frames from reference video for deep frame-by-frame analysis.")
    parser.add_argument("video_path", help="Path to reference video file")
    parser.add_argument("--output-dir", "-o", default="reference-assets/frames", help="Output directory for extracted frames")
    parser.add_argument("--all", action="store_true", help="Extract every single frame at native video framerate")
    parser.add_argument("--fps", type=float, default=None, help="Sampling frame rate (e.g. 1 for 1fps, 2 for 2fps, 4 for 4fps)")
    parser.add_argument("--start-time", type=float, default=None, help="Start time in seconds")
    parser.add_argument("--end-time", type=float, default=None, help="End time in seconds")
    parser.add_argument("--max-frames", type=int, default=None, help="Maximum number of frames to extract")
    parser.add_argument("--format", choices=["png", "jpg"], default="png", help="Image format (default: png)")
    
    args = parser.parse_args()
    
    try:
        extract_frames(
            video_path=args.video_path,
            output_dir=args.output_dir,
            fps=args.fps,
            extract_all=args.all,
            start_time=args.start_time,
            end_time=args.end_time,
            max_frames=args.max_frames,
            img_format=args.format
        )
    except Exception as e:
        print(f"Error extracting frames: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
