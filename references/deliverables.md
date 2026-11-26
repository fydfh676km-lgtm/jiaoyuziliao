# Product deliverable contracts and capability routing

Read this reference when authoring the lesson plan and again as needed for final production. It defines one shared teaching-plan baseline and the requested courseware variants, delivered through the existing `plan-first` checkpoint in `workflow.md`: teaching-plan Word first, then selected downstream variants after approval of that same plan.

## Product manifest

```yaml
product:
  version_policy: A-default-explicit-variants
  requested_versions: [A]
  lesson_plan: "<topic>-lesson-plan.docx"
  versions:
    A:
      ppt_outline_visual_blueprint: "<topic>-A-ppt-outline-visual-blueprint.docx"
      speaker_script: "<topic>-A-speaker-script.docx"
  optional:
    exercise_package: null
    pptx: null
    pdf: null
    xiaohongshu_notes: null
```

The filenames are examples derived from the approved topic; replace `<topic>` with the approved topic's delivery-safe name. The default A package still has four logical document deliverables in three Word files: its combined outline/blueprint, the shared lesson plan, and its script. Put only requested variants in `versions`; for B-only replace the A entry with B, and for both include separate A and B entries. The shared plan is never duplicated. Existing accepted unlabelled files may be recorded as A without renaming or rebuilding them just for migration. Visual-basis analysis is internal: use textbook understanding directly by default, or designated images as the primary visual authority when explicitly supplied. Supplementary visual search/library retrieval is opt-in. An explicit Xiaohongshu search activates the scope-specific image handoff below. Exercises, editable PPTX, PDF and marketing remain opt-in extras; selecting B or both does not activate them.

## Version selection and pairing

| Current request | Selected output | Final Word count, without explicit omissions/splits |
|---|---|---|
| No version named, ordinary start, or A only | A only | 3: shared plan + A outline/blueprint + A script |
| B / 参考增强版 explicitly requested | B only; do not also create A | 3: shared plan + B outline/blueprint + B script |
| A and B / 两个版本 / both explicitly requested | A and B | 5: shared plan + A outline/blueprint + A script + B outline/blueprint + B script |

**A is the existing approved standard**, not an intentionally thin or lower-quality edition. **B is the reference-enhanced content-and-layout edition** defined in `visual-system.md`, not a second lesson plan, a rendering mode, a fixed night/ink/rural style, or an automatic anti-garbled mode. Both remain subject to the existing Premium/Quick selection independently of the A/B labels. A current explicit custom instruction controls the requested scope and treatment; do not infer two versions from a reference attachment or a style request alone. With no version instruction, use A while honoring that requested style. Do not offer a routine version-selection question after start.

Read/understand the sources once and confirm one lesson-plan version once. After approval, each selected variant has its own complete outline, six-field blueprint and separately aligned script. The variants are alternative presentations of the same approved pedagogy, not different halves of the lesson. They may have different page counts within the original per-section cap; preserve each variant's own frozen order, titles, content, display timing and page-script mapping. Do not force A page n to match B page n or stretch the shared plan's teaching time to cover both decks sequentially. Carry the version ID in filenames, document titles and internal records, not new page fields or version-specific notes inside the teaching-plan Word.

For both, hand off five separate Word files, not one outline with two blueprint sections or one script with interleaved A/B page numbers. Only an explicit user merge/split/omission request changes this packaging. When only B changes, preserve valid A and the approved plan; when a variant is not requested, do not produce it as a prerequisite. Optional additional products still require their own explicit request.

Apply explicit user omissions/split requests to this manifest. Verify the requested scope rather than generating an omitted file to satisfy defaults. Research evidence belongs to `visual_research` and the source ledger in `workflow.md`. When resuming an older task, retire its automatic `reference_screenshot` requirement while preserving historical files. An active explicit Xiaohongshu request follows `visual-system.md`. If the user explicitly requests references or a source list, deliver only that added scope and verify its actual content.

