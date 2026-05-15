# Week 3 — Meta-Prompting

**Platform:** Google AI Studio (aistudio.google.com)  
**Technique:** Meta-prompting — using the model to generate or improve prompts  
**Source:** Based on [promptingguide.ai/techniques/meta-prompting](https://www.promptingguide.ai/techniques/meta-prompting)

Meta-prompting uses an LLM to generate, evaluate, or improve prompts for other tasks. Instead of writing a prompt manually, you describe what you want the prompt to accomplish and let the model construct an optimized prompt — which you then use as the actual input for your task. This is particularly useful when you know the outcome you want but are not sure how to phrase the prompt to get there.

---

## Example 1 — Prompt Generation from Task Description

**Version A (Write the prompt yourself — common result)**

You want to extract key information from academic paper abstracts. You write:

```
Extract the main findings from this paper abstract.
```

This works, but the output format is inconsistent. Some runs produce bullet points, some produce paragraphs, and the definition of "main findings" is interpreted differently each time.

---

**Version B — Ask the model to write the prompt for you**

First, run this meta-prompt on Google AI Studio:

```
You are an expert prompt engineer. I need a prompt that will be used to extract structured information from academic paper abstracts in computer science.

The prompt must:
- Instruct the model to extract: research problem, proposed method, key results, and limitations
- Specify that the output must be in a consistent JSON format
- Include clear instructions for handling abstracts where a field cannot be determined
- Be suitable for automated batch processing (no conversational language)

Write only the prompt. Do not include any explanation or commentary. The prompt should start with the instruction, not with "Here is a prompt for..."
```

The model will generate a well-structured extraction prompt. Copy that generated prompt and use it as your actual extraction prompt on real paper abstracts.

**Why this works better:** The model has seen thousands of extraction prompts and knows which patterns produce consistent, parseable output. It generates a better-structured prompt than most users write manually.

---

## Example 2 — Prompt Improvement (Before/After)

**Step 1 — Submit your draft prompt for improvement**

You have a prompt that is giving mediocre results. Ask the model to improve it:

```
The following prompt is producing inconsistent results. Improve it so that outputs are more reliable, more specific, and formatted consistently.

Current prompt:
"Explain machine learning to a beginner."

Problems with the current prompt:
- Output length is unpredictable (50 words to 500 words)
- Sometimes uses technical jargon despite asking for beginner level
- Format varies — sometimes paragraphs, sometimes bullet points

Write an improved version of this prompt. Then briefly explain (2 sentences) why your version addresses each problem.
```

Expected output: An improved prompt with explicit length constraints, a defined audience specification, and a required output format — followed by a brief explanation of each change.

**Step 2 — Test both prompts**

Run the original prompt and the model-generated improved prompt on Google AI Studio. Compare the consistency of outputs across five runs.

---

## Example 3 — Evaluating a Prompt Before Using It

Before using a new prompt in a system, you can ask the model to predict its failure modes.

```
Evaluate the following prompt for potential weaknesses. For each weakness you identify:
- Describe the failure mode
- Provide an example of an input that would trigger that failure
- Suggest a specific fix

Prompt to evaluate:
"Summarize the following customer complaint and classify it as: Billing Issue, Technical Issue, or Shipping Issue."
```

Expected output: The model identifies that the prompt does not handle complaints that span multiple categories, does not specify output format, and does not handle complaints in languages other than English. Each weakness includes an example and a specific fix.

This technique — using the model as a prompt reviewer before deployment — reduces the number of testing iterations required in production.

---

## Practical Use Cases for Meta-Prompting

| Use Case | What You Provide | What the Model Returns |
|----------|-----------------|----------------------|
| Prompt generation | Task description and requirements | A ready-to-use prompt |
| Prompt improvement | Your draft prompt and its problems | An improved version with explanations |
| Failure mode analysis | Your prompt | Predicted edge cases and fixes |
| Prompt comparison | Two prompts for the same task | Analysis of tradeoffs and recommendation |
| Constraint verification | Your prompt | Confirmation that all your constraints are correctly expressed |

---

## Limitation

Meta-prompting works well when the model has sufficient knowledge of the task domain to generate a good prompt. For highly specialized domains (e.g., a specific company's internal data format or a proprietary API), the model-generated prompt will still need human review and domain-specific adjustments.
