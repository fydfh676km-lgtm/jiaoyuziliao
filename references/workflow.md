# Execution contract

This file owns intake, textbook understanding, the staged execution flow, shared teaching records, source provenance, and bounded recovery. `SKILL.md` owns visible formats, output scope, page cap, and topic-matched style research. Artifact standards own acceptance. Every complete-courseware run uses the required `plan-first` lesson-plan approval checkpoint; other “approved” state names are internal checks.

## Select once and reuse

Create one project-local execution record (structured data or an existing equivalent) for an end-to-end run; do not create it for a simple question or inspection. Reuse it after interruptions and update it only when the user changes requirements, sources change, or a check exposes an error.

```yaml
task:
  started: false
  topic: ""
  audience: ""
  product_mode: premium
  review_mode: professional-advisor
  execution_mode: plan-first  # required lesson-plan approval before downstream work; distinct from review_mode
  mode_source: default
  requested_versions: [A]  # B or [A, B] only when explicitly requested
  version_source: default
  page_count: null  # optional single-variant alias, not authoritative for both
  page_counts: {}  # selected variant IDs mapped to their own totals
  source_period_count: null
  duration_minutes: null
  duration_source: unspecified  # user | source | estimate | unspecified
  lesson_sessions: []  # internal session/block times; not slide divisions or page-cap evidence
  anti_garbled_text: false
  requested_extras: []
sources: []
text_understanding:
  status: pending  # checked | incomplete
  source_anchors: []
  content_structure: []
  teaching_decisions: []
  unresolved_issues: []
lesson_plan:
  version: null
  status: pending  # drafted | internally-checked | awaiting-user | user-approved
  approved_version: null
  approval_evidence: null
teaching_blocks: []
visual_research:
  status: pending  # content-derived | reference-led | complete (explicit web research) | reused | skipped-by-user | unavailable
  queries: []
  reference_ids: []
  content_anchors: []
  design_decisions: []
  search_attempts: []
  selected_direction: null
  variant_decisions: {}  # requested version -> its direction/page-design decisions
  reason: null
pages: []
deliverables: []
checks: []
```

Record the explicit request that enabled each nondefault variant, optional output or prompt mode. Version selection follows `deliverables.md`: no version specified means A only; explicit B means B only; both must be explicitly requested. A reference image/style request alone does not enable both. “按流程开始制作” starts the existing scope without enabling B, PPTX, exercises, marketing or anti-garbled text. Honor current explicit custom requirements; identify and rebuild only affected dependencies.

Sources, checked understanding, teaching blocks and the approved lesson plan stay shared. Record selected variant IDs on page, visual-decision, script-mapping, deliverable and check entries; resolve a page by `(courseware_version, page)`, not its page number alone. Each selected variant has a complete page sequence and its own `page_counts` value within the same source-based cap. When only one is selected, the existing flat single-variant page records may be reused. For both, do not combine or overwrite independent A/B page orders, scene decisions or display cues. These fields are internal and never printed in lesson-plan/page schemas.

For duration, preserve a user/source value when supplied; otherwise state proposed session count, minutes per session and overall total in the teaching-plan Word, without routine confirmation. Check each session's block sum and the overall sum against the shared pacing record, including transitions, thought and feedback. Never present estimates as confirmed. These session decisions are teaching-plan implementation advice only: simulate and paginate the full requested textbook scope into one continuous complete outline, blueprint and script, not one selected session or multiple decks. No timing fields or period labels enter the fixed outline/blueprint or script section titles. A model-recommended three-session plan is not source_period_count evidence and does not enable the 30–35-page exception.

## Source intake

For ordinary SmartEdu requests, invoke `$smartedu-numbered-lesson-reader` (user alias `$smartedu-reader`) first. Read the requested electronic textbook, every associated teaching design, and every learning-task sheet in source order, including all source teaching segments. Reuse a complete current digest of the exact same source instead of rereading it. Invalidate only changed or previously unread portions.

When the user supplies only local files or another source, use the explicitly authorized materials and record that SmartEdu was not supplied. Never invent platform contents or silently substitute another lesson. A complete direct image-deck contract does not require new textbook intake.

Record the exact user-requested lesson/section scope before drafting. Access to a whole textbook, related official plan, template or unit does not authorize teaching its other lessons: filter cross-lesson suggestions out of the current plan's goals, tasks, homework, evaluation and reflection. Keep necessary contextual explanation in service of this lesson, not a new course task. Cross-text or unit-integrated learning requires the user's explicit requested scope; otherwise use this lesson's consolidation or omit unnecessary extension. Carry that same boundary into the later lecture, outline and blueprint.