In `plan-first`, first hand off only the complete, rendered/checked lesson-plan Word and wait for actual approval of that one plan version. It contains no PPT total count, page numbers or correspondence, including notes, headers and footers. After approval, complete lecture → selected variant outline → aligned variant script → variant blueprint, then deliver three Word files for A-only/B-only or five for both. Keep mappings internal without unauthorized pedagogical changes. Requesting B/both does not bypass or duplicate the plan approval and adds no downstream selection checkpoint. Internal checks are not user confirmation. The board module remains concise teacher preparation, not a board-slide/image deliverable. A request for plan/outline/script together does not omit the blueprint or request PPTX.

## Format-specific contracts

### Xiaohongshu first screen and overall background reference

Under the explicitly activated route in `visual-system.md`, save and separately display the single `课题名称_小红书搜索首屏.png` in chat at the reference stage. For a request that includes the full visual workflow, add one `课题名称_背景参考图.png` after completing the blueprint. Keep both PNGs with the requested lesson-plan, speaker-script and outline/blueprint Word files in the course-topic folder. A standalone search or screenshot request delivers only its screenshot. Record applicable PNGs as deliverables and check them under `quality-gates.md`. The default Word package applies when this route is inactive.

### Combined PPT page-outline + visual-blueprint Word — `<topic>-ppt-outline-visual-blueprint.docx`

- The document contains exactly two labeled sections: `PPT页纲`, followed by `视觉蓝图`.
- In the `PPT页纲` section, every page uses exactly:

  ```text
  第X页
  页面标题：
  页面文字：
  ```

- In the `视觉蓝图` section, every page uses exactly:

  ```text
  第X页
  画面风格：
  添加元素：
  文字字体与重点标注：
  布局排版：
  镜头与光影：
  画面去重与统一约束：
  ```

- Within the file's variant, page numbers, titles, page text and blueprint pages correspond one-to-one and preserve its approved total/order. Use that same variant's separately delivered script; cross-variant page matching is not required.
- The six visual fields appear exactly once in the fixed order, have no numeric/list prefix, and contain nonempty page-specific values. Do not add `页面标题：` or a seventh visual field such as teacher guidance, design intent, key-point labels, or notes.
- No user-facing string in either section may contain `课时` or its period-label variants.
- Apply `classroom-readability.md` while dividing the outline and authoring the blueprint: screen copy is the essential material, question and conclusion, not the complete lecture. Put explicit classroom size targets and text-first capacity decisions inside the existing six fields; preserve confirmed text and page count. These slide-size targets do not change the Word document's own paragraph sizes.

### Lesson plan Word — `<topic>-lesson-plan.docx`

