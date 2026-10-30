#!/usr/bin/env python3
"""
inspect_video.py - Comprehensive Video Metadata Inspector for Antigravity

Inspects reference video files using ffprobe to extract technical specifications:
- Duration (seconds and timecode)
- Resolution (width, height)
- Aspect Ratio (standard ratio label e.g., 16:9, 9:16, 4:3, 1:1)
- Frame Rate (exact FPS)
- Total Frame Count
- Video Codec, Pixel Format, Bitrate
- Audio Stream Information (if present)

Usage:
    python inspect_video.py path/to/video.mp4
    python inspect_video.py path/to/video.mp4 --output-json metadata.json
"""

import sys
import os
import json
import subprocess
import argparse
from fractions import Fraction
from typing import Dict, Any, Optional

def format_seconds(seconds: float) -> str:
    """Format seconds into HH:MM:SS.mmm timecode."""
    if seconds is None or seconds < 0:
        return "00:00:00.000"
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:06.3f}"

def calculate_aspect_ratio(width: int, height: int) -> str:
    """Calculate and classify the aspect ratio into standard video formats."""
    if not width or not height:
        return "Unknown"
    
    ratio = width / height
    tolerance = 0.04
    
    standard_ratios = [
        (16 / 9, "16:9 (Widescreen / Landscape)"),
        (9 / 16, "9:16 (Vertical / Shorts / Reels)"),
        (1.0, "1:1 (Square)"),
        (4 / 3, "4:3 (Classic Academy)"),
        (3 / 4, "3:4 (Portrait)"),
        (21 / 9, "21:9 (Ultrawide Cinematic)"),
        (3 / 2, "3:2 (Classic 35mm)"),
        (2 / 3, "2:3 (Portrait 35mm)"),
    ]
    
    for target_ratio, label in standard_ratios:
        if abs(ratio - target_ratio) <= tolerance:
            return label
            
    # Fallback to GCD reduction
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
        
    g = gcd(width, height)
    return f"{width // g}:{height // g} ({ratio:.2f}:1)"

def run_ffprobe(video_path: str) -> Dict[str, Any]:
    """Execute ffprobe and retrieve stream/format JSON."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_streams",
        "-show_format",
        "-print_format", "json",
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffprobe failed: {e.stderr.strip()}")
    except FileNotFoundError:
        raise RuntimeError("ffprobe is not installed or not found in system PATH.")

def analyze_metadata(raw_data: Dict[str, Any], file_path: str) -> Dict[str, Any]:
    """Parse raw ffprobe output into clean video production metadata."""
    format_info = raw_data.get("format", {})
    streams = raw_data.get("streams", [])
    
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
    
    if not video_stream:
        raise ValueError("No video stream found in the specified file.")
        
    # Resolution
    width = int(video_stream.get("width", 0))
    height = int(video_stream.get("height", 0))
    aspect_ratio_label = calculate_aspect_ratio(width, height)
    
    # Frame rate
    fps_raw = video_stream.get("avg_frame_rate", "0/0")
    if fps_raw == "0/0" or not fps_raw:
        fps_raw = video_stream.get("r_frame_rate", "0/0")
    try:
        fps = float(Fraction(fps_raw)) if "/" in fps_raw else float(fps_raw)
    except ZeroDivisionError:
        fps = 0.0
        
    # Duration
    duration_str = video_stream.get("duration") or format_info.get("duration")
    duration = float(duration_str) if duration_str else 0.0
    
    # Total frames
    nb_frames = video_stream.get("nb_frames")
    if nb_frames and nb_frames.isdigit():
        total_frames = int(nb_frames)
    elif duration > 0 and fps > 0:
        total_frames = int(round(duration * fps))
    else:
        total_frames = 0
        
    # File size and bitrate
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    bitrate = int(format_info.get("bit_rate", 0)) if format_info.get("bit_rate") else 0
    
    metadata = {
        "file_path": os.path.abspath(file_path),
        "file_name": os.path.basename(file_path),
        "file_size_mb": round(file_size_mb, 2),
        "duration_seconds": round(duration, 3),
        "duration_timecode": format_seconds(duration),
        "width": width,
        "height": height,
        "resolution": f"{width}x{height}",
        "aspect_ratio": aspect_ratio_label,
        "frame_rate": round(fps, 3),
        "total_frames": total_frames,
        "video_codec": video_stream.get("codec_name", "unknown"),
        "pixel_format": video_stream.get("pix_fmt", "unknown"),
        "bit_rate_kbps": round(bitrate / 1000, 1) if bitrate else None,
        "has_audio": audio_stream is not None,
        "audio_info": {
            "codec": audio_stream.get("codec_name") if audio_stream else None,
            "sample_rate": audio_stream.get("sample_rate") if audio_stream else None,
            "channels": audio_stream.get("channels") if audio_stream else None,
        } if audio_stream else None
    }
    
    return metadata

def print_summary(meta: Dict[str, Any]):
    """Print an aesthetic, readable terminal summary of the video specifications."""
    print("=" * 64)
    print(f" VIDEO METADATA INSPECTION: {meta['file_name']}")
    print("=" * 64)
    print(f" Resolution        : {meta['resolution']} ({meta['aspect_ratio']})")
    print(f" Duration          : {meta['duration_timecode']} ({meta['duration_seconds']}s)")
    print(f" Frame Rate (FPS)  : {meta['frame_rate']} fps")
    print(f" Total Frames      : {meta['total_frames']} frames")
    print(f" Video Codec       : {meta['video_codec']} (Pixel format: {meta['pixel_format']})")
    print(f" File Size         : {meta['file_size_mb']} MB")
    if meta['bit_rate_kbps']:
        print(f" Bitrate           : {meta['bit_rate_kbps']} kbps")
    print(f" Audio Track       : {'Present (' + meta['audio_info']['codec'] + ')' if meta['has_audio'] else 'None (Silent)'}")
    print("-" * 64)
    print(" Production Recommendation:")
    if "16:9" in meta['aspect_ratio']:
        print(" - Remotion Composition : width: 1920, height: 1080 (or 3840x2160 for 4K)")
        print(" - Google Flow Aspect   : 16:9")
    elif "9:16" in meta['aspect_ratio']:
        print(" - Remotion Composition : width: 1080, height: 1920")
        print(" - Google Flow Aspect   : 9:16")
    elif "1:1" in meta['aspect_ratio']:
        print(" - Remotion Composition : width: 1080, height: 1080")
        print(" - Google Flow Aspect   : 1:1")
    else:
        print(f" - Remotion Composition : width: {meta['width']}, height: {meta['height']}")
        print(" - Google Flow Aspect   : Choose closest standard aspect ratio")
    print(f" - Recommended Remotion FPS : {int(round(meta['frame_rate'])) if meta['frame_rate'] > 0 else 30} fps")
    print("=" * 64)

def main():
    parser = argparse.ArgumentParser(description="Inspect video file and extract technical metadata for Remotion / Flow production.")
    parser.add_argument("video_path", help="Path to reference video file")
    parser.add_argument("--output-json", "-o", help="Optional path to write JSON metadata output", default=None)
    args = parser.parse_args()

    try:
        raw_data = run_ffprobe(args.video_path)
        metadata = analyze_metadata(raw_data, args.video_path)
        print_summary(metadata)
        
        if args.output_json:
            os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
            with open(args.output_json, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"\n[Saved JSON metadata to: {args.output_json}]")
            
    except Exception as e:
        print(f"Error inspecting video: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
