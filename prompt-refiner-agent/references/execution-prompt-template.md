# Execution Prompt Template

Use only the sections applicable to the task and keep each section concise.

```text
[EXECUTION_PROMPT_DO_NOT_REFINE]

This prompt is already refined. Do not run prompt-refiner-agent again.

Original user language: <language>
Final answer: Respond in the original user language.

Objective:
<outcome>

Context and assumptions:
<only necessary context and assumptions>

Scope:
- Include: <required work>
- Exclude: <explicit exclusions, if any>

Routing:
<matching skill, tools, or normal Codex behavior>

Execution rules:
- Use the least code and smallest change that fully meet the objective.
- Keep progress and final responses brief unless detail is requested.
<task-specific safety or behavior rules>

Deliverables:
<outputs>

Validation:
<proportionate checks>

Final response:
<changed, validated, remaining risk>
```
