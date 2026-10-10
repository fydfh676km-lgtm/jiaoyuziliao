# Visual-system decision contract

Use this reference after `content_approved` to determine the visual system and page-by-page blueprint. After the explicit start command, complete this checkpoint internally and continue production; no separate visual approval is required.

When a persistent user visual-reference library is available, read `style-reference-library.md` before selecting the master visual direction. Combine compatible user references with content-matched web/image research as described below; textbook content remains authoritative for factual and scene accuracy. Do not perform a dedicated Xiaohongshu search or require a standalone reference screenshot.

## Content-matched style research

Before creating a new blueprint, derive a compact visual brief from the actual text already read: genre, era and geography, season, central imagery, emotional movement, audience, and page-level teaching purposes. Unknown facts remain unknown; do not assign a season, location, or historical setting merely to fit an attractive style. First identify a candidate aesthetic direction from the user's images or from understanding the text, then find actual visual references matching BOTH that style and the lesson content. Search for useful scenes, backgrounds, elements, materials, composition and light, not only a style name or finished courseware template.

For the search route, start with two or three distinct queries combining the identified style's concrete traits, a textual scene/subject, and the needed visual treatment. For example, if compatible user images establish restrained watercolor, seek watercolor spring vegetation or rural scenes rather than unrelated polished styles; this is not a preset for every lesson. Proactively use web/image search and open useful images. When browser interaction is needed, use the system default browser unless the user specifies another and read the applicable browsing skill. Do not create another mandatory browser or login workflow.

Actually open and inspect usable reference images before claiming to have analyzed their style. Search titles and snippets alone are not visual evidence. Prefer sources that allow the pictured work and its context to be inspected; exclude unreadable, irrelevant, login-only, blank, or error results. Stop once there is sufficient evidence to select a content-compatible direction; reformulate only to fill a concrete relevance gap. Do not search again for every page or keep collecting attractive but redundant examples.

Textbook facts and explicit user preferences take priority. With compatible user images, inspect them first, establish their primary aesthetic traits, and actively search for matching references to supplement relevant scenes, materials and composition; new results must not pull the deck into an unrelated style. With no current-task images, independently infer a suitable direction from the text: either research matching images or develop a concrete design directly from textual understanding and design judgment, optionally informed by an authorized library. The direct-understanding route is permitted normally, not only after search failure; never ask for a reference image as a prerequisite. A current explicit demand for web references still requires actual search. A contradictory reference cannot override textbook facts; retain compatible abstract traits or discard it instead of blending incompatible styles. Do not create a persistent library without a future-reuse request.

Maintain research evidence inside the existing task/reference records: actual queries, source URLs or authorized local paths, whether an image was visually inspected, its relevance to the text, and the concrete abstract rules adopted or rejected. This is internal evidence, not an extra report, screenshot delivery, or seventh blueprint field. For the no-image direct-understanding route, record `content-derived`, the textual anchors and design rationale instead of invented image sources. If networking is explicitly prohibited, record `skipped-by-user`; if required search is unavailable, record `unavailable` and the real limitation. Use `workflow.md` for route-specific acceptance and transitions. Never claim that a search result was viewed when it was not.

Translate chosen reference cues or text-derived design decisions into every page's existing six fields: style/material, content-specific elements, typographic hierarchy, composition, camera/light, and continuity/variation. Style keywords or collected image links alone are not a blueprint. If no real image was used, describe decisions as inferred, not observed or learned from an online reference.

For a local revision that preserves the topic and visual direction, reuse the already inspected evidence instead of researching again. Search anew only if the topic or main direction changes or the user explicitly asks for fresh references. Record missing historical evidence without inventing it or expanding the edit into a new search. Image-only execution with a frozen content/style contract reuses that contract and its references; it does not reopen content planning or style research.

## Reference authenticity and low-AI gate

Before extracting style rules or drafting the blueprint, inspect every supplied or collected reference for realism, provenance, and visible AI artifacts. Separate what is directly observable from any claim that the image is AI-generated; when the distinction cannot be established confidently, label the source `AI-likeness/provenance unverified` and use it only as an abstract style reference. Never copy its factual imagery, wording, logo, watermark, pseudo-text, or composition. If a visual reference has strong AI artifacts, do not reproduce those artifacts in the blueprint or generation prompt.

The visual system and generation prompts should deliberately minimize generic AI appearance. Prefer natural proportions, physically coherent light/shadow, believable material grain, controlled color, purposeful asymmetry, authentic editorial/photographic/print/handmade cues, and topic-specific objects. Reject or regenerate assets with waxy/plastic surfaces, hyper-saturated gradients, impossible anatomy or perspective, repetitive cloned details, floating objects, illegible pseudo-text, accidental logos/watermarks, excessive symmetry, generic glossy 3D, or decorative effects without a teaching purpose. Treat this as an internal preflight and asset-quality gate; it does not add a seventh field to the user-facing six-field blueprint.

