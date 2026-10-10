# Teaching modes and page-content blueprint

Use this reference after source understanding and lesson-plan review, when drafting the lecture and deriving pages. First follow the text-specific teaching mainline in `workflow.md`; the modes below are functional aids, not a generic template to overwrite it. Their page types are candidates to use only when appropriate, not mandatory extra slides. Preserve supplied/approved structure and the section cap; merge functions where appropriate instead of manufacturing a checklist page for every type.

| Lesson type | Possible instructional spine | Candidate page functions | Interaction pattern | Evidence or exercise needs | Closing behavior |
|---|---|---|---|---|---|
| `textbook` | Standard or curriculum anchor → knowledge structure → key/difficult points → worked application → consolidation | Cover; learning objectives; knowledge map; concept/explanation; worked example; practice; summary; homework or extension | Teacher modelling, guided questioning, then independent or paired application | Cite the applicable curriculum/source where supplied; include a worked example and practice with feedback or answers | Return to the learning objectives, summarize the knowledge structure, and assign a traceable practice or extension task. |
| `class-meeting` | Situation or question → story/experience → discussion → collective activity → personal commitment → value elevation | Cover; situation prompt; story or case; discussion; activity; commitment; summary/closing | Whole-class prompt, small-group discussion, sharing, and a visible individual or group commitment | Use age-appropriate stories, scenarios, class data, or reflection prompts; include an action-based activity rather than a knowledge-only quiz | Turn the shared value into a concrete class or personal commitment, name the next action, and close with an affirming collective message. |
| `mental-health` | Psychological safety → experience/notice → understand the pattern → practise a strategy → seek support when needed | Cover; safety agreement; experience activity; cognitive explanation; strategy practice; support/boundary; summary/closing | Opt-in, non-disclosing participation; private reflection; low-pressure pair or group practice; never require personal disclosure | Use validated, non-sensational examples and guided exercises; distinguish education from diagnosis; include help-seeking and escalation boundaries | Reinforce a usable self-care strategy, normalize seeking help, state available support and emergency boundaries, and end without forcing disclosure or a promise of recovery. |
| `parent-meeting` | Parent pain points → stage changes → shared understanding → family strategies → home-school coordination → action list | Cover; parent pain-points scan; stage-change explanation; family-strategy pages; home-school coordination; action list; Q&A/closing | Anonymous poll or reflection, scenario discussion, parent choice points, and a home-school follow-up channel | Use approved student/class evidence, developmental information, and family scenarios; provide strategies that parents can try and an action checklist | Recap parent pain points, stage changes, family strategies, home-school coordination, and the action list; name the first follow-up action and contact path. |
| `open-class` | High-value question → inquiry or task → student evidence → feedback and process evaluation → synthesis → public-ready close | Cover; learning objectives/success criteria; engaging task; inquiry or collaborative activity; student evidence/showcase; formative assessment; summary/closing | Visible student thinking, structured collaboration, timely feedback, and planned student presentation or showcase | Include authentic task materials, anticipated responses/misconceptions, observable evidence, and formative assessment criteria | Have learners synthesize the answer with evidence, make the learning visible to observers, revisit success criteria, and end with a concise transfer question or extension. |

## Premium page-content blueprint

First create the teacher's continuous oral draft from the checked/approved teaching blocks: actual spoken explanations, source-based questions, plausible response directions, guidance and transitions. Do not convert the plan into a list of lecture headings or derive this first draft by expanding an independently generated outline. Walk the draft as a teacher would, then choose slide breaks at genuine changes of teaching focus. Preserve source meaning while making the language natural and age-appropriate.

For every resulting Premium page, extend the shared record from `workflow.md` using the fields below. `role` uses one of the listed values. If duration was supplied, page estimates must fit it; otherwise use a clearly marked internal estimate or leave timing null. Do not request total duration after start, invent a confirmed value, or create a duplicate page plan.

```yaml
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

Finalize the five script fields against these pages, preserving the oral draft's logic instead of starting a separate script. Group each page's narration and questioning without duplicating the same spoken question in multiple fields; `预设回答` is anticipated student response, not teacher narration. Preserve meaningful pauses, reading/task instructions and response-sensitive guidance within the existing fields. End each page with a transition that actually prepares the next. Not every detail spoken by the teacher needs an on-screen counterpart, but every material/task the script asks learners to inspect must be available on the indicated page or clearly identified source.

The selected mode cannot drop required content or silently change confirmed page order, goals, text or timing. Keep source/block/lecture IDs resolvable and backfill true teaching-plan page ranges only after this page split. Later visual decisions extend these same records. These records and the pre-pagination lecture draft are internal, not separate deliverables or extra outline fields.

The YAML record above is an internal planning structure only. The user-facing PPT page outline must be rendered exactly as:

```text
第X页
页面标题：
页面文字：
```

Do not expose `role`, `teaching_objective`, `teacher_action`, timing fields, or any other internal fields in the page-outline output.
