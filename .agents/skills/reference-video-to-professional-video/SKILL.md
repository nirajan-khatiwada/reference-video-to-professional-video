---
name: reference-video-to-professional-video
description: Autonomous end-to-end professional video production system for Google Antigravity. Thoroughly analyzes reference videos frame-by-frame, extracts visual design systems and reusable UI assets, builds 14-field production storyboards, orchestrates programmatic Remotion animations and Google Flow MCP cinematic footage, renders silent videos, and generates separate natural Nepali voiceover scripts.
---

# Reference Video to Professional Video Production Skill

This skill automates the complete lifecycle of reverse-engineering any reference video, extracting its design language and reusable UI assets, creating a 14-field production storyboard, and producing an exceptional new video combining **Remotion** (for pixel-perfect UI and motion graphics) and **Google Flow MCP** (for cinematic AI b-roll and atmospheric footage).

---

## 🎯 Activation Triggers

Activate this skill when:
- The user provides or uploads a reference video file (e.g. `.mp4`, `.mov`, `.webm`).
- The user triggers `/reference-video-to-professional-video`.
- The user asks to:
  - "Analyze this reference video"
  - "Recreate / reproduce this video using Remotion and Flow"
  - "Turn this video into a professional app promo"
  - "Extract the visual design system from this video"
  - "Create a video production storyboard and generate the video"

---

## 🛠️ Included Production Tooling

All helper scripts reside in `./scripts/` within this skill:

| Script | Purpose | Key Commands |
| :--- | :--- | :--- |
| `inspect_video.py` | Extracts resolution, aspect ratio, frame rate, duration, and codecs. | `python scripts/inspect_video.py <video> -o metadata.json` |
| `extract_frames.py` | Extracts ordered frames with timestamp metadata and compiles `index.json`. | `python scripts/extract_frames.py <video> --fps 2 -o reference-assets/frames` |
| `generate_contact_sheets.py` | Builds 4x4 visual contact sheets with timestamps for systematic batch inspection. | `python scripts/generate_contact_sheets.py --frames-dir reference-assets/frames --grid 4x4` |
| `detect_scenes.py` | Detects cuts and scene boundaries; extracts keyframe stills. | `python scripts/detect_scenes.py <video> --save-stills -o scenes.json` |
| `other_helpers.py` | Extracts color palettes, crops UI components, and exports TypeScript design tokens. | `python other_helpers.py palette -i <frame>`<br>`python other_helpers.py tokens -c "<hex_list>"` |

---

## 📋 Comprehensive 8-Step Production Workflow

```
[REFERENCE VIDEO]
       │
       ▼
[STEP 1: Full Video Analysis] ────► inspect_video.py + extract_frames.py + contact sheets + detect_scenes.py
       │
       ▼
[STEP 2: Extract Design System] ──► Typography, Colors, Radii, Shadows, "Same App" Invariant -> designTokens.ts
       │
       ▼
[STEP 3: Reusable Assets & UI] ───► Crop reference frames -> Build modular Remotion components
       │
       ▼
[STEP 4: Engine Responsibility] ──► Remotion (UI/Text/Motion) vs Google Flow MCP (Cinematic/Atmospheric)
       │
       ▼
[STEP 5: 14-Field Storyboard] ────► Complete scene breakdown with timings, transitions & assets
       │
       ▼
[STEP 6: Video Generation] ───────► Flow b-roll + Remotion compositions + Studio preview + Final render
       │
       ▼
[STEP 7: Audio Rule Enforced] ────► MANDATORY SILENT VIDEO (Zero AI narration or vocals in render)
       │
       ▼
[STEP 8: Standalone Nepali VO] ───► Scene-timed Devanagari script saved as companion document
```

---

### STEP 1 — Complete Video Analysis
Whenever a reference video is provided, conduct forensic analysis rather than glancing at random frames:

1. **Technical Inspection**:
   ```bash
   python .agents/skills/reference-video-to-professional-video/scripts/inspect_video.py <video_path> --output-json metadata.json
   ```
   Determine exact canvas dimensions (16:9, 9:16, 1:1), native framerate, total duration, and bitrates.
2. **Frame Extraction**:
   ```bash
   python .agents/skills/reference-video-to-professional-video/scripts/extract_frames.py <video_path> --fps 2 --output-dir reference-assets/frames
   ```
   Preserves frame order and generates `index.json` mapping frame numbers to exact timestamps.
3. **Contact Sheet Batching**:
   ```bash
   python .agents/skills/reference-video-to-professional-video/scripts/generate_contact_sheets.py --frames-dir reference-assets/frames --grid 4x4
   ```
   Inspect frames systematically in 16-frame batches with timecode badges to identify exact animation onsets and transitions.
