# Google Flow MCP Video Workflow

This reference explains how to leverage your existing **Google Flow MCP** connection inside Google Antigravity to generate high-fidelity cinematic b-roll and atmospheric motion video assets.

---

## 1. Connected MCP Capabilities

The Antigravity workspace connects to Google Flow via the `flow-connector` MCP server:

| Tool Name | Real Capability | Arguments / Usage |
| :--- | :--- | :--- |
| `flow_generate` | Generates images or video on Google Flow without API costs | `prompt`, `mode`, `image_model`, `aspect_ratio`, `duration`, `image_paths`, `folder`, `wait` |
| `flow_status` | Checks if local bridge daemon and Flow browser tab are active | None |
| `flow_get_job` | Queries status and result URLs of a running or completed generation | `job_id` |
| `flow_list_jobs` | Lists recent generation jobs | `limit` |
| `flow_cancel_job` | Cancels a specific in-progress job | `job_id` |
| `flow_stop` | Emergency abort for all active operations | None |
| `flow_doctor` | Diagnostic health check for the Flow automation bridge | None |

> [!NOTE]
> Do **NOT** invent tool names (such as `flow_render_video` or `flow_create_clip`). Always use the authentic `flow_generate` tool through `call_mcp_tool`.

---

## 2. Model Selection Guide for Video Production

### Video Generation Models (`image_model`)
| Model | Reference Capacity | Optimal Use Case |
| :--- | :--- | :--- |
| `veo-3.1-quality` | 0 reference images | Highest-fidelity 1080p, natural physics, fluid cinematic lighting, realistic real-world b-roll. |
| `veo-3.1-fast` | Up to 3 reference images | High-speed video rendering, dramatic drone shots, rapid camera tracking. |
| `veo-3.1-lite` | Up to 3 reference images | Rapid test passes, motion previews, low-latency iteration. |
| `omni-flash` | Up to 7 reference images | Multi-ingredient blending, restyling reference screenshots into abstract 3D spaces. |

### Image Generation Models (`image_model`)
| Model | Optimal Use Case |
| :--- | :--- |
| `nano-banana-pro` | Photorealistic 4K stills, detailed product photography, high-resolution textures. |
| `nano-banana-2` | Balanced concept art, abstract UI backgrounds, rapid texture iteration. |

---

## 3. Invocation Formulas for Common Video Needs

### A. Atmospheric Tech Background (Text-to-Video)
```json
{
  "mode": "flow-text-to-video",
  "prompt": "Cinematic slow camera dolly through dark minimalist server room with subtle pulsing blue fiber optic strands, shallow depth of field, anamorphic lens flare, 4k",
  "aspect_ratio": "16:9",
  "duration": "6",
  "image_model": "veo-3.1-quality",
  "wait": true
}
```

### B. Animating a Reference Still into Video (Frame-to-Video)
When you have extracted a reference frame (or created a clean UI screenshot) and want to introduce realistic dynamic camera motion:
```json
{
  "mode": "flow-frame-to-video",
  "prompt": "Smooth cinematic camera pan right across the scene with subtle atmospheric lighting shift",
  "image_paths": ["C:/Users/Nirajan/Downloads/final/reference-assets/frames/frame_00045.png"],
  "aspect_ratio": "16:9",
  "duration": "6",
  "image_model": "veo-3.1-fast",
  "wait": true
}
```

### C. Real-World User / Lifestyle Context
```json
{
  "mode": "flow-text-to-video",
  "prompt": "Over-the-shoulder medium shot of a software engineer smiling while working on modern dual monitors in a sunlit Scandinavian office, cinematic natural daylight",
  "aspect_ratio": "16:9",
  "duration": "6",
  "image_model": "veo-3.1-quality",
  "wait": true
}
```

---

## 4. Asset Ingestion Pipeline into Remotion

1. **Verify Connection**:
   ```json
   // Call flow_status first
   {"ServerName": "flow-connector", "ToolName": "flow_status", "Arguments": {}}
   ```
2. **Execute Generation**:
   Call `flow_generate` with the specified scene parameters.
3. **Locate Downloaded Media**:
   Media files are stored in the user's `Downloads/flow/` directory (or specified `folder` argument).
4. **Copy Asset to Remotion Project**:
   Copy the generated `.mp4` into the Remotion project's `public/` directory (e.g., `public/assets/flow_scene_01.mp4`).
5. **Reference in Remotion**:
   Use `staticFile('assets/flow_scene_01.mp4')` within `<Video src={...} />`.

---

## 5. Strict Boundaries: What NOT to Do with Flow

1. **NEVER attempt to render readable text, buttons, dashboard metrics, or exact software interfaces in Flow.** Flow video models will hallucinate characters and produce jittery artifacts.
2. **NEVER use Flow for the final composition.** The master timeline, cuts, titles, transitions, overlays, and final video rendering belong exclusively to **Remotion**.
