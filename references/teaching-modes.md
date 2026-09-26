# Teaching modes and page-content blueprint

Use this reference after `scale_approved`, when the lesson type and approved duration, page count, and chapter structure are fixed. Select exactly one of the five modes below for the page-content blueprint. Do not silently change any frozen topic or scale decision.

| Lesson type | Instructional spine | Required page types | Interaction pattern | Evidence or exercise needs | Closing behavior |
|---|---|---|---|---|---|
| `textbook` | Standard or curriculum anchor → knowledge structure → key/difficult points → worked application → consolidation | Cover; learning objectives; knowledge map; concept/explanation; worked example; practice; summary; homework or extension | Teacher modelling, guided questioning, then independent or paired application | Cite the applicable curriculum/source where supplied; include a worked example and practice with feedback or answers | Return to the learning objectives, summarize the knowledge structure, and assign a traceable practice or extension task. |
| `class-meeting` | Situation or question → story/experience → discussion → collective activity → personal commitment → value elevation | Cover; situation prompt; story or case; discussion; activity; commitment; summary/closing | Whole-class prompt, small-group discussion, sharing, and a visible individual or group commitment | Use age-appropriate stories, scenarios, class data, or reflection prompts; include an action-based activity rather than a knowledge-only quiz | Turn the shared value into a concrete class or personal commitment, name the next action, and close with an affirming collective message. |
| `mental-health` | Psychological safety → experience/notice → understand the pattern → practise a strategy → seek support when needed | Cover; safety agreement; experience activity; cognitive explanation; strategy practice; support/boundary; summary/closing | Opt-in, non-disclosing participation; private reflection; low-pressure pair or group practice; never require personal disclosure | Use validated, non-sensational examples and guided exercises; distinguish education from diagnosis; include help-seeking and escalation boundaries | Reinforce a usable self-care strategy, normalize seeking help, state available support and emergency boundaries, and end without forcing disclosure or a promise of recovery. |
| `parent-meeting` | Parent pain points → stage changes → shared understanding → family strategies → home-school coordination → action list | Cover; parent pain-points scan; stage-change explanation; family-strategy pages; home-school coordination; action list; Q&A/closing | Anonymous poll or reflection, scenario discussion, parent choice points, and a home-school follow-up channel | Use approved student/class evidence, developmental information, and family scenarios; provide strategies that parents can try and an action checklist | Recap parent pain points, stage changes, family strategies, home-school coordination, and the action list; name the first follow-up action and contact path. |
| `open-class` | High-value question → inquiry or task → student evidence → feedback and process evaluation → synthesis → public-ready close | Cover; learning objectives/success criteria; engaging task; inquiry or collaborative activity; student evidence/showcase; formative assessment; summary/closing | Visible student thinking, structured collaboration, timely feedback, and planned student presentation or showcase | Include authentic task materials, anticipated responses/misconceptions, observable evidence, and formative assessment criteria | Have learners synthesize the answer with evidence, make the learning visible to observers, revisit success criteria, and end with a concise transfer question or extension. |

## Premium page-content blueprint

For every Premium page, create one record using this exact schema. `role` must use one of the listed values. The sum of `estimated_minutes` across all page records must fit the confirmed duration; revise the internal blueprint if it does not fit.

```yaml
page: 1
role: cover|section|concept|case|activity|practice|summary|closing
teaching_objective: "Why this page exists"
title: "Visible title"
core_message: "One central idea"
body: ["Approved on-slide points"]
teacher_action: "What the teacher does"
learner_or_parent_action: "What the audience does"
evidence_or_example: "Case, source, exercise, or none"
estimated_minutes: 2
```

The selected mode shapes the page sequence and actions, but does not permit omitted records, invented duration, or a change to the confirmed page order, goals, core content, activities/cases, or timing. The complete blueprint is an internal content checkpoint and source contract for the final deliverables; it is not a separate user-facing file or an extra section in the fixed page-outline format.

The YAML record above is an internal planning structure only. The user-facing PPT page outline must be rendered exactly as:

```text
第X页
页面标题：
页面文字：
```

Do not expose `role`, `teaching_objective`, `teacher_action`, timing fields, or any other internal fields in the page-outline output.
