---
name: edu-ppt
description: Use when creating commercial-grade educational PPT products from lesson topics, Xiaohongshu copy, outlines, or visual references for teachers, including lesson plans, speaker scripts, previews, and marketing copy. Invoke as $edu-ppt. Do not use for ordinary business decks or small slide edits.
---

# AI 教育 PPT 商业化生产

Task confirmation fixes the product direction; after the user explicitly starts production, AI completes the frozen workflow without intermediate approval requests. A commercial deck is not final until its teaching logic, page content, visual blueprint, and deliverables agree.

## Direct image-deck route

Select `image-deck` before Smart/Premium mode selection when either condition is observable:

1. the user explicitly names `image-deck` or 图片型 PPT 模式; or
2. the user supplies final per-page content, per-page layout/element style, and a visual reference, then asks for page images plus an image-only PPTX without content planning.

Read `references/image-deck-mode.md` immediately. Treat supplied page content as a strict production contract, normalize supported inputs, and proceed without the five Premium approval gates when the contract is complete. Before the explicit start command, ask only one blocking question when page order is ambiguous, a critical file is unreadable, sources contradict the same page, or exact text cannot fit without changing a frozen constraint; after start, report an unresolved blocker in the final verdict instead of asking mid-process.

Do not use this route to bypass Premium when the user also requests topic selection, content restructuring, lesson plan, speaker script, marketing notes, or the complete commercial product. In that case run Premium normally and allow `image-deck` only as the approved final PPT rendering method.

## Mode selection

Premium is the default when any commercial signal is present.

| Observable request | Mode | Required behavior |
|---|---|---|
| Mentions selling, 商品, 精品, full deck, lesson plan, script, or marketing copy | Premium | Run all internal quality gates automatically after the explicit start command |
| Requests a non-commercial draft or local exploration | Quick | Label the result as a draft |
| Purpose is unclear | Smart | Ask the intended use, then select Quick or Premium |

Before production starts, ask only for genuinely missing task information and preserve any page-count confirmation. Do not treat page-count confirmation alone as the production trigger. After the user explicitly says “开始制作”, “开始生成”, or an equivalent start command, do not ask intermediate questions or request content/visual/production approvals; complete the workflow from the frozen task contract and use safe defaults for routine decisions.

Product mode and content-review mode are separate decisions. At intake, use the default professional-advisor review unless the user explicitly requests strict structure preservation or explicitly authorizes content restructuring; read `references/workflow.md` for the observable review-mode contracts. No review mode may turn unsupported claims into facts, permit direct copying, or skip an internal quality check.

## Fixed section page-count rule

For a single textbook section, the PPT page count must not exceed 30 pages. The only exception is when the SmartEdu reader confirms that the section contains exactly 3 class periods; that section may use 30–35 pages, with 35 pages as the hard maximum. Determine the period count from the SmartEdu source structure, never from filenames or inference. If a proposed or requested page count exceeds the applicable limit, flag the conflict and offer a compliant page-count option; do not silently exceed the limit.

## Fixed start-command contract

The standard user sequence is: provide the courseware requirements, provide the SmartEdu textbook/lesson webpage, then say `按流程开始制作` (or an equivalent explicit start command). Treat that phrase as the production trigger. If no page count was separately confirmed before the trigger, calculate a compliant page count automatically from the SmartEdu source and the fixed cap above; do not ask for a page-count choice after the trigger.

## Route the work

- Read `references/workflow.md` for every new end-to-end product, content review, source ledger, or project-material request.
- When supplied visual references conflict or copying is requested, read `references/visual-system.md` immediately: explicitly classify the conflicts, decline copying, and select the strongest independent topic-appropriate direction internally after the start command.
- After `scale_approved`, use `references/teaching-modes.md` for the page-content blueprint.
- After `content_approved`, use `references/visual-system.md` for the visual review artifact.
- When the user supplies a batch of visual references for future reuse, or when a persistent user visual-reference library already exists, read `references/style-reference-library.md`. Ingest and index a new batch only when the user explicitly authorizes future reuse; during ordinary production, select only the small content-matched subset defined there rather than loading the full library.
- Read `references/quality-gates.md` for every Premium task and whenever approval state is unclear.
- For `image-deck`, read `references/commercial-whole-slide.md`. Saleable image-only courseware defaults to `commercial-whole-slide`: generate each finished page as one integrated commercial slide, review it, then use the bundled Node runtime and `scripts/render-image-deck.mjs` for 4K PNG verification and image-only PPTX packaging. Use the former text-free-asset plus deterministic exact-text route only when the user explicitly prioritizes editability, byte-for-byte text rendering, accessibility, or zero OCR risk over integrated composition. Runtime-generated inputs and outputs stay in the current project.

