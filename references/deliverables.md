# Product deliverable contracts and capability routing

Read this reference before final production, after the page-content and visual-blueprint contracts are frozen. It defines the only Premium product package and the checks required before the package can become `verified`.

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

The filenames are examples derived from the approved topic; replace `<topic>` with the approved topic's delivery-safe name. The default package has four logical document deliverables in three Word files: the combined outline/blueprint Word, the lesson-plan Word, and the speaker-script Word. Unless the user explicitly opts out of the Xiaohongshu reference, add exactly one standalone Xiaohongshu first-viewport reference screenshot to the final handoff even when user references were supplied; send it separately in the conversation and do not embed it in the Word files. The exercise package, editable PPTX, PDF preview, and Xiaohongshu notes are opt-in extras: keep them `null` and do not generate or verify them unless the user explicitly requests that specific extra. A normal start command never activates an exercise package.

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

- Read and follow [`teaching-plan-standard.md`](teaching-plan-standard.md) before authoring and verification. Use its required section order and its fixed detailed teaching-process block: content-based block title, corresponding PPT page range, `教学目标`, `教师组织`, `学生学习`, `关键问题`, `评价要点`, and `承接推进`.
- Follow the approved page order and timing from the combined outline/blueprint Word.
- Include teaching objectives, key points, difficulties, preparation, timed teaching flow, teacher activity, audience activity, rationale/design intent, evaluation, and an extension/homework/action follow-up.
- Write `教学重点` and `教学难点` as two separate sections, each at least 100 Chinese characters. Each must explain its textbook/learning-task basis, the intended student understanding or action, the likely obstacle, and the teaching response; do not satisfy the requirement with a one-sentence label or padded repetition.
- Apply the visible-emphasis system from `teaching-plan-standard.md`: default to dark red plus bold for short substantive key phrases in `教学重点`, `教学难点`, every major teaching-process block, and the final synthesis. Headings or field labels alone do not satisfy this requirement; reject missing, inconsistent, or excessive emphasis in the rendered Word file.
- Include both `板书成品示意` and `板书生成顺序`. The board must be lesson-specific, contain at least three logical layers and at least two explicit relationships, map to the detailed teaching process, and remain writable/readable in classroom use. Reject generic procedures, disconnected keywords, or a board with no stated generation order.
- Do not add a section or field named `成果证据`, `学习成果证据`, or equivalent outcome-evidence wording.
- Do not print an overall duration statement such as `总时长：X分钟`, `课程总时长`, or `全课共X分钟`. Use timing internally for planning and consistency checks only; do not summarize it as a total-duration heading or sentence in this Word file.
- Do not introduce a new page sequence or contradict the approved page outline.

### Speaker script Word — `<topic>-speaker-script.docx`

- Follow the approved page order and timing from the combined outline/blueprint Word.
- Include an opening, explanation for each page, questions and likely answer directions, transitions, activity instructions, and a closing.
- Give every PPT page one corresponding script block with these fields, in this order: `教师逐字讲述`, `课堂提问`, `预设回答`, `教师点拨`, `过渡语`. Use `无` only when a field is genuinely not applicable.
- Do not introduce a new page sequence or contradict the approved page outline.

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

Generate only when explicitly requested. When requested, provide exactly ten notes (`note_count: 10`). Each note must have a genuinely distinct marketing angle; do not create ten superficial rewrites of the same hook, audience pain point, use case, teaching feature, or product value. Every note must make truthful claims: each claim about pages, content, use, audience, files, or product value must be supported by the approved blueprint and this manifest, with no invented results, features, endorsements, or separate display-only version.

Every note includes:

- a title;
- a hook;
- body copy;
- product value;
- image suggestions based on actual product pages or truthful supporting visuals;
- keywords; and
- an engagement prompt.

## Cross-file verification matrix

Compare every listed field across the approved blueprint and every produced artifact. The approved page outline and visual blueprint are the source contracts; the three mandatory Word files must represent them directly. The optional exercise package, PPTX, PDF, and notes participate only when explicitly requested. When an exercise package participates, also compare its scope, terminology, objective/key-point/difficulty coverage, source anchors, selected PPT practice/homework references, and lesson-plan homework references against the frozen source ledger and sibling files.

