# Execution contract

This file owns intake, textbook understanding, execution modes, shared teaching records, source provenance, and bounded recovery. `SKILL.md` owns visible formats, output scope, page cap, and topic-matched style research. Artifact standards own acceptance. Only the selected `plan-first` mode creates a human lesson-plan approval checkpoint; other “approved” state names are internal checks.

## Select once and reuse

Create one project-local execution record (structured data or an existing equivalent) for an end-to-end run; do not create it for a simple question or inspection. Reuse it after interruptions and update it only when the user changes requirements, sources change, or a check exposes an error.

```yaml
task:
  started: false
  topic: ""
  audience: ""
  product_mode: premium
  review_mode: professional-advisor
  execution_mode: auto  # auto | plan-first; distinct from review_mode
  mode_source: default
  page_count: null
  source_period_count: null
  duration_minutes: null
  duration_source: unspecified  # user | source | estimate | unspecified
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
  status: pending  # complete | content-derived | reused | skipped-by-user | unavailable
  queries: []
  reference_ids: []
  content_anchors: []
  design_decisions: []
  search_attempts: []
  selected_direction: null
  reason: null
pages: []
deliverables: []
checks: []
```

Record the explicit request that enabled each optional output or prompt mode. “按流程开始制作” starts the existing scope; it does not enable PPTX, exercises, marketing, or anti-garbled text. Current explicit user changes supersede older task decisions; identify and rebuild only their affected dependencies.

For duration, preserve a user/source value when supplied. Otherwise use a marked internal teaching estimate if pacing is useful, or leave it unspecified when it is not. Never invent a “confirmed” duration or pause after start to ask for one. Internal timing lives in the page records, not in the fixed user-facing page-outline Word; do not print an overall total in the teaching-plan Word.

## Source intake

For ordinary SmartEdu requests, invoke `$smartedu-numbered-lesson-reader` (user alias `$smartedu-reader`) first. Read the requested electronic textbook, every associated teaching design, and every learning-task sheet in source order, including all source teaching segments. Reuse a complete current digest of the exact same source instead of rereading it. Invalidate only changed or previously unread portions.

When the user supplies only local files or another source, use the explicitly authorized materials and record that SmartEdu was not supplied. Never invent platform contents or silently substitute another lesson. A complete direct image-deck contract does not require new textbook intake.

Read lesson inputs within the user's requested scope and the current project's reference materials. New blueprint production may use relevant public-web visual-style research under the routing rules below and `visual-system.md`; without user images, text-grounded design is also an authorized normal route. Neither route authorizes scanning unrelated local folders. Project content never becomes installed Skill content. Explicit future-library reuse authorizes indexing the supplied images under `style-reference-library.md`; ordinary production does not authorize a new reusable rule or library import.

Give each source item a stable ID and record:

- kind: textbook, teaching design, task sheet, visual reference, user fact/preference, or model inference;
- exact file/URL and page/section/segment, plus read/support status;
- required content/task IDs and their intended page IDs or teaching-process blocks;
- any source conflict, gap, or uncertainty that affects the product.

Facts come from evidence; user confirmation records a preference, not proof of an empirical claim. Textbook controls facts and sequence; teaching designs and task sheets supply teaching emphasis/tasks. Visual references support aesthetic choices, not new textbook facts or required lesson coverage. Deduplicate repeated segment content into one continuous lesson while preserving required coverage. Check every required ID has a valid target, then review semantic accuracy separately: an ID match alone does not prove coverage.

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

## Two execution modes

| Current user instruction | Mode and handoff |
|---|---|
| “先出教学设计，我确认后继续” or equivalent | `plan-first`: understand sources, draft and internally check the complete seven-section table lesson plan with embedded board image; render/verify this Word and hand it off. Set `awaiting-user` and end the turn. Do not generate the outline, final script or visual blueprint before actual approval of this plan version. |
| “自动校对，一起出” or an ordinary start without a plan-approval request | `auto` (default): internally check the lesson plan, simulate teaching, derive the pages and complete all requested outputs without interim approval. Deliver the default three Word files together. |

This selection does not change the four logical outputs, extras, formats or page cap. “教学设计、PPT大纲、逐字稿一起出” retains the default visual blueprint inside the combined Word unless explicitly omitted; “PPT大纲” does not request a PPTX.

Choose the default only for a new task with no selected mode. On an existing task, retain its recorded mode; a generic “开始/继续” or a page-count answer does not silently switch an awaiting-approval task to `auto`. Interpret confirmation against the immediately identified plan version, not an unrelated earlier choice.

For `plan-first`, record the exact approved version and the user's confirming message. A page-count confirmation, generic earlier start, or an internal PASS is not plan approval. If the user requests changes at this checkpoint, update and recheck the plan, then present the revised version for confirmation; do not proceed on the superseded approval. If the user explicitly switches to automatic production, remove this waiting checkpoint and continue the scoped work.