- Follow [`teaching-plan-standard.md`](teaching-plan-standard.md), [`teaching-plan-template.md`](teaching-plan-template.md) and `../assets/teaching-plan-template.docx`: the 2026-10-20 paragraph template and paired prompt (`../assets/teaching-plan-prompt.docx`), with twelve native numbered modules, reference typography and two functional matrices: 课程基本信息 / 设计依据 / 设计理念 / 教学目标 / 教学重点、难点与突破策略 / 教学准备 / 教—学—评一体化设计 / 教学过程 / 板书设计 / 作业设计 / 教学评价 / 教学反思预设与课后改进. This supersedes the 2026-10-19 A4/black-heading/fixed-process version.
- Verify concrete applicable curriculum-standard content and academic requirements; write 2–4 observable objectives and align objectives, learning activities, assessment tasks and rubric. Use the practical daily-teaching/ordinary-open-class prose in `teaching-plan-standard.md`: two concise source-grounded curriculum-basis sentences, focused analysis, and concrete classroom questions/activities/guidance rather than repeated explanatory theory. Reflection stays substantive: approximately five lesson-specific aspects connecting observation, possible problem/cause, actionable adjustment and recheck, with natural small headings/paragraphs rather than empty placeholders or copied example headings. Do not invent standards, class data or achieved teaching results; pre-class reflection is anticipatory and conditional. Preserve the twelve-module template and natural pagination, not a fixed shortened Word page count.
- Write content-led timed blocks in connected paragraphs, with teacher guidance, student actions/output, evidence, support and logical progression. Block count and optional sublabels follow actual teaching needs, not a five-block/five-field rule or fixed time ratios. Do not put PPT total count, page numbers, correspondence or other production notes anywhere in the teaching-plan Word; preserve cross-file mappings internally.
- The checked/approved plan guides lecture and pages. State proposed/required session count, minutes per session, per-block times and overall total; check each session and overall sums against actual or clearly estimated shared pacing. Cover every session in the requested scope. This implementation advice neither splits/truncates the continuous complete outline nor enables the source-based page-cap exception. The combined outline/blueprint Word still has no timing fields.
- Within 教学重点与难点, write 教学重点 and 教学难点 separately, each at least 100 Chinese characters, plus targeted 突破策略. Explain basis, intended understanding/action, obstacle and teaching response; labels or padding do not pass.
- Apply the visible-emphasis system from `teaching-plan-standard.md`: default to dark red plus bold for short substantive key phrases in `教学重点`, `教学难点`, every major teaching-process block, and the final synthesis. Headings or field labels alone do not satisfy this requirement; reject missing, inconsistent, or excessive emphasis in the rendered Word file.
- Board presents the actual brief blackboard content in native text: the lesson title, essential keywords/phrases and clear relationships, using simple indentation, parallel groups or arrows when useful. It should be directly usable on one blackboard, not an essay about implementation or a disconnected keyword list. Do not add 板书主线/主板书, 副板书 or 生成时机 subfields; do not generate or embed a board image unless separately requested. This latest rule overrides the retained source template's old board-filling prompts.
- Use the new template's student-output/evaluation-evidence terminology where it serves teaching. Do not add unrelated production fields or repeat evidence descriptions merely to fill columns.
- Keep the lesson-plan metadata label 设计者/日期 but leave its value blank. Do not autofill names/accounts/organizations/dates, write missing-data placeholders or add those authorship/date details in headers, footers or notes; no user follow-up is needed for this deliberately blank field. Other metadata and source-date verification remain unchanged. This rule supersedes the retained template's filling prompts.
- Keep the entire lesson plan within the user's specified lesson/section scope under `teaching-plan-standard.md`, including optional tasks, homework, evaluation and reflection. Do not add another lesson, next-lesson preview, cross-text reading or an unrequested writing/grammar topic merely because it appears in the same unit/template/reference plan. Homework can consist only of meaningful current-lesson consolidation; optional/extension work is not mandatory. Cross-lesson integration requires an explicit user request and remains limited to its specified scope; downstream courseware inherits this boundary.
- The new lesson plan includes the template's necessary teaching-period/time and evaluation-evidence information; this supersedes those older lesson-plan-only bans. Do not transfer them into PPT/outline/blueprint/script/exercise period labels. Keep original source/reference files unchanged; never treat a template's claimed policy revision as verified current policy.
- Do not change approved pedagogical decisions to fit an independently generated outline. Internal page mapping and layout-only improvements may be updated; substantive approved-plan changes follow the authorization boundary in `workflow.md`.

### Speaker script Word — `<topic>-speaker-script.docx`

- First draft a continuous, natural teacher lecture from the user-approved teaching design, then derive the selected variant's PPT outline and finalize its own script mapping. Follow that variant's frozen page order and internal pacing; keep the common approved teaching sequence, without inventing a confirmed duration or a different lesson mainline.
- Include an opening, explanation for each page, questions and likely answer directions, transitions, activity instructions, and a closing.
- Follow [`speaker-script-standard.md`](speaker-script-standard.md) and the retained `../assets/speaker-script-reference.docx`: one `P1 页面标题` section per PPT page, black `师：` spoken paragraphs and separate red `【…】` non-spoken reading/activity/pause/conditional-response cues, naturally interleaved. The old five fields remain internal quality dimensions, not printed labels; do not mechanically add 无 blocks.
- Do not introduce a new page sequence or contradict the approved page outline.
- Automatically rehearse the actual page sequence: material exists when mentioned, questions allow response time before reveal, guidance answers the actual question and transitions connect to the next page. Keep oral explanation distinct from concise slide copy. Check actual black/red DOCX styling and original facts rather than copying the reference lesson or its 27 pages. This does not enable animations/PPTX.

### Optional exercise-and-answer Word

