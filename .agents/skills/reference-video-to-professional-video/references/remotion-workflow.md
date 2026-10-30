# Remotion Production Workflow & Best Practices

This guide details how to construct, animate, preview, and render high-production-value video compositions inside Google Antigravity using Remotion.

---

## 1. Project Initialization & Architecture

When starting a project or inspecting an existing setup, follow the canonical Remotion directory structure:

```
my-video-project/
├── package.json
├── remotion.config.ts
├── tsconfig.json
├── public/                 # Static assets (images, SVGs, Google Flow video clips)
└── src/
    ├── index.ts            # Registers Remotion root
    ├── Root.tsx            # Declares <Composition /> entries
    ├── designTokens.ts     # Master visual tokens
    ├── compositions/
    │   └── MainVideo.tsx   # Master timeline coordinating sequences
    ├── scenes/
    │   ├── Scene01_Intro.tsx
    │   ├── Scene02_FeatureA.tsx
    │   ├── Scene03_FeatureB.tsx
    │   └── Scene04_Outro.tsx
    └── components/         # Reusable UI & motion elements
        ├── AppWindow.tsx
        ├── KineticTitle.tsx
        ├── CursorClick.tsx
        └── FlowVideoLayer.tsx
```

### Initializing a Project
If no Remotion project exists in the workspace:
```bash
npx create-video --template blank my-video-project
# or with bun
bun create video
```

---

## 2. Master Composition Architecture

In `src/Root.tsx`, define precise canvas dimensions and total duration:

```tsx
import { Composition } from 'remotion';
import { MainVideo } from './compositions/MainVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Main"
      component={MainVideo}
      durationInFrames={900} // 30 seconds at 30 fps
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

In `src/compositions/MainVideo.tsx`, assemble scenes sequentially using `<Sequence>`:

```tsx
import { AbsoluteFill, Sequence } from 'remotion';
import { Scene01_Intro } from '../scenes/Scene01_Intro';
import { Scene02_FeatureA } from '../scenes/Scene02_FeatureA';
import { Scene03_FeatureB } from '../scenes/Scene03_FeatureB';
import { Scene04_Outro } from '../scenes/Scene04_Outro';

export const MainVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0B0F19' }}>
      <Sequence from={0} durationInFrames={180} name="Scene 1 - Intro">
        <Scene01_Intro />
      </Sequence>
      <Sequence from={180} durationInFrames={240} name="Scene 2 - Analytics">
        <Scene02_FeatureA />
      </Sequence>
      <Sequence from={420} durationInFrames={270} name="Scene 3 - Collaboration">
        <Scene03_FeatureB />
      </Sequence>
      <Sequence from={690} durationInFrames={210} name="Scene 4 - Outro">
        <Scene04_Outro />
      </Sequence>
    </AbsoluteFill>
  );
};
```

---

## 3. High-Fidelity Animation Primitives

### Smooth Spring Entrances
Always prefer `spring()` over raw linear math for natural organic motion:

```tsx
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

export const AnimatedCard: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.8, stiffness: 120 },
  });

  const translateY = interpolate(entrance, [0, 1], [60, 0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);
  const scale = interpolate(entrance, [0, 1], [0.94, 1.0]);

  return (
    <div
      style={{
        transform: `translateY(${translateY}px) scale(${scale})`,
        opacity,
      }}
    >
      {children}
    </div>
  );
};
```

### Programmatic Camera Dynamics (Zoom & Pan)
Simulate high-end 4K camera movements directly in code:

```tsx
export const CameraRig: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();

  // Subtle continuous push-in from frame 0 to frame 240
  const zoom = interpolate(frame, [0, 240], [1.0, 1.07], {
    extrapolateRight: 'clamp',
  });
  
  // Gentle pan tracking
  const panX = interpolate(frame, [0, 240], [0, -30], {
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        transform: `scale(${zoom}) translateX(${panX}px)`,
        transformOrigin: 'center center',
      }}
    >
      {children}
    </div>
  );
};
```

---

## 4. Integrating Google Flow Video Footage

Seamlessly embed AI footage rendered via Flow MCP as textured atmospheric backdrops:

```tsx
import { AbsoluteFill, Video, staticFile, interpolate, useCurrentFrame } from 'remotion';

export const FlowHybridScene: React.FC = () => {
  const frame = useCurrentFrame();
  
  // Optional gentle fade-in for the background video
  const bgOpacity = interpolate(frame, [0, 20], [0, 0.45], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#090D16' }}>
      {/* 1. Google Flow Atmospheric Video Layer */}
      <AbsoluteFill style={{ opacity: bgOpacity }}>
        <Video
          src={staticFile('flow_cinematic_bg.mp4')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          muted
        />
      </AbsoluteFill>

      {/* 2. Ambient Gradient Vignette for UI Readability */}
      <AbsoluteFill
        style={{
          background: 'radial-gradient(circle at center, rgba(9,13,22,0.4) 0%, rgba(9,13,22,0.92) 100%)',
        }}
      />

      {/* 3. Vector-Sharp Remotion Application UI */}
      <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
        <AppWindow />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

---

## 5. Previewing & Rendering

### Studio Live Preview
Always start Studio to preview and verify animations interactively:
```bash
# In Antigravity terminal (starts long-running server without blocking browser):
npx remotion studio --no-open
```

### Production Rendering
When verification passes, render the final video:
```bash
# Render to MP4
npx remotion render src/index.ts Main out/final_video.mp4 --gl=angle
```

> [!IMPORTANT]
> The final rendered video must be **silent**. Never configure background music, AI speech, voiceover, or sound effects directly in the video render command or Remotion composition.