## Analyze every active visual reference

Create one analysis record for every current-task reference and every library reference selected for this deck. Do not re-analyze or load the entire persistent library during ordinary production; use its stored index to retrieve the active subset first. Record what is directly observed separately from an inference, and assess it against the approved lesson type, audience, topic, and content contract. Do not recreate a third-party page, composition, illustration, photograph, logo, type treatment, or other protected element.

For researched images, record what was actually visible at the inspected resolution. A thumbnail supports only traits that can genuinely be seen; it cannot establish an unseen full-page layout, legibility, or deck-wide page rhythm. User-supplied search-result screenshots may be analyzed as composite references, but do not infer unseen individual pages or treat third-party popularity as proof of content suitability.

```yaml
reference: "Source identifier and provenance"
source: "Actual source URL or authorized local path; query when discovered by search"
inspection: "What image was actually viewed and any resolution or access limitations"
content_fit: "Connection to the text's imagery, setting, emotion, and teaching purpose"
palette: "Observed colors and their roles"
typography: "Observed hierarchy, relative scale and weight, color roles, spacing, and legibility; name a font only when the user explicitly specified it"
imagery: "Illustration, photography, icon, or texture language"
grid: "Alignment, columns, margins, and repeated structures"
hierarchy: "How title, key message, support, and actions are prioritized"
whitespace: "Breathing room, margins, and grouping"
density: "Information volume and scanability"
page_rhythm: "How cover, section, body, activity, and closing pages vary"
suitable_contexts: ["Audience, subject, age, or teaching situation it supports"]
unsuitable_contexts: ["Audience, subject, age, or teaching situation it weakens"]
copyright_sensitive_elements: ["Specific artwork, photo, logo, character, font, layout, or other element requiring avoidance, permission, or licensed use"]
adopted_rules: ["Concrete abstract principles retained for this deck; no copied source assets"]
```

`copyright_sensitive_elements` must be explicit even when the answer is `none identified from the supplied reference`; unknown provenance is not permission to reuse. Extract only abstract, transferable rules. For any asset used later, use an original generation prompt, a licensed source with its licence checked, or a user-supplied asset with confirmed rights.

## Resolve conflicts and select one direction

For a clear topic and compatible references, select one suitable direction directly. Do not routinely generate 3–5 discarded alternatives. When references genuinely conflict, record the incompatible languages and topic/audience fit; compare at most two or three plausible directions if comparison would resolve the conflict. Offer choices only when the user asks for exploration or is still planning a consequential unresolved choice; after start select internally. Each direction actually needed can use this compact record:

```yaml
name: "Direction name"
keywords: ["three", "to", "five"]
palette: ["#RRGGBB"]
layout_logic: "Repeated grid and hierarchy"
imagery: "Illustration or photography language"
fit_reason: "Why it suits the approved lesson"
risks: ["Readability or tone risk"]
retained_rules: ["Abstract rules observed in references or justified from the text; distinguish the basis"]
discarded_elements: ["Elements that do not fit"]
```

The options must differ in visual language, not merely shade, decoration, or slide-cover treatment. Do not present “choose the children’s illustration/Apple minimal/magazine style” as the decision; each option must be a newly named direction that applies abstract rules to the approved lesson. `retained_rules` may contain only abstract principles; `discarded_elements` must name unsuitable, unlicensed, overly derivative, or lesson-incompatible cues. Before the start command, these may be shown as planning options; after the start command, select the strongest topic-appropriate direction internally and continue without asking for approval.

## Gate order for provisional directions

Visual conflict analysis is conditional, not a new compulsory artifact. Reuse a previously selected direction unless the user changes it or concrete source/quality evidence invalidates it. After start, do not solicit a visual choice or other routine mid-process approval.

## Scene-driven prompts and Chinese-aesthetic routing

Every selected direction and per-page prompt must create a recognizable place, moment, viewpoint, and atmosphere. A style label such as `古风背景`, `水墨风`, `山水画`, or `唯美意境` is not a complete visual instruction. Build the scene from the lesson content using this positive recipe:

1. identify the page's teaching purpose and the exact textual image, event, object, person, or relationship that should become the visual focus;
2. define the viewpoint and spatial depth through foreground, middle ground, and distance, using scale, overlap, mist, light, water, paths, architecture, or vegetation only when they fit the source;
3. specify source-supported season, time of day and weather; when these are unknown, retain an unspecified or neutral setting and distinguish chosen light, color temperature, material/brush language and emotional treatment as design decisions rather than textbook facts;
4. reserve purposeful negative space and a readable text region without weakening the main scene; and
5. keep every motif historically, geographically, seasonally, and semantically compatible with the text.