Generate only when the user explicitly requests `单课习题`/`课后习题` or `单元综合复习题`/`单元复习卷`. Read and follow [`exercise-package.md`](exercise-package.md). Use `<课题>-课后习题与答案.docx` for the single-lesson route and `<单元>-单元综合复习题与答案.docx` for the unit route. Do not generate both unless the user explicitly requests both. Keep the student paper and teacher answer section in the same Word file, separated by a page break. The exercise package remains separate from the PPT outline and may not change the approved slide count.

### Optional editable PPTX — `<topic>.pptx`

- Use a 16:9 layout.
- Keep text, shapes, diagrams, tables, and charts editable where practical; do not flatten editable teaching content merely for appearance.
- When raster backgrounds or illustrations are needed, route them through `imagegen` using the highest available GPT image-generation model/configuration; keep generated artwork separate from editable text and teaching elements.
- Preserve the approved page order, each page's approved goal, title, core content, activity or case, and timing.
- Implement the approved visual system and every approved page-level visual blueprint (or its approved reusable layout family).
- Maintain classroom readability under `classroom-readability.md`: explicit size floors for student-essential copy and labels, clear contrast, text-first geometry and actual rendered inspection. Never auto-shrink or compress essential copy to solve overflow; preserve approved text/count and report unresolved page capacity conflicts.
- Keep the user-facing page outline exactly `第X页 / 页面标题： / 页面文字：` and the user-facing visual blueprint exactly `第X页 / 画面风格： / 添加元素： / 文字字体与重点标注： / 布局排版： / 镜头与光影： / 画面去重与统一约束：`; do not add a seventh field or alter the approved page count/order.
- Do not allow `课时` or variants such as `第一课时`, `第二课时`, `课时导入`, or `课时总结` in any PPT-visible title, body, activity label, footer, or transition. Scan before delivery and rewrite any match.
- Pass the complete WPS-safe checklist in [`wps-safe.md`](wps-safe.md): open/render in WPS without repair, preserve fonts/layout/assets/editability, and compare the WPS render with the approved source.
- Render the finished deck page by page for a visual pass; check text clipping, overlaps, contrast, accidental pseudo-text/watermarks, missing assets, and style drift. Repair only failed pages, then re-run the complete slide and WPS checks.
- During that visual pass, also reject obvious generic-AI artifacts (waxy surfaces, warped anatomy/perspective, cloned details, incoherent lighting, illegible image text, fake logos/watermarks, or style mismatch) and regenerate only the affected visual element/page.

### Optional image-only PPTX

An approved Premium product may opt into `image-deck` for its PPT rendering only when that rendering choice is explicitly present in the approved visual/production contract. The resulting PPTX is intentionally image-only; do not describe it as editable. The matching PDF and sibling deliverables still follow the existing Premium cross-file contracts.

### Optional PDF preview — `<topic>-preview.pdf`

- Generate it from the final PPTX or from the same final source of truth.
- It has the same page count and page order as the final PPTX.
- Its text and visuals are the same as the final PPTX; it is a faithful preview, not a prettier or reduced-quality alternative.
- It represents the exact saleable product described by the manifest.

### Optional Xiaohongshu notes DOCX — `<topic>-xiaohongshu-notes.docx`

Generate only when explicitly requested. Default to ten notes (`note_count: 10`) unless the user specified another count. Each note must have a genuinely distinct marketing angle; do not create superficial rewrites of the same hook, audience pain point, use case, teaching feature, or product value. Every claim about pages, content, use, audience, files, or value must be supported by the approved page records and manifest, with no invented results, features, endorsements, or separate display-only version.

Every note includes:

- a title;
- a hook;
- body copy;
- product value;
- image suggestions based on actual product pages or truthful supporting visuals;
- keywords; and
- an engagement prompt.

## Cross-file verification matrix

Apply this matrix separately to each selected variant against the one shared approved plan. Never validate A's outline with B's script or substitute one passing variant for the other's evidence. Default A and B-only each have three Word files; both have five, before explicit omissions/splits. Optional exercises, PPTX, PDF and notes participate only when requested. For exercises also compare scope, terminology, objective/key-point/difficulty coverage, source anchors and any practice/homework cross-references.

