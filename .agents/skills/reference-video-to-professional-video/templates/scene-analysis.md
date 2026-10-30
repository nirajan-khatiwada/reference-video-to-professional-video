# Scene Analysis Protocol & Template

Use this template to document the forensic analysis of a single scene from the reference video.

---

## Scene Overview
- **Scene ID**: Scene [Number]
- **Timecode Range**: `[HH:MM:SS.mmm]` -> `[HH:MM:SS.mmm]`
- **Duration**: `[X.XX]` seconds (`[YY]` frames at 30fps)
- **Primary Subject**: [e.g. Dashboard Metric Overview / User Authentication / Feature Workflow]

---

## 1. Frame-by-Frame Progression
- **Entry Frame (Frame [N])**:  
  [What appears at the very beginning of the scene? Initial element coordinates and opacity.]
- **Midpoint / Peak Action Frame (Frame [N])**:  
  [What is the focal interaction? Cursor movement, card expansion, data counter updating.]
- **Exit Frame (Frame [N])**:  
  [How does the scene conclude? Dissolve, slide, zoom-in, or cut.]

---

## 2. Visual Elements & UI Structure
- **Persistent Elements (Carried from previous scenes)**:  
  [e.g. Top application bar, left sidebar navigation with active indicator]
- **New Elements Introduced**:  
  [e.g. Center modal dialog, floating notification pill, line chart]
- **Dismissed Elements**:  
  [e.g. Welcome banner fades out]
- **Layout & Spatial Alignment**:  
  [e.g. 2-column grid, left 280px sidebar, 32px padding, centered modal]

---

## 3. Motion Dynamics & Animation Curves
- **Motion Type**: [e.g. Spring entrance / Linear pan / Decelerating slide]
- **Observed Duration**: [e.g. 18 frames (~0.6 seconds)]
- **Estimated Spring Parameters**:  
  - Damping: `[e.g. 14]`
  - Mass: `[e.g. 0.8]`
  - Stiffness: `[e.g. 120]`
- **Camera Dynamics**:  
  [e.g. Static camera / Subtle continuous 1.0 -> 1.06 zoom / 20px slow downward pan]

---

## 4. Typography & Color Inspection
- **Displayed Text**:  
  - Primary: `"[Heading Text]"`
  - Secondary: `"[Subtitle or Data Label]"`
- **Dominant Colors Detected**:  
  - Background: `[Hex]`
  - Surface: `[Hex]`
  - Accent / CTA: `[Hex]`
  - Text: `[Hex]`

---

## 5. Production Assignment
- **Allocated Engine**: [Remotion | Google Flow MCP | Hybrid]
- **Justification**:  
  [Why this engine is ideal: e.g. "Contains sharp interactive UI and exact text labels requiring Remotion" OR "Photorealistic atmospheric environment requiring Flow MCP"]
- **Reusable Component Reference**:  
  `<[ComponentName] />`
