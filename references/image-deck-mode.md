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

For every page, first copy `title` and the ordered `content` array as immutable values. Only then author design-intent fields and render layers around those values. Each supplied content item remains one array item. In deterministic-text mode it maps to one exact text layer; in commercial-whole-slide mode it is checked against the reviewed full-page raster.

## Canonical brief manifest

Use one normalized JSON manifest as the sole rendering input. Its `deck` object fixes title, aspect ratio, resolution, reference image, global style, and reusable visual theme. Each `slides` record has an explicit `page`, frozen text/content, layout and element instructions, visual emphasis, and an ordered list of render layers. Preserve supplied page order and exact text unless the user authorizes a change.

For a minimal **one-page commercial deck**, use the following coherent schema. Alternatives are described in prose, never inserted as a pipe-separated string in JSON.

| Record | Required values and relationships |
|---|---|
| `deck` | Nonempty `title` and `styleBible`; `renderMode: "commercial-whole-slide"`; `anchorPages: [1]`; `aspectRatio: "16:9"`; `resolution: {"width": 3840, "height": 2160}`; authorized `referenceImage`. |
| `deck.visualTheme.courseware` | Nonempty `topicFamily`, `visualWorld`, `material`, `imageryLanguage`; two to four nonempty `recurringMotifs`; `densitySequence: ["standard"]`. Other valid densities are `immersive`, `light`, and `dense`; choose one actual value for each page. |
| `slides` | An array containing exactly one page record with `page: 1`, frozen `title`, ordered `content` array, `layout`, `elements` array, `elementStyle`, `emphasis`, and nonempty `layoutArchetype`. |
| `slides[0].coursewareDesign` | Nonempty `pageRole`, `instructionalAction`, `focalPoint`, `composition`, `textSafeZone`, `readingPath`, `continuityCue`, and `density: "standard"` matching the deck sequence. |
| `slides[0].layers` | Exactly one image: `kind: "image"`, `id: "whole-slide"`, `generated: true`, authorized raster `src`, `x: 0`, `y: 0`, `width: 3840`, `height: 2160`, and its actual `visualReview`. There are no separate text layers in this mode. |

Resolve relative asset paths from the **manifest file's directory**, not from the project root. For a manifest saved at `<project>/image-deck/render-manifest.json`, example project-local paths are `referenceImage: "../reference/style.png"` and layer `src: "assets/001-reviewed.png"`. These are illustrative filenames: supply existing authorized files, and ensure the reviewed page raster is 16:9.

Build `visualReview` only after reviewing that actual raster. Do not copy passing flags or scores from an example or test fixture. Record all of the following:

- `status: "pass"` only after real review; `checkedFor` must include `watermark`, `logo`, `reference-copying`, `ocr-text`, `commercial-quality`, `style-continuity`, and `page-specific-relevance`.
- `ocr.titleExact` and `ocr.essentialTextExact` must be `true`; the measured `ocr.bodyMatchRatio` must be from 0.98 through 1, with no semantic change.
- `commercialScores` contains the six measured 0–100 values `contentIntegration`, `visualHierarchy`, `pageSpecificity`, `styleContinuity`, `compositionQuality`, and `artifactCleanliness`; each is at least 75 and their mean is at least 85.
- `candidateCount`, `generationAttempts`, and `repairRounds` reflect actual calls. A passing initial single candidate records `1`, `1`, and `0` respectively; multiple candidates need the complete history described below.
- `dominantPanelAreaRatio` is a measured value from 0 through 1; values above 0.45 also need a nonempty, content-based `largePanelJustification`.

The executable schema fixture is [`commercialManifest(1, options)`](../scripts/tests/helpers/image-deck-fixture.mjs), tested by [`render-review-contract.test.mjs`](../scripts/tests/render-review-contract.test.mjs) and [`candidate-budget.test.mjs`](../scripts/tests/candidate-budget.test.mjs). The fixture's synthetic images and passing review records are **test data, not production assets or review evidence**. [`render-assets.test.mjs`](../scripts/tests/render-assets.test.mjs) replaces the image with a local PNG, runs `normalizeManifest` with `projectRoot`, validates the schema, and checks actual Chromium decoding; it also rejects image-ratio mismatch and unauthorized file paths. Use this structure with the frozen page content, real project images, and genuine review records.

