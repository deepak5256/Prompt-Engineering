# Topic 2: Core Techniques

**Course:** Prompt Engineering: Principles, Techniques & Applications  
**Institution:** Chanakya University — School of Engineering  
**Instructor:** Mr. Deepak B  

---

## Learning Objectives

By the end of this topic, you will be able to:
- Apply few-shot prompting to guide model behavior with examples
- Use Chain-of-Thought to make the model reason step by step
- Write effective role prompts and system instructions
- Understand self-consistency for more reliable reasoning

---

## Topics Covered

| File | Concept | Difficulty |
|------|---------|------------|
| [01_few_shot_prompting.md](./01_few_shot_prompting.md) | Few-Shot Prompting | Beginner–Intermediate |
| [02_chain_of_thought.md](./02_chain_of_thought.md) | Chain-of-Thought Reasoning | Intermediate |
| [03_role_and_system_prompts.md](./03_role_and_system_prompts.md) | Role & System Prompts | Intermediate |
| [04_self_consistency.md](./04_self_consistency.md) | Self-Consistency Decoding | Advanced |

---

## Conceptual Overview

### The Progression from Zero-Shot to Few-Shot

In Topic 1, you learned that well-structured zero-shot prompts can produce reliable output. But there's a ceiling: the model can only infer your intent from the words in your instruction. Sometimes you need to **demonstrate** what you want rather than describe it.

This is the insight behind **few-shot prompting**: providing input-output examples inside the prompt itself. The model uses those examples as a live demonstration and generalizes the pattern to new inputs.

```
Zero-shot:  "Classify sentiment"         → Model guesses format
Few-shot:   "Classify sentiment like this:
             Input: Great product! → Positive
             Input: Terrible quality → Negative
             Input: [YOUR TEXT] →"      → Model follows the pattern
```

### Why Chain-of-Thought Changes Everything

Chain-of-Thought (CoT) prompting was formalized by Wei et al. (2022) and demonstrated that adding the phrase "Let's think step by step" dramatically improved LLM performance on math and reasoning tasks. The mechanism is clear: the model's generation of intermediate steps uses those steps as context for the final answer, dramatically reducing errors.

### Role Prompts: The Power of Context-Setting

When you tell a model "You are a senior cybersecurity engineer," you activate patterns associated with that role — technical vocabulary, defensive thinking, awareness of edge cases. This isn't just flavor — it genuinely shifts the distribution of probable next tokens toward the domain knowledge you need.

---

*Back to [main repository](../README.md)*
