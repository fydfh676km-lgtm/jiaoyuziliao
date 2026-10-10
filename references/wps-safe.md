# WPS-safe PPTX checklist

Apply this checklist only to requested PPTX output, after generation and again when that PPTX changes. Record `WPS-safe: PASS | FAIL | NOT_RUN | N/A` with the actual file/version, WPS open observation and exported comparison evidence. PASS requires a real WPS check; another renderer or an OOXML inspection cannot substitute for it. NOT_RUN means WPS/evidence is unavailable; N/A means no PPTX was requested.

## File and layout

- The file opens in WPS Office without a repair, recovery, or compatibility warning.
- The deck uses 16:9 widescreen and preserves the approved page count and order.
- Every page renders without clipped, missing, shifted, or overlapping content.
- Text, shapes, tables, diagrams, and charts remain editable where the approved contract requires editability.

## Fonts and text

- Use installed, WPS-compatible Chinese fonts; do not depend on web fonts or unavailable custom fonts.
- Check Chinese glyphs, punctuation, line breaks, superscripts, and emphasis after opening in WPS.
- Keep text inside safe margins and verify that fallback fonts do not change wrapping or hierarchy.
- Search all PPT-visible text for `课时` and its period-label variants; rewrite before delivery if found.

## Visual compatibility

- Prefer standard PPT shapes, text boxes, tables, PNG/JPG assets, and ordinary fills/strokes.
- Avoid unsupported or fragile effects unless they have been opened and verified in WPS: complex SVG filters, 3D effects, web embeds, unsupported plugins, and unlicensed fonts.
- Verify image crops, transparency, masks, shadows, alignment, and z-order in WPS.
- Export a PDF or slide renders from the WPS-opened file and compare page count, order, text, and visual placement with the approved source.

## Failure handling

If any check fails, keep the workflow at `production_approved`, repair only the affected artifact or page, and rerun the complete checklist plus the cross-file matrix. Do not claim `verified` until the verdict is `PASS`.

If WPS cannot be opened or its output cannot be inspected, record NOT_RUN and the reason. Do not repeatedly retry an unchanged unavailable environment, ask for routine mid-process confirmation, or claim compatibility. Deliver independently verified Word files and identify any optional PPTX as awaiting WPS validation. WPS-exported PDF/PNGs are internal QA evidence unless the user requested them as deliverables.
