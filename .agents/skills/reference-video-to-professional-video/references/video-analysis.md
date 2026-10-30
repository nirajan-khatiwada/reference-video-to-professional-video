# Reference Video Analysis Guide

This guide establishes the systematic, frame-by-frame methodology for reverse-engineering any reference video inside Google Antigravity.

---

## 1. Systematic Batch Inspection

Never rely on glancing at a video or picking 2–3 arbitrary frames. High-end video production demands rigorous inspection of:
- **Spatial layout**: Where elements enter, sit, and exit.
- **Temporal dynamics**: Exact onset, duration, acceleration, and deceleration of animations.
- **Persistence**: Distinguishing persistent UI components from transient motion effects.

### Workflow
1. **Technical Inspection**: Run `python scripts/inspect_video.py <video_path>` to establish the canvas geometry (resolution, aspect ratio, native fps, duration).
2. **Keyframe Extraction**: Run `python scripts/extract_frames.py <video_path> --fps 2` (or `--all` for fast kinetic segments).
3. **Contact Sheet Generation**: Run `python scripts/generate_contact_sheets.py --frames-dir <frames_dir> --grid 4x4`.
4. **Boundary Detection**: Run `python scripts/detect_scenes.py <video_path> --save-stills`.

---

## 2. Frame-by-Frame Observation Protocol

For every scene detected, analyze the frame sequence against four core questions:

### A. What happens in each frame?
- What visual elements occupy the screen?
- What text is displayed? What is its typographical hierarchy?
- Is there an underlying application interface, a 3D mock, or a cinematic backdrop?

### B. What changes between consecutive frames?
- Detect movement vectors: translation ($X, Y$), scale, rotation, opacity, blur.
- Measure keyframe intervals:
  $$\text{Duration (seconds)} = \frac{\text{End Frame} - \text{Start Frame}}{\text{FPS}}$$
- Identify the easing curve:
  - **Linear**: Constant velocity (rare in premium video; used for infinite ticker loops or constant marquee).
  - **Ease-Out / Spring**: Explosive entry decelerating smoothly into place (standard for UI windows and cards).
  - **Anticipation / Overshoot**: Spring animation passing the target by $5\text{–}10\%$ and settling back (modern product videos).

### C. Which elements remain consistent?
- In app demonstration videos, note which interface chrome (navigation bars, sidebars, search bars, account avatars, window frame bezels) stays anchored.
- Background gradients, lighting direction, and ambient shadows.

### D. Which elements are introduced or dismissed?
- Identify trigger events: mouse cursor hover, modal pop-in, dropdown expansion, toast notification.
- Exit transitions: fade-out, slide-down, blur dissipation, camera cut.

---

## 3. Motion & Camera Analysis

### Camera Movements
Categorize programmatic camera actions:
- **Slow Push-In (Dolly Zoom)**: Scale increases from $1.0 \rightarrow 1.08$ over 3–5 seconds to sustain viewer focus.
- **Whip Pan / Tracking Shot**: Rapid horizontal translation ($X: 0 \rightarrow -800\text{px}$) with directional motion blur.
- **Perspective Tilt (Isometric / 3D Look)**: CSS `transform: perspective(1000px) rotateX(15deg) rotateY(-10deg)`.

### Transition Mechanics
Document the cut technique between scenes:
- **Hard Cut**: Clean instantaneous transition at beat drop or scene boundary.
- **Morph / Shared Element**: A card or icon in Scene A scales up to become the container of Scene B.
- **Directional Slide**: Scene A pushes out while Scene B slides in synchronously.
- **Alpha Mask / Stash Wipe**: Contrast wipe or geometric sweep.

---

## 4. Documentation Output

Synthesize findings into `scene-analysis.md` and `storyboard.md` before writing code or prompting Google Flow.
