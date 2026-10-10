# Product deliverable contracts and capability routing

Read this reference when authoring the lesson plan and again as needed for final production. It defines one Premium package, delivered together in `auto` or through the `plan-first` checkpoint in `workflow.md`.

## Product manifest

```yaml
product:
  version_policy: one-premium-version
  ppt_outline_visual_blueprint: "<topic>-ppt-outline-visual-blueprint.docx"
  lesson_plan: "<topic>-lesson-plan.docx"
  speaker_script: "<topic>-speaker-script.docx"
  optional:
    exercise_package: null
    pptx: null
    pdf: null
    xiaohongshu_notes: null
```

The filenames are examples derived from the approved topic; replace `<topic>` with the approved topic's delivery-safe name. The default package has four logical document deliverables in three Word files: the combined outline/blueprint Word, the lesson-plan Word, and the speaker-script Word. Reference research/analysis or the authorized content-derived visual route are internal production steps, not extra deliverables. Do not capture or attach a Xiaohongshu search screenshot, reference-image package or research report by default. The exercise package, editable PPTX, PDF preview, and Xiaohongshu notes are opt-in extras: keep them `null` and do not generate or verify them unless the user explicitly requests that specific extra. A normal start command never activates an exercise package.

Apply explicit user omissions/split requests to this manifest. Verify the requested scope rather than generating an omitted file to satisfy defaults. Research evidence belongs to `visual_research` and the source ledger in `workflow.md`, not a mandatory screenshot field. When resuming an older task, retire its automatic `reference_screenshot` requirement while preserving historical files; do not delete user files or trigger a fresh screenshot. If the user explicitly requests references or a source list, deliver only that added scope and verify its actual content.

In `plan-first`, the first handoff is only the complete, rendered/checked lesson-plan Word, awaiting actual approval of that version. It has no invented PPT page ranges. After approval, complete the lecture → outline → aligned script → visual blueprint sequence and deliver the three current Word files together; the plan receives real page references without unauthorized substantive changes. `auto` performs the lesson-plan review internally and has no intermediate handoff. The embedded board image belongs inside the lesson plan, not a fourth default file. A request for the plan, PPT outline and script together does not implicitly omit the visual blueprint or request a PPTX.

## Format-specific contracts

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

- Page numbers, titles, page text, and blueprint pages correspond one-to-one and preserve the approved total and order.
- The six visual fields appear exactly once in the fixed order, have no numeric/list prefix, and contain nonempty page-specific values. Do not add `页面标题：` or a seventh visual field such as teacher guidance, design intent, key-point labels, or notes.
- No user-facing string in either section may contain `课时` or its period-label variants.

### Lesson plan Word — `<topic>-lesson-plan.docx`

- Follow [`teaching-plan-standard.md`](teaching-plan-standard.md): seven top sections `课程信息 / 教材与学情分析 / 教学目标 / 教学重难点 / 教学过程 / 板书设计 / 作业设计`, in native editable Word tables with a centered title, gray section rows and readable cell spacing. Do not replace the whole document with screenshots or continuous prose.
- In the `教学环节 | 具体教学安排` process table, use content-based block titles and the six detailed process fields from the standard. Add actual corresponding PPT ranges only in the final mapped plan; omit them at the first plan-review stage. Preparation, evaluation and implementation cautions belong within the relevant process block; reflection is not a default extra section.
- The checked/approved plan guides the lecture and pages; final page references must follow their shared teaching order. Use pacing internally. The combined Word contains no timing fields and is not a timing source.
- Inside `教学重难点`, write distinct `教学重点` and `教学难点` subsections, each at least 100 Chinese characters. Explain textbook/task basis, intended student understanding/action, likely obstacle and teaching response; one-sentence labels or padded repetition do not pass.
- Apply the visible-emphasis system from `teaching-plan-standard.md`: default to dark red plus bold for short substantive key phrases in `教学重点`, `教学难点`, every major teaching-process block, and the final synthesis. Headings or field labels alone do not satisfy this requirement; reject missing, inconsistent, or excessive emphasis in the rendered Word file.
- Include `板书成品示意` as an actual embedded complete PNG/JPEG blackboard diagram, followed by concise `板书生成顺序`. Default green board, white text and yellow key terms/relationship lines. Use exact text and deliberate diagram rendering; check every visible word and link. It needs three logical layers, at least two explicit relationships and at least three process-linked additions. Fit the usable Word page/cell width and height proportionally; use a dedicated page if needed, never cropping, stretching or illegibly shrinking. A text placeholder, generic keyword list or image elsewhere in the document does not satisfy this section.
- Do not add a section or field named `成果证据`, `学习成果证据`, or equivalent outcome-evidence wording.
- Do not print an overall duration statement such as `总时长：X分钟`, `课程总时长`, or `全课共X分钟`. Use timing internally for planning and consistency checks only; do not summarize it as a total-duration heading or sentence in this Word file.
- Do not change approved pedagogical decisions to fit an independently generated outline. Page references and layout-only improvements may be backfilled; substantive approved-plan changes follow the authorization boundary in `workflow.md`.