For final production, read `references/deliverables.md` for the one-premium-version manifest, format contracts, cross-file verification matrix, capability routing, optional adapters, and failure isolation.

When and only when the user explicitly requests `单课习题`/`课后习题` or `单元综合复习题`/`单元复习卷`, read `references/exercise-package.md` and add the matching exercise-and-answer Word to the optional manifest. A generic start command, textbook exercises, a lesson-plan homework section, or the presence of a learning-task sheet does not activate this deliverable. If neither exercise type is explicitly requested, do not generate an exercise file, do not add one to the manifest, and do not ask about it after production has started.

For every teaching-plan Word, read `references/teaching-plan-standard.md` before authoring and again during final verification. It defines the approved section order, detailed teaching-process block, visible-emphasis system, board-design contract, and lesson-plan acceptance checks.

At runtime, read only the current project's `reference/` tree or paths the user explicitly authorizes; never implicitly scan Desktop or other directories. Keep source facts, user preferences, and model inferences separate with provenance and support or confirmation status. Never copy project materials into the personal Skill, and obtain confirmation before persisting newly inferred reusable rules into project knowledge. The one-highest-impact-question rule still applies; when a request combines unauthorized scanning and silent persistence, ask the single authorization or persistence question before asking product purpose.

## Default source intake: `$smartedu-reader`

For a normal educational-courseware request, invoke `$smartedu-reader` (installed skill: `smartedu-numbered-lesson-reader`) as the default first source-reading stage before drafting any page content. It must read the requested SmartEdu textbook/lesson, teaching designs, and learning task sheets in source order, then hand the structured source digest to this Skill. The reader's scope and authentication rules remain authoritative; read its platform-reading and handoff references as required. If the user supplies only local files or a non-SmartEdu source, record that SmartEdu source is unavailable and read only the explicitly authorized materials; do not invent platform content. Skip this default only when the user explicitly says not to use it or explicitly supplies a complete final-page contract for the direct `image-deck` route.

## Fixed output contracts and hard checks

The page outline and visual blueprint are user-facing contracts. Output them exactly in the following formats and do not add fields such as teacher guidance, design intent, highlights, or notes:

**PPT page outline**

```text
第X页
页面标题：
页面文字：
```

**Per-page visual blueprint**

```text
第X页
画面风格：
添加元素：
文字字体与重点标注：
布局排版：
镜头与光影：
画面去重与统一约束：
```

Replace `X` with the actual Arabic page number. Apart from that number inside `第X页`, do not prefix any of the six field labels with `1.`, `2.`, Chinese numerals, circled numbers, letters, bullets, or any other list marker; every label begins directly at the left edge in the order shown, appears exactly once, and is nonempty. The visual-blueprint block must not contain `页面标题：` or any seventh field. Page numbers and all six visual decisions must correspond one-to-one with the approved page outline; do not add transition pages or change the approved total. Teaching-period labels are internal source context only. Before delivery, scan every user-facing PPT, page-outline, visual-blueprint, teaching-plan, and speaker-script string and remove or rewrite `课时` and variants such as `第一课时`, `第二课时`, `课时导入`, and `课时总结`; use content-based transitions instead. A final PPTX is not deliverable until it passes the WPS-safe checklist in `references/wps-safe.md`.

Once the visual direction is selected, lock one recognizable master visual world for the entire deck. Keep its core material, palette roles, typographic hierarchy, border/shape grammar, recurring motifs, and emotional logic stable. For multi-text or multi-chapter lessons, allow content-driven chapter dialects—related accent palettes, brush treatments, scene vocabulary, composition, and shot choices—when they remain visibly part of that master world. Do not jump to an unrelated visual language or modern style merely for variety. Run a whole-deck consistency check before delivery and rewrite any page that reads as an unrelated deck.

