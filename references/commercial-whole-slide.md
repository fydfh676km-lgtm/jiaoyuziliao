# Commercial whole-slide image contract

Use this contract whenever an educational image-only PPT is intended to look saleable, premium, commercial, or comparable to a polished courseware marketplace preview. It replaces the background-first workflow for that PPT rendering stage.

## Non-negotiable outcome

Every final PNG must already look like a finished commercial slide before it is placed in PPTX. The generated raster contains the complete composition: topic-specific illustration, title hierarchy, body copy, information modules, decorative details, page rhythm, and visual storytelling. Do not generate wallpaper and then cover it with a large generic text panel.

The slide must communicate its teaching purpose at thumbnail size and remain readable at full-screen classroom size. Visual polish never permits invented textbook facts or reordered frozen content.

## Strategy selection

Use `commercial-whole-slide` by default when all of the following are true:

- the requested PPTX is image-only or the user prioritizes visual quality over editability;
- the deck is described as commercial, saleable, premium, polished, marketplace-ready, or is compared with a high-quality courseware reference;
- the page outline and visual blueprint are frozen or can be frozen before generation.

Use `deterministic-text` only when the user explicitly prioritizes editable text, byte-for-byte text rendering, accessibility, or zero OCR risk over integrated whole-slide composition. Do not silently choose deterministic text merely because it is easier to verify.

If the user later requests an editable version of a commercial whole-slide deck, preserve the approved full-page visual as the source of truth and reconstruct editable text/objects after visual production. Never downgrade the commercial whole-slide design in advance to simplify editing.

## Reference-to-style pipeline

1. Reuse the frozen blueprint's style and its actually inspected user, authorized-library, and content-matched web/image references. If a new blueprint is genuinely needed within the requested scope, first follow `visual-system.md`; do not re-plan frozen content/style or initiate a dedicated Xiaohongshu search. Analyze active references only for transferable principles: palette roles, illustration family, material, title scale, information density, page rhythm, and decorative grammar. Keep provenance and adopted rules internal; no standalone reference screenshot is required.
2. Write one deck style bible with a named visual world, fixed palette, material vocabulary, recurring motifs, character sheet, typography behavior, prohibited cues, and originality boundaries.
3. Select `min(3, pageCount)` distinct anchor pages before the full run. For decks of at least three pages, use the cover, a standard content page, and a dense information/analysis page; for one- or two-page decks, use all pages. Generate one candidate per anchor first and retain it as soon as it passes. The anchors must demonstrate the available design range; three anchors do not require nine generated images.
4. Use the style bible and the most relevant approved anchor as visual conditioning for every subsequent page. A verbal prompt alone is insufficient for continuity.
5. Do not copy a reference slide, branded asset, logo, creator signature, or distinctive protected composition.

## Whole-slide prompt stack

Every page-generation call must include, in this order:

1. `product standard`: finished 16:9 commercial educational slide, not background art, not poster-only art, not a template mockup;
2. `deck style bible`: palette, material, illustration language, typography behavior, recurring motifs, character continuity, and prohibited cues;
3. `page role and teaching action`: what the audience must understand or do on this page;
4. `exact visible copy`: approved title and concise page text, with hierarchy and line grouping;
5. `page-specific visual narrative`: named people, objects, scenes, diagrams, textual evidence, or relationships that directly explain this page;
6. `layout archetype`: a composition chosen for this page rather than a repeated default;
7. `micro-detail requirements`: page number, divider, label, seal, texture, marginalia, or content-relevant ornament as appropriate;
8. `negative constraints`: no watermark, no logo, no UI chrome, no mockup frame, no generic stock-photo look, no pseudo-text, no empty oversized panel, no unrelated decoration, no repeated prior-page composition.

Do not ask the model for a text-free background in this mode. Do not reserve a generic rectangular safe zone covering most of the slide.

## Composition and density rules

For decks of 20–30 pages:

- use at least six distinct dominant layout archetypes across the deck;
- do not repeat the same dominant composition on more than two consecutive pages;
- no single layout archetype may occupy more than 25% of the deck;
- alternate scale, axis, depth, focal position, and density while preserving the same visual world;
- use at least one immersive cover/section composition, one contextual portrait/document composition, one story/process composition, one comparison/evidence composition, one activity/workspace composition, and one synthesis/closing composition when the content supports them;
- a pale or translucent text panel may occupy more than 45% of a slide only for genuinely text-intensive evidence, ancient-text, or workspace pages, and never on more than two consecutive slides;
- on story, context, process, comparison, and synthesis pages, include at least three meaningful content-linked visual units or one sufficiently rich visual narrative with multiple readable layers;
- cards are semantic containers, not the default page surface.

