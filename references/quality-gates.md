# Evidence-based quality checks

Use the two execution modes and stages in `workflow.md`; this file adds no approval gate. The user-selected `plan-first` checkpoint remains mandatory, while `auto` runs without interim approval. Check current stage/scope only. Existing evidence for unchanged files remains valid; after a repair, rerun that file's checks and affected cross-file relationships.

## Default document package

1. **Source and understanding:** original text has been understood and checked before lesson design: central meaning/concepts, content structure, critical evidence and learner obstacles support concrete teaching choices. All official designs/task sheets are considered against that reading, not copied as a substitute for it. Required items map to actual teaching blocks/pages; facts, quotations and tasks agree. Mechanical coverage or a summary alone does not prove understanding.
2. **Structure:** the outline and six-field visual blueprint follow the exact formats in `SKILL.md`, share contiguous page IDs, and preserve page count. The script has the same page IDs and five fields. User-visible materials contain no banned teaching-period labels.
3. **Teaching plan:** verify the seven-section native table layout, detailed process rows, distinct key/difficult point subsections (each ≥100 Chinese characters), substantive red/bold emphasis and lesson-specific design. Board must be a complete embedded image, not a text placeholder, and pass word accuracy, meaningful relationships, generation-order and readable proportional page-fit checks. First-stage plan-review deliberately has no PPT ranges; final mapped plan needs real complete page mappings.
4. **Rendered files:** every requested Word is a valid DOCX and every rendered page has been inspected for clipping, overflow, missing glyphs/pages, tables, contrast, emphasis and layout.
5. **Content-matched visual basis:** apply the actual route in `workflow.md`. With user images, verify their inspection and style identification, then active research and viewing of matching, lesson-compatible images unless the user excluded search. Without images, either verify inspected search references and traceable sources or validate `content-derived` text anchors, concrete aesthetic decisions and rationale; do not require a failed search before choosing the latter. A current explicit mandatory-online request must still be satisfied. Both routes need one coherent master style, content-specific page variation and low-AI/readability checks. For valid content-derived work, web-only checks are N/A because the route does not require them; this does not automatically make the blueprint a draft or block verification. Follow `workflow.md` for reuse, user-requested no-search and unavailable required research; retain failed optional-search attempts if switching to content-derived design, without claiming search completion. A screenshot or separate reference attachment is not required.
6. **Consistency and simulated lecture:** use the matrix in `deliverables.md` against shared source/teaching/lecture/page records. Walk the final spoken script and actual pages in sequence, checking teachability, natural transitions, question/anticipated answer/feedback coherence, available materials and correctly timed display. Detect omissions, contradictions, sudden topic jumps, excessive repetition and premature conclusions. Confirm that approved plan decisions were not silently rewritten. Internal pacing is not inferred from a prohibited Word field; structural passes do not certify classroom effectiveness.

Apply `classroom-readability.md` during those checks in both ordinary and anti-garbled modes. For Word-only scope, review the outline's text capacity and blueprint size/layout decisions without generating slides or enlarging Word paragraphs to slide sizes. For requested slides or page images, inspect the actual essential text and labels at the standard-widescreen-equivalent size floor, contrast and normal full-page display; reject undersized or overflowing text even if OCR and file structure pass. A 4K export, contact-sheet thumbnail, prompt instruction or desktop preview is not evidence of a real classroom back-row trial. Preserve approved text/page count, repair only affected layouts, and record unavailable real-device checks truthfully.

Run the structural helper for the standard three-Word package:

```sh
python scripts/validate-documents.py --outline-visual "<combined.docx>" --lesson-plan "<plan.docx>" --speaker-script "<script.docx>" --expected-pages 30
```

For the first `plan-first` handoff before page division, check the complete lesson-plan Word alone:

```sh
python scripts/validate-documents.py --phase plan-review --lesson-plan "<plan.docx>"
```

This phase still checks the seven sections, process fields, key/difficulty length, table structure and embedded board image. It omits page-range requirements because no final pages exist yet. Render and review that Word and its source-backed teaching logic, then hand it off as awaiting user approval, not a finished three-Word package. Do not generate downstream files just to make this first-stage check pass.

Use the available bundled Python and the actual skill script path when outside the skill directory. Replace 30 with the approved count. The helper's `automatic_checks_pass` does not certify semantic accuracy, substantive emphasis, board quality, rendered layout, source coverage or WPS. Complete those manual/visual checks separately. For explicitly split/omitted artifacts or a user-requested alternate teaching-plan template, apply the relevant contracts to that actual scope rather than fabricating missing default files to satisfy the helper.

## Optional routes

Load optional standards only for outputs explicitly requested: `exercise-package.md`, `image-deck-mode.md`, `commercial-whole-slide.md`, `wps-safe.md`, or the requested PDF/marketing contract in `deliverables.md`.

For every optional PPTX, actual WPS opening/rendering is required to claim WPS-safe. If WPS cannot be used, record NOT_RUN and hand off a clearly unverified draft only when useful; do not call the optional PPTX or overall package verified. Do not withhold independently verified Word files.

## Final status

Record each applicable check as PASS, FAIL, NOT_RUN or N/A with artifact/version, actual evidence and reason. N/A must identify why the check does not apply (for example no PPTX requested), never hide an unavailable tool. Missing required evidence blocks verified. Make only observed pass claims; a planned action or a filename is not proof that it happened.

The default handoff is the requested Word documents, with no automatic search screenshot or research report. Keep reference provenance and selection evidence internal. If the user explicitly requests a source list or reference images, check and deliver that additional scope without changing the blueprint's six-field format.

Repair only failed artifacts/pages from the shared records. Apart from the user-selected teaching-plan checkpoint or an unresolved material conflict requiring direction, do not ask for intermediate approval. Do not repeat an acceptance disclaimer in routine responses.