For educational courseware, `visualTheme.courseware` and every slide's `coursewareDesign` are required planning records. Complete and review them before creating any generated asset or render layer. They remain part of the slide input hash and may be consumed as planning metadata even when the deterministic renderer does not draw them directly.

`visualTheme.fontFamily` is `null` by default in visual-performance-first work. Resolve an installed WPS-compatible family only for deterministic-text/editable rendering, or when the user explicitly specifies a font; do not leak that renderer choice into the user-facing visual blueprint unless requested.

These JSON/YAML records are internal production metadata. If a user-facing visual blueprint is requested or displayed, render it only in the fixed six-field format: `第X页` / `画面风格：` / `添加元素：` / `文字字体与重点标注：` / `布局排版：` / `镜头与光影：` / `画面去重与统一约束：`. The six field labels have no list numbering, and the block contains no `页面标题：` or seventh field.

## Reference abstraction and rule priority

Analyze a reference image only for abstract, transferable rules: palette roles, spacing, hierarchy, material, density, and contrast. Do not copy logos, people or characters, title effects, distinctive composition, or other protected expression. Substitute original complete-page artwork in `commercial-whole-slide`, or original text-free assets in `deterministic-text`, while retaining only the agreed abstract rules. Apply `per-page instruction > global instruction > abstract reference rules > safe defaults` whenever constraints compete.

## Render-manifest layers

### Commercial whole-slide mode

Follow `commercial-whole-slide.md`. Each slide contains exactly one generated `image` layer named `whole-slide` at `x: 0`, `y: 0`, covering the exact deck resolution. The source raster must match the deck aspect ratio; the renderer rejects a mismatch instead of cropping or stretching the reviewed page. The visible title and page copy are integrated into that raster. Record `layoutArchetype`, candidate count/history, OCR verdict, large-panel ratio/justification, commercial score, continuity review, and repair metadata. The renderer validates and packages these finished page images without adding generic text panels.

Use `min(3, slideCount)` distinct valid `deck.anchorPages`. Generate one candidate per anchor first and reuse it when it passes. For every page, `visualReview.candidateCount` is between 1 and 3, including all full-page regenerations. Each candidate allows at most two localized repairs. Multi-candidate reviews require `candidateHistory: [{"repairRounds": 0, "generationAttempts": 1}, ...]` covering every candidate in generation order and a 1-based `selectedCandidate`; the selected entry must match the review's top-level retry fields. Legacy single-candidate records may omit the history. Do not claim a bounded multi-candidate budget when the earlier candidate records are missing.

### Deterministic text mode

Apply `classroom-readability.md` to frozen text and layout capacity. In deck pixel coordinates, classroom-equivalent points are `fontSize * 540 / deck.resolution.height`: titles must be at least 40 pt and every canonical body string at least 32 pt. The renderer rejects undersized text and overflow without publishing a page; it does not auto-shrink text or compress line spacing. Recompose in orchestration without changing frozen copy/count. Whole-slide raster text requires actual visual review because those pixel text regions are not DOM text layers.

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

Every filesystem-backed `deck.referenceImage`, raster `src`, and SVG `src` must resolve lexically and physically inside `--project-root`, including after symbolic-link resolution, and must be an existing readable regular file. Data URLs remain subject to the renderer's local-data and SVG safety rules. After authorization, local raster bytes are embedded as data URLs for Chromium to decode without relaxing browser security. Normalization records immutable SHA-256 fingerprints for authorized files; resume hashes include those fingerprints, aspect ratio, resolution, and the renderer contract version, so asset, geometry, or acceptance-contract changes invalidate reuse.

## Stage ownership

```text
Skill orchestration: source extraction, reference analysis, page planning, imagegen calls, visual inspection, page-local retry decisions.
Renderer script: schema validation, exact text/layout rendering, classroom text-size and overflow rejection, PNG metadata/hash checks, contact sheet, PPTX packaging, machine-readable report.
```

