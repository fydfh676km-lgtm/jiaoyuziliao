# Direct image-deck production contract

## Route precedence

Select `image-deck` before Smart/Premium selection when the user explicitly names `image-deck` or 图片型 PPT 模式, or supplies final per-page content, per-page layout/element style, a visual reference, and requests page images plus an image-only PPTX without content planning. A complete direct contract skips the five Premium internal checkpoints. If the request also asks for topic selection, restructuring, lesson plan, speaker script, marketing notes, or the complete commercial product, keep Premium and permit `image-deck` only as its final PPT rendering method after the explicit start command.

When the requested deck is educational courseware for classroom teaching, curriculum, teacher, or student use, read `references/courseware-visual-language.md` after this file and before authoring the manifest. Infer its visual-world and per-page design-intent fields from the frozen content, supplied page instructions, and abstract reference rules; do not make the user fill those internal fields.

## Rendering-strategy decision

Read `references/commercial-whole-slide.md` before asset generation. Set `deck.renderMode` explicitly:

- `commercial-whole-slide` is the default for saleable, premium, marketplace-ready, or reference-led image-only courseware. The model generates the entire composed page, including integrated typography and information modules. Do not create text-free wallpaper plus a large generic overlay panel.
- `deterministic-text` is reserved for requests that explicitly prioritize editable text, byte-for-byte rendering, accessibility, or zero OCR risk over integrated commercial composition.

Do not infer `deterministic-text` merely because the manifest renderer supports it. The user's desired product quality determines the mode.

## Supported input adapters

Normalize conversation text and Markdown directly. Read Word with the bundled document-reading capability and PPTX with the bundled presentation-reading capability. For mixed inputs, both owners extract their page records before merging by explicit page number. Resolve contradictions as `per-page instruction > global instruction > abstract reference rules > safe defaults`; old PPT formatting is ignored unless the user explicitly requests preservation.

Convert every accepted source to one page contract before rendering. Before the explicit start command, one blocking clarification may be requested only when page order is ambiguous, a critical file is unreadable, sources contradict the same page, or exact text cannot fit without changing a frozen constraint. After the start command, do not ask a mid-process question; use safe repair or report the unresolved blocker in the final verdict.

For every page, first copy `title` and the ordered `content` array as immutable values. Only then author design-intent fields and render layers around those values. Each supplied content item remains one array item and later maps to one exact text layer.

## Canonical brief manifest

Use one normalized JSON manifest as the sole rendering input. Its `deck` object fixes title, aspect ratio, resolution, reference image, global style, and reusable visual theme. Each `slides` record has an explicit `page`, frozen text/content, layout and element instructions, visual emphasis, and an ordered list of render layers. Preserve supplied page order and exact text unless the user authorizes a change.

```json
{
  "deck": {
    "title": "课件名称",
    "renderMode": "commercial-whole-slide | deterministic-text",
    "styleBible": "商业整页模式下必填的统一视觉世界、人物、材质、配色、字体行为与禁用规则",
    "anchorPages": [1, 4, 12],
    "aspectRatio": "16:9",
    "resolution": { "width": 3840, "height": 2160 },
    "referenceImage": "reference/style.png",
    "globalStyle": "整套通用风格要求",
    "visualTheme": {
      "background": "#F7F4EE",
      "title": "#16263D",
      "body": "#334155",
      "accent": "#E76F51",
      "fontFamily": null,
      "radius": 32,
      "shadow": "0 20px 60px rgba(22,38,61,0.14)",
      "illustrationLanguage": "原创几何教育插画",
      "courseware": {
        "topicFamily": "literary-humanities",
        "visualWorld": "与课文主题相符的统一视觉世界",
        "material": "纸张、水墨与克制的印章线条",
        "imageryLanguage": "与每页教学内容直接相关的原创场景和图解；商业整页模式同时整合排版文字",
        "recurringMotifs": ["远山", "水纹", "朱砂节点"],
        "densitySequence": ["immersive", "standard", "light"]
      }
    }
  },
  "slides": [
    {
      "page": 1,
      "title": "页面标题",
      "content": ["必须原样呈现的文字"],
      "layout": "页面布局和区域关系",
      "elements": ["插画、图形、图标、装饰等"],
      "elementStyle": "元素造型、材质、线条和配色",
      "emphasis": "本页视觉重点",
      "coursewareDesign": {
        "pageRole": "本页教学角色",
        "instructionalAction": "教师或学生在本页完成的动作",
        "focalPoint": "第一视觉焦点",
        "composition": "主要构图关系",
        "textSafeZone": "准确文字区域与边界",
        "readingPath": "观看顺序",
        "density": "immersive | light | standard | dense",
        "continuityCue": "与前后页相连的母题或变化"
      },
      "layers": [
        {
          "kind": "text",
          "id": "title",
          "source": "title",
          "text": "页面标题",
          "x": 240,
          "y": 180,
          "width": 1800,
          "height": 240,
          "style": { "fontSize": 96, "minFontSize": 64, "fontWeight": 700, "color": "#16263D", "lineHeight": 1.1, "align": "left" }
        }
      ]
    }
  ]
}
```

