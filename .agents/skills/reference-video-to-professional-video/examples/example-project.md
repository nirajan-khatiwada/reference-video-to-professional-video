# End-to-End Example Project: "ApexTask SaaS Explainer"

This document showcases a complete, real-world execution of the **reference-video-to-professional-video** workflow inside Google Antigravity.

---

## 1. Project Overview & Reference Video Analysis

**Reference Video**: `samples/reference_task_app.mp4`  
- **Technical Specs**:
  - Resolution: `1920x1080` (16:9 Landscape)
  - Frame Rate: `30 fps`
  - Total Duration: `00:00:24.000` (720 frames)
  - Color Theme: Modern Dark Slate & Electric Indigo

### Execution of Analysis Helpers:
```bash
# 1. Technical inspection
python .agents/skills/reference-video-to-professional-video/scripts/inspect_video.py samples/reference_task_app.mp4

# 2. Extract keyframes at 2 fps for visual inspection
python .agents/skills/reference-video-to-professional-video/scripts/extract_frames.py samples/reference_task_app.mp4 --fps 2 --output-dir reference-assets/frames

# 3. Generate 4x4 contact sheets with timestamps
python .agents/skills/reference-video-to-professional-video/scripts/generate_contact_sheets.py --frames-dir reference-assets/frames --grid 4x4

# 4. Detect exact scene cuts
python .agents/skills/reference-video-to-professional-video/scripts/detect_scenes.py samples/reference_task_app.mp4 --save-stills
```

### Detected Scene Breakdown:
- **Scene 1** (`00:00 - 00:06`, 180 frames): Cinematic 3D backdrop + ApexTask app window spring reveal.
- **Scene 2** (`00:06 - 00:12`, 180 frames): Task board UI interaction, cursor dragging card from "In Progress" to "Completed", real-time progress bar filling.
- **Scene 3** (`00:12 - 00:18`, 180 frames): Analytics tab switch, velocity chart animating upward, metric badge showing "+34% Speed".
- **Scene 4** (`00:18 - 00:24`, 180 frames): Camera zooms back, glowing logo badge reveals with kinetic typography CTA.

---

## 2. Extracted Visual Design System (`src/designTokens.ts`)

```typescript
// Extracted via: python other_helpers.py palette --input reference-assets/frames/frame_00010.png
export const TOKENS = {
  colors: {
    primary: '#6366F1',       // Electric Indigo
    primaryHover: '#4F46E5',  // Deep Indigo
    background: '#0B0F19',    // Root dark canvas
    appChrome: '#111827',     // App window header & sidebar
    appSurface: '#1F2937',    // Task cards & panels
    border: '#374151',        // Dividers
    textPrimary: '#F9FAFB',   // High contrast white
    textMuted: '#9CA3AF',     // Slate gray labels
    accentSuccess: '#10B981', // Emerald badge
  },
  geometry: {
    windowRadius: 16,
    cardRadius: 10,
    buttonRadius: 8,
  },
  shadows: {
    window: '0 30px 60px -12px rgba(0, 0, 0, 0.75)',
    card: '0 8px 16px -4px rgba(0, 0, 0, 0.4)',
  },
} as const;
```

---

## 3. The 14-Field Storyboard (Scene 1 Excerpt)

1. **Scene Number**: Scene 01
2. **Start Timestamp**: `00:00:00.000` (Frame 0)
3. **End Timestamp**: `00:00:06.000` (Frame 180)
4. **Duration**: 6.0 seconds (180 frames)
5. **Scene Description**: Cinematic atmospheric tech background with subtle camera push-in. The ApexTask application window springs smoothly into the center of the frame, showing the active workspace.
6. **Visual Elements**: Dark indigo particle flow background (Google Flow), centered macOS-style window container (Remotion), traffic-light controls, left sidebar, active "Sprint 14" board.
7. **Text Displayed**: Heading: "Focus on What Moves the Needle", Subtitle: "ApexTask 2.0 Workspace".
8. **Required Animations**: Flow video plays in loop; Remotion app window enters with spring (`damping: 14, mass: 0.8`), scale `0.92 -> 1.0`, opacity `0 -> 1`.
9. **Transition Type**: Shared element zoom into Scene 02.
10. **Reference Frames**: `reference-assets/frames/frame_00001.png`, `frame_00012.png`.
11. **Reusable Components**: `<AppWindowContainer />`, `<FlowVideoLayer />`, `<KineticTitle />`.
12. **Production Tool**: **Hybrid (Flow + Remotion)**.
13. **Required Input Assets**: `public/assets/flow_tech_ambient.mp4`, `src/designTokens.ts`.
14. **Expected Output Assets**: `src/scenes/Scene01_Intro.tsx`.

---

## 4. Google Flow MCP Generation Prompt

To generate the atmospheric b-roll for Scene 01:

```json
{
  "mode": "flow-text-to-video",
  "prompt": "Cinematic slow forward camera movement through dark minimalist tech space with subtle floating electric indigo particle dust and soft volumetric lighting, anamorphic lens, photorealistic, 4k",
  "aspect_ratio": "16:9",
  "duration": "6",
  "image_model": "veo-3.1-quality",
  "wait": true
}
```