| Comparison field | Approved outline/blueprint Word | Lesson plan Word | Speaker script Word | Optional exercise Word | Optional PPTX | Optional PDF | Optional Xiaohongshu notes |
|---|---|---|---|---|---|---|---|
| Topic | Approved topic and product positioning | Course name and scope use it | Opening and page narration use it | Uses the exact requested lesson or unit scope | Uses it only if requested | Same as optional PPTX | Describe this product only if requested |
| Audience | Approved school level and audience | Activities fit it | Questions and delivery fit it | Difficulty, wording, and response demand fit it | Language and examples fit it | Same as optional PPTX | Target user and claims fit it |
| Duration | Internal page records hold supplied or explicitly estimated pacing; no extra outline/blueprint field | Template total/block times match that record; estimates labeled | Speech and cue pacing fits that record | Does not alter that pacing | Matches it when used | Same as optional PPTX | Do not present an estimate as confirmed |
| Page order | Pages derived from the user-approved plan's lecture sequence; blueprint follows them | Substantive teaching flow preserved; actual page mappings internal, no visible PPT count/page references | Oral draft finalized against those pages; no separate sequence | Follows the approved knowledge order without adding slides | Pages match exactly | Same as optional PPTX | Suggested pages do not imply another sequence |
| Learning objectives | Frozen objectives and page goals | Objectives, flow, evaluation, extension match | Opening, explanations, closing reinforce them | Questions and analyses cover the approved objectives, key points, and difficulties | Objectives and reinforcement match | Same as optional PPTX | Value claims accurately reflect them |
| Terminology | Approved terms, names, and definitions | Use terms consistently | Use the same terms | Stems, answers, and analyses use the same terms | Use terms consistently | Same as optional PPTX | Use terms consistently if requested |
| Activity timing and display | Internal page record describes what is visible during instruction/question/feedback | Teacher/audience actions and question progression match | Materials, prompts, likely response, feedback and transitions match the current page and do not reveal conclusions too soon | Cited practice/homework matches sibling files | Activities use the same pages and internal plan | Same as optional PPTX | Do not claim extra or differently timed activities |
| Product claims | Approved scope and manifest | Describes the same package | Describes the same package | Exists only when explicitly requested and matches the selected route | Shows only the requested product | Faithful preview if requested | Truthfully markets the requested package |
| Source coverage | Frozen textbook + all SmartEdu teaching designs and learning-task sheets | Uses the same source facts, objectives, tasks, and sequence | Narrates the same source-backed page content and activities | Every item has a supported source anchor and the selected scope is fully covered | Implements only the approved source-backed content | Same as optional PPTX | Claims only what the approved source-backed product contains |
| WPS compatibility | N/A unless an optional PPTX is requested; then record its approved WPS-safe constraints and verdict | N/A | N/A | N/A; verify valid DOCX package and rendered layout | Opens, renders, and remains editable in WPS when the editable PPTX route is requested; image-only route preserves its declared image-only contract | Matches the WPS-verified PPTX render | N/A |

## Authoritative verification predicate

Record an explicit evidence-backed verdict before any final-deliverable claim. Each check uses PASS, FAIL, NOT_RUN or N/A with artifact/version and evidence; unavailable required checks are NOT_RUN, never N/A or PASS. These two groups control the transition from `production_approved` to `verified`:

1. **Full format-contract verdict:** check combined outline/blueprint Word (unchanged exact formats, page correspondence, banned terms); lesson-plan Word (twelve standard modules, verified curriculum basis, aligned objectives/tasks/evaluation, connected paragraph process, full-scope session coverage and per-session/overall time consistency, key/difficult points each ≥100 Chinese characters, text board, substantive emphasis and genuine anticipatory reflection); script Word (`P1 页面标题` sections, actual black speech/red cues, natural lecture flow, accurate facts and real display mapping). Render every requested Word, honoring omissions/splits/scoped edits. First `plan-first` handoff checks only the plan, without fictitious page mappings or whole-package completion claims. Optional products remain opt-in.
2. **Cross-file matrix verdict:** record actual status for each applicable matrix row from shared source/page records. Validate teaching-source coverage and internal block/page mappings, then semantic accuracy. Explicit omissions are N/A with the request recorded. Apply the visual route in `workflow.md`: no explicit style-reference instruction means direct `content-derived` design with no automatic visual search/library retrieval; explicit designated images mean `reference-led` design with their actual inspected style leading and textbook context supporting content. Only additionally requested web/library work enters acceptance. Both normal routes must pass content-fit, style unity and page-level quality checks. Missing designated images or explicitly requested research cannot be claimed complete or silently substituted. Preserve the true basis. Apply the dedicated screenshot and background checks in `quality-gates.md` when the Xiaohongshu route is requested and in scope.

