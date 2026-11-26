# Persistent user visual-reference library

Use this reference when the user explicitly supplies a batch of images for future reuse, or when the current user request explicitly asks to use a previously created library. Availability alone is not an activation trigger. The library is a retrieval aid, not model training and not a set of slide templates to copy.

## Available bundled library

The user-supplied Chinese classical/ink-wash collection is bundled in `assets/style-references/chinese-ink-wash/`, with 20 unchanged originals and a per-image `index.json`. Only when the user explicitly asks to reference this collection or use their previous images, read `chinese-ink-wash.md` and retrieve a relevant subset. A request for an ink-wash style or an ancient-poetry topic alone is not a request to consult the library. Do not reload every image, force this direction on unrelated lessons, or depend on the original desktop folder. Current-task user instructions and references still take precedence. Including an image in the reference library is not commercial-use permission or authorization to upload it to a public repository.

## One-time ingestion

Explicit instructions such as `这些图以后自动调用`, `建立参考图库`, or an equivalent future-reuse request authorize persistent indexing of the supplied files. Create the library directory only on the first real import; do not create empty placeholders. Preserve the source images without editing them and create one metadata record per readable image. Deduplicate exact files and near-identical variants, while retaining provenance and the user's folder or group boundaries when they carry meaning.

Each record must support retrieval by these attributes:

```yaml
id: "stable unique id"
source_file: "authorized source path or stored relative path"
provenance: "user-supplied source and import date"
subject_and_grade: ["applicable subjects and age ranges"]
genre_and_topic: ["ancient poetry, prose, history, English, science, etc."]
era_geography_season: ["content-accuracy constraints or unknown"]
visual_language: ["ink wash, blue-green landscape, editorial, documentary, etc."]
palette_and_material: ["dominant color roles, texture, brush or image treatment"]
composition_archetypes: ["cover, comparison, relationship, map, timeline, close reading, etc."]
scene_traits: ["viewpoint, foreground/middle/distance, light, weather, atmosphere"]
typography_and_spacing: ["observable hierarchy, negative space, reading-region traits"]
suitable_for: ["lesson and page functions this reference supports"]
avoid_for: ["content, audience, or density it weakens"]
copyright_sensitive_elements: ["specific assets, wording, branding, or compositions not to copy"]
quality_risks: ["AI artifacts, pseudo-text, anatomy, perspective, or readability risks"]
similarity_group: "cluster for duplicate and overuse control"
```

The index records observable traits and cautious inferences; it does not claim that the base model was trained on the images. If an image is unreadable, corrupt, or lacks enough visual information, exclude it from retrieval and report it in the ingestion result rather than inventing tags.

## Retrieval only when requested

Once explicit library use is established, derive a compact retrieval brief from the source ledger: subject, grade, genre, historical/cultural setting, geography, season, time, central imagery, emotional curve, page functions, projection density, and any explicit user preference. Retrieve candidates in this order:

1. factual and cultural compatibility with the textbook;
2. genre, topic, central imagery, and emotional fit;
3. audience and teaching-function fit;
4. the user's current explicit visual preference; and
5. visual distinctiveness from recently used courseware when that history is available.

Select one master-style anchor and at most two supporting composition or element references. Do not load the whole library into the prompt. If no candidate survives factual, cultural, or audience-fit checks, use a new content-driven direction rather than forcing an attractive but unsuitable reference.

For ancient poetry or classical literature, an explicitly requested library lookup can select compatible landscape, ink, gongbi or literary references. Without that request, design directly from textbook understanding; the genre does not enable automatic library loading.

## Reference priority

Follow the current `visual-system.md` and `workflow.md` route, which supersedes older automatic retrieval and combined-research instructions:

1. Without an explicit reference-image instruction, use original-textbook understanding directly. Do not search this library simply because it exists.
2. Explicitly designated current-task images determine the main visual style; textbook understanding partly supports subject/content adaptation and necessary factual accuracy, not a competing style selection.
3. A library subset contributes only when the user specifically requests that library or their earlier images. If current-task primary images are designated, any requested library support remains subordinate unless the user says to replace them.
4. Web reference research is also opt-in, not a required companion to library use. Do not automatically add search images.

Inspect every active image, keep observed traits separate from inferences and record actual paths/IDs and adopted aesthetic rules. Do not copy entire source pages, artwork, logos or protected compositions; do not alter teaching facts to fit a reference. Current-task images are not automatically added to a permanent library. The analysis is internal, not a new report or blueprint field.

## Variety without style drift

The master anchor fixes material logic, palette roles, typographic hierarchy and color roles, illustration/photo language, border grammar, recurring anchors, and emotional world. It does not fix one background, one layout, one shot, or one narrow chapter palette for the full deck. Multi-text lessons may use related, content-driven chapter dialects while retaining those master anchors.

For each page, select a content-specific focal subject and a teaching-function-specific composition. Track a scene signature containing focal subject, viewpoint, spatial depth, time/weather, and information structure. Apply these checks before blueprint delivery:

- never reuse the same complete background, hero image, crop, or scene arrangement on another page;
- never place the same dominant composition archetype on adjacent pages;
- do not repeatedly default to `top text + bottom landscape strip`, `left text + right image`, or any other familiar template when the teaching function changes;
- preserve meaningful maps, relationships, comparisons, timelines, close-ups, evidence diagrams, and reading routes instead of replacing them with decorative scenery; and
- use repeated palette, brushwork, paper or border treatment, waterline, and restrained motifs for unity while varying scene, crop, focal subject, scale, and information structure.

If the repetition review finds a run of visually interchangeable pages, rewrite only those page blueprints. Do not change the approved outline, page count, six-field visual-blueprint format, default deliverables, or the opt-in trigger for anti-garbled-text mode.