Before writing the visual blueprint, perform an internal reference-authenticity check. Distinguish observed visual facts from guesses about whether a supplied or Xiaohongshu reference is AI-generated; if provenance or AI-likeness is uncertain, mark it unverified and use it only for abstract design tendencies, never as a factual or asset source. When generating visual elements, reduce the generic AI look: prefer believable proportions, coherent lighting and shadows, natural material texture, restrained color, human-designed spacing, and editorial/photographic/handmade cues. Avoid plastic gloss, over-saturation, impossible anatomy, warped perspective, random micro-details, fake logos/watermarks, excessive symmetry, generic 3D renders, and decorative effects unrelated to the lesson. Any generated element must pass an internal realism/readability check and be regenerated if artifacts are visible. In an editable or deterministic-text route, required teaching copy remains real editable text and generated assets contain no pseudo-text. In the default commercial-whole-slide route, integrated model-rendered typography is allowed under that route's exact-copy and visual-review checks; this choice does not activate the optional anti-garbled-text mode.

Every visual blueprint and image-generation prompt must describe a concrete, topic-specific scene rather than naming only a broad style or background. When the content supports an Eastern literary or traditional-cultural treatment, prefer landscape, classical Chinese, ink-wash, blue-green landscape, gongbi, or related Chinese visual languages over generic template styling. Ancient poetry and classical-poetry content is a hard trigger: the locked master visual world must visibly express a coherent Chinese landscape/classical/ink aesthetic and translate the poem's actual imagery, season, geography, viewpoint, atmosphere, and emotional tone into the scene. By default, do not name a specific installed font or fixed font category unless the user explicitly requests one; still specify hierarchy, relative scale and weight, placement, color roles, and one to three short emphasis targets. Required classroom text must remain comfortably readable at projection distance and must not be made small to enlarge the picture. Read `references/visual-system.md` for the complete scene recipe, six-field encoding, controlled chapter variation, consistency rules, and coexistence with the optional anti-garbled-text mode.

## Optional anti-garbled-text visual-prompt mode

This is an opt-in prompt mode, not the default visual-blueprint contract. Activate it only when the user explicitly asks for `防乱码`, `约束乱码`, `降低乱码`, `WPS转可编辑防乱码`, `防乱码提示词模式`, or an unambiguously equivalent requirement. Do not infer or activate it merely because slide images, a PPTX, visual quality, or possible future editing are mentioned. When no explicit anti-garbled-text request is present, ignore the rest of this section and follow the pre-existing visual-blueprint and image-generation prompt rules unchanged.

When explicitly activated, this section constrains only the visual blueprint and the image-generation prompt derived from it. It does not change or add rules for OCR, PPT reconstruction, WPS verification, or any downstream conversion workflow.

Treat page 1 as an explicit exception. The cover prioritizes maximum visual quality and may use immersive scenes, complex composition, integrated artistic typography, calligraphic treatment, and other high-impact devices. Do not simplify the cover into a generic blank background or apply the inner-page anti-garbled-text restrictions to it.

For page 2 onward, preserve commercial visual richness while making every required text area visually regular and easy to recognize:

- Keep people, landscape, setting, material detail, foreground/background depth, and page-specific composition rich and topic-appropriate. Do not reduce the deck to white backgrounds with small corner illustrations, repeated left-text/right-image splits, or oversized generic blank panels.
- Place required text on light or otherwise high-contrast regions with low texture, stable brightness, and enough internal padding. Characters must remain visually separate from people, branches, borders, lines, illustrations, and decoration.
- Use a limited, consistent typographic hierarchy across the deck; this means few text styles, not small text. Body copy must not be tiny, thin, low-contrast, or compressed to make an oversized illustration fit. Keep required teaching text horizontal and regularly aligned; do not bend it along a path or apply perspective, skew, warping, texture fill, fading, or complex glow effects.
- Express emphasis with clear hierarchy, weight, size, or solid color. Avoid decorative effects that make the emphasized characters harder to recognize.
- Scrolls, books, ancient pages, seals, title slips, plaques, and similar topic-appropriate elements remain allowed. Use them as text-free decoration or as front-facing, low-texture containers with clear text space; do not ask the image model to fuse required teaching copy into angled, curved, heavily textured, or worn object surfaces.
- Do not place required micro-text inside book pages, maps, scenery, artifacts, seals, or other props. Move essential place names, map labels, captions, or short tags into clear, separate horizontal text positions.
- Give each inner page one dominant information-organizing structure, with at most one subordinate summary area when needed. Avoid combining multiple competing routes, scattered nodes, vertical title slips, side scrolls, and duplicate process summaries on the same page.
- Allocate enough area for the approved copy before sizing the illustration. If the text does not fit legibly, revise the composition rather than shrinking the text.
- Use only visible copy already present in the approved page outline. Do not invent labels, highlighted terms, marginal notes, prop text, or other readable characters, and do not request pseudo-text.

