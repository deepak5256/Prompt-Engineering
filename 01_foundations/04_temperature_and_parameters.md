# Temperature and Sampling Parameters

**Topic:** Foundations of Prompt Engineering  
**Technique:** Understanding LLM generation parameters that control randomness and diversity  
**Platform:** Google AI Studio ([aistudio.google.com](https://aistudio.google.com))  

---

## Theory: How LLMs Generate Text

LLMs generate text **token by token**. At each step, the model produces a **probability distribution** over all possible next tokens. Parameters like Temperature and Top-P control how the model **samples** from this distribution.

```
Example: After "The capital of France is "
Token         Probability
"Paris"       0.97
"Lyon"        0.01
"London"      0.009
"a"           0.005
...
```

At Temperature=0: Model always picks "Paris" (highest probability)  
At Temperature=1: Model samples probabilistically, "Paris" almost always but occasionally something else  
At Temperature=2: Model takes wild risks — might output "a" or even "London"  

---

## Parameter Reference

| Parameter | Range | Effect | Best Setting For |
|-----------|-------|--------|-----------------|
| **Temperature** | 0.0 – 2.0 | Controls randomness of sampling | See table below |
| **Top-P (Nucleus)** | 0.0 – 1.0 | Limits sampling to top P% probability mass | Set to 0.95 and adjust temperature |
| **Top-K** | 1 – ∞ | Limits sampling to top K tokens | Rarely needs adjustment (default ~40) |
| **Max Output Tokens** | 1 – context limit | Hard cap on response length | Control costs and verbosity |
| **Stop Sequences** | String(s) | Model stops generating when it hits this | Useful in structured generation |

### Temperature Quick Reference

| Temperature | Behavior | Use This For |
|-------------|----------|-------------|
| **0.0** | Fully deterministic — same output every run | Code, classification, data extraction |
| **0.1 – 0.3** | Very consistent, minimal variation | Technical writing, Q&A, summarization |
| **0.5 – 0.7** | Balanced — consistent but natural-sounding | Business emails, reports, explanations |
| **0.8 – 1.0** | Creative variation — different outputs each run | Marketing copy, brainstorming |
| **1.2 – 2.0** | High creativity / occasional incoherence | Experimental, poetry, creative fiction |

---

## Example 1 — Temperature Effect on Code

### Low Temperature (Use 0.0)

```
[Temperature: 0.0]

Write a Python function that returns True if a number is prime, False otherwise.
Include the function signature and a docstring.
```

Run this 5 times at Temperature 0. **The output should be identical every time.** This is critical for code generation — you want predictable, reproducible outputs.

---

### High Temperature (Use 1.2)

```
[Temperature: 1.2]

Write a Python function that returns True if a number is prime, False otherwise.
Include the function signature and a docstring.
```

Run this 5 times at Temperature 1.2. You will observe:
- Different variable names
- Different algorithm approaches (trial division vs sieve)
- Different docstring styles
- Occasionally: bugs, unusual constructs, or non-standard patterns

**Lesson:** For code generation, always use low temperature (0.0–0.3).

---

## Example 2 — Temperature Effect on Creative Tasks

### Low Temperature (0.0) — Creative Writing

```
[Temperature: 0.0]

Write the opening sentence of a science fiction novel set on Mars.
```

Run 5 times. You will get the **same sentence** every time — predictable but potentially flat.

---

### High Temperature (0.9) — Creative Writing

```
[Temperature: 0.9]

Write the opening sentence of a science fiction novel set on Mars.
```

Run 5 times. You will get **5 different sentences**, each with a different narrative angle, tone, and imagery. This diversity is exactly what you want for creative tasks — you pick the best one.

---

## Example 3 — Top-P (Nucleus Sampling)

Top-P sampling restricts the model to the smallest set of tokens whose combined probability exceeds P.

```
[Top-P: 0.1]
[Temperature: 1.0]

Complete this sentence: "The best programming language for beginners is "
```

At Top-P = 0.1, only the top few most-likely tokens are eligible. Output: almost always "Python".

```
[Top-P: 0.9]
[Temperature: 1.0]

Complete this sentence: "The best programming language for beginners is "
```

At Top-P = 0.9, many tokens are eligible. Outputs might include: Python, JavaScript, Scratch, Basic, Ruby — each run may differ.

**Rule of thumb:** Set Top-P = 0.95 and control diversity through Temperature. They interact multiplicatively.

---

## Example 4 — Stop Sequences

Stop sequences make the model halt when it produces a specific string. This is critical for structured generation.

```
[Stop sequence: "---"]
[Temperature: 0.0]

Generate a product description for noise-cancelling headphones.
End with "---"

Product Description:
```

The model will stop generating as soon as it produces "---". This allows you to:
- Generate exactly one section of a document
- Parse the output before the stop sequence
- Chain multiple prompts, each stopped at a delimiter

**Practical application:**
```
Generate a JSON object for a book. Stop at "---".
Use this format:
{"title": "...", "author": "...", "genre": "..."}
---
```

---

## Experiment: Parameter Sensitivity Table

Conduct this experiment in Google AI Studio:

**Prompt (keep it constant):**
```
Describe the risks of artificial intelligence in exactly 3 sentences.
```

**Run it 3 times at each temperature setting:**

| Temperature | Run 1 (length) | Run 2 (length) | Run 3 (length) | Output Consistency |
|-------------|---------------|---------------|---------------|-------------------|
| 0.0 | | | | |
| 0.5 | | | | |
| 1.0 | | | | |
| 1.5 | | | | |

Count the sentences in each output. At high temperatures, the model may violate the "3 sentences" constraint.

**Observation:** Higher temperature increases the chance of the model ignoring format constraints.

---

## Practical Decision Framework

```
Is my task...

├── Requiring consistent, reproducible output?
│   → Temperature: 0.0
│   → Use case: Code, classification, data extraction
│
├── Technical but needing natural language variation?
│   → Temperature: 0.2–0.4
│   → Use case: Documentation, Q&A, summarization
│
├── Professional communication?
│   → Temperature: 0.5–0.7
│   → Use case: Emails, reports, explanations
│
├── Creative with controlled variation?
│   → Temperature: 0.8–1.0
│   → Use case: Marketing, ideation, storytelling
│
└── Highly experimental / brainstorming?
    → Temperature: 1.0–1.5
    → Use case: Concept generation, poetry, fiction
```

---

## Key Takeaways

1. **Temperature is the most important parameter** — master it first
2. **Low temperature ≠ low quality** — it means consistent, reliable quality
3. **High temperature ≠ creativity** — it means variance, which is useful only for creative tasks
4. **Top-P and Temperature interact** — don't set both to extreme values simultaneously
5. **Stop sequences are underused** — they're essential for structured generation pipelines

---

*Previous: [Output Format Control ←](./03_output_format_control.md)*  
*Next Topic: [Core Techniques →](../02_core_techniques/README.md)*  
*Back to [Topic 1 README](./README.md)*