For educational courseware, `visualTheme.courseware` and every slide's `coursewareDesign` are required planning records. Complete and review them before creating any generated asset or render layer. They remain part of the slide input hash and may be consumed as planning metadata even when the deterministic renderer does not draw them directly.

`visualTheme.fontFamily` is `null` by default in visual-performance-first work. Resolve an installed WPS-compatible family only for deterministic-text/editable rendering, or when the user explicitly specifies a font; do not leak that renderer choice into the user-facing visual blueprint unless requested.

These JSON/YAML records are internal production metadata. If a user-facing visual blueprint is requested or displayed, render it only in the fixed six-field format: `第X页` / `画面风格：` / `添加元素：` / `文字字体与重点标注：` / `布局排版：` / `镜头与光影：` / `画面去重与统一约束：`. The six field labels have no list numbering, and the block contains no `页面标题：` or seventh field.

## Reference abstraction and rule priority

Analyze a reference image only for abstract, transferable rules: palette roles, spacing, hierarchy, material, density, and contrast. Do not copy logos, people or characters, title effects, distinctive composition, or other protected expression. Substitute original complete-page artwork in `commercial-whole-slide`, or original text-free assets in `deterministic-text`, while retaining only the agreed abstract rules. Apply `per-page instruction > global instruction > abstract reference rules > safe defaults` whenever constraints compete.

## Render-manifest layers

### Commercial whole-slide mode

Follow `commercial-whole-slide.md`. Each slide contains exactly one generated `image` layer named `whole-slide` at `x: 0`, `y: 0`, covering the exact deck resolution. The visible title and page copy are integrated into that reviewed raster. Record `layoutArchetype`, candidate count, OCR verdict, large-panel ratio/justification, commercial score, continuity review, and repair metadata. The renderer validates and packages these finished page images without adding generic text panels.

### Deterministic text mode

Supported layer kinds are `text`, `image`, `shape`, and `svg`. Layers are deterministic records with an `id`, geometry in the deck's pixel coordinate space, and the content/style fields required by their kind. Text is rendered by the renderer, never by an image-generation model. An `image` layer with `generated: true` must contain:

```json
{
  "visualReview": {
    "status": "pass",
    "generationAttempts": 1,
    "repairRounds": 0,
    "checkedFor": ["pseudo-text", "watermark", "logo", "reference-copying", "safe-text-region"]
  }
}
```

Every frozen canonical string must be represented exactly once: `slide.title` maps to one text layer with `source: "title"`, and each ordered `slide.content` item maps to one layer with `source: "content[n]"`. The layer's `text` must be byte-for-byte equivalent to that canonical value. Omitted, altered, duplicated, out-of-range, or split canonical text is invalid.

Before publishing any educational image-deck, scan all slide-visible strings for `课时` and variants such as `第一课时`, `第二课时`, `课时导入`, and `课时总结`; rewrite them as content-based titles or transitions before rendering.

All layer rectangles are protected against accidental overlap. Declare an intentional overlap explicitly with `allowOverlapWith: ["other-layer-id"]` on either participating layer. The renderer rejects undeclared collisions and any later layer that obscures protected text. It also waits for every raster image to decode and verifies positive natural dimensions before publishing a screenshot.

Every filesystem-backed `deck.referenceImage`, raster `src`, and SVG `src` must resolve lexically and physically inside `--project-root`, including after symbolic-link resolution, and must be an existing readable regular file. Data URLs remain subject to the renderer's local-data and SVG safety rules. Normalization records immutable SHA-256 fingerprints for authorized files; resume hashes include those fingerprints plus aspect ratio and resolution, so same-path file changes or geometry changes invalidate reuse.

