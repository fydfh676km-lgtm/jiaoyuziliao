# Educational courseware visual-language contract

Use this reference only for educational `image-deck` work. It shapes the visual blueprint before assets or render layers are authored; it does not change frozen page content, page order, or the image-only PPTX output contract. For saleable whole-page generation, also read `commercial-whole-slide.md`; its whole-slide composition and acceptance rules take precedence over the deterministic text-safe-zone steps below.

## Core outcome

Build one topic-specific visual world for the deck, then let each page's instructional role choose its composition. Consistency comes from shared material, palette roles, imagery language, type hierarchy, and recurring motifs. Variety comes from different teaching actions, focal points, reading paths, and density levels.

## Build the deck visual world

Record the following under `deck.visualTheme.courseware`:

```yaml
topicFamily: "literary-humanities | news-documentary | science-technology | derived"
visualWorld: "One-sentence setting and emotional tone"
material: "Surface, texture, light, line, and depth language"
imageryLanguage: "Content-specific original scenes, diagrams, photography, or illustration"
recurringMotifs: ["Two to four restrained continuity cues"]
densitySequence: ["One density value for every page, in page order"]
```

The density sequence is intentional deck rhythm:

| Density | Visual load | Typical use |
|---|---|---|
| `immersive` | One dominant scene and minimal text | Cover, section opening, emotional transition |
| `light` | One focal idea with two or three supporting units | Prompt, key quotation, closing |
| `standard` | Three to five organized units | Explanation, context, concept, practice |
| `dense` | Five to seven tightly related units with a clear scan path | Evidence comparison, structured summary, data-rich page |

Use `dense` only when the frozen content requires it. Place a lighter page before or after a dense run so the class can reset attention.

## Select a topic family

These are design directions, not templates:

| Topic family | Visual-world recipe | Evidence-bearing visuals |
|---|---|---|
| `literary-humanities` | Tactile paper or restrained painterly field, culturally appropriate image language, expressive whitespace, one accent color | Landscape or scene, author/context material, imagery sequence, annotated textual evidence |
| `news-documentary` | Editorial or archival surface, disciplined red/black/neutral hierarchy, documentary contrast, map and time cues | Headline anatomy, document crop, map, timeline, route, source comparison |
| `science-technology` | Atmospheric or technical field, cool luminous accents, controlled depth, clean geometric annotation | System diagram, timeline, process, measured data, object or environment cutaway |
| `derived` | Derive an original visual world from the subject, audience, frozen content, and abstract reference rules | Use visuals that explain this subject's evidence and actions |

Do not force a family when another subject needs a new visual world. Interface panels and dashboard grids are appropriate only when the lesson content itself is interface- or dashboard-like.

## Match page role to composition

Choose the closest role, then adapt the composition to the supplied layout instructions:

| Page role | Instructional action | Composition recipe |
|---|---|---|
| `cover-or-section` | Enter a topic or shift chapter | Immersive scene, short title group, large quiet region |
| `orientation-or-goals` | Preview route, goals, or tasks | Journey, sequence, constellation, or directional path |
| `author-or-context` | Place a person, event, or text in context | Portrait/document with timeline, map, or contextual scene |
| `close-reading-or-evidence` | Observe, annotate, or infer from exact evidence | Text-safe evidence field plus scene, detail lens, or annotation path |
| `imagery-or-layers` | Decompose scene, space, structure, or levels | Depth layers, exploded scene, labeled terrain, or staged reveal |
| `concept-or-method` | Explain a rule, relationship, or process | Cause-effect chain, cycle, hierarchy, sequence, or worked example |
| `comparison` | Compare evidence, viewpoints, or outcomes | Paired evidence, common axis, matrix, before/after, or converging paths |
| `activity-or-workspace` | Discuss, classify, write, or create | Brief task scaffold plus the largest practical work area |
| `synthesis-or-check` | Consolidate, retrieve, or assess | Concept map, checklist, loop, ladder, or structured summary |
| `transfer-or-closing` | Apply beyond the page and conclude | Reduced density, one next action, returning signature motif |

A card is a semantic container for grouping, comparison, or writing—not the default page surface. When adjacent pages have different roles, give them different dominant compositions while retaining the same visual world.

## Required per-page design record

Before any render layer, fill every field under `slide.coursewareDesign`:

```yaml
pageRole: "One role from the table or a precise derived role"
instructionalAction: "What the teacher or learner does here"
focalPoint: "The first thing the audience should notice"
composition: "Dominant spatial relationship, not a list of decorations"
textSafeZone: "Protected exact-text region with position and usable bounds"
readingPath: "Ordered scan path through the page"
density: "immersive | light | standard | dense"
continuityCue: "Motif, color, line, scene, or transition connecting adjacent pages"
```

Write these fields as production decisions. `composition` determines geometry; `textSafeZone` constrains generated assets; `readingPath` determines hierarchy; `density` must match the deck sequence; `continuityCue` keeps pages related without repeating the same layout.

## Exact-content planning order

For each page:

1. Copy the supplied `title` and ordered `content` items into the manifest exactly as separate immutable values.
2. Determine the page role and instructional action from those values.
3. Fill the eight-field `coursewareDesign` record.
4. In `commercial-whole-slide`, integrate the approved visible copy into the complete page composition and record OCR/essential-text requirements. In `deterministic-text`, reserve the text-safe zone and place one exact text layer for each immutable value.
5. Add only visuals that explain, locate, compare, sequence, or emotionally frame the supplied content.

This order keeps visual planning from merging items, adding punctuation, inventing headings, or turning placeholders into new lesson content.

## Blueprint gate

Proceed to asset generation only when all checks pass:

- Every page has all eight `coursewareDesign` fields.
- `densitySequence` has one entry per page and matches every page's density.
- Each frozen title and content item remains separate and byte-for-byte unchanged.
- Every page has one obvious focal point and one stated reading path.
- Different instructional roles use meaningfully different dominant compositions.
- Recurring motifs connect the deck without becoming repeated decoration.
- Every requested or generated visual has a direct relationship to the page's content or action.
- In `commercial-whole-slide`, each page is a finished commercial composition and passes the commercial acceptance score. In `deterministic-text`, generated assets remain text-free and preserve the declared text-safe zone.

## Common corrections

| Symptom | Correct blueprint move |
|---|---|
| Many pages look like the same card grid | Re-select each page role and use its composition recipe. |
| Decoration feels generic | Replace it with subject evidence, a scene, a process, or a content-linked motif. |
| A dense page has no entry point | Reduce secondary emphasis and make the reading path explicit. |
| The deck is consistent but monotonous | Keep material and motifs; change scale, depth, axis, and density by page role. |
| Exact content drifted during planning | Restore the immutable title/content array before authoring layers. |