| Comparison field | Approved outline/blueprint Word | Lesson plan Word | Speaker script Word | Optional exercise Word | Optional PPTX | Optional PDF | Optional Xiaohongshu notes |
|---|---|---|---|---|---|---|---|
| Topic | Approved topic and product positioning | Course name and scope use it | Opening and page narration use it | Uses the exact requested lesson or unit scope | Uses it only if requested | Same as optional PPTX | Describe this product only if requested |
| Audience | Approved school level and audience | Activities fit it | Questions and delivery fit it | Difficulty, wording, and response demand fit it | Language and examples fit it | Same as optional PPTX | Target user and claims fit it |
| Duration | Approved total and page timing | Timed flow totals to it | Speaking/activity pacing fits it | Does not alter the approved lesson/PPT duration | Page timings total to it | Same as optional PPTX | Do not imply a different duration |
| Page order | Frozen page sequence, outline, and blueprint | Flow and page references follow it | Explanations follow it | Follows the approved knowledge order without adding slides | Pages match exactly | Same as optional PPTX | Suggested pages do not imply another sequence |
| Learning objectives | Frozen objectives and page goals | Objectives, flow, evaluation, extension match | Opening, explanations, closing reinforce them | Questions and analyses cover the approved objectives, key points, and difficulties | Objectives and reinforcement match | Same as optional PPTX | Value claims accurately reflect them |
| Terminology | Approved terms, names, and definitions | Use terms consistently | Use the same terms | Stems, answers, and analyses use the same terms | Use terms consistently | Same as optional PPTX | Use terms consistently if requested |
| Activity timing | Frozen timing for each activity/page | Timed flow and teacher/audience actions match | Instructions and pacing match | Any cited practice/homework item matches the sibling files | Activities occur at approved pages/times | Same as optional PPTX | Do not claim extra or differently timed activities |
| Product claims | Approved scope and manifest | Describes the same package | Describes the same package | Exists only when explicitly requested and matches the selected route | Shows only the requested product | Faithful preview if requested | Truthfully markets the requested package |
| Source coverage | Frozen textbook + all SmartEdu teaching designs and learning-task sheets | Uses the same source facts, objectives, tasks, and sequence | Narrates the same source-backed page content and activities | Every item has a supported source anchor and the selected scope is fully covered | Implements only the approved source-backed content | Same as optional PPTX | Claims only what the approved source-backed product contains |
| WPS compatibility | N/A unless an optional PPTX is requested; then record its approved WPS-safe constraints and verdict | N/A | N/A | N/A; verify valid DOCX package and rendered layout | Opens, renders, and remains editable in WPS when the editable PPTX route is requested; image-only route preserves its declared image-only contract | Matches the WPS-verified PPTX render | N/A |

## Authoritative verification predicate

Record an explicit verification verdict before any final-deliverable claim. This two-group technical verdict is the sole authoritative predicate for the transition from `production_approved` to `verified`:

1. **Full format-contract verdict:** record pass or fail for each mandatory artifact: combined outline/visual-blueprint Word (exact sections and fields, page correspondence, no `课时` variants); lesson-plan Word (all required sections and detailed process fields, `教学重点` and `教学难点` each at least 100 Chinese characters, approved flow and timing, visible substantive emphasis, and a three-layer lesson-specific board with an explicit generation order); and speaker-script Word (one page block per slide with all five delivery fields, approved facts, and timing). Also record rendered-layout and valid-DOCX-package checks for all three Word files. Check an optional exercise package, PPTX, PDF, or Xiaohongshu notes only when explicitly requested; apply its format contract and WPS-safe checklist where applicable.
2. **Cross-file matrix verdict:** record pass or fail for every row in the matrix above—topic, audience, duration, page order, learning objectives, terminology, activity timing, product claims, source coverage, and WPS compatibility when applicable—across the mandatory Word files and any requested optional files.

`verified` is entered automatically only when both verdict groups pass in full. Any format-contract failure or matrix mismatch keeps the workflow state at `production_approved`, never `verified`. No sixth human approval gate, user acceptance, or user confirmation is required for this technical transition. Every user-facing verification or repair transition response must explicitly state that user acceptance or feedback is an optional post-verification handoff, not a condition for entering `verified`.

## Capability routing

Use the bundled capability that owns the relevant stage. The stage owner works from the frozen contracts and does not alter approved decisions.

| Stage | Primary bundled capability | Responsibility |
|---|---|---|
| Combined outline/visual-blueprint Word, lesson-plan Word, and speaker-script Word | `documents` | Produce the three mandatory Word files from the frozen teaching and visual contracts. |
| Explicitly requested exercise-and-answer Word | `documents` | Produce the selected single-lesson or unit exercise package from the frozen source ledger and teaching contracts. |
| Optional PPTX creation, editing, and verification | `presentations` | Produce and inspect an editable PPTX only when explicitly requested. |
| Optional original illustrations and backgrounds | `imagegen` | Create needed generated raster assets only for an explicitly requested PPTX/image route. |
| Optional PDF rendering, export, and inspection | `pdf` or the presentation export workflow | Create or inspect a PDF only when explicitly requested. |

## Required production-start response

A response that accepts a fully approved Premium request for production must explicitly name `documents` as the owner of the three mandatory Word files: the combined PPT页纲+视觉蓝图 Word, the lesson-plan Word, and the speaker-script Word. If an exercise package was explicitly requested, also name `documents` as its owner. Name `presentations`, `imagegen`, or `pdf` only when the user explicitly requested the corresponding optional output. Community PPT Skills remain runtime-checked optional adapters, never prerequisites; their absence does not block the bundled route.

## Optional adapter routing

Check adapter availability at runtime. None of these adapters is required: absence never blocks the workflow, and the bundled route remains available. Assign one primary producer to a stage; an adapter may assist only when it is the selected stage owner and may not independently rewrite a sibling artifact or an approved contract. HTML output is opt-in: it is used only when the user explicitly asks for an HTML presentation or preview, and it is not part of the default manifest.

| Optional adapter | Useful stage ownership when available |
|---|---|
| PPT-Master | Native editable PPTX production or refinement. |
| Frontend-Slides | Visual-direction exploration before visual approval. |
| Beautiful-HTML-Templates | Design-asset and layout-reference exploration before visual approval. |
| Guizang-PPT-Skill | Education, emotional, or magazine-style visual design before visual approval. |
| HTML-PPT-Skill | Explicitly requested dynamic HTML presentation or preview production. |

## Failure isolation and repair

When a produced artifact fails its format contract or a matrix check, regenerate only that failed artifact from the frozen contracts. Do not reopen approved decisions and do not silently change successful sibling artifacts. After repair, re-run that artifact's full format-contract checks, then place the regenerated artifact back into the complete cross-file verification matrix and update the explicit verification verdict. Only all-pass full format-contract and cross-file matrix verdicts permit the move from `production_approved` to `verified`.