## Stage ownership

```text
Skill orchestration: source extraction, reference analysis, page planning, imagegen calls, visual inspection, page-local retry decisions.
Renderer script: schema validation, exact text/layout rendering, overflow repair, PNG metadata/hash checks, contact sheet, PPTX packaging, machine-readable report.
```

In `commercial-whole-slide`, use the selected image-generation provider for reviewed complete-page rasters and use the bundled Node runtime and `scripts/render-image-deck.mjs` for 4K PNG verification, contact-sheet generation, and image-only PPTX packaging. In `deterministic-text`, use image generation only for original text-free raster assets and use the renderer for exact text. Keep runtime-generated inputs and outputs in the current project.

Obtain the actual bundled runtime paths from `load_workspace_dependencies`; do not assume a versioned local path. Define the variables from that result, with `IMAGE_DECK_PROJECT_ROOT` set to the current authorized project root:

```bash
IMAGE_DECK_NODE="<Node executable returned by load_workspace_dependencies>"
IMAGE_DECK_MODULES_ROOT="<node_modules directory returned by load_workspace_dependencies>"
IMAGE_DECK_PROJECT_ROOT="<current authorized project root>"
```

```bash
"$IMAGE_DECK_NODE" edu-ppt/scripts/render-image-deck.mjs \
  --project-root "$IMAGE_DECK_PROJECT_ROOT" \
  --manifest image-deck/render-manifest.json \
  --output-dir outputs/认识情绪_图片版 \
  --internal-dir image-deck/run \
  --resume
```

Set `IMAGE_DECK_MODULES_ROOT` as shown, or pass the same path explicitly with `--modules-root`. The environment variable is preferred for repeated calls; the personal bundled-runtime fallback is home-relative and remains available when neither is supplied.

## Generated-asset visual review

Inspect every generated asset before it enters a slide. In `commercial-whole-slide`, apply the OCR, composition-diversity, style-continuity, page-specificity, and commercial-score checks in `commercial-whole-slide.md`. In `deterministic-text`, check pseudo-text, watermark, logo, reference-copying, and the safe text region. Record the review result in the associated generated image layer. If an asset fails, regenerate and re-review only that asset; leave passing pages and assets unchanged. Permit at most two automatic repair rounds for the affected asset/page, then surface the failure as a blocking question only before the start command or as a failed completion verdict after start.

## Fatal preflight failures

Do not render if page order is ambiguous, a critical source cannot be read, inputs contradict the same page, or frozen exact text cannot fit its frozen layout while preserving the minimum font size. Preserve page count and original text. Before the start command, ask only the single highest-impact question needed to resolve the conflict; after the start command, do not ask and instead report the fatal preflight failure in the final verdict.

## Deterministic rendering and repair

Validate the canonical manifest before rendering. In `commercial-whole-slide`, render the single reviewed complete-page image unchanged at the manifest resolution. In `deterministic-text`, render shapes, SVG, exact text, and reviewed image layers deterministically and attempt overflow repair without changing frozen text, page order, or approved constraints. Name default page images `001.png`, `002.png`, and so on in ascending page order and place them under `<outputDir>/pages/`. On a page-local repair, rerender and recheck only the failed page/asset, then rerun whole-deck count and order checks before the completion verdict.

## Output contract

Unless the canonical manifest overrides them, output 16:9 PNGs at 3840×2160, a contact sheet, an image-only PPTX containing one full-slide page image per page, and a machine-readable render report. Verify PNG dimensions and metadata/hash results, output count, and numeric page order. Build a custom PPTX layout from the manifest geometry; verify slide dimensions, one uncropped full-slide image per page, page-to-media order, and embedded PNG byte hashes before publication. The PPTX intentionally contains page images only and must not be described as editable. Keep final page PNGs in `<outputDir>/pages/` and the final PPTX at `<outputDir>/`; keep the contact sheet and report in the project-internal directory outside `outputDir`.

## Completion verdict

Complete only when schema validation, generated-asset reviews, exact-text/layout rendering, per-page PNG metadata/hash checks, output count/order checks, and image-only PPTX packaging all pass. Report any failed page or asset precisely. After a page-local repair, include the refreshed page check and whole-deck count/order check in the final verdict.