### Speaker script Word — `<topic>-speaker-script.docx`

- First draft a continuous, natural teacher lecture from the checked/approved teaching design, then derive the PPT outline and finalize this script's page mapping. Follow the final shared page order and internal pacing; do not invent a confirmed duration or independently rewrite the teaching sequence.
- Include an opening, explanation for each page, questions and likely answer directions, transitions, activity instructions, and a closing.
- Give every PPT page one corresponding script block with these fields, in this order: `教师逐字讲述`, `课堂提问`, `预设回答`, `教师点拨`, `过渡语`. Use `无` only when a field is genuinely not applicable.
- Do not introduce a new page sequence or contradict the approved page outline.
- Automatically rehearse the actual page sequence against the script: source material must be available when mentioned, questions precede the intended answer reveal, response guidance answers the actual question, and transitions connect to the next page. Keep oral explanation distinct from concise on-slide copy; no requirement to put all narration on slides. Preserve the five fields, using display cues within them, without automatically creating animations or PPTX.

### Optional exercise-and-answer Word

Generate only when the user explicitly requests `单课习题`/`课后习题` or `单元综合复习题`/`单元复习卷`. Read and follow [`exercise-package.md`](exercise-package.md). Use `<课题>-课后习题与答案.docx` for the single-lesson route and `<单元>-单元综合复习题与答案.docx` for the unit route. Do not generate both unless the user explicitly requests both. Keep the student paper and teacher answer section in the same Word file, separated by a page break. The exercise package remains separate from the PPT outline and may not change the approved slide count.

### Optional editable PPTX — `<topic>.pptx`

- Use a 16:9 layout.
- Keep text, shapes, diagrams, tables, and charts editable where practical; do not flatten editable teaching content merely for appearance.
- When raster backgrounds or illustrations are needed, route them through `imagegen` using the highest available GPT image-generation model/configuration; keep generated artwork separate from editable text and teaching elements.
- Preserve the approved page order, each page's approved goal, title, core content, activity or case, and timing.
- Implement the approved visual system and every approved page-level visual blueprint (or its approved reusable layout family).
- Maintain classroom readability: clear hierarchy, legible type and contrast, usable information density, and stable display at normal teaching distance.
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

Compare every listed field across the shared page records and the currently requested artifacts. The default is three Word files, but explicit omissions/splits and scoped edits determine the actual checklist. Optional exercises, PPTX, PDF and notes participate only when requested. For exercises also compare scope, terminology, objective/key-point/difficulty coverage, source anchors and any practice/homework cross-references.