`verified` is entered automatically only when all applicable required checks in both groups pass with evidence. FAIL or NOT_RUN blocks that whole-package verdict; independently checked artifacts may be handed off with missing checks identified. The required `plan-first` checkpoint waits for actual user approval, not for package verification; passing first-stage checks does not authorize the next stage. After actual plan approval, the final downstream handoff requires no further routine acceptance. Do not claim that automatic structural checks alone guarantee no semantic or classroom-flow errors.

## Capability routing

Use the bundled capability that owns the relevant stage. The stage owner works from the frozen contracts and does not alter approved decisions.

For lesson plans, the new curriculum-standard twelve-module template in `teaching-plan-standard.md` and `teaching-plan-template.md` owns structure and the 2026-10-20 paragraph-template numbered layout. For scripts, `speaker-script-standard.md` owns P-page sections and actual black/red speech/cues. Use their retained DOCX assets for formatting only, not as sources of lesson facts or policy truth. Apply `documents` within those templates, without restoring legacy layouts or printed five-field script labels.

| Stage | Primary bundled capability | Responsibility |
|---|---|---|
| Combined outline/visual-blueprint Word, lesson-plan Word, and speaker-script Word | `documents` | Produce the requested Word files from shared teaching and visual records, honoring explicit omissions or splits. |
| Board content inside lesson-plan Word | Native document text | Present concise, directly writable lesson title, core keywords and relationships; no main/secondary board or generation-timing fields. Images only on separate explicit request. |
| Explicitly requested exercise-and-answer Word | `documents` | Produce the selected single-lesson or unit exercise package from the frozen source ledger and teaching contracts. |
| Optional PPTX creation, editing, and verification | `presentations` | Produce and inspect an editable PPTX only when explicitly requested. |
| Optional original illustrations and backgrounds | `imagegen` | Create needed generated raster assets only for an explicitly requested PPTX/image route. |
| Optional PDF rendering, export, and inspection | `pdf` or the presentation export workflow | Create or inspect a PDF only when explicitly requested. |

## Production communication

Acknowledge the scoped deliverables concisely and execute. Explain skill use when the host requires it, but do not recite every capability or adapter. Community PPT Skills are optional; inspect availability only when the requested output needs one. Their absence does not block an available primary capability.

## Optional adapter routing

Check adapter availability at runtime. None of these adapters is required: absence never blocks the workflow, and the bundled route remains available. Assign one primary producer to a stage; an adapter may assist only when it is the selected stage owner and may not independently rewrite a sibling artifact or an approved contract. HTML output is opt-in: it is used only when the user explicitly asks for an HTML presentation or preview, and it is not part of the default manifest.

| Optional adapter | Useful stage ownership when available |
|---|---|
| PPT-Master | Native editable PPTX production or refinement. |
| Frontend-Slides | Explicitly requested HTML/web presentation or preview; do not start HTML work for the default Word package. |
| Beautiful-HTML-Templates | Design-asset and layout-reference exploration before visual approval. |
| Guizang-PPT-Skill | Education, emotional, or magazine-style visual design before visual approval. |
| HTML-PPT-Skill | Explicitly requested dynamic HTML presentation or preview production. |

## Failure isolation and repair

When an artifact fails, repair only the failed parts from the current shared records. Do not silently change successful siblings or rebuild their unchanged rendering evidence. Rerun the repaired artifact's checks and affected cross-file comparisons; retained evidence must correspond to unchanged file versions. A changed source/content contract invalidates all genuinely dependent outputs. Only all applicable required checks passing permits `verified`.
