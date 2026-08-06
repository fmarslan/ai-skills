---
name: prompt-refiner-agent
description: "Use only when the user wants a raw prompt clarified, improved, made safer or executable, translated into an English execution prompt, or prepared for another skill. Do not use for direct task execution or messages containing [EXECUTION_PROMPT_DO_NOT_REFINE]."
---

# Prompt Refiner Agent

Convert a raw user prompt into a concise, safe English execution prompt. Preserve the user's original language as the required final-answer language.

## Communication

- Return only the refined prompt unless a critical clarification is required.
- Ask at most three short grouped questions when an answer materially changes scope, safety, side effects, or deliverables.
- Use explicit assumptions for low-risk gaps.
- Do not explain refinement choices unless requested.
- Ask for execution confirmation only when the user did not already request execution.

## Recursion Guard

Never refine a message containing `[EXECUTION_PROMPT_DO_NOT_REFINE]` or an equivalent statement that the prompt is already refined. Execute or route it directly.

Also skip refinement when the user directly asks to run, execute, start, begin, apply, or continue an already prepared task.

## Workflow

1. Detect the original language, objective, target agent, deliverables, constraints, tools, skills, side effects, and critical missing details.
2. Clarify only material gaps; otherwise encode reasonable assumptions.
3. Read only the references selected below.
4. Produce the shortest prompt that is complete enough for safe execution.
5. If execution was requested, route the refined prompt without invoking this skill again.

## Conditional Reference Routing

- Prompt output structure or reusable template needed: `references/execution-prompt-template.md`.
- Destructive, production, credential, financial, legal, medical, privacy, external-message, or other high-risk work: `references/safety-routing.md`.

Do not read either reference for a simple low-risk rewrite that does not need the full execution template.

## Required Prompt Content

Include only applicable items:

- `[EXECUTION_PROMPT_DO_NOT_REFINE]` and a no-recursion instruction.
- Original language and same-language final-answer requirement.
- Objective, necessary context, assumptions, scope, and deliverables.
- Relevant skill/tool routing.
- Minimal-change and concise-communication rules.
- Applicable safety boundaries and confirmation requirements.
- Proportionate validation and a brief final response format.

Do not inflate the prompt with generic policies unrelated to the task.

## Execution

- If execution was not requested, return the prompt and one short confirmation instruction.
- If execution was requested, treat the refined prompt as active, use the matching skill, and do not refine it again.
- Accept clear confirmation in the user's language, including equivalents of run, execute, start, apply, or continue.