Read lesson inputs within the user's requested scope and the current project's reference materials. New blueprints use textbook understanding directly unless the user explicitly designates style-reference images. Designated references lead the aesthetic direction, with textbook understanding as supporting content context. Visual-reference web search and library retrieval are opt-in only under the rules below and `visual-system.md`; necessary textbook/official-source/curriculum verification is unaffected. Neither route authorizes scanning unrelated local folders. Project content never becomes installed Skill content. Explicit future-library reuse authorizes indexing the supplied images under `style-reference-library.md`; ordinary production does not authorize a new reusable rule or library import.

Give each source item a stable ID and record:

- kind: textbook, teaching design, task sheet, visual reference, user fact/preference, or model inference;
- exact file/URL and page/section/segment, plus read/support status;
- required content/task IDs and their intended page IDs or teaching-process blocks;
- any source conflict, gap, or uncertainty that affects the product.

Facts come from evidence; user confirmation records a preference, not proof of an empirical claim. Textbook controls facts and sequence; teaching designs and task sheets supply teaching emphasis/tasks. Visual references support aesthetic choices, not new textbook facts or required lesson coverage. Deduplicate repeated segment content into one continuous lesson while preserving required coverage. Check every required ID has a valid target, then review semantic accuracy separately: an ID match alone does not prove coverage.

For every requested topic, inspect its own textbook edition's accompanying `读读写写` section, including the pages after the main text. Preserve its complete word list and exact source anchor in the existing source/understanding record; retain topic attribution when several texts are combined. Treat these words as required in-scope teaching content, not an opt-in exercise package. Map the full list to actual lesson-plan learning blocks before plan handoff, then to visible outline copy in each selected variant after approval. Follow `teaching-plan-standard.md` for classroom treatment. A verified absence is N/A; an unread/missing column page is an unresolved source gap, not evidence that the column does not exist. Use the existing source-recovery/material-conflict rules rather than borrowing another edition's list or inventing one.

## Review mode

| User instruction | Action |
|---|---|
| No explicit preserve/restructure instruction | `professional-advisor`: preserve facts/order; note actual strengths, problems and useful improvements in the execution record. Apply conservative source-supported improvements. |
| Explicitly preserve supplied outline/structure | `strict-execution`: do not silently rewrite/reorder. Record actual factual, copying or pedagogical conflicts; do not manufacture unsupported fixes. |
| Explicitly authorizes restructuring | `authorized-auto-upgrade`: restructure within the authorized source and scope; retain changes and rationale in the record. |

Commercial intent, urgency or “精品” alone does not authorize restructuring. Do not generate repeated long review reports or empty “no issue” sections simply to pass an internal state.

## Understand and verify before designing

Do not stop at text extraction or a paraphrased summary. Read the original lesson and its exercises/notes as a whole, then check the resulting understanding against specific passages, diagrams, definitions or problems. Keep a compact source-grounded synthesis and resulting decisions, not a long internal reasoning transcript or a new user-facing report:

- What is being taught: central meaning/concept, content relationships, original sequence, and source-required learning tasks.
- Why these details matter: key language, textual evidence, imagery/emotion, argumentative links, historical context or disciplinary reasoning as applicable. Do not mechanically impose literary categories on other subjects or invent authorial intentions.
- What learners need: actual target-grade demands, prior knowledge supported by supplied information, likely obstacles and misconceptions. Distinguish a reasonable anticipated difficulty from a claimed fact about this class.
- What the lesson should do: a text-specific central question, objective, core activity and response criterion linked to each important difficulty; reject activities reusable unchanged across unrelated texts.

Only then compare all official teaching designs and task sheets: retain useful prompts, scaffolds and tasks, merge duplicated source segments, and reconcile differences against the original textbook. Official plans are teaching references, not text to paste wholesale; do not invent facts to resolve a conflict. Check quotations, names, factual/interpretive boundaries, sequencing and required coverage once before drafting the lesson plan. Mark missing evidence rather than claiming complete understanding. Reuse this checked synthesis downstream; do not reread unchanged inputs for each document.