The resulting file is saved to `Downloads/flow/` and moved to `public/assets/flow_tech_ambient.mp4`.

---

## 5. Remotion Implementation (`src/scenes/Scene01_Intro.tsx`)

```tsx
import { AbsoluteFill, Video, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { TOKENS } from '../designTokens';

export const Scene01_Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 1. Spring physics for application window entrance
  const windowEntrance = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.8, stiffness: 110 },
  });

  const scale = interpolate(windowEntrance, [0, 1], [0.92, 1.0]);
  const opacity = interpolate(windowEntrance, [0, 1], [0, 1]);
  const translateY = interpolate(windowEntrance, [0, 1], [40, 0]);

  // 2. Continuous subtle camera zoom
  const cameraZoom = interpolate(frame, [0, 180], [1.0, 1.04]);

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.colors.background }}>
      {/* Background: Google Flow Cinematic B-Roll */}
      <AbsoluteFill style={{ transform: `scale(${cameraZoom})`, opacity: 0.4 }}>
        <Video
          src={staticFile('assets/flow_tech_ambient.mp4')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          muted
        />
      </AbsoluteFill>

      {/* Foreground: Pixel-Perfect Remotion App UI */}
      <AbsoluteFill
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          transform: `scale(${scale}) translateY(${translateY}px)`,
          opacity,
        }}
      >
        <div
          style={{
            width: 1400,
            height: 820,
            backgroundColor: TOKENS.colors.appChrome,
            borderRadius: TOKENS.geometry.windowRadius,
            boxShadow: TOKENS.shadows.window,
            border: `1px solid ${TOKENS.colors.border}`,
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          {/* Window Header */}
          <div style={{ height: 48, backgroundColor: '#0F172A', display: 'flex', alignItems: 'center', padding: '0 16px' }}>
            <div style={{ display: 'flex', gap: 8 }}>
              <div style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: '#EF4444' }} />
              <div style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: '#F59E0B' }} />
              <div style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: '#10B981' }} />
            </div>
            <span style={{ marginLeft: 20, color: TOKENS.colors.textMuted, fontSize: 13, fontFamily: 'Inter' }}>
              ApexTask 2.0 — Sprint 14
            </span>
          </div>

          {/* App Body Content */}
          <div style={{ flex: 1, backgroundColor: TOKENS.colors.appSurface, padding: 32 }}>
            <h1 style={{ color: TOKENS.colors.textPrimary, fontSize: 32, fontFamily: 'Inter', margin: 0 }}>
              Focus on What Moves the Needle
            </h1>
            <p style={{ color: TOKENS.colors.textMuted, fontSize: 16, fontFamily: 'Inter', marginTop: 8 }}>
              Real-time collaboration across engineering, design, and product.
            </p>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

---

## 6. Rendering Command (Silent Video)

```bash
# Preview first in Studio
npx remotion studio --no-open

# Render silent MP4
npx remotion render src/index.ts Main out/apextask_promo.mp4 --gl=angle
```

---

## 7. Standalone Nepali Voiceover Script (`nepali-voiceover-script.md`)

```markdown
# ApexTask SaaS - Official Nepali Voiceover Script (नेपाली भ्वाइसओभर)

> Note: For external voice recording only. Not embedded into video audio.

---

### दृश्य १ — ००:०० देखि ००:०६ (६ सेकेन्ड)
**भिजुअल**: ३D टेक ब्याकड्रप र ApexTask एप विन्डोको सहज इन्ट्री  
**नेपाली संवाद**:  
"के तपाईंको टिम अझै पनि कामको प्राथमिकीकरण र डेडलाइन म्यानेजमेन्टमा अलमलिएको छ? अब चिन्ता छोड्नुहोस्!"

---

### दृश्य २ — ००:०६ देखि ००:१२ (६ सेकेन्ड)
**भिजुअल**: सहज ड्र्याग-एन्ड-ड्रप टास्क बोर्ड र रियल-टाइम प्रोग्रेस  
**नेपाली संवाद**:  
"ApexTask सँग काम असाइन गर्नुहोस्, प्रगति ट्र्याक गर्नुहोस्, र एकै क्लिकमा सम्पूर्ण टास्क सम्पन्न गर्नुहोस्।"

---

### दृश्य ३ — ००:१२ देखि ००:१८ (६ सेकेन्ड)
**भिजुअल**: स्मार्ट एनालिटिक्स चार्ट र ३४% गति वृद्धिको मेट्रिक ब्याच  
**नेपाली संवाद**:  
"स्मार्ट डेटा एनालिटिक्सले दिन्छ तपाईंको टिमको कार्यक्षमतामा ३४ प्रतिशत भन्दा बढी सुधार।"

---

### दृश्य ४ — ००:१८ देखि ००:२४ (६ सेकेन्ड)
**भिजुअल**: लोगो एनिमेसन र कल-टु-एक्सन स्क्रिन  
**नेपाली संवाद**:  
"आजै आफ्नो टिमलाई स्मार्ट बनाउनुहोस्। ApexTask अहिले नै सुरु गर्नुहोस्, पूर्ण रूपमा निःशुल्क!"
```
