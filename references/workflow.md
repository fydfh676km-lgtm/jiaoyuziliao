# Premium workflow state contract

Use this contract for every Premium product. Confirmed task data are immutable: a later state may not silently rewrite them. Page-count confirmation freezes the scale; the explicit start command begins automatic execution through all internal checkpoints.

```text
intake -> topic_approved -> scale_approved -> content_approved -> visual_approved -> production_approved -> verified
```

## Default source-reading stage

For ordinary educational-courseware requests, begin `intake` by invoking `$smartedu-reader` (installed skill: `smartedu-numbered-lesson-reader`) when the requested textbook or lesson can be resolved on the SmartEdu platform. Read the lesson, teaching designs, and learning task sheets in source order and hand the structured source digest to this workflow before drafting the page outline. If the user supplies only local files or another explicitly authorized source, state that SmartEdu is unavailable for this request and use only those materials. Do not silently substitute unrelated platform content. An explicit user skip or a complete direct `image-deck` page contract is the only default-route exception.

## Xiaohongshu reference collection before the visual gate

After the page content is approved and before producing the visual-system proposal or page-by-page visual blueprint, collect the Xiaohongshu style reference unless the user explicitly requests no Xiaohongshu reference. A current-task reference image or a persistent-library match does not replace this step. Open Xiaohongshu in the system default browser and search with this fixed short query, replacing `课题名称` with the exact lesson/topic title. If the user explicitly names a browser, use that browser instead:

```text
#课题名称 课件ppt
```

Example: `#隋朝统一与灭亡 课件ppt`.

Capture exactly one independent screenshot of the initial search-results page/first viewport, including the search bar, filters, and visible result thumbnails. Analyze it before drafting the visual blueprint, then send that same screenshot exactly once as a separate final-handoff attachment. Do not scroll, paginate, open notes, click detail pages, or collect additional screenshots. Treat the screenshot only as a composite style reference: extract abstract visual rules and feed them into the visual-system review; never copy note wording, page composition, or assets. Omit this collection step only when the user explicitly skips the Xiaohongshu reference, and record that reason.

## Image-deck boundary

`image-deck` is a direct production route only for a complete final-page contract. When the request includes topic selection, content restructuring, a lesson plan, speaker script, marketing notes, or the complete commercial product, keep the Premium sequence and run its internal checkpoints automatically after the explicit start command. After the visual/production contract is internally complete, that Premium product may choose `image-deck` only as the final PPT rendering method; it does not replace Premium planning or the remaining Premium deliverables.

## Strict opt-in exercise package

Exercise files are not part of the default workflow. Activate exactly one exercise route only when the user explicitly requests it before production or includes it in the frozen task contract:

- `单课习题` or `课后习题` -> `<课题>-课后习题与答案.docx`;
- `单元综合复习题` or `单元复习卷` -> `<单元>-单元综合复习题与答案.docx`.

Do not infer either route from a generic request for the normal workflow, the existence of textbook exercises, a teaching-plan homework section, or a SmartEdu learning-task sheet. Do not ask whether to add exercises after the explicit start command. If activated, read `exercise-package.md`, freeze the selected exercise type in the intake contract, add only that Word file to the optional production manifest, and verify it with the other requested artifacts. Do not generate both unless both are explicitly requested.