Draft the delivered lesson plan for daily teaching/ordinary open classes under `teaching-plan-standard.md`: internal understanding/checks remain thorough, while curriculum-basis and explanatory prose are concise. Before handoff, remove duplicated theory without cutting useful classroom questions, activities or support; separately review the substantive, lesson-specific reflection aspects and their adjustments/rechecks. Keep the existing twelve modules, time rules, key/difficulty depth and approval checkpoint; no sample Word page count becomes a limit.

## Required lesson-plan-first workflow

| Current user instruction | Mode and handoff |
|---|---|
| Ordinary start, “先出教学设计”, “按流程制作”, or “一起出” | `plan-first`: understand sources and verify relevant curriculum standards; draft/check the twelve-module paragraph-template lesson plan with a content-led, flexibly organized process, aligned evaluation and concise directly writable board content; render/verify this Word and hand it off. Set `awaiting-user` and end the turn. Do not generate the outline, final script or visual blueprint before actual approval of this plan version. |
| User supplies a specific already-approved plan | Read it, record the user’s explicit approval evidence/version, then continue downstream without requesting the same approval again. |

This approval-stage selection does not change output types, optional extras, formats or the per-variant page cap. Select A/B under `deliverables.md` without creating another teaching plan. “教学设计、PPT大纲、逐字稿一起出” retains the visual blueprint in each requested outline's combined Word unless omitted; “PPT大纲” does not request PPTX or both variants.

Use plan-first for all subsequent production. The 2026-10-20 instruction supersedes prior automatic-package defaults. When resuming an unapproved legacy auto task, preserve completed files/source evidence but stop downstream generation until its current teaching plan is explicitly confirmed. Do not delete or remake already valid outputs simply to migrate modes. A generic start, page-count answer or request to receive everything is not a waiver; interpret an actual confirmation against the immediately presented plan version. A later explicit user change to this approval policy may supersede it, but never infer such a change.

For `plan-first`, record the exact approved version and the user's confirming message. A page-count confirmation, generic earlier start, or an internal PASS is not plan approval. If the user requests changes at this checkpoint, update and recheck the plan, then present the revised version for confirmation; do not proceed on the superseded approval.

A supplied plan explicitly identified as already approved counts as the baseline once its actual content is read. Preserve its goals, key/difficult points, core activities and teaching mainline. Source checks still apply: approval is not proof of factual accuracy. Do not silently replace a material source conflict in an approved plan or ignore it; report the narrow conflict when user direction is genuinely required. After approval, internal page mapping, layout repairs and meaning-preserving language polish are routine; changing the pedagogical baseline requires the user's authorization. No repeated approval for pages, style or ordinary downstream repairs.

## One teaching record, then page mapping

Before page division, maintain ordered `teaching_blocks` with stable IDs, source anchors, objectives, teacher/student actions, core questions, anticipated answers/misconceptions, evaluation and transitions. These are the shared lesson-plan decisions, not a second deliverable. In `plan-first`, these blocks make a complete teachable plan before PPT page numbers exist. Keep page mappings internal in both initial and final teaching-plan Words; no PPT total count, page numbers or page correspondence may appear anywhere in the teaching-plan content, headers, footers or notes; never insert guessed numbers, empty range fields or “待定” placeholders merely to satisfy a checker.

Only after actual user approval of the current teaching plan, simulate the teacher's talk through these blocks in sequence. Write a coherent oral draft including opening, reading/observation/task instructions, purposeful questions, anticipated learner responses, responsive explanation, synthesis and natural transitions. Anticipated responses are possible directions, not claimed real student dialogue. Check that each new idea is prepared by the preceding talk and each activity has usable instructions and a follow-up.

Derive the PPT outline from that lecture flow: decide what must be visible at each teaching moment and what remains oral. Do not paste the entire transcript onto slides. Divide into legible pages within the cap, then finalize `P1 页面标题` script sections under `speaker-script-standard.md`: black `师：` speech and red `【…】` non-spoken display/activity/pause/conditional-response cues. The old five script fields remain internal quality dimensions only. No extra outline fields or automatic animations/PPTX; do not reveal answers before inquiry.

Extend the per-page record in `teaching-modes.md` with teaching-block/lecture links, six visual decisions, page-linked spoken paragraphs/non-spoken cues and check status. Keep actual block/lecture/page mappings in these internal records; the teaching-plan body follows the paragraph template with no PPT total count, page numbers or correspondence notes. Keep the concise board content consistent with the lesson's core concepts; its module contains no main/secondary board or generation-timing commentary. The plan's substantive sequence controls downstream production; splitting pages does not authorize rewriting approved goals/mainline. Preserve an explicitly frozen outline or report a material conflict.

