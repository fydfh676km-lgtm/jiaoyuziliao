# Optional anti-garbled-text visual-prompt mode
This is an opt-in prompt mode, not the default visual-blueprint contract. Activate it only when the user explicitly asks for `防乱码`, `约束乱码`, `降低乱码`, `WPS转可编辑防乱码`, `防乱码提示词模式`, or an unambiguously equivalent requirement. Do not infer or activate it merely because slide images, a PPTX, visual quality, or possible future editing are mentioned. When no explicit anti-garbled-text request is present, ignore the rest of this section and follow the pre-existing visual-blueprint and image-generation prompt rules unchanged.

When explicitly activated, this section constrains only the visual blueprint and the image-generation prompt derived from it. It does not change or add rules for OCR, PPT reconstruction, WPS verification, or any downstream conversion workflow.

`classroom-readability.md` remains the shared baseline in ordinary and anti-garbled-text modes, including the cover. Its explicit size targets and text-first capacity rules apply without making the ordinary mode use this file's font/glyph restrictions. The cover exception below concerns stylistic anti-garbled restrictions, not a permission to make essential words too small.

Treat page 1 as an explicit exception. The cover prioritizes maximum visual quality and may use immersive scenes, complex composition, integrated artistic typography, calligraphic treatment, and other high-impact devices. Do not simplify the cover into a generic blank background or apply the inner-page anti-garbled-text restrictions to it.

## Font and glyph recipe for opted-in inner pages

Apply this recipe only to page 2 onward while this mode is explicitly active. In `文字字体与重点标注`, name one deck-wide plan using one or two real font families as visual references and keep their roles stable. For Chinese classical/ink-wash courseware, default to `思源宋体` for inner-page titles and `思源黑体` for body copy; for other compatible courseware, one `思源黑体` family with distinct weights is sufficient. An explicit current-task font choice overrides these defaults. The official Source Han families use SIL OFL licensing: [Source Han Serif](https://github.com/adobe-fonts/source-han-serif/blob/master/LICENSE.txt), [Source Han Sans](https://github.com/adobe-fonts/source-han-sans/blob/master/LICENSE.txt). Do not download, install or bundle font files merely to write prompts.

Required inner-page text uses standard simplified-Chinese glyphs with complete, separate strokes, horizontal alignment and regular spacing. Preserve source-required traditional, foreign-language or special characters accurately instead of silently converting the approved copy. Avoid connected handwriting, flying-white or distressed strokes, missing-stroke art lettering, decorative seal/clerical forms, invented variant glyphs, texture-filled characters and distortion. Emphasize one to three existing teaching priorities with weight, adequate size or a solid accent color, not another font family. Keep rich landscape, ink, paper and light treatment in the surrounding picture; do not remove scene richness to regularize the text.

Write the selected font roles and glyph constraints into each inner page's existing `文字字体与重点标注` field, followed by that page's actual hierarchy and emphasis; do not add a font field, renumber fields, alter approved text or apply this recipe to the cover. Example for a classical-literature inner page:

> 文字字体与重点标注：内页统一以思源宋体标题、思源黑体正文为字形参考；标准简体、笔画完整、水平排列，不连笔、不飞白、不缺笔、不使用变形艺术字。正文保持课堂投影可读大小，标题醒目；从本页已有文字中选择1—3处重点，用深红或加粗突出。

A named font in an image prompt is a visual target, not proof that the image generator loaded that font file. Do not claim exact font identity, installed-font availability, actual rendering compliance or guaranteed error-free WPS conversion from the prompt alone. This recipe changes only prompt wording; it does not switch renderers, add post-processing or modify the downstream conversion workflow.

## Existing inner-page visual constraints

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
