#!/usr/bin/env python3
"""
detect_scenes.py - Scene Boundary and Cut Detector for Reference Videos

Uses FFmpeg's internal scene detection engine (select='gt(scene,THRESHOLD)') to:
- Detect exact cut points, scene changes, and visual shifts.
- Break down the video into distinct scenes with start, end, and duration.
- Export keyframe thumbnails representing each scene.
- Save a structured scenes.json file for storyboard mapping.

Usage:
    python detect_scenes.py path/to/video.mp4
    python detect_scenes.py path/to/video.mp4 --threshold 0.35 --save-stills
"""

import sys
import os
import re
import json
import subprocess
import argparse
from typing import List, Dict, Any

def format_timecode(seconds: float) -> str:
    """Format seconds into HH:MM:SS.mmm."""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:06.3f}"

def get_video_duration(video_path: str) -> float:
    """Retrieve total duration using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-print_format", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def detect_cuts(video_path: str, threshold: float = 0.35) -> List[float]:
    """Run FFmpeg showinfo with scene detection to find cut timestamps."""
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-filter:v", f"select='gt(scene,{threshold})',showinfo",
        "-f", "null",
        "-"
    ]
    
    print(f"Analyzing scene boundaries (threshold={threshold})...")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    cuts = []
    # Match patterns like: pts_time:12.3456
    pattern = re.compile(r"pts_time:([0-9\.]+)")
    for line in proc.stderr.splitlines():
        if "showinfo" in line:
            match = pattern.search(line)
            if match:
                cut_sec = float(match.group(1))
                if not cuts or (cut_sec - cuts[-1] >= 0.5): # Minimum 0.5s scene threshold
                    cuts.append(cut_sec)
                    
    return cuts

def compile_scenes(cuts: List[float], total_duration: float, min_scene_duration: float = 0.4) -> List[Dict[str, Any]]:
    """Assemble cut timestamps into continuous scenes."""
    boundaries = [0.0] + [c for c in cuts if c < total_duration] + [total_duration]
    # Deduplicate closely spaced cuts
    cleaned = [boundaries[0]]
    for b in boundaries[1:]:
        if b - cleaned[-1] >= min_scene_duration:
            cleaned.append(b)
            
    if cleaned[-1] < total_duration:
        cleaned[-1] = total_duration

    scenes = []
    for idx in range(len(cleaned) - 1):
        st = cleaned[idx]
        et = cleaned[idx + 1]
        dur = et - st
        scenes.append({
            "scene_number": idx + 1,
            "start_time": round(st, 3),
            "end_time": round(et, 3),
            "duration": round(dur, 3),
            "start_timecode": format_timecode(st),
            "end_timecode": format_timecode(et),
            "midpoint_time": round(st + (dur / 2.0), 3)
        })
    return scenes

def extract_scene_thumbnail(video_path: str, timestamp: float, output_path: str):
    """Extract a representative keyframe still at the scene midpoint."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(timestamp),
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

def main():
    parser = argparse.ArgumentParser(description="Detect scenes and cut transitions in reference videos.")
    parser.add_argument("video_path", help="Path to video file")
    parser.add_argument("--threshold", "-t", type=float, default=0.35, help="Scene detection sensitivity (0.1 to 0.6, default: 0.35)")
    parser.add_argument("--min-duration", type=float, default=0.5, help="Minimum scene duration in seconds (default: 0.5)")
    parser.add_argument("--output-json", "-o", default=None, help="Path to write scenes.json")
    parser.add_argument("--save-stills", action="store_true", help="Extract a keyframe thumbnail for each scene")
    parser.add_argument("--stills-dir", default="reference-assets/scene_stills", help="Directory for keyframe stills")

    args = parser.parse_args()
    
    if not os.path.exists(args.video_path):
        print(f"Error: File not found: {args.video_path}", file=sys.stderr)
        sys.exit(1)
        
    duration = get_video_duration(args.video_path)
    cuts = detect_cuts(args.video_path, threshold=args.threshold)
    scenes = compile_scenes(cuts, duration, min_scene_duration=args.min_duration)
    
    if args.save_stills:
        os.makedirs(args.stills_dir, exist_ok=True)
        for scene in scenes:
            still_name = f"scene_{scene['scene_number']:02d}.jpg"
            still_path = os.path.join(args.stills_dir, still_name)
            try:
                extract_scene_thumbnail(args.video_path, scene["midpoint_time"], still_path)
                scene["thumbnail"] = still_path.replace("\\", "/")
            except Exception as e:
                print(f"Warning: Failed to extract thumbnail for Scene {scene['scene_number']}: {e}", file=sys.stderr)
                
    # Display scene timeline
    print("\n" + "=" * 68)
    print(f" DETECTED SCENE BREAKDOWN (Total Scenes: {len(scenes)})")
    print("=" * 68)
    for sc in scenes:
        thumb_info = f" [Still: {sc['thumbnail']}]" if "thumbnail" in sc else ""
        print(f" Scene {sc['scene_number']:02d}: {sc['start_timecode']} -> {sc['end_timecode']} (Duration: {sc['duration']:0.2f}s){thumb_info}")
    print("=" * 68)
    
    out_json = args.output_json or os.path.join(os.path.dirname(args.video_path) or ".", "scenes.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "source_video": os.path.abspath(args.video_path),
            "total_duration": round(duration, 3),
            "scene_count": len(scenes),
            "scenes": scenes
        }, f, indent=2)
    print(f"\n[Saved Scene Manifest] JSON written to: {out_json}")

if __name__ == "__main__":
    main()