The cover must contain a content-specific protagonist or symbolic action, contextual environment, and title treatment integrated into the same composition. A large title beside one generic object is not a commercial cover.

## Text integration and correction

Model-rendered text is allowed because integrated typography is part of the commercial composition. Keep page copy concise enough to render well; split overloaded content during the frozen outline stage rather than shrinking it into illegibility.

After generation, compare the visible title and essential teaching text with the frozen strings using OCR plus visual inspection:

- title: exact match required;
- names, quotations, dates, definitions, and task instructions: exact match required;
- ordinary explanatory body text: at least 98% character match and no semantic change;
- no pseudo-text, duplicated words, broken punctuation, missing line, or invented label is permitted.

Repair a failed text region by localized image editing or by replacing only the defective typographic region with a style-matched overlay. Do not cover the page with a new large panel. After correction, re-run OCR and visual review.

## Candidate and repair policy

- Generate one candidate for each anchor and each remaining page first. Reuse a passing candidate immediately; do not generate extra candidates for routine comparison.
- The total budget is at most three full-page candidates per page, including the initial generation and every full-page regeneration. A failed local repair may lead to another candidate from the same frozen content and a different layout archetype, only while that budget remains.
- Permit at most two localized repair rounds per candidate. Each candidate's `generationAttempts` equals its initial generation plus its local repairs (`repairRounds + 1`); it is not the page's full-candidate count. Switching to a new full-page candidate never resets the total page budget.
- Record `candidateCount` from 1 to 3. For multiple candidates, record `candidateHistory` in actual generation order, with each entry containing `repairRounds` and `generationAttempts`; its length must equal `candidateCount`. Record the 1-based `selectedCandidate`, and make the top-level retry fields match that selected entry. A legacy single-candidate record may omit this history because its existing retry fields describe the complete budget; multi-candidate records with missing history do not pass budget verification.
- If all three full-page candidates or the final candidate's two local repairs fail, report the page as failed. Do not generate a fourth candidate or report the page as verified.
- Preserve passing pages. Do not restart the full deck to repair one page.

## Commercial acceptance score

Review every final page against six 0–100 dimensions:

| Dimension | Required evidence |
|---|---|
| Content integration | Visuals and typography jointly explain this page's teaching content |
| Visual hierarchy | Clear title, entry point, reading path, and supporting levels |
| Page specificity | The page cannot be reused for an unrelated lesson by changing only text |
| Style continuity | Palette, material, motifs, characters, and typography belong to the same deck |
| Composition quality | Balanced density, intentional cropping, depth, spacing, and thumbnail impact |
| Artifact cleanliness | Correct text, no watermark/logo/pseudo-text, no anatomical or visual defects |

A page passes only when the average is at least 85, every dimension is at least 75, title and essential-text checks pass, and no fatal defect remains. The whole deck additionally passes only when the layout-diversity rules and adjacent-page continuity checks pass.

## Fatal rejection symptoms

Reject and regenerate any page showing one of these symptoms:

- wallpaper plus a large blank/transparent text board;
- repeated left-text/right-picture split used as a default template;
- attractive but content-agnostic hero art;
- one isolated object with insufficient teaching information;
- dense cards floating on an unrelated background;
- inconsistent protagonist, costume, era, illustration medium, or palette;
- visible text errors, pseudo-text, watermark, logo, interface chrome, creator handle, or marketplace badge;
- a composition materially copied from a supplied reference.

## Packaging and verification

Set `deck.renderMode` to `commercial-whole-slide`. Each slide has one reviewed generated image layer named `whole-slide`, positioned at `x: 0, y: 0` and covering the exact deck resolution. The source raster must have the same aspect ratio as the deck: proportional enlargement is allowed, but implicit cropping or stretching is not. A ratio mismatch is a failed page and must be repaired and re-reviewed before packaging. Record the layout archetype, OCR verdict, per-dimension commercial score, candidate count/history, repair rounds, and visual checks in `visualReview`.

Package the reviewed full-page PNGs without adding generic layout panels. Produce 3840×2160 final PNGs, a contact sheet, and the image-only PPTX. Inspect the contact sheet for deck rhythm and at least the cover, one standard page, one dense page, one activity page, and the closing page at full resolution. Open the PPTX in WPS when available and reject any file that prompts for repair or displays cropping, scaling, or page-order errors.
