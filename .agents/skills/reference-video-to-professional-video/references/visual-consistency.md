# Visual Consistency & Application Identity Protocol

One of the most critical failures in AI-assisted video production is **interface drifting**: where Scene 1 shows a dark sleek dashboard, Scene 2 shows a generic light template, and Scene 3 shows an entirely different button and font style.

This protocol enforces strict, immutable visual identity across all scenes.

---

## 1. The "Single Application" Invariant

When reproducing or improving an application video:
> **The viewer must believe they are watching a single, cohesive, production-grade software application from frame 0 to the final frame.**

### Non-Negotiable Consistency Rules:
1. **Identical Chrome**: The primary app window frame, title bar (traffic light dots or minimize/maximize controls), sidebar navigation, and user header must remain strictly consistent across all scenes where the interface appears.
2. **Unified Color Palette**: Never allow buttons in Scene 1 to be `#3B82F6` and in Scene 2 to be `#8B5CF6` unless intentionally highlighting a distinct sub-brand feature. Use single-source design tokens.
3. **Exact Typography**: Heading font family, weight, tracking, and anti-aliasing must match across all title cards and UI surfaces.
4. **Consistent Elevation & Radius**: If dashboard cards use `border-radius: 12px` and `box-shadow: 0 10px 25px rgba(0,0,0,0.3)`, this exact token must apply to all modals, popovers, and detail panels.

---

## 2. Extracting & Enforcing Design Tokens

Use `scripts/other_helpers.py tokens` to generate a centralized `designTokens.ts` file in the Remotion project.

### Token Architecture:
```typescript
// src/designTokens.ts
export const TOKENS = {
  colors: {
    primary: '#3B82F6',       // Main CTA, active states, key data curves
    secondary: '#1D4ED8',     // Hover states, secondary accents
    background: '#0B0F19',    // Video root canvas & outer backdrop
    appBackground: '#111827', // Application interior canvas
    surface: '#1F2937',       // Cards, modals, sidebars
    surfaceBorder: '#374151', // Dividers and container outlines
    textPrimary: '#F9FAFB',   // Primary readable headers and active labels
    textMuted: '#9CA3AF',     // Subtitles, metadata, inactive links
    accentSuccess: '#10B981', // Metrics increase, positive indicators
  },
  typography: {
    fontFamily: 'Inter, system-ui, sans-serif',
    titleSize: 52,
    headingSize: 32,
    bodySize: 18,
    labelSize: 14,
  },
  geometry: {
    cardRadius: 12,
    windowRadius: 16,
    buttonRadius: 8,
    pillRadius: 9999,
  },
  shadows: {
    window: '0 25px 50px -12px rgba(0, 0, 0, 0.7)',
    card: '0 8px 24px -4px rgba(0, 0, 0, 0.4)',
  }
} as const;
```

---

## 3. Component Contract Architecture in Remotion

Never code ad-hoc HTML/CSS in individual scene files. Always encapsulate shared visual elements into dedicated, reusable components:

1. `<AppWindowContainer />`:
   - Handles consistent window framing, glassmorphism blur, header title bar, and drop shadows.
   - Wraps every in-app demonstration scene.
2. `<SidebarNav activeItem="analytics" />`:
   - Renders the exact same sidebar with the correct active tab indicator.
3. `<MetricCard label="Revenue" value="$42,850" change="+14.2%" />`:
   - Consistent typography, icon styling, and sparkline animations.
4. `<KineticTitle text="Instant Analytics" highlightWord="Instant" />`:
   - Reusable kinetic text entrance with spring physics and highlight badge styling.

---

## 4. Avoiding AI Footage Bleed into Application UI

> [!CAUTION]
> **NEVER generate readable application UI via Google Flow MCP.**
> Generative video models (Veo, Omni Flash) hallucinate text, blur fine lines, and produce morphing interfaces. 
> 
> - **Remotion**: Renders crisp, vector-sharp, pixel-perfect application UI, responsive text, animated charts, and button clicks.
> - **Google Flow MCP**: Renders cinematic ambient background footage, real-world scenes, 3D abstract textures, and atmospheric b-roll.
> - **Hybrid Layering**: In Remotion, place the Flow video clip as a background layer (`<Video src={flowClip} />`), apply subtle dark vignette/tint, and overlay the Remotion `<AppWindowContainer />` on top with spring entrance.