In `commercial-whole-slide`, use the selected image-generation provider for reviewed complete-page rasters and use the bundled Node runtime and `scripts/render-image-deck.mjs` for 4K PNG verification, contact-sheet generation, and image-only PPTX packaging. In `deterministic-text`, use image generation only for original text-free raster assets and use the renderer for exact text. Keep runtime-generated inputs and outputs in the current project.

Obtain the actual bundled runtime paths from `load_workspace_dependencies`; do not assume a versioned local path. Define the variables from that result, with `IMAGE_DECK_PROJECT_ROOT` set to the current authorized project root:

```bash
IMAGE_DECK_NODE="<Node executable returned by load_workspace_dependencies>"
export IMAGE_DECK_MODULES_ROOT="<node_modules directory returned by load_workspace_dependencies>"
IMAGE_DECK_PROJECT_ROOT="<current authorized project root>"
IMAGE_DECK_SCRIPT="<absolute path to this skill>/scripts/render-image-deck.mjs"
```

```bash
"$IMAGE_DECK_NODE" "$IMAGE_DECK_SCRIPT" \
  --project-root "$IMAGE_DECK_PROJECT_ROOT" \
  --manifest image-deck/render-manifest.json \
  --output-dir outputs/认识情绪_图片版 \
  --internal-dir image-deck/run \
  --resume
```

Set `IMAGE_DECK_MODULES_ROOT` as shown, or pass the same path explicitly with `--modules-root`. The environment variable is preferred for repeated calls; the personal bundled-runtime fallback is home-relative and remains available when neither is supplied.

## Generated-asset visual review

Inspect every generated asset before it enters a slide. In `commercial-whole-slide`, apply the OCR, composition-diversity, style-continuity, page-specificity, and commercial-score checks in `commercial-whole-slide.md`, with its total budget of three full-page candidates and two localized repairs per candidate. In `deterministic-text`, check pseudo-text, watermark, logo, reference-copying, and the safe text region, with at most two automatic repair rounds per affected asset. Record the review result in the associated generated image layer. Repair and re-review only the failed asset/page; leave passing pages and assets unchanged. After the relevant budget is exhausted, surface the failure as a blocking question only before the start command or as a failed completion verdict after start.

## Fatal preflight failures

Do not render if page order is ambiguous, a critical source cannot be read, inputs contradict the same page, or frozen exact text cannot fit its frozen layout while preserving the minimum font size. Preserve page count and original text. Before the start command, ask only the single highest-impact question needed to resolve the conflict; after the start command, do not ask and instead report the fatal preflight failure in the final verdict.

## Deterministic rendering and repair

Validate the canonical manifest before rendering. In `commercial-whole-slide`, render the single reviewed complete-page image unchanged at the manifest resolution. In `deterministic-text`, render shapes, SVG, exact text, and reviewed image layers deterministically; reject undersized or overflowing text rather than repairing it by font reduction or compressed line spacing. Recompose only the affected layout in orchestration without changing frozen text, page order, or approved constraints. Name default page images `001.png`, `002.png`, and so on in ascending page order and place them under `<outputDir>/pages/`. On a page-local repair, rerender and recheck only the failed page/asset, then rerun whole-deck count and order checks before the completion verdict.

## Output contract

Unless the canonical manifest overrides them, output 16:9 PNGs at 3840×2160, a contact sheet, an image-only PPTX containing one full-slide page image per page, and a machine-readable render report. Verify PNG dimensions and metadata/hash results, output count, and numeric page order. Build a custom PPTX layout from the manifest geometry; verify slide dimensions, one uncropped full-slide image per page, page-to-media order, and embedded PNG byte hashes before publication. The PPTX intentionally contains page images only and must not be described as editable. Keep final page PNGs in `<outputDir>/pages/` and the final PPTX at `<outputDir>/`; keep the contact sheet and report in the project-internal directory outside `outputDir`.

## Completion verdict

Complete only when schema validation, generated-asset reviews, exact-text/layout rendering, per-page PNG metadata/hash checks, output count/order checks, and image-only PPTX packaging all pass. Report any failed page or asset precisely. After a page-local repair, include the refreshed page check and whole-deck count/order check in the final verdict.
