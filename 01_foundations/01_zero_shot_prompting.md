# Zero-Shot Prompting

**Topic:** Foundations of Prompt Engineering  
**Technique:** Zero-Shot Prompting — instructing a model without providing any examples  
**Platform:** Google AI Studio ([aistudio.google.com](https://aistudio.google.com))  
**Source:** Adapted from [promptingguide.ai/techniques/zeroshot](https://www.promptingguide.ai/techniques/zeroshot)  

---

## Theory

**Zero-shot prompting** means giving an LLM a task with no examples of how to solve it. The model relies entirely on patterns learned during pre-training on vast text corpora. This works because modern LLMs are instruction-tuned — they have seen millions of instruction-response pairs and can generalize to new instructions.

### When Zero-Shot Works Best
- The task type is well-defined (classification, summarization, translation, Q&A)
- The instruction is explicit and complete
- Output format is clearly specified
- The domain is within the model's training distribution

### When Zero-Shot Fails
- Vague or ambiguous instructions
- Novel task formats the model has never seen
- Highly specialized domains (medical codes, legal citations, niche APIs)
- Tasks requiring multi-step arithmetic or logical deduction

---

## Example 1 — Sentiment Classification

This is the canonical zero-shot example from the DAIR.AI Prompt Engineering Guide.

### Version A — Vague Prompt

```
The food at the restaurant was okay. Sentiment:
```

**What typically happens:** The model outputs `Neutral`, but might also output:
- "The sentiment is neutral"
- "Neutral tone"  
- "Mixed/Neutral"

Each run may produce a different format. This is unusable for automated processing.

---

### Version B — Structured Zero-Shot

```
Classify the sentiment of the following text. 
Choose exactly one label from: Positive, Negative, Neutral.
Output only the label. Do not explain or add any other text.

Text: The food at the restaurant was okay.
Sentiment:
```

**Expected output:** `Neutral`

Run this five times. The output will be consistent every time because:
- The label space is defined (Positive, Negative, Neutral)
- The output format is specified (label only)
- The instruction is unambiguous

### Why This Matters in Practice

In a real sentiment analysis pipeline, you might process 10,000 reviews. Version A produces inconsistent formats requiring complex parsing. Version B produces clean, predictable output directly usable in a database or dashboard.

---

## Example 2 — Text Summarization

### Version A — Minimal

```
Summarize this:
Antibiotics are a type of medication used to treat bacterial infections. They work by killing the bacteria or preventing them from reproducing, allowing the body's immune system to fight off the infection. Antibiotics are usually taken orally in the form of pills, capsules, or liquid solutions, or sometimes administered intravenously. They are not effective against viral infections, and using them inappropriately can lead to antibiotic resistance.
```

**Typical output:** A paragraph nearly as long as the input, loosely paraphrasing content. No control over length, audience, or structure.

---

### Version B — Controlled Summarization

```
Summarize the following text in exactly one sentence suitable for a first-year medical student.
The sentence must mention: the purpose of antibiotics, how they work, and their key limitation.

Text:
Antibiotics are a type of medication used to treat bacterial infections. They work by killing the bacteria or preventing them from reproducing, allowing the body's immune system to fight off the infection. Antibiotics are usually taken orally in the form of pills, capsules, or liquid solutions, or sometimes administered intravenously. They are not effective against viral infections, and using them inappropriately can lead to antibiotic resistance.

One-sentence summary:
```

**Expected output:** "Antibiotics are medications that treat bacterial infections by killing or inhibiting bacterial reproduction, but they are ineffective against viral infections and must be used carefully to avoid antibiotic resistance."

---

## Example 3 — Code Generation (Zero-Shot)

### Version A — Ambiguous

```
Write a function to check duplicates.
```

**Problem:** What language? What should it return? What about edge cases? The model will make assumptions, which may not match what you need.

---

### Version B — Precise

```
Write a Python function that takes a list as input and returns a new list containing only the elements that appear more than once in the input. Each duplicate element should appear only once in the result. Include:
- A docstring explaining the function
- Type hints
- One example usage in a comment

Function name: find_duplicates
```

**Expected output:**
```python
def find_duplicates(lst: list) -> list:
    """
    Returns a list of elements that appear more than once in the input list.
    Each duplicate element appears only once in the result.
    """
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)

# Example: find_duplicates([1, 2, 2, 3, 3, 3]) → [2, 3]
```

---

## The Completion vs Instruction Trap

Understanding this distinction is fundamental to all of prompt engineering.

### Completion Mode (avoid this)

```
The sky is
```

The model predicts the statistically most likely next token. Output might be "blue", "the limit", or the opening of a poem. This is **autocomplete**, not instruction-following.

### Instruction Mode (always use this)

```
Complete the following sentence with a scientifically accurate statement about atmospheric optics:

The sky is
```

**Expected:** "...blue during the day due to Rayleigh scattering, where shorter blue wavelengths scatter more than longer red wavelengths."

Always frame your input as an explicit instruction, not an open completion.

---

## Observation Table

Run both versions of each example and record your results:

| Example | Version A Format | Version B Format | Consistency (A) | Consistency (B) |
|---------|-----------------|-----------------|-----------------|-----------------|
| Sentiment classification | | | | |
| Text summarization | | | | |
| Code generation | | | | |

Use this table for your Topic 1 activity submission.

---

## Key Principles

| Principle | Bad Practice | Good Practice |
|-----------|-------------|---------------|
| Define the task | "Tell me about Python" | "List 5 features of Python vs Java in a table" |
| Specify output format | Leave open-ended | "Respond with only the label" |
| Define constraints | Assume the model knows | "In exactly one sentence" / "3 bullet points" |
| Name the audience | Assume general | "For a first-year medical student" |
| Set label space | For classification tasks | "Choose from: Positive, Negative, Neutral" |

---

*Next: [Prompt Anatomy →](./02_prompt_anatomy.md)*  
*Back to [Topic 1 README](./README.md)*
