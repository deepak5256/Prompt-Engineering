# Week 3 — ReAct: Reasoning and Acting

**Platform:** Google AI Studio (aistudio.google.com) or ChatGPT (chat.openai.com)  
**Technique:** ReAct (Reasoning + Acting) — interleaving thought and action  
**Source:** Based on [Yao et al., 2023](https://arxiv.org/abs/2210.03629) via [promptingguide.ai/techniques/react](https://www.promptingguide.ai/techniques/react)

ReAct is a prompting framework that asks the model to alternate between Thought (explicit reasoning), Action (a step to take or a question to answer), and Observation (result of that action). This prevents the model from jumping to conclusions and makes complex multi-step reasoning transparent and verifiable.

The pattern: **Thought → Action → Observation → Thought → Action → ...**

---

## Example 1 — System Design Planning (ReAct Simulation)

ReAct is most visible in agentic systems with tool access, but you can simulate the pattern in any chat interface by asking the model to follow the Thought/Action/Observation structure explicitly.

**Version A (Single-prompt approach)**

```
Design the architecture for a real-time chat application.
```

Typical output: A monolithic description of WebSockets, a database, a backend — correct but undifferentiated. The model does not reason about tradeoffs or requirements.

---

**Version B (ReAct-structured prompt)**

```
You are a software architect designing a real-time chat application. Use the following structured reasoning format for your analysis:

Thought: [Your current reasoning or analysis]
Action: [The specific design decision or question you are addressing]
Observation: [What this decision implies or requires]

Repeat this cycle at least 4 times, covering: user scale requirements, message delivery guarantees, database choice, and infrastructure. Then conclude with a final architecture summary.

Begin now.
```

Expected output: A structured sequence showing the reasoning chain — for example:

```
Thought: I need to determine the scale before choosing any technology.
Action: Define scale requirements — assume 10,000 concurrent users, 1M messages per day.
Observation: At this scale, a single-server approach will not work. I need horizontal scaling.

Thought: Message delivery must be reliable but also real-time.
Action: Choose WebSocket for real-time delivery with a message queue for reliability.
Observation: A message queue (e.g., Redis Pub/Sub) decouples producers from consumers and supports reconnection.

...
```

The explicit Thought-Action-Observation format forces the model to justify each architectural choice before making the next one, rather than listing decisions without rationale.

---

## Example 2 — Debugging a Logic Error with ReAct

**Version A (Direct request)**

```
This code is wrong, fix it:

def find_duplicates(lst):
    seen = []
    duplicates = []
    for item in lst:
        if item in seen:
            duplicates.append(item)
        seen.append(item)
    return duplicates
```

The model may fix the code but may introduce a different issue (adding the same duplicate multiple times) without catching it.

---

**Version B (ReAct-guided debugging)**

```
Debug the following Python function using this structured format:

Thought: [What you observe or hypothesize]
Action: [What you check or trace through]
Observation: [What you discover]

Repeat until the root cause is identified. Then provide the corrected function.

Function:
def find_duplicates(lst):
    seen = []
    duplicates = []
    for item in lst:
        if item in seen:
            duplicates.append(item)
        seen.append(item)
    return duplicates

Test case that fails: find_duplicates([1, 2, 2, 3, 3, 3]) returns [2, 3, 3] instead of [2, 3]
```

Expected output: The model traces through the iteration, discovers that 3 appears three times and is added to duplicates twice, identifies the fix (use a set for duplicates or add a condition to only add on first duplicate encounter), and produces a corrected function.

---

## Why ReAct Matters

| Approach | What the model does | Risk |
|----------|---------------------|------|
| Direct answer | Jumps to a conclusion | Skips steps, misses edge cases |
| Chain-of-Thought | Reasons linearly | Cannot backtrack or reconsider |
| ReAct | Reasons, acts, observes, and adjusts | Slower but more reliable for complex multi-step tasks |

ReAct is the foundation of modern AI agents. Every tool-using AI assistant (Google's Gemini with extensions, OpenAI's function-calling agents) uses a form of the ReAct loop internally.