A supplied plan explicitly identified as already approved counts as the baseline once its actual content is read. Preserve its goals, key/difficult points, core activities and teaching mainline. Source checks still apply: approval is not proof of factual accuracy. Do not silently replace a material source conflict in an approved plan or ignore it; report the narrow conflict when user direction is genuinely required. After approval, page-range backfill, layout repairs and meaning-preserving language polish are routine; changing the pedagogical baseline requires the user's authorization. No repeated approval for pages, style or ordinary downstream repairs.

## One teaching record, then page mapping

Before page division, maintain ordered `teaching_blocks` with stable IDs, source anchors, objectives, teacher/student actions, core questions, anticipated answers/misconceptions, evaluation and transitions. These are the shared lesson-plan decisions, not a second deliverable. In `plan-first`, these blocks make a complete teachable plan before PPT page numbers exist. Omit page ranges in that first Word; never insert guessed numbers, empty range fields or “待定” placeholders merely to satisfy a checker.

After internal approval (`auto`) or actual user approval (`plan-first`), simulate the teacher's talk through these blocks in sequence. Write a coherent oral draft including opening, reading/observation/task instructions, purposeful questions, anticipated learner responses, responsive explanation, synthesis and natural transitions. Anticipated responses are possible directions, not claimed real student dialogue. Check that each new idea is prepared by the preceding talk and each activity has usable instructions and a follow-up.

Derive the PPT outline from that lecture flow: decide what must be visible at each teaching moment (material, question, task, key evidence, diagram or conclusion) and what remains oral. Do not paste the entire transcript onto slides. Divide into legible pages within the cap, then align the oral draft to those pages and finalize the five script fields. Keep before/after display cues inside the existing script fields and visual layout, not extra outline fields or an automatic animation/PPTX requirement. Do not reveal an answer before the intended inquiry; when needed use compliant page allocation or leave explanation oral.

Extend the per-page record in `teaching-modes.md` with its teaching-block/lecture links, six visual decisions, final script fields and check status. Backfill actual page ranges into the same lesson plan and board-generation sequence. The plan's substantive sequence controls downstream production; page split does not authorize rewriting approved goals/mainline. An explicitly preserved existing outline is also binding: fit the lecture to its page sequence or report a material conflict rather than silently restructuring it.

Derive outline, blueprint, script and lesson-plan mappings from this one record. Repeated facts, titles and page numbers are not reinvented independently. Optional image-deck rendering adapts these frozen decisions into its manifest without replanning the lesson.

## Internal sequence

`intake → text_understood → lesson_plan_checked → [awaiting_plan_approval only in plan-first] → lecture_drafted → scale_approved → content_approved → visual_approved → production_approved → verified`

| Stage | Before an explicit start | After an explicit start |
|---|---|---|
| Topic/intake | Resolve only consequential missing inputs; preserve supplied facts and preferences. | Read, understand and verify scoped sources; record unrecoverable gaps. |
| Teaching design | Discuss or draft only what was requested. | Produce the seven-section, text-specific plan; check objectives, key/difficult points, activities and transitions. `plan-first` hands off this checked Word and waits at its one selected checkpoint. `auto` continues. |
| Lecture | Do not infer permission to start downstream production. | Simulate the teaching sequence from the current approved/checked plan; internally read through the spoken flow before deciding slide breaks. |
| Scale | Honor confirmed page count; offer options only when the user is still choosing a plan. | Reuse confirmed count or select a source-supported count within the cap. No page-count choice or duration question. |
| Content | Produce requested planning material only. | Derive page records/outline from the lecture, finalize page-aligned script and backfill plan ranges. Check source coverage, order, spoken continuity, display timing and readability together. |
| Visual | Offer alternatives only if requested or a consequential conflict remains during planning. | Follow the reference route below: inspect supplied images and actively search matching references; without images, independently search or derive concrete design decisions from the text. Select one compatible direction, complete every six-field page blueprint and check unity/variation internally. |
| Production | An approved page count alone is not a start. | Freeze the current file list, generate the required documents and explicitly requested extras. |
| Verification | Inspect only what the current request asks to inspect. | Apply `quality-gates.md`; record actual evidence and deliver once required checks pass. |

In `plan-first`, a checked first-stage lesson plan is a legitimate partial handoff, not a completed package. Use the plan-review validation phase; the not-yet-created documents and page mapping are outside this stage, not failed or invented. Resume from the approved plan instead of redoing source intake. Final handoff includes the three current Word files (the approved plan with true page references and routine formatting updates), unless explicitly excluded.

