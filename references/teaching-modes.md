# Teaching modes and page-content blueprint

Use this reference only after source understanding and explicit user approval of the current lesson-plan version, when drafting the lecture and deriving pages. First follow the text-specific teaching mainline in `workflow.md`; the modes below are functional aids, not a generic template to overwrite it. Their page types are candidates to use only when appropriate, not mandatory extra slides. Preserve supplied/approved structure and the section cap; merge functions where appropriate instead of manufacturing a checklist page for every type.

All candidate practice/closing tasks stay within the user's specified lesson scope. A mode's mention of application or transfer is not permission to add other lessons, a next-lesson preview or an unrequested writing/grammar topic. Use current-lesson consolidation where useful, otherwise close without an extension task; cross-lesson integration requires an explicit user request.

Do not allocate a PPT page to board writing, board design or a board display (`板书`, `板书设计`, `板书展示`), including the same dedicated board page under another title. The lesson plan retains its board-design module; it is teacher preparation, not a requirement to show every plan module on screen. Necessary teacher board-writing actions may remain non-spoken script cues on existing teaching pages, without a separate page ID. Content-led structure maps, knowledge summaries and lesson recaps remain valid when they serve student learning; shared keywords, arrows or diagram forms alone do not make a page a board page. Carry this distinction into the visual blueprint, aligned script and any explicitly requested PPT, without restoring a board page downstream.

| Lesson type | Possible instructional spine | Candidate page functions | Interaction pattern | Evidence or exercise needs | Closing behavior |
|---|---|---|---|---|---|
| `textbook` | Standard or curriculum anchor → knowledge structure → key/difficult points → worked application → consolidation | Cover; learning objectives; knowledge map; concept/explanation; worked example; practice; summary; current-lesson homework | Teacher modelling, guided questioning, then independent or paired application | Cite the applicable curriculum/source where supplied; include a worked example and practice with feedback or answers | Return to the learning objectives, summarize the knowledge structure, and use a relevant current-lesson consolidation task when needed. |
| `class-meeting` | Situation or question → story/experience → discussion → collective activity → personal commitment → value elevation | Cover; situation prompt; story or case; discussion; activity; commitment; summary/closing | Whole-class prompt, small-group discussion, sharing, and a visible individual or group commitment | Use age-appropriate stories, scenarios, class data, or reflection prompts; include an action-based activity rather than a knowledge-only quiz | Turn the shared value into a concrete class or personal commitment, name the next action, and close with an affirming collective message. |
| `mental-health` | Psychological safety → experience/notice → understand the pattern → practise a strategy → seek support when needed | Cover; safety agreement; experience activity; cognitive explanation; strategy practice; support/boundary; summary/closing | Opt-in, non-disclosing participation; private reflection; low-pressure pair or group practice; never require personal disclosure | Use validated, non-sensational examples and guided exercises; distinguish education from diagnosis; include help-seeking and escalation boundaries | Reinforce a usable self-care strategy, normalize seeking help, state available support and emergency boundaries, and end without forcing disclosure or a promise of recovery. |
| `parent-meeting` | Parent pain points → stage changes → shared understanding → family strategies → home-school coordination → action list | Cover; parent pain-points scan; stage-change explanation; family-strategy pages; home-school coordination; action list; Q&A/closing | Anonymous poll or reflection, scenario discussion, parent choice points, and a home-school follow-up channel | Use approved student/class evidence, developmental information, and family scenarios; provide strategies that parents can try and an action checklist | Recap parent pain points, stage changes, family strategies, home-school coordination, and the action list; name the first follow-up action and contact path. |
| `open-class` | High-value question → inquiry or task → student evidence → feedback and process evaluation → synthesis → public-ready close | Cover; learning objectives/success criteria; engaging task; inquiry or collaborative activity; student evidence/showcase; formative assessment; summary/closing | Visible student thinking, structured collaboration, timely feedback, and planned student presentation or showcase | Include authentic task materials, anticipated responses/misconceptions, observable evidence, and formative assessment criteria | Have learners synthesize the answer with evidence, make the learning visible to observers, revisit success criteria, and close within this lesson's learning scope; no compulsory extension. |

## Premium page-content blueprint

First create the teacher's continuous oral draft from the user-approved teaching blocks: actual spoken explanations, source-based questions, plausible response directions, guidance and transitions. Do not convert the plan into a list of lecture headings or derive this first draft by expanding an independently generated outline. Walk the draft as a teacher would, then choose slide breaks at genuine changes of teaching focus. Preserve source meaning while making the language natural and age-appropriate.