| State | Required inputs | Internal checkpoint artifact | Checkpoint evidence | Data frozen at checkpoint | Single next action |
|---|---|---|---|---|---|
| `intake` | User request; known theme, audience, duration, source materials, and intended use | Requirements and source-analysis brief; resolve only genuinely missing pre-start information | Task confirmation is present; page count may still be confirmed separately | Theme, audience, teaching objective, product positioning, source facts and stated preferences | Produce the scale options. |
| `topic_approved` | Frozen topic contract; duration or the need to resolve it; lesson type, school level, complexity, and positioning | Scale proposal with duration, page-count options, and chapter structure | Task and page-count confirmation are present; this does not start production | Duration, page count, and chapter structure | Wait for the explicit start command, then produce the page-by-page content blueprint. |
| `scale_approved` | Frozen topic and scale contracts; source interpretation | Page-by-page content blueprint with each page's goal, title, core content, activity or case, and timing | Internal content completeness and timing checks pass after start | Page order, page goals, titles, core content, activities/cases, and timing | Produce the visual-system and page-by-page visual blueprint internally. |
| `content_approved` | Frozen topic, scale, and content contracts; visual references if supplied | Visual-system proposal plus one six-field visual blueprint for every page (`第X页 / 画面风格 / 添加元素 / 文字字体与重点标注 / 布局排版 / 镜头与光影 / 画面去重与统一约束`), with original direction, layout, hierarchy, palette, elements, shot/light, and page-specific differentiation | Internal visual completeness and reference-use checks pass | Visual direction, palette, typographic hierarchy, layout rules, page layouts, elements, shot/light, and design intent | Produce the final delivery manifest internally. |
| `visual_approved` | Frozen topic, scale, content, and visual contracts | Production manifest for the default four logical deliverables: one combined PPT页纲+视觉蓝图 Word, one lesson-plan Word, and one speaker-script Word; an exercise Word, PPTX, PDF, or marketing file is listed only when that specific extra was explicitly requested | Internal manifest and scope checks pass | File list, formats, version scope, production routing, and delivery naming | Produce the approved files. |
| `production_approved` | Frozen contracts and approved production manifest | The three default Word files, any explicitly requested optional files, and the two-group verification report | Both the full format-contract verdict and the complete cross-file matrix verdict are `PASS` in full, including the exercise-package checks when requested, the `课时` scan, and WPS-safe check whenever PPTX is requested; this technical all-pass result requires no user approval or acceptance | Technically verified product package and verification record | Enter `verified` automatically when both verdict groups pass; otherwise repair only failed artifacts and remain here. |
| `verified` | Technically verified package and both all-pass verdict groups | Final verified delivery record | No additional user approval is required; all internal checks pass | All confirmed contracts, final files, and authoritative verification record | Hand off the verified package and optional post-delivery feedback. |

## Explicit start-production trigger

The standard start sequence is: courseware requirements + SmartEdu textbook/lesson webpage + the user's command `按流程开始制作` (or an equivalent explicit start command). Task confirmation and page-count confirmation may happen before production. Page-count confirmation freezes the scale but is not itself a start command. If page count is still unspecified when the start command arrives, calculate it automatically within the fixed cap. From the start command onward, `topic_approved`, `scale_approved`, `content_approved`, `visual_approved`, and `production_approved` are internal checkpoints, not user pauses: do not request intermediate approval, visual-direction selection, page-count reconfirmation, or routine clarification. Complete the default deliverables and verification, and report any unavoidable blocker only in the final result.

## Content-review mode

Content-review mode is orthogonal to the Premium, Quick, or Smart product mode. Select it from the user's observable instruction; never use a product-mode choice as a substitute. In every review mode, preserve the source ledger below, surface factual, copyright, and teaching risks, and use the start-production rule above once the user has explicitly started.

| Observable instruction | Content-review mode | Required review artifact and behavior |
|---|---|---|
| No explicit instruction to preserve or restructure the supplied content | `professional-advisor` (default) | The internal review must use explicit `Strengths`, `Issues/risks`, and `Improvement recommendations` sections, even when a section says none were identified from the limited supplied material. Include factual/copyright/teaching risk flags; separate source facts, user preferences, and model inferences with provenance and status. After the start command, apply the recommendation automatically within the frozen task scope. |
| Explicit request to preserve the supplied outline or structure and not rewrite it | `strict-execution` | Preserve the supplied structure and do not silently optimize, rewrite, or reorder it. The internal review must explicitly state `Factual risk`, `Copyright risk`, and `Teaching/pedagogical risk`, even when a category says none were identified. Refuse unsupported factual claims and direct copying of third-party wording or design; after the start command, apply only compliant substitutions or status markers without asking a mid-process question. |
| Explicit authorization to restructure, such as “优化成精品课件，可以重构内容” | `authorized-auto-upgrade` | May restructure the supplied content into an improved review artifact, with changes and rationale visible and facts/preferences/inferences still separated. After the start command, apply the approved restructuring automatically and continue to final production. |

No restructuring is authorized by “直接用”, commercial intent, urgency, or the word “精品” alone. If authorization is absent or ambiguous, use `professional-advisor`; after the start command, make only conservative, source-supported improvements.

## Runtime project and source governance

