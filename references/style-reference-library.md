# Persistent user visual-reference library

Use this reference when the user explicitly supplies a batch of images for future reuse, or when a previously created user visual-reference library is available during courseware production. The library is a retrieval aid, not model training and not a set of slide templates to copy.

## Available bundled library

The user-supplied Chinese classical/ink-wash collection is bundled in `assets/style-references/chinese-ink-wash/`, with 20 unchanged originals and a per-image `index.json`. For requests for 古风水墨, 水墨山水 or a compatible text-derived direction, read `chinese-ink-wash.md` and retrieve the active subset from this index before the existing reference-analysis step. Do not reload every image, force this direction on unrelated lessons, or depend on the original desktop folder. Current-task user instructions and references still take precedence. Including an image in the reference library is not commercial-use permission or authorization to upload it to a public repository.

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

## Automatic retrieval for each deck

Before visual-direction selection, derive a compact retrieval brief from the source ledger: subject, grade, genre, historical/cultural setting, geography, season, time, central imagery, emotional curve, page functions, projection density, and any explicit user preference. Retrieve candidates in this order:

1. factual and cultural compatibility with the textbook;
2. genre, topic, central imagery, and emotional fit;
3. audience and teaching-function fit;
4. the user's current explicit visual preference; and
5. visual distinctiveness from recently used courseware when that history is available.

Select one master-style anchor and at most two supporting composition or element references. Do not load the whole library into the prompt. If no candidate survives factual, cultural, or audience-fit checks, use a new content-driven direction rather than forcing an attractive but unsuitable reference.

Ancient poetry and classical-literature work should search the library first for compatible landscape, classical, ink-wash, blue-green landscape, gongbi, or literary-illustration references, while still matching the actual poem's season, geography, viewpoint, imagery, and emotional tone.

## Combine user references with content-matched research

The evidence order is fixed:

1. textbook and source ledger control facts, sequence, scene meaning, and historical/cultural accuracy;
2. the user's current explicit direction controls intentional overrides;
3. compatible current-task user references establish the primary aesthetic direction;
4. a compatible selected user-library anchor and supporting references contribute reusable aesthetic, composition, or element principles, subordinate to the current request; and
5. actual inspected web/image research supplies scene, material and composition evidence matching both the established style and text. Without current-task user images, the direction may instead be derived from textual understanding and design judgment, with compatible authorized-library evidence where available; keep observed cues distinct from inferred choices.

For a new blueprint, follow `visual-system.md`: understand supplied images first, then actively find same-style, content-compatible visual references. Without current-task images, independently select the permitted research or text-derived design route. A current explicit requirement for web research still controls. No dedicated Xiaohongshu search or standalone screenshot is required. A local revision that retains its direction reuses existing evidence, and a frozen image-rendering contract is not re-planned. Record the actual route truthfully; a library match or design inference must not be presented as a newly searched result.

Extract abstract principles from every active source separately, record provenance and the adopted rules internally, and synthesize one independent master system; do not average conflicting styles or reproduce any source page, asset, text, logo, watermark, or protected composition. Current-task references and researched images are not automatically added to the persistent library. The research record is not a new deliverable or blueprint field.

## Variety without style drift

The master anchor fixes material logic, palette roles, typographic hierarchy and color roles, illustration/photo language, border grammar, recurring anchors, and emotional world. It does not fix one background, one layout, one shot, or one narrow chapter palette for the full deck. Multi-text lessons may use related, content-driven chapter dialects while retaining those master anchors.

For each page, select a content-specific focal subject and a teaching-function-specific composition. Track a scene signature containing focal subject, viewpoint, spatial depth, time/weather, and information structure. Apply these checks before blueprint delivery:

- never reuse the same complete background, hero image, crop, or scene arrangement on another page;
- never place the same dominant composition archetype on adjacent pages;
- do not repeatedly default to `top text + bottom landscape strip`, `left text + right image`, or any other familiar template when the teaching function changes;
- preserve meaningful maps, relationships, comparisons, timelines, close-ups, evidence diagrams, and reading routes instead of replacing them with decorative scenery; and
- use repeated palette, brushwork, paper or border treatment, waterline, and restrained motifs for unity while varying scene, crop, focal subject, scale, and information structure.

If the repetition review finds a run of visually interchangeable pages, rewrite only those page blueprints. Do not change the approved outline, page count, six-field visual-blueprint format, default deliverables, or the opt-in trigger for anti-garbled-text mode.