For either mode, automatically read through the final script while walking the actual page order: compare plan intention → spoken instruction/question → currently visible material → anticipated response/teacher feedback → transition. Check omissions, contradictions, duplicated talk, abrupt pronouns/transitions, premature answers and mismatched page cues. Fix the responsible draft/page and recheck the affected links. This reduces inconsistency but is not a guarantee of a flawless real classroom; do not claim automatic checks prove perfect understanding or teaching effectiveness.

If a requested page count conflicts with the single-section cap, do not silently exceed it. During planning give a compliant option. After start apply the established cap when ordinary scope permits and state the adjustment at handoff; if the user also made the conflicting count an immutable requirement, report that unresolved conflict rather than fabricating compliance.

## Topic-matched visual research

Before a new blueprint, apply `visual-system.md` to the actual text. With user images, first inspect them and identify a compatible style direction, then actively search for actual scenes, backgrounds, elements, materials, compositions or lighting in that style that fit the lesson. Open and view useful images; search snippets or style names alone are not visual evidence. Do not search only generic PPT templates. An explicit no-web/only-supplied-images instruction overrides this search route.

Without user images, autonomously choose either relevant web/image research or concrete design based on understanding the text. The content-derived route is normally authorized, not merely a fallback after search failure; do not ask the user for images or a style selection. If the current request explicitly requires online reference research, however, carry out that research rather than substituting text-only design. There is no dedicated Xiaohongshu search, login or case-screenshot step, and no default reference-image attachment.

Keep the actual basis inside `visual_research`:

- `complete`: queries, stable visual-reference IDs, exact source URLs or authorized local paths, actually viewed images, adopted/rejected cues and a content-fit synthesis into one master direction. Inaccessible or irrelevant results are not successful references.
- `content-derived`: no user images and no current mandatory-online instruction; record specific text anchors, aesthetic decisions and their rationale. Do not invent reference IDs, source URLs or claims of viewing images. This route can pass normal visual-quality checks; web-only checks are N/A because the selected route does not require them, not because a tool failed.
- `reused`: points to existing evidence for the same text and direction, preserving whether its basis was inspected images or content-derived design.
- `skipped-by-user`: records an explicit no-search/only-supplied-images instruction and the actual supplied-image or text basis.
- `unavailable`: records actual access failure or unsuccessful targeted research when the search remains required. Required research is not PASS or N/A.

If optional research without user images fails and the current request does not require online evidence, a switch to `content-derived` is allowed. Retain the failed attempts in `search_attempts` and the switch reason; never relabel the failed search as successful.

Reuse current, inspected references and their analyses for the same text/direction. Research once for the deck, not once per slide or after a Word formatting repair. Source URLs are internal traceability records by default; a requested source list may be supplied separately, never as a seventh blueprint field. Do not claim popularity, asset reuse rights or real-world factual accuracy merely because an image appears in search.

## Failure and resumption

For a transient source/browser failure, make at most two targeted recovery attempts only when an observation suggests progress; stop repeating identical failures. Do not bypass authentication or permission boundaries. Preserve a completed source digest, accepted pages, valid references and finished files. If a needed input remains inaccessible, finish independent authorized work and disclose the missing item in the final result; do not claim a complete verified package.

If required web style research is unavailable while teaching sources are complete, continue a provisional blueprint from the actual text and accessible authorized references. Finish and check independent Word work; disclose the missing required research and keep its check NOT_RUN or FAIL as appropriate, not PASS or N/A. When no user images were supplied and online research was not explicitly required, instead use the authorized `content-derived` route with the failed attempts and switch reason preserved; this does not automatically make the blueprint a draft or the package incomplete. A content-derived choice made before searching needs no failure record. An explicit user no-search instruction also makes web research N/A. In every case, content-fit and visual-quality checks still apply. Never ask the user to log into Xiaohongshu to recover this route. If essential textbook content is missing, do not invent it to finish a document.

For a scoped edit of an existing blueprint that preserves its topic and master direction, inherit the original reference evidence rather than launching a new full workflow. Missing historical evidence is recorded, not invented; repeat style research only for a newly requested direction/topic or an explicit reference-search request. A complete image-deck execution contract likewise reuses the frozen blueprint and references instead of replanning them. The generated-text ban excludes unmodified source documents and reference images.

Each check records `PASS | FAIL | NOT_RUN | N/A`, the artifact/version, evidence and reason when not passing. Missing evidence is NOT_RUN, not PASS. A task reaches verified only when all applicable required checks have actual PASS evidence. Unchanged passing files retain their evidence; changes invalidate the affected checks and cross-file relationships. Do not rerender unrelated unchanged files.

On resume, inspect the execution record and existing outputs before doing new source reads or generation. The final delivery contains only requested products, with a concise truthful status. Internal research notes, reference records, review proposals and QA renders remain internal unless requested; do not add a screenshot requirement when resuming a task created under an older rule.