Treat Chinese landscape, classical, and ink aesthetics as a preferred direction whenever they genuinely support the lesson. For ancient poetry and classical-poetry content, this preference becomes mandatory: lock the whole deck to one coherent Eastern master visual world. A multi-poem or multi-text deck may use controlled, source-driven chapter dialects—such as related variations of restrained ink wash, blue-green landscape, gongbi, mineral color, or classical literary illustration—provided they share the same material logic, palette roles, typographic hierarchy, border/shape grammar, recurring anchors, and emotional progression. Ground every page in the poem's actual imagery and emotional movement—for example its mountain-water relationship, moonlight, river, frontier, fields, pavilion, boat, rain, snow, flowers, birds, figures, or travel perspective—only when supported by the text. Show the poem's season, geography, viewing position, distance, stillness or motion, and emotional temperature; do not substitute an interchangeable landscape wallpaper or switch to an unrelated style.

Keep the result vivid without turning it into a pile of generic `Chinese-style` symbols. Seals, scrolls, cloud patterns, cranes, lanterns, bamboo, plum blossom, pagodas, torn paper, and calligraphy are optional content-dependent accents, not an automatic checklist. Remove any motif that lacks a textual or teaching reason. Prefer one memorable scene and a restrained set of authentic details over decorative abundance, tourist-poster clichés, or AI-looking fantasy spectacle.

Encode the scene through the fixed six user-facing fields only:

- `画面风格` begins with a compact master-world anchor, then names any content-driven chapter dialect, medium or brush treatment, atmosphere, and color relationship;
- `添加元素` identifies content-supported subjects and their foreground/middle-ground/distant placement, including only necessary traditional accents;
- `文字字体与重点标注` defines typographic hierarchy, relative scale and weight, placement, color roles, and selective emphasis without naming a specific font by default;
- `布局排版` defines scene-to-text proportion, visual movement, negative space, reading order, and the stable reading zone;
- `镜头与光影` defines camera position and height, shot scale, viewpoint or lens feeling, spatial depth, time, light direction, softness, color temperature, and atmosphere; and
- `画面去重与统一约束` states this page's unique scene signature, how it differs from the nearest similar or adjacent pages, what must not be reused, and which master-world anchors remain constant.

Controlled chapter dialects do not create unrelated decks. Vary the crop, spatial depth, focal subject, accent palette, related brush treatment, and scene rhythm from page to page or text to text while retaining the same master material, palette roles, typographic hierarchy, border/shape grammar, recurring anchors, and emotional logic. When the optional anti-garbled-text mode is active, keep the landscape and classical scene richness, but place required inner-page text in the clean, front-facing, high-contrast reading regions defined by that mode; page 1 retains its existing visual-quality exception.

## Composition, focal hierarchy, continuity, readability, and rhythm

Before choosing a composition, classify the page's teaching function internally: cover or opening, context, explanation or close reading, comparison or evidence, relationship/map/timeline, activity or practice, synthesis, transfer, or closing. Select a content-appropriate composition archetype from that function. A deck's subject style does not justify forcing every page into the same landscape, desk, scroll, split-screen, card grid, or text-over-image arrangement.

Give every page one primary visual focal point and an intentional reading order. Define what the audience sees first, reads second, and inspects last; use one main subject or core diagram with no more than two supporting semantic groups. A semantic group may contain multiple tightly related objects. Overview, comparison, route, timeline, and task pages may use three to five visible nodes when those nodes belong to one clear organizing structure and do not compete as equal focal points. The title, scene, person, decorative frame, and information graphic must not compete at equal strength. Encode the focal order and reading path inside `布局排版`.

When a person, place, building, or important prop recurs, create an internal recurring-character and recurring-object continuity sheet before drafting the page blueprints. Keep identity anchors stable across pages: age and facial features, hair, clothing silhouette and color, role, era, architecture, vessel, book, desk, map, tool, or other defining form. If the source requires a time, season, location, or emotional change, describe that change while preserving enough anchors for the entity to remain recognizable. Put page-specific continuity cues inside `添加元素`; do not print the continuity sheet as an extra deliverable.

Before drafting the user-facing blueprint, extend the existing shared page records with the visual map: page/text or chapter, teaching function, primary subject/action, composition axis or route, shot/viewpoint, time/light/weather, motion or stillness, information structure, nearest similar page, and forbidden reuse. Do not separately rewrite a second full page plan. For a multi-text deck, plan a justified emotion-and-light progression. Use these decisions to populate the six output fields; the internal map is not another deliverable.

