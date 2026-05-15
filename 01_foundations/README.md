# Topic 1: Foundations of Prompt Engineering

## Learning Objectives

By the end of this topic, you will be able to:
- Explain what a prompt is and why its design affects model output
- Identify the structural components of a well-formed prompt
- Apply zero-shot prompting with controlled output formatting
- Understand how temperature and sampling parameters shape responses

---

## Topics Covered

| File | Concept | Difficulty |
|------|---------|------------|
| [01_zero_shot_prompting.md](./01_zero_shot_prompting.md) | Zero-Shot Prompting | Beginner |
| [02_prompt_anatomy.md](./02_prompt_anatomy.md) | Prompt Anatomy & Structure | Beginner |
| [03_output_format_control.md](./03_output_format_control.md) | Output Format Control | Beginner–Intermediate |
| [04_temperature_and_parameters.md](./04_temperature_and_parameters.md) | Temperature & Sampling Parameters | Intermediate |

---

## Conceptual Overview

### What is a Prompt?

A **prompt** is any input you provide to a language model (LLM) that instructs it on what to generate. The model's output is entirely conditioned on what you write. This makes prompt design the primary lever for controlling AI behavior.

> "Prompts are the programming language of large language models." — Andrej Karpathy

### The Instruction-Following Paradigm

Modern LLMs (GPT-4, Gemini, Claude, Llama) are trained using a technique called **Reinforcement Learning from Human Feedback (RLHF)**. This training makes them highly responsive to:
- Explicit instructions ("Classify the sentiment as...")
- Role assignments ("You are a senior software engineer...")
- Output constraints ("Respond in exactly 3 bullet points...")

### Why Prompt Quality Matters

A vague prompt triggers pattern-completion behavior — the model predicts what word comes next based on statistical likelihood. A structured prompt triggers instruction-following behavior — the model attempts to complete a task to your specification.

```
Vague prompt:    "Tell me about Python"          → 2000-word essay on everything
Structured:      "List 5 Python features that
                  distinguish it from Java.
                  Use a comparison table."       → Precise, usable output
```

### The Five Elements of Prompt Anatomy

Every effective prompt contains some combination of:

1. **Instruction** — What the model should do
2. **Context** — Background information the model needs
3. **Input Data** — The specific content to process
4. **Output Indicator** — Format/structure of expected output
5. **Constraints** — Boundaries on tone, length, or content

---

## Platform Setup

**Required for all exercises:**
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account (free)
3. Click **"Create new prompt"** → **"Freeform"**
4. Set Temperature to 0 for deterministic outputs during comparison exercises

---

*Back to [main repository](../README.md)*
