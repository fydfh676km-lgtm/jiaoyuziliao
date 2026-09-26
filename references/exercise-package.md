# Optional exercise-package contract

Read this reference only when the frozen task contract explicitly requests one of the supported exercise deliverables. Exercise generation is strict opt-in and never part of the normal `按流程开始制作` output.

## Activation and routing

| Explicit request | Deliverable | Filename |
|---|---|---|
| `单课习题` or `课后习题` | Single-lesson exercise and answer Word | `<课题>-课后习题与答案.docx` |
| `单元综合复习题` or `单元复习卷` | Unit review and answer Word | `<单元>-单元综合复习题与答案.docx` |

Do not infer activation from textbook exercises, teaching-plan homework, SmartEdu learning-task sheets, or a generic production command. Do not generate both routes unless both are explicitly requested. If no supported exercise request is present, leave `exercise_package: null`, perform no exercise drafting, and ask no exercise-related question after the explicit start command.

## Source authority and construction

Build every item from the frozen source ledger in this order:

1. original textbook text, annotations, figures, tables, activities, and textbook questions;
2. all SmartEdu teaching designs in source order;
3. all SmartEdu learning-task sheets;
4. the approved lesson-plan objectives, key points, and difficulties; and
5. the approved PPT content order and classroom tasks.

The textbook is the factual authority. Teaching designs determine instructional emphasis; learning-task sheets inform task type and expected response but are not copied mechanically. Keep each item's source anchor internally during drafting. Do not introduce unsupported facts, off-scope knowledge, or a claim that cannot be answered from the frozen source set unless the item is visibly labeled as an optional extension and its supporting source is recorded.

## Route-specific composition

### Single lesson or section

- Produce approximately 12–18 items, adjusted to the actual content density rather than padded to a number.
- Target roughly 40% foundational consolidation, 40% comprehension/application, and 20% synthesis/transfer.
- Cover the approved teaching objectives, central key point, and central difficulty.

### Whole unit or multiple related sections

- Produce approximately 20–30 items, adjusted to the number and density of included sections.
- Target roughly 30% foundational knowledge, 40% core application, and 30% cross-section synthesis/transfer.
- Include every included text/lesson/section in the internal coverage matrix; do not over-concentrate questions on one source.

## Subject-sensitive question design

- Chinese: language foundations, content comprehension, textual appreciation, reading transfer, and expression/writing.
- History: chronology, concept discrimination, source/material analysis, chart or map interpretation, causation/comparison, and evidence-based response.
- English: vocabulary, grammar, target sentence use, reading comprehension, contextual expression, and writing.
- Other subjects: choose question types from the source's disciplinary practices and stated learning objectives; do not force a humanities template onto them.

## One-file Word structure

The exercise deliverable is one Word file with two parts separated by a page break:

1. `学生练习卷` — title, applicable scope, instructions when needed, and numbered questions. It contains no answers, analyses, scoring points, difficulty labels, source anchors, or knowledge-point tags.
2. `参考答案与解析` — matching question number, reference answer, concise explanation, scoring points for open responses, source anchor, and the corresponding objective/key point/difficulty where applicable.

Open-response items must provide usable reference content and explicit scoring points; `言之有理即可` alone is not an answer. Objective items must have one defensible answer. Keep answer material out of the student section, including headers and footers.

## Cross-file behavior

- Follow textbook and approved PPT knowledge order where it supports a coherent progression.
- A lesson-plan `作业设计` may cite exact exercise numbers from this Word; those numbers and tasks must match.
- A PPT practice or homework page may select a subset of the exercise package, but exercise generation may not add slides or change the frozen page count.
- Do not duplicate the same item merely to satisfy coverage or count targets.
- Apply the global ban on `课时` and teaching-period variants to the entire exercise Word.

## Verification

Before delivery, record pass/fail for all of the following:

- every item has a supported source anchor and stays within the requested lesson/unit scope;
- the internal coverage matrix includes every approved objective, key point, and difficulty, and every included unit section when using the unit route;
- objective answers are unique and distractors are plausible without accidental clues;
- open responses have reference answers and concrete scoring points;
- question numbering matches the answer section exactly, with no missing, duplicate, or reordered item;
- terminology, facts, assignments, and any selected PPT questions agree with the page outline, lesson plan, and speaker script;
- no `课时` or teaching-period variant remains;
- the DOCX opens as a valid package; and
- rendered pages contain no blank pages, clipped text, overflow, broken tables, illegible type, or answer leakage into the student section.

If the exercise file fails, regenerate only that file from the frozen source ledger and contracts, then rerun its complete checks and the cross-file verification matrix.
