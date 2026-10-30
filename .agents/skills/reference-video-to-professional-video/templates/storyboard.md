# Master Production Storyboard Template

**Project Title:** [Project Name / Video Title]  
**Source Reference Video:** [Path or description of reference video]  
**Master Resolution:** [e.g. 1920x1080 (16:9)]  
**Master Frame Rate:** [e.g. 30 fps]  
**Total Target Duration:** [e.g. 00:00:30.000 (900 frames)]  
**Audio Track:** Strictly Silent (No voiceover / narration in render)

---

## Complete Scene-by-Scene Breakdown (14-Field Storyboard)

<!-- Duplicate this block for each scene in the production plan -->

### Scene [Scene Number]

1. **Scene Number**: Scene 01
2. **Start Timestamp**: `00:00:00.000` (Frame 0)
3. **End Timestamp**: `00:00:06.000` (Frame 180)
4. **Duration**: 6.0 seconds (180 frames)
5. **Scene Description**:  
   [Describe the narrative purpose, user journey moment, and overarching action taking place.]
6. **Visual Elements**:  
   - [List background element: e.g. dark textured ambient canvas or Google Flow atmospheric video]
   - [List foreground UI: e.g. macOS-style app window container with navigation sidebar and search]
   - [List graphics: e.g. glowing accent badges, sparkline graph, animated status indicator]
7. **Text Displayed**:  
   - Heading: "[Exact Title / Kinetic Typography text]"
   - Subtitle: "[Supporting label or body text]"
   - UI Labels: "[Button text, table headers, numeric values]"
8. **Required Animations**:  
   - [Entrance: e.g. Spring scale entrance `0.94 -> 1.0` with fade `opacity: 0 -> 1`]
   - [Active motion: e.g. Metric counter rolling from `$0` to `$42,850`]
   - [Camera: e.g. Gentle continuous push-in zoom `scale: 1.0 -> 1.05`]
   - [Exit: e.g. Card slides left `translateX: 0 -> -120px` with fade]
9. **Transition Type**:  
   [e.g. Clean Cut / Directional Push Left / Smooth Zoom Blur / Shared Element Morph]
10. **Reference Frames**:  
    - `reference-assets/frames/frame_00001.png` (Scene entry state)
    - `reference-assets/frames/frame_00045.png` (Peak action state)
    - `reference-assets/frames/frame_00090.png` (Exit transition state)
11. **Reusable Components**:  
    - `<AppWindowContainer />`
    - `<SidebarNav activeItem="dashboard" />`
    - `<KineticTitle />`
12. **Production Tool**:  
    [Select one: **Remotion** | **Google Flow MCP** | **Hybrid (Flow + Remotion)**]
13. **Required Input Assets**:  
    - [e.g. Extracted UI icon `assets/icons/analytics.svg`]
    - [e.g. Flow generated background `public/assets/flow_ambient_bg.mp4`]
    - [e.g. Master design tokens `src/designTokens.ts`]
14. **Expected Output Assets**:  
    - Remotion scene component: `src/scenes/Scene01_Intro.tsx`
    - Rendered test clip: `out/test_scene_01.mp4`

---

### Scene 02

1. **Scene Number**: Scene 02
2. **Start Timestamp**: `00:00:06.000` (Frame 180)
3. **End Timestamp**: `00:00:13.500` (Frame 405)
4. **Duration**: 7.5 seconds (225 frames)
5. **Scene Description**:  
   [Detailed description]
6. **Visual Elements**:  
   - [Foreground / background elements]
7. **Text Displayed**:  
   - Heading: "..."
8. **Required Animations**:  
   - [Interactions, spring physics, cursor movement]
9. **Transition Type**:  
   [Cut / Wipe / Morph / Fade]
10. **Reference Frames**:  
    - `reference-assets/frames/frame_00120.png`
11. **Reusable Components**:  
    - `<AppWindowContainer />`
    - `<MetricCard />`
12. **Production Tool**:  
    [Remotion / Google Flow MCP / Hybrid]
13. **Required Input Assets**:  
    - [Inputs]
14. **Expected Output Assets**:  
    - `src/scenes/Scene02_Feature.tsx`

---

## Production Storyboard Summary Table

| Scene # | Timecode Window | Duration | Core Feature / Subject | Engine | Transition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | `00:00 - 00:06` | 6.0s | Hook & App Introduction | Hybrid | Push Left |
| **02** | `00:06 - 00:13` | 7.5s | Core Feature Deep Dive | Remotion | Smooth Cut |
| **03** | `00:13 - 00:22` | 8.5s | Workflow Automation & Speed | Remotion | Morph Zoom |
| **04** | `00:22 - 00:30` | 8.0s | Results, ROI & Call-to-Action | Hybrid | Fade to Black |
