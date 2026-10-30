# Production Guidelines, Responsibilities & Delivery Standards

This document establishes the official quality standards, role distribution, audio policies, and verification criteria for video production under this skill.

---

## 1. Production Responsibility Matrix

Every visual asset and scene element is strictly assigned according to the optimal technology:

| Video Element | Assigned Engine | Rationale |
| :--- | :--- | :--- |
| **Application UI & Dashboards** | **Remotion** | Must be pixel-perfect, vector-crisp, and identical across all scenes. |
| **Accurate App Screenshots / Recreations** | **Remotion** | Exact layout, fonts, icons, tables, and brand components. |
| **UI Interactions & Cursor Clicks** | **Remotion** | Precise programmatic timing and natural spring physics. |
| **Kinetic Typography & Titles** | **Remotion** | Clean text rendering, custom web fonts, and timed character animations. |
| **Motion Graphics & Overlays** | **Remotion** | Smooth 60fps transitions, badges, tooltips, and lower thirds. |
| **Data Visualizations & Sparklines** | **Remotion** | SVG path interpolation and dynamic numeric counters. |
| **Programmatic Camera Pans / Zooms** | **Remotion** | High-precision CSS transform scaling and camera rigs. |
| **Master Timeline & Final Rendering** | **Remotion** | Frame-accurate sequence assembly and MP4 rendering. |
| **Cinematic Real-World B-Roll** | **Google Flow MCP** | Photorealistic lighting, human actors, and physical environments. |
| **Atmospheric Backgrounds & Textures** | **Google Flow MCP** | Abstract 3D light streams, glowing particles, and fluid motions. |
| **Lifestyle & Storytelling Sequences** | **Google Flow MCP** | Contextual footage (e.g. users working in coffee shops or offices). |
| **Hybrid Scenes (Flow B-Roll + UI)** | **Hybrid (Flow + Remotion)** | Flow renders background footage; Remotion renders UI overlay on top. |

> [!CAUTION]
> **Cardinal Rule**: Never use Google Flow AI video generation for readable software interfaces, text headers, buttons, or charts. Remotion must always generate these elements.

---

## 2. Audio Policies (MANDATORY RESTRICTIONS)

### The Default Final Video Must Be Silent
- **NO AI Narration**: Do not run text-to-speech tools to generate voice tracks for the video.
- **NO Voiceover**: Do not insert voice recordings into Remotion compositions or FFmpeg audio streams.
- **NO Spoken Dialogue or Vocals**: The rendered video file (`.mp4`) must be completely voice-free.
- **Default Render**: The master video delivery must be **silent**.

---

## 3. Separate Nepali Voiceover Scripting Standard

The Nepali voiceover script is generated **exclusively as a standalone companion document** (e.g., `nepali-voiceover-script.md`). It is intended for subsequent human voice recording or manual dubbing.

### Script Quality Requirements:
1. **Language & Script**: Standard Nepali written in authentic **Devanagari** (`नेपाली देवनागरी`).
2. **Tone**: Professional, conversational, modern, and engaging. Avoid robotic, literal translations from English or overly archaic formal phrasing.
3. **Pacing & Timing**: Each spoken line must match the exact duration of its corresponding scene in the final video.
4. **Structure**:
   - **Scene 1 (Hook)**: Attention-grabbing opening statement highlighting a core user pain point or breakthrough solution.
   - **Body Scenes (Features)**: Clear, enthusiastic walkthrough of the actions and benefits shown on screen.
   - **Final Scene (Call to Action)**: Compelling closing invitation (e.g., sign up, start free trial, download).

### Standard Script Format:
```markdown
# [Project Name] - Official Nepali Voiceover Script (Standalone)

> [!NOTE]
> This script is for external voice recording only. It is NOT embedded into the rendered video.

---

### Scene 1 — 00:00–00:05 (Duration: 5s)
**Visual**: Cinematic hook & app window reveal  
**Nepali Dialogue**:  
"के तपाईंको टिम अझै पनि छरपस्ट डेटा र ढिलो रिपोर्टिङबाट हैरान छ? अब समय बदलिएको छ!"

---

### Scene 2 — 00:05–00:12 (Duration: 7s)
**Visual**: Real-time analytics dashboard & instant sync  
**Nepali Dialogue**:  
"हेर्नुहोस्, कसरी केवल एक क्लिकमा तपाईंको सम्पूर्ण बिजनेस मेट्रिक्स रियल-टाइममा अपडेट हुन्छ। कुनै झन्झट बिना, एकदमै सहज!"

---

### Scene 3 — 00:12–00:18 (Duration: 6s)
**Visual**: AI automated insights & chart generation  
**Nepali Dialogue**:  
"स्मार्ट AI ले तपाईंको डेटा विश्लेषण गर्छ र आगामी निर्णयहरूका लागि स्पष्ट योजना तयार पार्छ।"

---

### Scene 4 — 00:18–00:24 (Duration: 6s)
**Visual**: Final call-to-action & brand logo  
**Nepali Dialogue**:  
"आजै आफ्नो कामलाई नयाँ उचाइमा पुर्‍याउनुहोस्। अहिले नै सुरु गर्नुहोस्, पूर्ण रूपमा निःशुल्क!"
```

---

## 4. Final Quality Assurance Checklist

Before declaring any video production task complete, verify every item:

- [ ] **Frame Inspection Verified**: All frames analyzed using contact sheets and scene detection scripts.
- [ ] **Single Application Invariant**: All scenes featuring the UI share identical design tokens, colors, fonts, and window styling.
- [ ] **Responsibility Matrix Respected**: UI generated in Remotion; generative footage generated in Flow MCP.
- [ ] **No Hallucinated Tool Calls**: Only authentic MCP tools (`flow_generate`, `flow_status`, etc.) invoked.
- [ ] **Silent Video Verified**: Master rendered `.mp4` contains zero voice tracks or narration.
- [ ] **Separate Nepali Script Delivered**: Complete Devanagari script provided with scene timestamps matching the final cut.
- [ ] **Render Integrity**: Video renders without dropped frames, visual tearing, or font fallbacks.