Simulate the approved plan as a real lesson while drafting the lecture: preserve explanation and modelling where useful, and carry its questions, learner thinking/actions and responsive guidance at the moments they help understanding, expression or application. Interaction is woven into this teaching flow, not appended as a final question list or added merely to make each page interactive. Use preparation, sharing, feedback and revision/recheck only where the actual task calls for them, not as a compulsory cycle everywhere. Put only the currently needed material/question/task on screen, keeping probes and response-sensitive guidance in speech/cues; do not reveal an inquiry conclusion before students have a chance to respond. Preserve approved pedagogy, pacing, page cap and exact outline fields; no silent restructuring to add activities.

For every resulting Premium page, extend the shared record from `workflow.md` using the fields below. `role` uses one of the listed values. If duration was supplied, page estimates must fit it; otherwise use a clearly marked internal estimate or leave timing null. Do not request total duration after start, invent a confirmed value, or create a duplicate page plan.

Apply `deliverables.md`'s requested variant scope: A by default, B-only or A+B only when requested. A retains the existing content treatment; B uses the conditional content/layout recipe in `visual-system.md`. Start from the same approved pedagogy and continuous lecture baseline, but decide each variant's on-screen detail and page division separately, then finalize its own page-aligned script. Keep both scripts separate when both are selected; do not invent another lesson mainline, duplicate the plan or force both variants into identical pagination.

For B, develop the page copy here, before freezing that variant's outline: give each point the specific object, necessary explanation, method, source evidence or guiding question needed at this teaching moment. Select useful components, not a mandatory checklist. Do not merely add adjectives to A, paste the whole lecture on screen, pre-reveal inquiry conclusions or import the references' other texts/activities. A still requires complete, usable coverage and must not be deliberately thinned. Freeze each variant's on-screen content before its final blueprint and page-aligned script are completed; the later visual stage arranges this copy rather than independently expanding it.

Carry each topic's verified `读读写写` list from the approved plan into every selected variant's visible `页面文字`, preserving all source word entries and their topic attribution. A heading alone, an oral-only instruction, homework reference or `见教材` does not satisfy this requirement. Arrange the corresponding reading/writing task naturally in the approved lecture flow, with needed pronunciation/form/meaning support; the visual blueprint and final script must preserve its material and display timing. Before freezing the outline, group or split the list by actual classroom large-text capacity within the existing page cap; do not force it onto one page, shrink essential text or drop words to fit artwork. After freezing, keep the existing authorization boundary for content/page-count changes. This required textbook content does not enable a separate exercise deliverable or add fields to the outline/blueprint schemas.

```yaml
courseware_version: A  # internal A/B page namespace, not a visible field
page: 1
teaching_block_ids: ["block-01"]
lecture_segment_ids: ["talk-01"]
source_ids: ["textbook-p3-paragraph2"]
role: cover|section|concept|case|activity|practice|summary|closing
teaching_objective: "Why this page exists"
title: "Visible title"
core_message: "One central idea"
body: ["Approved on-slide points"]
display_moment: "What is visible when the question/instruction/explanation is spoken"
oral_only: ["Explanation or feedback that need not be copied onto the slide"]
teacher_action: "What the teacher does"
learner_or_parent_action: "What the audience does"
evidence_or_example: "Case, source, exercise, or none"
estimated_minutes: 2  # internal estimate; null when not used
```

Finalize the spoken script against these pages using `speaker-script-standard.md`: `P1 页面标题` sections with black `师：` speech and separate red `【…】` non-spoken cues. Preserve the oral draft's logic, not a second independent script. The former five script fields are internal quality dimensions, not visible labels; anticipated responses belong to conditional cues, not invented actual student dialogue. Preserve meaningful pauses, reading/task instructions, response-sensitive guidance and natural transitions. Every material/task learners are asked to inspect must exist on the indicated page or clearly identified source.

The selected mode cannot drop required content or silently change confirmed page order, goals, text or timing. Keep source/block/lecture IDs and true teaching-plan/page mappings resolvable internally after this page split. Do not put PPT total count, page numbers or correspondence into the teaching-plan Word. Multiple suggested sessions organize only its implementation times; produce the complete requested scope as one continuous page sequence, without repeated session covers or truncation to one session. Later visual decisions extend these same records. These records and the pre-pagination lecture draft are internal, not separate deliverables or extra outline fields.

The YAML record above is an internal planning structure only. The user-facing PPT page outline must be rendered exactly as:

```text
第X页
页面标题：
页面文字：
```

Do not expose `role`, `teaching_objective`, `teacher_action`, timing fields, or any other internal fields in the page-outline output.
