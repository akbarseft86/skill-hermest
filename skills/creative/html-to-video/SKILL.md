---
name: html-to-video
title: html-to-video
description: Turn HTML+CSS+GSAP animations into MP4 video. Two pipelines — HyperFrames full render (fast, GPU) or headless Chrome frame capture + ffmpeg (fallback, works on any VPS). Covers GSAP timeline design, HyperFrames lint compliance, and screenshot-stitch workaround for GPU-less servers.
triggers:
  - "video dari html"
  - "bikin video animasi"
  - "html ke video"
  - "render animasi ke mp4"
  - "HyperFrames"
  - "heygen-com/hyperframes"
  - "gsap animation rendering"
---

# HTML → Video (HyperFrames + Headless Fallback)

Two rendering pipelines, chosen based on environment:

| Pipeline | Speed | Requires | Best for |
|----------|-------|----------|----------|
| **HyperFrames** (fast) | Minutes | GPU (NVENC/VAAPI) or patience | Production, final renders |
| **Capture** (fallback) | Fast | Chrome headless + ffmpeg | Iteration, VPS without GPU |

---

## Pipeline A: HyperFrames (full render)

### Setup

```bash
cd [project-dir]
npx hyperframes init [name]
# → creates index.html, hyperframes.json, package.json
```

### Key HyperFrames HTML Rules

1. Every timed element needs: `data-start`, `data-duration`, `data-track-index`, `class="clip"`
2. Root container:
   ```html
   <div id="root" data-composition-id="main" data-start="0" data-duration="N" data-width="1920" data-height="1080">
   ```
3. Timeline registration:
   ```html
   <script>
     window.__timelines = window.__timelines || {};
     const tl = gsap.timeline({ paused: true });
     // ... your timeline
     window.__timelines['main'] = tl;
   </script>
   ```
4. Use only `Inter` or fonts with explicit `@font-face` declarations. System fonts (`-apple-system`, `BlinkMacSystemFont`, `Segoe UI`) cause lint errors.
5. After every exit tween, add a `tl.set()` hard kill at the boundary:
   ```js
   tl.to('#scene1', { opacity: 0, y: -50, duration: .75 }, 3.25);
   tl.set('#scene1', { opacity: 0 }, 4.0); // hard kill at clip boundary
   ```

### Commands

```bash
npm run check        # lint + validate + inspect (run after EVERY edit)
npm run render       # render to MP4
npm run render -- -q draft -f 24   # fast preview
```

### Render Options

- `-q draft|standard|high` — draft is fastest
- `-f 24|30|60` — FPS
- `--crf N` — quality vs file size
- `-w N` — parallel workers (default auto; 1-8)

### Pitfalls

- **No GPU** = SwiftShader software rendering. At 1920×1080 this can be impractically slow. Use Pipeline B for quick samples on small VPS.
- **`font_family_without_font_face`** lint error: only Inter is auto-resolved. For other fonts, add `@font-face`.
- **Studio edit blocked** warning is harmless for automated renders.

---

## Pipeline B: Headless Chrome + ffmpeg (GPU-less VPS fallback)

Use when HyperFrames render is too slow but a sample MP4 is needed fast.

### Step 1: Add timeline seeking via URL parameter

Add to the bottom of your script, after `window.__timelines['main'] = tl;`:

```html
<script>
  const params = new URLSearchParams(window.location.search);
  if (params.has('t')) {
    tl.seek(Number(params.get('t')) || 0);
  } else {
    tl.play(0); // auto-play for normal preview
  }
</script>
```

### Step 2: Capture frames with headless Chrome

```bash
mkdir -p out/frames
cd [project-dir]
for i in $(seq 0 0.5 6); do
  n=$(python -c "print(int($i * 2))")
  /usr/bin/google-chrome --headless --disable-gpu --no-sandbox --disable-software-rasterizer \
    --screenshot="$PWD/out/frames/frame_$(printf '%02d' $n).png" \
    --window-size=1280,720 \
    "file://$PWD/index.html?t=$i" 2>/dev/null
  echo "Frame $i done"
done
```

### Step 3: Stitch to MP4 with ffmpeg

```bash
ffmpeg -y -framerate 2 -pattern_type glob -i 'out/frames/*.png' \
  -c:v libx264 -pix_fmt yuv420p -preset ultrafast -crf 28 out/output.mp4
```

Higher fidelity: shorter intervals + higher framerate. For a 4fps sample use intervals of 0.25s.

### Chrome flags explained

| Flag | Purpose |
|------|---------|
| `--headless` | Render without display |
| `--no-sandbox` | Required when running Chrome as root |
| `--window-size=W,H` | Output resolution |
| `--screenshot=PATH` | Save page as PNG |

---

## Workflow: Design the animation

1. **Concept**: 3 scenes max for a 6s sample. Each scene = headline + subtext or cards.
2. **Resolution**: 1920×1080 for full-res, but scale down to 1280×720 for fallback capture.
3. **GSAP timing**: stagger entrances, crossfade scenes. Use `power3.out` / `back.out()` for polish.
4. **Background**: dark gradient + floating decorative orbs + subtle grid for depth.
5. **Font**: Inter (auto-loaded by HyperFrames). Use bold weights (800-950).

### 6-second scene structure

| Second | Content |
|--------|---------|
| 0–2    | Hero: headline + eyebrow + subtext (staggered enter) |
| 2–4    | Value props: 3 cards (staggered enter) |
| 4–6    | Close: CTA with pulse/scale animation |

---

## Verification

- `npm run check` returns zero errors.
- Output MP4 exists and is non-empty.
- If publishing to public web, copy MP4 + preview HTML together.
- Tell the user clearly if this is a fallback screenshot-stitch sample, not a full HyperFrames render.

## References

- HyperFrames CLI docs: `npx hyperframes docs <topic>`
- HyperFrames guides: hyperframes.heygen.com/guides/prompting
