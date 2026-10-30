# Master Video Production Plan

**Project Name:** [Project Title]  
**Creation Date:** [YYYY-MM-DD]  
**Lead Agent / Director:** Antigravity AI  
**Target Delivery Status:** [Draft / Storyboard Complete / Production / Final Verification]

---

## 1. Technical Specifications
- **Master Resolution**: `1920x1080` (1080p Full HD) or `3840x2160` (4K UHD)
- **Aspect Ratio**: `16:9` (Widescreen) or `9:16` (Vertical Reels/Shorts)
- **Target Frame Rate**: `30 fps` (or `60 fps` for extreme kinetic UI)
- **Total Duration**: `[XX]` seconds (`[YY]` frames)
- **Audio Output**: **Strictly Silent** (Voiceover forbidden in render)
- **Companion Audio Script**: Standalone Nepali Voiceover Markdown

---

## 2. Visual Identity & Design System
- **Primary Color**: `[Hex Code]`
- **Secondary Color**: `[Hex Code]`
- **Background Color**: `[Hex Code]`
- **Surface / Card Color**: `[Hex Code]`
- **Accent / Metric Color**: `[Hex Code]`
- **Font Families**:
  - Headings / Display: `[e.g. Inter / Geist / SF Pro Display]`
  - Body / Code: `[e.g. JetBrains Mono]`
- **Corner Radii**: Cards (`12px`), Window (`16px`), Buttons (`8px`)
- **Animation Physics**: Damping `15`, Mass `0.8`, Stiffness `100`

---

## 3. Tool Allocation & Responsibility Summary

| Production Domain | Assigned Tool | Specific Deliverables |
| :--- | :--- | :--- |
| **Video Pre-Analysis** | FFmpeg + Helper Scripts | Metadata JSON, contact sheets, detected scene cuts |
| **UI Recreation & Motion** | Remotion | App window chrome, dashboard cards, metric animations |
| **Kinetic Titles & Text** | Remotion | Heading typography, subtitle reveals, badge counters |
| **Cinematic B-Roll** | Google Flow MCP (`veo-3.1-quality`) | Atmospheric background loops, real-world scenes |
| **Final Assembly & Rendering** | Remotion CLI | Silent master MP4 composition render |
| **Voiceover Scripting** | Standalone Documentation | Scene-timed Nepali Devanagari voiceover script |

---

## 4. Production Milestones & Execution Checklist

- [ ] **Phase 1: Video Inspection & Frame Analysis**
  - Run `inspect_video.py` and review technical geometry.
  - Run `extract_frames.py` and export keyframe batches.
  - Run `generate_contact_sheets.py` for visual inspection.
  - Run `detect_scenes.py` to map cut boundaries.
- [ ] **Phase 2: Design Token Extraction & Component Library**
  - Run `other_helpers.py palette` and document color roles.
  - Generate `src/designTokens.ts`.
  - Build reusable UI components (`AppWindow`, `SidebarNav`, `MetricCard`).
- [ ] **Phase 3: Storyboard & Script Approval**
  - Complete 14-field scene storyboard.
  - Draft standalone Nepali voiceover script in Devanagari.
- [ ] **Phase 4: Generative Footage Generation**
  - Verify Flow connection via `flow_status`.
  - Invoke `flow_generate` for cinematic background clips.
  - Ingest clips into Remotion `public/` directory.
- [ ] **Phase 5: Remotion Scene Construction & Studio Preview**
  - Code individual scene components in `src/scenes/`.
  - Assemble timeline in `src/compositions/MainVideo.tsx`.
  - Launch `npx remotion studio --no-open` to preview and refine timing.
- [ ] **Phase 6: Final Verification & Silent Video Render**
  - Render silent MP4 via `npx remotion render`.
  - Confirm video has no voice tracks.
  - Confirm companion Nepali script matches final scene timecodes.