Encode these constraints inside the fixed six blueprint fields rather than adding a seventh field: visual richness and cover treatment in `画面风格`; text-free or safe decorative containers in `添加元素`; the restrained hierarchy and emphasis system in `文字字体与重点标注`; text-region cleanliness, spacing, and the dominant information structure in `布局排版`; camera, viewpoint, shot scale, depth, light direction, softness, color temperature, and atmosphere in `镜头与光影`; and page-specific differentiation plus the master-world continuity anchors in `画面去重与统一约束`.

## Final generation contract and verification

The source ledger is the single source of truth for production. Before handoff, compare the textbook, every SmartEdu teaching design, and every learning-task sheet against the outline, visual blueprint, teaching plan, and speaker script. Preserve textbook order, cover all required source facts/terms/quotations/annotations/exercises and teaching tasks, merge repeated session material into one continuous line, and do not invent unsupported claims. If an artifact fails, regenerate only that artifact from the frozen ledger and page contracts.

If an exercise package was explicitly requested, include it in the same source-ledger and cross-file comparison. Its questions, answers, explanations, scoring points, and source anchors must agree with the frozen textbook, teaching objectives, key points, difficulties, page outline, and lesson-plan homework references. It remains a separate Word deliverable and must not silently expand the PPT page count.

The speaker-script Word must contain one block for every PPT page, in the same order. Each page block must include the delivery fields `教师逐字讲述`, `课堂提问`, `预设回答`, `教师点拨`, and `过渡语` (use `无` only when a field is genuinely not applicable). The script may add supporting activity instructions, but it must not create a new page sequence or contradict the page outline.

Before declaring completion, render every mandatory Word file and inspect the rendered pages for blank pages, missing pages, clipping, overflow, broken tables, font substitution, unreadable contrast, and page-number/order errors; also verify that each DOCX opens as a valid package. Run mechanical checks for exact outline/blueprint fields, one-to-one page correspondence, source coverage, and zero banned teaching-period wording. For any optional PPTX, render every slide, inspect every page, repair only failed pages, then re-run the full checks.

## Default delivery scope

By default, produce exactly four logical deliverables in three Word files:

1. one combined Word containing the complete PPT page outline and the complete page-by-page visual blueprint;
2. one teaching-plan Word; and
3. one speaker-script Word.

The combined Word keeps two clearly labeled sections—`PPT页纲` followed by `视觉蓝图`—while each page block preserves the exact fixed fields above. The default final handoff is the four logical document deliverables in three Word files, plus one separately sent Xiaohongshu reference screenshot when the screenshot rule is triggered. Do not deliver other intermediate review artifacts as separate files. Do not generate an exercise package, editable PPTX, PDF, or Xiaohongshu marketing notes unless the user explicitly requests that specific extra. If the user explicitly asks for separate outline and blueprint files, split the combined Word without changing either contract.

The exercise package is a strict opt-in extra. Explicit `单课习题` or `课后习题` requests produce one `<课题>-课后习题与答案.docx`; explicit `单元综合复习题` or `单元复习卷` requests produce one `<单元>-单元综合复习题与答案.docx`. Do not produce both unless the user explicitly requests both. Merely saying `按流程开始制作`, supplying a textbook with exercises, or including `作业设计` in the teaching plan does not authorize either file.

The teaching-plan Word has two fixed exclusions: do not add a section or field named `成果证据` (or equivalent outcome-evidence wording), and do not print an overall duration statement such as `总时长：X分钟` or `全课共X分钟`. Timing may be used internally to arrange activities and cross-file checks, but it must not appear as a total-duration heading or summary in the teaching-plan Word.

The teaching-plan Word must explain `教学重点` and `教学难点` separately and substantively. Each section must contain at least 100 Chinese characters, identify the relevant textbook/learning-task basis, explain what students need to understand or do, describe the likely learning obstacle, and state how the teaching process addresses it. A one-sentence label or padding to reach the count is not acceptable.

The teaching-plan Word must follow the complete standard in `references/teaching-plan-standard.md`. Its major teaching-process blocks use content-based titles and contain, in order, the corresponding PPT page range, `教学目标`, `教师组织`, `学生学习`, `关键问题`, `评价要点`, and `承接推进`. Important information must be visually discoverable: by default use dark red plus bold for short substantive key phrases, including the central teaching point, central difficulty or breakthrough, one to three lesson-specific priorities in every major process block, and the final synthesis. Every process block must place at least one such emphasis inside the substantive text of `关键问题` or `评价要点`. Do not count colored headings or field labels as substantive emphasis, do not color whole paragraphs, and do not over-highlight.