Make each page description self-contained enough to be copied into an external image-generation call without losing the deck identity. Begin `画面风格` with a short master-world anchor, then add the chapter dialect and page-specific scene. In `添加元素`, name the primary subject, action or state, approximate count or role where relevant, foreground/middle-ground/distant placement, scale, relationships, and any historical/geographic constraints. In `布局排版`, name the dominant axis or path, image-to-text proportion and zones, reading order, and purposeful negative space. Avoid padding these fields with repeated generic prose.

A baseline classroom-readability floor applies even when the optional anti-garbled-text mode is inactive. This baseline does not activate that mode, require large blank panels, prohibit artistic typography, or reduce scene richness. It requires projected body text to remain comfortably legible, adequately contrasted, and separated from high-frequency texture or competing detail; do not describe required body copy as tiny, narrow, miniature, fine-print, or “缩小一级”, do not shrink essential copy to enlarge an illustration, let decoration cross critical character strokes, or use low-contrast thin text. Reserve calligraphic or highly decorative treatment for short display text, and keep emphasis selective—normally one to three short teaching priorities per page—so hierarchy remains clear. By default, describe typographic character and hierarchy rather than naming a specific installed font or font category; an explicit user font request overrides this default. Encode this baseline inside `文字字体与重点标注` and the reading-region placement inside `布局排版`.

Run a whole-deck rhythm check in addition to the duplicate-background check. Adjacent pages must not repeat the same dominant composition. No three consecutive pages may all use the same visual-density pattern, the same image-to-text balance, all full-bleed scenery, or all heavy text. Alternate scene-led, information-led, diagram-led, and quieter pages as the teaching sequence permits, while retaining the locked master visual language. When a content sequence legitimately needs related page types, vary focal subject, crop, viewpoint, scale, depth, and information structure so the pages remain distinguishable. Rewrite only the repeated or monotonous page blueprints.

## Per-page visual blueprint

After a direction is selected internally or by prior task confirmation, define every page using this exact user-facing format. Do not add or rename fields. Any internal analysis may remain internal and must not be printed in the blueprint.

### Master-world lock with controlled chapter dialects

The selected direction becomes the deck's only master visual world. Apply the same underlying material/texture logic, palette roles, typographic hierarchy and color roles, icon and border/shape grammar, recurring anchors, and tone to every page. Allow content-driven chapter dialects in related accent palette, brush treatment, scene vocabulary, composition, crop, element choice, information density, and shot language, especially when one deck contains several poems, texts, places, or periods. Do not introduce an unrelated second style such as switching from Eastern literary illustration to neon flat graphics, from documentary photography to cartoon fantasy, or from handmade print to generic glossy 3D. Every variation must still look authored inside the same master world.

Before finalizing the blueprint, compare all pages against the locked master world and flag any page whose `画面风格` introduces an unrelated language or lacks the compact master anchor. Rewrite that page inside the master world; preserve justified chapter dialects rather than flattening every text into identical scenery. This check is internal and does not add a field to the user-facing blueprint.

Consistency applies to the visual language, not to repeated backgrounds or repeated composition. Do not reuse the same complete background, hero image, crop, or scene arrangement across multiple pages. Adjacent pages must not share the same dominant composition archetype. Track each page's scene signature—focal subject, viewpoint, spatial depth, time/weather, and information structure—and rewrite repeated runs before delivery. Recurrent palette, brushwork, border grammar, waterline, paper texture, or small motifs may unify the deck, but every page must receive a content-specific scene and teaching-function-specific composition.

```text
第X页
画面风格：
添加元素：
文字字体与重点标注：
布局排版：
镜头与光影：
画面去重与统一约束：
```

Replace `X` with the actual Arabic page number. The page number and all six visual decisions must correspond to the approved page outline. Apart from the page number inside `第X页`, do not prefix any field with a number, Chinese numeral, circled number, letter, bullet, or other list marker; each of the six labels must start directly with its exact text, appear exactly once in the fixed order above, and contain a nonempty page-specific value. Do not output `页面标题：` in the visual-blueprint block and do not add a seventh field. The blueprint must cover every page exactly once, preserve the approved total, and contain no `课时` wording or period labels. `镜头与光影` must be specific to this page rather than generic “柔和光影”; `画面去重与统一约束` must name a concrete difference and retained master anchor rather than repeat the same boilerplate on every page.

An approved reusable layout family is the only exception to a bespoke page blueprint. It may define repeated rules internally, but the user-facing mapping for every covered page must still use exactly the six fields above and identify that page's topic-specific style, elements, text emphasis, layout, camera/light, and unique-versus-shared visual decisions.

Final coordinated-package production requires every page to have a complete six-field visual blueprint or an explicitly defined reusable layout family. The earlier `plan-first` lesson-plan Word handoff is governed by `workflow.md` and does not require nonexistent page blueprints. Complete the visual check internally and continue; it adds no visual approval checkpoint.