4. **Scene Boundary Detection**:
   ```bash
   python .agents/skills/reference-video-to-professional-video/scripts/detect_scenes.py <video_path> --save-stills --output-json scenes.json
   ```
5. **Frame-by-Frame Observation**:
   - What happens in each frame?
   - What changes between consecutive frames?
   - How does each scene progress?
   - Which elements remain consistent vs introduced or removed?
   - How do animations (springs, fades, camera moves) behave?
   - See [references/video-analysis.md](references/video-analysis.md).

---

### STEP 2 — Extract the Visual Design System
Synthesize the reference's complete aesthetic into structured, reusable tokens:

1. **Typography**: Font families (display vs code), weights, font sizes, text hierarchy, letter spacing, line height.
2. **Colors & Theme**: Primary, secondary, background, surface, gradients, and semantic accent colors. Extract using:
   ```bash
   python .agents/skills/reference-video-to-professional-video/scripts/other_helpers.py palette --input reference-assets/frames/frame_00001.png
   ```
3. **Geometry & Styling**: Padding, margin grid, borders, drop shadows, and corner radii.
4. **Motion Curves**: Damping, stiffness, mass, and transition durations.
5. **Enforce Design Tokens**: Run `other_helpers.py tokens` to generate `src/designTokens.ts`.
6. **The "Single Application" Invariant**:
   > [!IMPORTANT]
   > When the reference shows an application, preserve the identity of that **same application** across every scene. It must look like one cohesive, production-grade product throughout—not inconsistent, unrelated templates.
   > See [references/visual-consistency.md](references/visual-consistency.md).

---

### STEP 3 — Create Reusable Reference Frames & Assets
1. Organize keyframes into `reference-assets/`.
2. Crop specific UI components (navigation bar, search bar, metric card, modal dialog) using:
   ```bash
   python .agents/skills/reference-video-to-professional-video/scripts/other_helpers.py crop --image reference-assets/frames/frame_00020.png --box 120 40 1200 64 --output reference-assets/components/navbar.png
   ```
3. Build modular React/Remotion components (`<AppWindow />`, `<SidebarNav />`, `<MetricCard />`, `<KineticTitle />`) that share the master design tokens.
4. Do not recreate the same component from scratch in each scene.

---

### STEP 4 — Remotion vs Google Flow Responsibility Matrix
Before generating any media, explicitly allocate tasks according to core technology strengths:

#### A. Remotion (Programmatic Precision)
- Application UI demonstrations & screen recreations.
- UI interactions (cursor movement, clicks, toggles).
- Text, kinetic typography, titles, subtitles, and badges.
- Motion graphics, SVG animations, and dynamic data counters.
- Programmatic camera moves (zoom push-in, pan, tilt).
- Master timeline sequencing, transitions, and final MP4 rendering.
- Consult the installed [remotion-best-practices](../remotion-best-practices/SKILL.md) skill.

#### B. Google Flow MCP (Cinematic AI Footage)
- Cinematic b-roll, atmospheric 3D backgrounds, and glowing particle environments.
- Real-world human contexts (engineers collaborating, office daylight scenes).
- Natural physics, fluid lighting, and outdoor drone shots.
- Use authentic `flow-connector` MCP tools:
  - `flow_status`: Verify automation bridge and logged-in browser tab.
  - `flow_generate`: Execute text-to-video (`veo-3.1-quality`), frame-to-video (`veo-3.1-fast`), or stills (`nano-banana-pro`).
  - `flow_get_job` / `flow_list_jobs`: Monitor generations.
  - See [references/google-flow-workflow.md](references/google-flow-workflow.md).

#### C. Hybrid Production
- Combine Flow footage as background layers (`<Video src={...} />`) with Remotion UI components overlaid on top.
- Apply subtle radial dark vignettes in Remotion to ensure UI text readability.
- **CRITICAL RESTRICTION**: Never use AI generative video to render readable application UI, exact text, buttons, or dashboard metrics. Remotion must always generate these elements.

---

### STEP 5 — Build a Complete 14-Field Production Storyboard
Before coding compositions, build the complete scene storyboard using `templates/storyboard.md`. Every scene must specify all 14 mandatory fields:

1. **Scene Number**: (e.g. Scene 01)
2. **Start Timestamp**: (e.g. `00:00:00.000` / Frame 0)
3. **End Timestamp**: (e.g. `00:00:06.000` / Frame 180)
4. **Duration**: (e.g. 6.0 seconds)
5. **Scene Description**: Clear narrative explanation of the user journey.
6. **Visual Elements**: Foreground UI, background elements, badges, cards.
7. **Text Displayed**: Exact title, subtitle, and UI text.
8. **Required Animations**: Entrance physics, active counter animations, exit transitions.
9. **Transition Type**: Cut, slide, shared element morph, zoom-blur.
10. **Reference Frames**: Filenames from `reference-assets/frames/`.
11. **Reusable Components**: Component tags used in the scene.
12. **Production Tool**: **Remotion**, **Google Flow MCP**, or **Hybrid**.
13. **Required Input Assets**: Image paths, Flow video files, tokens.
14. **Expected Output Assets**: Remotion scene component and test clip.

---

### STEP 6 — Video Generation & Composition
1. Initialize or inspect the Remotion project structure (see [references/remotion-workflow.md](references/remotion-workflow.md)).
2. Generate required cinematic footage via `flow_generate` and copy downloaded MP4s into `public/assets/`.
3. Construct modular UI components and scene components under `src/scenes/`.
4. Assemble all sequences in `src/compositions/MainVideo.tsx` using `<Sequence>` and `<AbsoluteFill>`.
5. Preview composition interactively in Remotion Studio:
   ```bash
   npx remotion studio --no-open
   ```
6. Render the master video:
   ```bash
   npx remotion render src/index.ts Main out/final_video.mp4 --gl=angle
   ```
7. Do not stop at documentation or storyboard—execute the actual production and rendering.

---

### STEP 7 — Audio Restrictions (MANDATORY SILENCE)
> [!CAUTION]
> **DO NOT ADD ANY VOICE TO THE VIDEO.**
> - No AI narration.
> - No voiceover.
> - No spoken dialogue.
> - No generated speech.
> - No vocals.
>
> The default rendered video must be **completely silent**. Do NOT generate or insert a Nepali voiceover into the video file or composition audio tracks.

---

### STEP 8 — Standalone Nepali Voiceover Script
Generate the Nepali voiceover script as a **separate text/markdown file** (e.g. `nepali-voiceover-script.md`) using `templates/nepali-voiceover.md`.

**Requirements**:
- Authentic **Nepali Devanagari** (`नेपाली देवनागरी`).
- Natural, modern, conversational promotional tone.
- Attention-grabbing opening hook.
- Explains core features, benefits, and actions shown on screen.
- Follows the exact scene order and timestamps of the final video:
  ```markdown
  ### दृश्य १ — ००:००–००:०५ (५ सेकेन्ड)
  **भिजुअल**: एप विन्डो इन्ट्री र मुख्य समस्याको उठान
  **नेपाली संवाद**: [स्वाभाविक, व्यावसायिक नेपाली संवाद]
  ```
- Includes an effective closing and clear call to action.
- Must remain a standalone document—never embedded into the rendered video audio.

---

## 📁 Repository Directory Structure

```
reference-video-to-professional-video/
├── SKILL.md                          # Main entry point & workflow router
├── scripts/
│   ├── inspect_video.py              # ffprobe video geometry extractor
│   ├── extract_frames.py             # FFmpeg frame extractor & index builder
│   ├── generate_contact_sheets.py    # Pillow-based 4x4 visual contact sheets
│   ├── detect_scenes.py              # FFmpeg scene boundary & cut detector
│   └── other_helpers.py              # Palette extractor, UI cropper & token generator
├── references/
│   ├── video-analysis.md             # Deep frame-by-frame analysis guide
│   ├── visual-consistency.md         # Single application identity preservation
│   ├── remotion-workflow.md          # Remotion composition, spring physics & render
│   ├── google-flow-workflow.md       # Flow MCP integration, models & prompt formulas
│   └── production-guidelines.md      # Matrix, silent audio rule & QA standards
├── templates/
│   ├── storyboard.md                 # 14-field scene-by-scene storyboard template
│   ├── production-plan.md            # Technical specs & milestone checklist
│   ├── scene-analysis.md             # Forensic scene inspection protocol
│   └── nepali-voiceover.md           # Standalone Nepali Devanagari script template
└── examples/
    └── example-project.md            # Complete end-to-end walkthrough project
```

---

## ✅ Quality Assurance Verification

Before marking completion:
- [ ] Technical video metadata inspected via `inspect_video.py`.
- [ ] Keyframes extracted and visual contact sheets generated.
- [ ] Scene cuts mapped and visual identity documented.
- [ ] Application identity verified consistent across all scenes.
- [ ] Remotion vs Google Flow responsibilities strictly demarcated.
- [ ] 14-field storyboard completed.
- [ ] Final video rendered silently without voice or narration.
- [ ] Separate companion Nepali Devanagari voiceover script delivered.
