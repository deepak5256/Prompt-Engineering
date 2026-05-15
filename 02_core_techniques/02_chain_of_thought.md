# Chain-of-Thought Prompting

**Topic:** Core Techniques  
**Technique:** Chain-of-Thought (CoT) — eliciting step-by-step reasoning  
**Platform:** Google AI Studio ([aistudio.google.com](https://aistudio.google.com))  
**Source:** [Wei et al. 2022 — "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"](https://arxiv.org/abs/2201.11903)  

---

## Theory

**Chain-of-Thought (CoT) prompting** encourages the model to produce intermediate reasoning steps before arriving at a final answer. This dramatically improves performance on tasks requiring:
- Multi-step arithmetic
- Logical deduction
- Commonsense reasoning
- Code debugging

### Why CoT Works

Without CoT, the model must compress all reasoning into selecting a single next token (the answer). With CoT, the model's own intermediate steps become part of the context — each step conditions the next. This gives the model more "working memory" by using the context window as scratchpad.

```
Without CoT:  "What is 37 × 48?" → Model predicts: 1776 (possibly wrong)
With CoT:     "37 × 48 = ?
               Let me compute: 37 × 40 = 1480, 37 × 8 = 296
               1480 + 296 = 1776" → Model gets it right by doing the arithmetic
```

### Two Flavors of CoT

| Type | Trigger | When to Use |
|------|---------|-------------|
| **Zero-Shot CoT** | Add "Let's think step by step" | Quick, works on most reasoning tasks |
| **Few-Shot CoT** | Provide examples with reasoning chains | Complex tasks, custom reasoning format |

---

## Example 1 — Arithmetic Reasoning

### Without CoT (Direct Answer)

```
Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 balls. How many tennis balls does he have now?
```

**Model output (Temperature 0):** `11`

This is correct — but on harder problems, the model frequently fails by jumping directly to an answer without computing.

---

### With Zero-Shot CoT

```
Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 balls. How many tennis balls does he have now?

Let's think step by step.
```

**Model output:**
```
Roger starts with 5 tennis balls.
He buys 2 cans, each with 3 balls → 2 × 3 = 6 additional balls.
Total: 5 + 6 = 11 tennis balls.
Answer: 11
```

Same answer, but now the reasoning is visible and verifiable. On harder problems (multi-digit arithmetic, word problems), Zero-Shot CoT reduces errors by 30–50%.

---

## Example 2 — Multi-Step Word Problem

This example shows where CoT makes the critical difference.

### Without CoT

```
A train travels from City A to City B at 60 km/h and returns at 40 km/h. The total distance for both trips is 240 km. What is the average speed for the entire journey?
```

**Common wrong answer:** `50 km/h` (the arithmetic mean — a common mistake)

---

### With Zero-Shot CoT

```
A train travels from City A to City B at 60 km/h and returns at 40 km/h. The total distance for both trips is 240 km. What is the average speed for the entire journey?

Let's think step by step and show all calculations.
```

**Expected correct reasoning:**
```
Step 1: Total distance = 240 km (both ways combined), so one way = 120 km.

Step 2: Time for A→B: 120 km ÷ 60 km/h = 2 hours
        Time for B→A: 120 km ÷ 40 km/h = 3 hours
        Total time = 5 hours

Step 3: Average speed = Total distance ÷ Total time
        = 240 km ÷ 5 hours = 48 km/h

Answer: 48 km/h
```

The correct answer is **48**, not 50. CoT prevented the model from averaging the speeds directly (a well-known trap in average speed problems).

---

## Example 3 — Few-Shot CoT (Custom Reasoning Format)

Providing CoT examples lets you control the reasoning structure precisely.

### Few-Shot CoT for Software Debugging

```
Debug each issue using this reasoning format:
Observation: [What the symptom is]
Hypothesis: [What might cause this]
Test: [How to verify]
Fix: [The solution]

---
Issue: "My Python script prints nothing when I run it."
Observation: No output appears despite the script having print statements.
Hypothesis: The print statements may be inside a function that is never called, or there is an indentation error silently skipping the block.
Test: Add print("Script started") as the very first line (no indentation) to confirm execution reaches the file.
Fix: Check that all function calls are present outside function definitions, and verify indentation.

---
Issue: "My Flask app runs locally but returns 500 errors in production."
Observation: The app works perfectly on localhost but crashes on the server.
Hypothesis: The production environment is missing a required environment variable or dependency that exists on the local machine.
Test: Check the production logs for the specific exception message. Run pip freeze locally vs the server to compare installed packages.
Fix: Add all required environment variables to the production config and ensure requirements.txt is complete.

---
Issue: "My SQL query returns duplicate rows."
Observation:
```

**Expected output:** The model follows the established Observation → Hypothesis → Test → Fix format, not just giving a direct answer.

---

## Example 4 — Logical Deduction with CoT

### Without CoT

```
All mammals are warm-blooded. All whales are mammals. Are whales warm-blooded?
```

Output: `Yes` — correct but trivial. Try this harder one:

```
All members of the Chess Club are members of the Science Club. 
Some members of the Science Club are members of the Drama Club.
Is it necessarily true that some Chess Club members are in the Drama Club?
```

Without CoT, models frequently (and incorrectly) output `Yes`.

---

### With CoT

```
All members of the Chess Club are members of the Science Club. 
Some members of the Science Club are members of the Drama Club.
Is it necessarily true that some Chess Club members are in the Drama Club?

Work through this logically. Consider a scenario that could disprove the claim.
```

**Expected reasoning:**
```
Let's construct a counterexample:
- Science Club has members: {A, B, C, D, E}
- Chess Club is a subset: {A, B} (both are in Science Club)
- Drama Club members: {C, D} (members of Science Club, but NOT Chess Club members)

In this scenario: All Chess Club rules are satisfied (A, B are in Science Club).
Some Science Club members (C, D) are in Drama Club.
But NO Chess Club members (A, B) are in Drama Club.

Therefore: It is NOT necessarily true.
Answer: No — the statement does not necessarily follow.
```

---

## CoT Limitations

| Limitation | Description | Mitigation |
|------------|-------------|-----------|
| **Hallucinated reasoning** | Model can produce plausible-sounding but wrong reasoning chains | Use Self-Consistency (see next topic) |
| **Token cost** | CoT responses are much longer | Only use when accuracy > speed |
| **Format sensitivity** | Small changes to the trigger phrase change behavior | Test "Let's think step by step" vs "Think carefully" |
| **Arithmetic errors** | Models still make arithmetic mistakes in long chains | Use code execution tools for arithmetic |

---

## Trigger Phrases Compared

| Phrase | Effect |
|--------|--------|
| `Let's think step by step.` | Standard CoT trigger — widely tested |
| `Work through this problem carefully.` | Good alternative |
| `Show all reasoning before giving the final answer.` | Explicitly requires full chain |
| `Think out loud.` | More conversational; slightly less structured |
| `Do not give the answer yet. First, explain your reasoning.` | Forces reasoning before answer |

---

*Previous: [Few-Shot Prompting ←](./01_few_shot_prompting.md)*  
*Next: [Role & System Prompts →](./03_role_and_system_prompts.md)*  
*Back to [Topic 2 README](./README.md)*
