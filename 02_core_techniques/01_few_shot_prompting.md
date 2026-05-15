# Few-Shot Prompting

**Topic:** Core Techniques  
**Technique:** Few-Shot Prompting — teaching by example inside the prompt  
**Platform:** Google AI Studio ([aistudio.google.com](https://aistudio.google.com))  
**Source:** Adapted from [Brown et al. 2020 "Language Models are Few-Shot Learners"](https://arxiv.org/abs/2005.14165)  

---

## Theory

**Few-shot prompting** provides the model with a small number of input-output demonstrations — called "shots" — before presenting the actual task. The model learns the pattern from the examples and applies it to the new input.

### Why It Works

LLMs are trained on patterns in data. When you show examples inside a prompt, you are performing **in-context learning**: the model's attention mechanism weights the example patterns heavily when generating the next response. Unlike fine-tuning, this requires no model updates — the learning happens entirely within the context window.

### Shot Count Guidelines

| Shots | When to Use | Tradeoff |
|-------|-------------|---------|
| 0 (zero-shot) | Simple, well-defined tasks | No token cost; may need precision in instruction |
| 1 (one-shot) | When format is complex | Reduces ambiguity with minimal tokens |
| 3–5 (few-shot) | Classification, extraction, style matching | High control; costs more tokens |
| 10+ (many-shot) | Highly specific domain tasks | Best accuracy; significant context usage |

**Practical rule:** Start with 3 examples. Add more only if quality is insufficient.

---

## Example 1 — Sentiment Classification (The Canonical Example)

From Brown et al. (2020), the paper that introduced "few-shot" terminology.

### Zero-Shot (Topic 1 Baseline)

```
Classify the sentiment of: "The movie was surprisingly engaging."
Sentiment:
```

Output varies in format — "Positive", "The sentiment is positive", "Mixed/Positive"

---

### Few-Shot (3 Shots)

```
Classify the sentiment of each review as Positive, Negative, or Neutral.
Output only the label.

Review: This phone has excellent battery life.
Sentiment: Positive

Review: The delivery took three weeks and the package was damaged.
Sentiment: Negative

Review: The product works as described, nothing exceptional.
Sentiment: Neutral

Review: The movie was surprisingly engaging.
Sentiment:
```

**Expected output:** `Positive`

The format is now locked by example. The model cannot output "The sentiment is positive" because none of your examples did that.

---

## Example 2 — Custom Classification Labels

Few-shot is essential when your label vocabulary is non-standard.

### The Problem

You are building a customer support triage system with custom categories. Zero-shot won't reliably use your exact labels.

### Few-Shot Solution

```
Classify the following customer support ticket into one of these categories:
BILLING, TECHNICAL, ACCOUNT, FEATURE_REQUEST, COMPLAINT

Use the format: Category: [LABEL]

Ticket: I was charged twice for my subscription this month.
Category: BILLING

Ticket: The app crashes every time I try to upload a file larger than 10MB.
Category: TECHNICAL

Ticket: I would love to see dark mode added to the mobile app.
Category: FEATURE_REQUEST

Ticket: I cannot log in — my email says it's not recognized despite being registered.
Category: ACCOUNT

Ticket: Your support team kept me waiting 45 minutes and never resolved my issue.
Category:
```

**Expected:** `COMPLAINT`

Without the examples, the model might output "Customer Service Issue" or "Support Quality" — neither of which is in your label set.

---

## Example 3 — Named Entity Extraction

Few-shot defines the exact extraction schema.

```
Extract named entities from each sentence. Format:
Person: [name] | Organization: [org] | Location: [place]
If a type is absent, write None.

Sentence: Tim Cook announced Apple's new product line at WWDC in San Francisco.
Person: Tim Cook | Organization: Apple | Location: San Francisco

Sentence: Sundar Pichai spoke at Google I/O held in Mountain View.
Person: Sundar Pichai | Organization: Google | Location: Mountain View

Sentence: The Reserve Bank of India raised interest rates last Tuesday.
Person: None | Organization: Reserve Bank of India | Location: None

Sentence: Narendra Modi inaugurated the new AIIMS hospital in Rajkot last week.
Person:
```

**Expected:** `Person: Narendra Modi | Organization: AIIMS | Location: Rajkot`

---

## Example 4 — Style Transfer

Few-shot teaches tone and voice, not just structure.

```
Rewrite each formal sentence in a casual, friendly tone suitable for a startup blog.

Formal: "We regret to inform you that the requested feature is not currently available."
Casual: "Totally hear you — that feature isn't live yet, but it's on our radar!"

Formal: "Your subscription has been successfully renewed for another billing cycle."
Casual: "You're all set! We've renewed your subscription — thanks for sticking with us."

Formal: "The application has encountered an unexpected error and must be terminated."
Casual:
```

**Expected:** Something like: "Oops! Something went sideways — the app hit a snag and had to close. Don't worry, we're on it!"

---

## Shot Selection Best Practices

| Principle | Description |
|-----------|-------------|
| **Diversity** | Chose examples that cover different cases (positive, negative, edge cases) |
| **Recency bias** | The last example before the task has the highest influence — choose it carefully |
| **Format consistency** | All examples must follow the same exact format |
| **No contradictions** | If two examples imply different rules, the model will average them (poorly) |
| **Domain match** | Examples should come from the same domain as the test input |

---

## Common Mistakes

| Mistake | Effect | Fix |
|---------|--------|-----|
| All examples from one class | Model biases toward that class | Include balanced examples |
| Inconsistent formatting | Model switches format mid-output | Verify every example has identical format |
| Examples too similar | Model doesn't generalize | Use diverse examples |
| Too many examples | Context window fills up | Use 3–5 unless accuracy demands more |

---

*Previous: [Topic 1 — Foundations ←](../01_foundations/README.md)*  
*Next: [Chain-of-Thought →](./02_chain_of_thought.md)*  
*Back to [Topic 2 README](./README.md)*