| Comparison field | Approved outline/blueprint Word | Lesson plan Word | Speaker script Word | Optional exercise Word | Optional PPTX | Optional PDF | Optional Xiaohongshu notes |
|---|---|---|---|---|---|---|---|
| Topic | Approved topic and product positioning | Course name and scope use it | Opening and page narration use it | Uses the exact requested lesson or unit scope | Uses it only if requested | Same as optional PPTX | Describe this product only if requested |
| Audience | Approved school level and audience | Activities fit it | Questions and delivery fit it | Difficulty, wording, and response demand fit it | Language and examples fit it | Same as optional PPTX | Target user and claims fit it |
| Duration | Internal page records hold supplied or explicitly estimated pacing; no extra Word field | Planned pacing fits that record; no visible total | Speaking/activity pacing fits that record | Does not alter that pacing | Matches it when timing is used | Same as optional PPTX | Do not present an estimate as a confirmed duration |
| Page order | Pages derived from the checked/approved plan's lecture sequence; blueprint follows them | Substantive teaching flow preserved; actual page ranges backfilled | Oral draft finalized against those pages; no separate sequence | Follows the approved knowledge order without adding slides | Pages match exactly | Same as optional PPTX | Suggested pages do not imply another sequence |
| Learning objectives | Frozen objectives and page goals | Objectives, flow, evaluation, extension match | Opening, explanations, closing reinforce them | Questions and analyses cover the approved objectives, key points, and difficulties | Objectives and reinforcement match | Same as optional PPTX | Value claims accurately reflect them |
| Terminology | Approved terms, names, and definitions | Use terms consistently | Use the same terms | Stems, answers, and analyses use the same terms | Use terms consistently | Same as optional PPTX | Use terms consistently if requested |
| Activity timing and display | Internal page record describes what is visible during instruction/question/feedback | Teacher/audience actions and question progression match | Materials, prompts, likely response, feedback and transitions match the current page and do not reveal conclusions too soon | Cited practice/homework matches sibling files | Activities use the same pages and internal plan | Same as optional PPTX | Do not claim extra or differently timed activities |
| Product claims | Approved scope and manifest | Describes the same package | Describes the same package | Exists only when explicitly requested and matches the selected route | Shows only the requested product | Faithful preview if requested | Truthfully markets the requested package |
| Source coverage | Frozen textbook + all SmartEdu teaching designs and learning-task sheets | Uses the same source facts, objectives, tasks, and sequence | Narrates the same source-backed page content and activities | Every item has a supported source anchor and the selected scope is fully covered | Implements only the approved source-backed content | Same as optional PPTX | Claims only what the approved source-backed product contains |
| WPS compatibility | N/A unless an optional PPTX is requested; then record its approved WPS-safe constraints and verdict | N/A | N/A | N/A; verify valid DOCX package and rendered layout | Opens, renders, and remains editable in WPS when the editable PPTX route is requested; image-only route preserves its declared image-only contract | Matches the WPS-verified PPTX render | N/A |

## Authoritative verification predicate

Record an explicit evidence-backed verdict before any final-deliverable claim. Each check uses PASS, FAIL, NOT_RUN or N/A with artifact/version and evidence; unavailable required checks are NOT_RUN, never N/A or PASS. These two groups control the transition from `production_approved` to `verified`:

1. **Full format-contract verdict:** check requested artifacts: combined outline/blueprint Word (exact formats, page correspondence, no banned terms); lesson-plan Word (seven-section native tables, six process fields, key/difficult point subsections each ≥100 Chinese characters, approved mainline, substantive emphasis, complete embedded board image and generation order); script Word (one five-field block per page, natural lecture flow, source accuracy and real display mapping). Render and inspect every current requested Word, honoring omissions/splits/scoped edits. At the first `plan-first` handoff, check only the plan-review scope, without fabricated PPT mappings or a whole-package pass claim. Optional products require their explicit request and relevant checks.
2. **Cross-file matrix verdict:** record actual status for each applicable matrix row from shared source/page records. Validate teaching-source coverage and page ranges, then semantic accuracy. Explicit omissions are N/A with the request recorded. Apply the visual route and evidence rules in `workflow.md`: inspected same-style references or permitted `content-derived` text anchors and design rationale. Both must pass content-fit, unified-style and page-level quality checks; the authorized text-derived route does not itself make a package incomplete. Required online research cannot be replaced or claimed complete when unavailable. Preserve the real basis and any failed attempts. No screenshot evidence or separate reference attachment is required by default.

`verified` is entered automatically only when all applicable required checks in both groups pass with evidence. FAIL or NOT_RUN blocks that whole-package verdict; independently checked artifacts may be handed off with missing checks identified. The selected `plan-first` checkpoint waits for actual user approval, not for package verification; passing first-stage checks does not authorize the next stage. `auto` and the post-approval final handoff require no further routine acceptance. Do not claim that automatic structural checks alone guarantee no semantic or classroom-flow errors.

## Capability routing

Use the bundled capability that owns the relevant stage. The stage owner works from the frozen contracts and does not alter approved decisions.

For lesson-plan Word creation, the user's seven-section table template in `teaching-plan-standard.md` controls the document structure and gray section rows. Apply `documents` for authoring, readability and render verification within that template; its generic preferences must not move the required analysis/process cells into prose or introduce new sections.

| Stage | Primary bundled capability | Responsibility |
|---|---|---|
| Combined outline/visual-blueprint Word, lesson-plan Word, and speaker-script Word | `documents` | Produce the requested Word files from shared teaching and visual records, honoring explicit omissions or splits. |
| Board image embedded in the lesson-plan Word | Exact text/diagram rendering within document production | Render the approved lesson-specific board into PNG/JPEG, embed and inspect its page fit; not a slide-image production route or extra attachment. |
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