Derive the selected outlines, blueprints and scripts from this one record and shared approved lecture/teaching baseline. Each variant adapts on-screen detail, page division and layout, then finalizes its own script against its pages; B is not just A's background replacement, and a shared lecture draft does not replace the two final scripts when both are requested. Repeated facts/terms remain consistent, but version-specific titles, page numbers and display moments are resolved inside their variant. Optional image-deck rendering adapts only its requested variant's frozen decisions without replanning the lesson.

## Internal sequence

`intake → text_understood → lesson_plan_checked → awaiting_plan_approval → user_approved_plan → lecture_drafted → scale_approved → content_approved → visual_approved → production_approved → verified`

| Stage | Before an explicit start | After an explicit start |
|---|---|---|
| Topic/intake | Resolve only consequential missing inputs; preserve supplied facts and preferences. | Read, understand and verify scoped sources; record unrecoverable gaps. |
| Teaching design | Discuss or draft only what was requested. | Produce the text-specific twelve-module curriculum-standard plan in `teaching-plan-standard.md`; check verified standards, objectives, key/difficult points, activities, design intent, assessment, text-board and time consistency. Hand off only this checked Word and end the turn awaiting confirmation. Internal PASS is not user approval. |
| Lecture | Do not infer permission to start downstream production. | After recorded user approval, simulate the teaching sequence from that plan; internally read through the spoken flow before deciding slide breaks. |
| Scale | Honor confirmed page count; offer options only when the user is still choosing a plan. | Reuse confirmed count or select a source-supported count within the cap. No page-count choice or duration question. |
| Content | Produce requested planning material only. | Derive page records/outline from the lecture, finalize the page-aligned script and internal cross-file mapping. Check source coverage, order, spoken continuity, display timing and readability together. |
| Visual | Offer alternatives only if requested or a consequential conflict remains during planning. | Follow the visual-basis route below: without explicit style references derive directly from textbook understanding; with designated images use them as the visual authority and the text as supporting context. Do not automatically search or retrieve library references. Select one compatible direction, complete every six-field page blueprint and check unity/variation internally. |
| Production | An approved page count alone is not a start. | Freeze the current file list, generate the required documents and explicitly requested extras. |
| Verification | Inspect only what the current request asks to inspect. | Apply `quality-gates.md`; record actual evidence and deliver once required checks pass. |

In `plan-first`, a checked first-stage lesson plan is a legitimate partial handoff, not a completed package. Use plan-review validation; downstream documents and mappings are outside this stage, not failed or invented. Resume from the one approved plan instead of redoing intake or asking for a second plan approval. Final handoff includes three current Words for A-only/B-only or five for explicitly requested A+B, honoring omissions/splits and explicitly activated extras. The shared plan receives only routine formatting updates and no PPT page/version-mapping notes.

After plan approval, automatically read through the final script while walking the actual page order: compare plan intention → spoken instruction/question → currently visible material → anticipated response/teacher feedback → transition. Check omissions, contradictions, duplicated talk, abrupt pronouns/transitions, premature answers and mismatched page cues. Fix the responsible draft/page and recheck the affected links. This reduces inconsistency but is not a guarantee of a flawless real classroom; do not claim automatic checks prove perfect understanding or teaching effectiveness.

If a requested page count conflicts with the single-section cap, do not silently exceed it. During planning give a compliant option. After start apply the established cap when ordinary scope permits and state the adjustment at handoff; if the user also made the conflicting count an immutable requirement, report that unresolved conflict rather than fabricating compliance.

## Visual-basis routing

After the teaching plan has been confirmed and page content determined, choose the basis once under `visual-system.md`:

