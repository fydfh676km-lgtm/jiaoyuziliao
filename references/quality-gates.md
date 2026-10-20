# Evidence-based quality checks

Use the required plan-first stages in `workflow.md`. First deliver only the checked teaching-plan Word and wait for actual user approval before producing the outline, blueprint or script; this file adds no further approval gate. Check current stage/scope only. Existing evidence for unchanged files remains valid; after a repair, rerun that file's checks and affected cross-file relationships.

## Default document package

1. **Source and understanding:** original text has been understood and checked before lesson design: central meaning/concepts, content structure, critical evidence and learner obstacles support concrete teaching choices. All official designs/task sheets are considered against that reading, not copied as a substitute for it. Required items map to actual teaching blocks/pages; facts, quotations and tasks agree. Mechanical coverage or a summary alone does not prove understanding.
2. **Structure:** outline and six-field blueprint preserve their exact schemas and contiguous page IDs. Script `P1 页面标题` sections correspond to those IDs, with black spoken `师：` and red `【…】` cues, not legacy five-field labels. Period labels remain banned in courseware/outline/blueprint/script/exercises; only the new teaching-plan template permits its necessary period/time metadata.
3. **Teaching plan:** verify the twelve-module paragraph template and paired prompt rules, source-backed curriculum items, 2–4 measurable objectives and aligned tasks/activities/rubric. Check key/difficult points each ≥100 Chinese characters, substantive red/bold emphasis, flexibly organized, timed learning blocks with connected paragraphs covering teacher guidance, student action/output, transitions, evidence and support without repeated-field requirements, text-board structure/generation timing, layered homework and honest anticipatory reflection. Check session count, per-session block sums and overall total including labeled estimates; all suggested sessions must be covered. Both first-stage and final plans forbid PPT total count, page numbers and page-correspondence notes throughout body/tables/headers/footers/notes; verify actual mappings internally. Teaching-plan session advice must not truncate or split the complete continuous outline, nor count as official source segmentation for the page-cap exception.
4. **Rendered files:** every requested Word is a valid DOCX and every rendered page has been inspected for clipping, overflow, missing glyphs/pages, tables, contrast, emphasis and layout.
5. **Content-matched visual basis:** apply the actual route in `workflow.md`. With user images, verify their inspection and style identification, then active research and viewing of matching, lesson-compatible images unless the user excluded search. Without images, either verify inspected search references and traceable sources or validate `content-derived` text anchors, concrete aesthetic decisions and rationale; do not require a failed search before choosing the latter. A current explicit mandatory-online request must still be satisfied. Both routes need one coherent master style, content-specific page variation and low-AI/readability checks. For valid content-derived work, web-only checks are N/A because the route does not require them; this does not automatically make the blueprint a draft or block verification. Follow `workflow.md` for reuse, user-requested no-search and unavailable required research; retain failed optional-search attempts if switching to content-derived design, without claiming search completion. A screenshot or separate reference attachment is not required.
6. **Consistency and simulated lecture:** use the matrix in `deliverables.md` against shared records. Rehearse speech and real pages in order, checking teachability, black/red distinction, pauses, conditional responses, feedback, available material and display timing. Detect omissions, contradictions, jumps, repetition and premature conclusions. Check plan time fields against actual or explicitly estimated shared pacing; do not alter approved pedagogy. Structural passes cannot certify classroom effectiveness.

Apply `classroom-readability.md` during those checks in both ordinary and anti-garbled modes. For Word-only scope, review the outline's text capacity and blueprint size/layout decisions without generating slides or enlarging Word paragraphs to slide sizes. For requested slides or page images, inspect the actual essential text and labels at the standard-widescreen-equivalent size floor, contrast and normal full-page display; reject undersized or overflowing text even if OCR and file structure pass. A 4K export, contact-sheet thumbnail, prompt instruction or desktop preview is not evidence of a real classroom back-row trial. Preserve approved text/page count, repair only affected layouts, and record unavailable real-device checks truthfully.

Run the structural helper for the standard three-Word package:

```sh
python scripts/validate-documents.py --outline-visual "<combined.docx>" --lesson-plan "<plan.docx>" --speaker-script "<script.docx>" --expected-pages 30
```

For the first `plan-first` handoff before page division, check the complete lesson-plan Word alone:

```sh
python scripts/validate-documents.py --phase plan-review --lesson-plan "<plan.docx>"
```

This phase checks twelve modules, curriculum-basis structure, objective count, key/difficulty length, timed paragraph process blocks and text-board content. Neither phase requires visible page ranges; internal semantic mapping remains necessary. Render/review this Word and its source-backed logic, then hand off awaiting approval, not a finished package. Do not generate downstream files merely to satisfy this check.

Use the available bundled Python and the actual skill script path when outside the skill directory. Replace 30 with the approved count. The helper's `automatic_checks_pass` does not certify semantic accuracy, substantive emphasis, board quality, rendered layout, source coverage or WPS. Complete those manual/visual checks separately. For explicitly split/omitted artifacts or a user-requested alternate teaching-plan template, apply the relevant contracts to that actual scope rather than fabricating missing default files to satisfy the helper.

## Optional routes

Load optional standards only for outputs explicitly requested: `exercise-package.md`, `image-deck-mode.md`, `commercial-whole-slide.md`, `wps-safe.md`, or the requested PDF/marketing contract in `deliverables.md`.

For every optional PPTX, actual WPS opening/rendering is required to claim WPS-safe. If WPS cannot be used, record NOT_RUN and hand off a clearly unverified draft only when useful; do not call the optional PPTX or overall package verified. Do not withhold independently verified Word files.

## Final status

Record each applicable check as PASS, FAIL, NOT_RUN or N/A with artifact/version, actual evidence and reason. N/A must identify why the check does not apply (for example no PPTX requested), never hide an unavailable tool. Missing required evidence blocks verified. Make only observed pass claims; a planned action or a filename is not proof that it happened.

The default handoff is the requested Word documents, with no automatic search screenshot or research report. Keep reference provenance and selection evidence internal. If the user explicitly requests a source list or reference images, check and deliver that additional scope without changing the blueprint's six-field format.

Repair only failed artifacts/pages from the shared records. Apart from the required teaching-plan checkpoint or an unresolved material conflict requiring direction, do not ask for intermediate approval. Do not repeat an acceptance disclaimer in routine responses.