Use only materials inside the current project's `reference/` tree or individual paths the user explicitly authorizes. Never implicitly enumerate, search, or read Desktop or any other directory. When authorized project materials need organization, offer this project-local structure:

```text
reference/
├── xiaohongshu-notes/
├── visual-references/
├── teaching-templates/
└── marketing-examples/
```

Create a source ledger before turning supplied material into a review artifact:

```yaml
source_ledger:
  source_facts:
    - claim: "What the source states"
      provenance: "File, URL, author, page, or user-supplied identifier"
      support_status: supported|unsupported|pending-verification
  user_preferences:
    - preference: "What the user wants"
      provenance: "User statement or approved brief"
      confirmation_status: confirmed|pending-confirmation
  model_inferences:
    - inference: "Interpretation or proposed conclusion"
      provenance: "Source facts or reasoning it was derived from"
      support_status: supported|unsupported|pending-verification
      confirmation_status: confirmed|pending-confirmation
```

Unsupported source claims or model inferences never become product facts or marketing claims without adequate support or explicit confirmation where confirmation is appropriate. User confirmation records a preference or decision; it does not make an unsupported empirical claim true.

## Global PPT text and WPS constraints

Teaching-period labels are internal source context only. No user-facing PPT, page outline, visual blueprint, teaching plan, speaker script, title, body text, activity label, footer, or transition may contain `课时` or variants such as `第一课时`, `第二课时`, `课时导入`, or `课时总结`; rewrite them as content-based titles/transitions. The page outline must use exactly `第X页 / 页面标题： / 页面文字：`; the visual blueprint must use exactly the six fields specified above, in order and without field numbering, `页面标题：`, or any seventh field. Whenever an optional PPTX is requested, apply `references/wps-safe.md` before `verified` and record a WPS-safe verdict; the default three-Word package does not require a PPTX/WPS verdict.

## Default packaging contract

The default production package contains four logical document deliverables in three Word files, plus one standalone Xiaohongshu reference screenshot when the reference rule is triggered:

- `<topic>-ppt-outline-visual-blueprint.docx`: section `PPT页纲`, then section `视觉蓝图`;
- `<topic>-lesson-plan.docx`;
- `<topic>-speaker-script.docx`.

Unless the user explicitly opted out of the Xiaohongshu reference, send its one first-viewport screenshot separately in the conversation as the additional reference handoff item; do not embed it in the Word files. User-supplied references do not replace it.

The exercise package, editable PPTX, PDF preview, and Xiaohongshu marketing-notes file are opt-in extras. Do not create them, add them to the manifest, or verify them unless the user explicitly requests the specific extra. For exercises, the user must explicitly request `单课习题`/`课后习题` or `单元综合复习题`/`单元复习卷`; the standard start command alone never activates them.

Project materials remain project data: never copy them into the installed personal Skill. Newly inferred reusable rules may be proposed for the project knowledge base, but persist them only after the user confirms the exact rule and destination. If authorization, provenance, or persistence scope is missing, ask only the single highest-impact question in that turn. When one request combines unauthorized scanning and silent persistence, refuse both actions, offer the project `reference/` tree, and ask one authorization or persistence question before asking product purpose.

## Scale rule

For each single textbook section, enforce the page-count cap before presenting scale options: no more than 30 PPT pages. If the SmartEdu source structure explicitly confirms exactly 3 class periods for that section, allow 30–35 pages, with 35 as the hard maximum. Use the reader's period continuity and resource relations as the authority; do not infer the count from filenames. When the user specifies a page count, check it against both teaching completeness and this cap, identify any conflict before proceeding, and offer a compliant alternative. When page count is unspecified before the start command, provide 2–3 options only if the user is still planning; once the start command is given, select the strongest compliant count automatically and continue without asking.

## Blocked gates

Do not pause after the explicit start command to request approval for an artifact. If an internal artifact is missing, produce it from the confirmed task contract and continue; apply the final verification predicate before delivery.

## Complete example

Request: "制作一套90分钟高一开学家长会精品商品，主题是《新高一，不焦虑》，未指定页数。"

Correct next output: classify it as Premium, preserve the given audience/duration/theme, then offer page-count options such as 24 pages for a concise meeting, 32 pages for the recommended complete product, and 40 pages for an interaction-rich version. Ask only the page-count choice.