1. No designated or explicitly requested visual references: `content-derived`. Use the already checked textbook understanding directly; do not launch web/image searches, consult a stored library or request images. Ordinary textbook-page screenshots remain teaching sources, not an implicit style-reference instruction.
2. Explicitly supplied/designated reference images: `reference-led`. View the actual designated images and anchor the palette, material, brushwork, atmosphere and light language in them. Learn abstract spatial/hierarchy principles rather than freezing their depicted scene, subject positions or text containers as every page's layout. Use the understood textbook and each approved page's teaching purpose to conceive its concrete scene or knowledge relationship, subject/action, viewpoint and composition inside that same style. Do not replace the reference language with a new style, mix in library images or perform automatic supplementary search. Reuse a layout framework only when the user explicitly fixes it; a supplied style image alone is not that instruction.
3. User explicitly requests ordinary visual web research or an authorized library: perform only that requested extension. Use the designated image style as primary when one exists. An ancient-poetry topic or a request for an ink-wash style does not itself authorize library retrieval.
4. User explicitly requests a Xiaohongshu search: apply the dedicated sequence in `visual-system.md`. Capture, save and separately display the real first-screen screenshot, build the blueprint with its observed style traits, and generate the single text-free background reference after the blueprint is finalized. Follow the scope of standalone search or screenshot requests. Record the screenshot and background paths in the existing source/deliverable records.

Keep truthful evidence in the existing `visual_research` record:

- `content-derived`: concrete text/page anchors and aesthetic decisions, with no fabricated image IDs, searches or viewing claims. Image-reference/search checks are N/A because the route does not require them; content fit and visual quality still apply.
- `reference-led`: the user's reference instruction, exact inspected image IDs/paths (or an explicitly requested library subset), observed style anchors and how supporting textbook context is used. Web-search checks are N/A unless additionally requested.
- `complete`: an explicitly requested web-reference task with actual queries, inspected image URLs/IDs or the actual first-screen screenshot path for Xiaohongshu, the requested style relationship and adopted rules. Search snippets or inaccessible results are not visual evidence.
- `reused`: actual evidence already accepted for the same project/topic/direction; preserve its original basis and permission scope.
- `skipped-by-user`: an express no-search/only-given-images instruction and the real supplied-image or textual basis.
- `unavailable`: a designated image or explicitly requested reference task remains inaccessible. Do not claim success, silently substitute a different source or relabel the failure as a voluntary no-image route.

Only analyze active selected sources, not the whole library. Reuse prior accepted source understanding and the current plan/page records instead of rereading or making another full plan. A new topic/direction requires a fresh basis choice under these rules, not automatic permission to search. Requested provenance lists remain optional separate scope, never a seventh blueprint field. Inspect reference quality and avoid copying source artwork, logos or pseudo-text; reference style authority is not permission to alter textbook facts or classroom-readable copy.

## Failure and resumption

For a transient source/browser failure, make at most two targeted recovery attempts only when an observation suggests progress; stop repeating identical failures. Do not bypass authentication or permission boundaries. Preserve a completed source digest, accepted pages, valid references and finished files. If a needed input remains inaccessible, finish independent authorized work and disclose the missing item in the final result; do not claim a complete verified package.

Without an explicit reference instruction, use the normal content-derived route from the outset; it does not depend on failed searches and is not a provisional substitute. If designated images or an explicitly requested reference search are unavailable, preserve the actual requirement, finish independent authorized work and disclose the narrow input/access gap; keep the relevant check NOT_RUN or FAIL. Do not silently replace image-led work with text-only work or unrequested internet/library images. If a provisional blueprint is useful, label it provisional and do not claim that it follows an unseen reference. Ask for the missing image only when it genuinely blocks the current stage; do not add routine style or page approvals. Xiaohongshu access is relevant only when that search is explicitly requested. Missing essential textbook facts still cannot be invented.

For a scoped edit of an existing blueprint that preserves its topic and master direction, inherit the original reference evidence rather than launching a new full workflow. Missing historical evidence is recorded, not invented; reselect the visual basis only for changed topic/direction/reference instructions; search or retrieve a library only when explicitly requested. A complete image-deck execution contract likewise reuses the frozen blueprint and references instead of replanning them. The generated-text ban excludes unmodified source documents and reference images.

Each check records `PASS | FAIL | NOT_RUN | N/A`, the artifact/version, evidence and reason when not passing. Missing evidence is NOT_RUN, not PASS. A task reaches verified only when all applicable required checks have actual PASS evidence. Unchanged passing files retain their evidence; changes invalidate the affected checks and cross-file relationships. Do not rerender unrelated unchanged files.

On resume, inspect the execution record and existing outputs before doing new source reads or generation. The final delivery contains only requested products, with a concise truthful status. Internal research notes, reference records, review proposals and QA renders remain internal unless requested. An older automatic screenshot requirement does not activate the explicit Xiaohongshu route; use the user's current request and retain accepted evidence.