`板书设计` is mandatory and must include both `板书成品示意` and `板书生成顺序`. The completed board must show at least three logical layers—the lesson title plus a central question or actionable focus, lesson-specific content or evidence, and relationships/synthesis—with at least two semantically clear connections. Its generation order must map those layers to the actual teaching process through at least three distinct additions, connections, or revisions. Reject a generic procedure list, disconnected keyword pile, lesson-agnostic board, board without relationships, board without a generation order, or a board too dense for classroom use.

## Xiaohongshu reference screenshot rule

Before the visual blueprint, perform this step regardless of whether the user supplied current-task references or a persistent user visual-reference library provided matching references. Skip it only when the user explicitly requests no Xiaohongshu reference. Open Xiaohongshu in the system default browser and search with the fixed short query `#课题名称 课件ppt`, replacing `课题名称` with the exact lesson/topic title—for example, `#隋朝统一与灭亡 课件ppt` (use the user's supplied Xiaohongshu search URL only when they provide one). If the user explicitly names a browser, use that browser instead of the default. Capture exactly one independent screenshot of the initial search-results page/first viewport showing the result grid. Preserve the search bar, filters, and visible result thumbnails, analyze that screenshot before drafting the visual blueprint, and send the same screenshot exactly once as a separate final-handoff attachment.

Do not scroll, paginate, open individual notes, click into detail pages, collect multiple screenshots, or send unrelated recommendations. Do not treat note text or thumbnails as content to copy; extract only abstract visual rules for the later visual-system review. The one screenshot is a required standalone final handoff item unless the user explicitly skipped Xiaohongshu references: send it separately in the conversation and do not embed it in any Word file. A user-supplied reference or a library match does not replace this screenshot.

- PPTX creation/editing/verification: use `presentations`.
- DOCX lesson plan, speaker script, and any explicitly requested exercise package: use `documents`.
- Original illustrations/backgrounds: use `imagegen` when generated raster assets are needed.
- PDF rendering or inspection: use `pdf` or the presentation export workflow.
- WPS compatibility verification: use the checklist in `references/wps-safe.md` and a WPS Office open/render check when available.

Check optional community adapters at runtime; none is required. HTML output is opt-in, and one primary producer owns each stage.

A fully approved production reply must name `documents` as the owner of the three mandatory Word files and any explicitly requested exercise Word. Name `presentations`, `imagegen`, or `pdf` only when the user explicitly requested the corresponding optional PPTX, image, or PDF output. Community PPT Skills are runtime-checked optional adapters, never prerequisites.

## Premium sequence

Follow `intake -> topic_approved -> scale_approved -> content_approved -> visual_approved -> production_approved -> verified`. These are internal checkpoints after the explicit start command. At a blocked gate, produce the missing review artifact internally and continue; report only an unavoidable blocker in the final result.

## Explicit start-production rule

The user may confirm the task, topic, and page count before production. Page-count confirmation freezes the scale but does not start production. An explicit command such as `按流程开始制作`, `开始制作`, `开始生成`, or `执行` starts the automatic production run. From that point, the named states above are internal execution and verification states: do not pause for intermediate approval, visual-direction selection, page-count reconfirmation, or routine clarification. Capture and analyze any required Xiaohongshu reference before the visual blueprint, complete the four logical document deliverables in three Word files plus only those extras explicitly present in the frozen task contract, then send that screenshot exactly once as a separate final-handoff attachment together with the verified files and verdict. If an unavoidable external failure remains after safe retries, record it in the final result instead of asking a mid-process question.

## Common mistakes

| Mistake | Correct behavior |
|---|---|
| Repeating questions | Preserve supplied facts; ask only the highest-impact missing question. |
| Fixing page counts without timing | Check stated counts against teaching completeness; otherwise offer 2–3 timing-based options. |
| Copying references | Extract transferable principles and create an independent, topic-appropriate system. |
| Skipping a gate | Stop at the current gate and produce or offer its review artifact. |
| Creating a prettier display-only version | Deliver one saleable version; any requested PDF or preview must match the selected final PPTX route, whether editable or image-only. |
| Treating optional adapters as mandatory | Use available built-in capabilities when an external adapter is absent. |
| Generating decorative backgrounds and covering them with large text panels | For saleable image-only PPTs, use the commercial whole-slide contract and generate the complete composed slide. |
| Repeating one split layout across most pages | Enforce layout-archetype diversity, adjacent-page variation, and the commercial acceptance score. |
