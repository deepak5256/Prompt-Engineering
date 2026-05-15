# Role Prompts & System Instructions

**Topic:** Core Techniques  
**Technique:** Role Prompts — activating domain knowledge through identity assignment  
**Platform:** Google AI Studio ([aistudio.google.com](https://aistudio.google.com))  

---

## Theory

**Role prompting** assigns a specific identity, expertise, or persona to the model before giving it a task. This works because LLMs have learned patterns associated with different roles from their training data — text written by doctors, lawyers, engineers, teachers, and many others. When you say "You are a senior software architect," you activate those learned patterns.

### What Changes with a Role

| Without Role | With Role |
|-------------|----------|
| Generic vocabulary | Domain-specific terminology |
| Balanced view of all options | Perspective shaped by expertise |
| Generic caution | Professional-grade critical analysis |
| Average depth | Expert-level depth in the domain |

### System Instructions vs Role Prompts

In platforms with separate system instruction fields (like Google AI Studio):

```
System Instruction (persistent, invisible to user):
"You are a cybersecurity auditor. Always identify security vulnerabilities
before recommending solutions. Use OWASP terminology."

User Message (the task):
"Review this login form code."
```

In platforms without system instruction support, prepend the role to the prompt:
```
[ROLE]
You are a cybersecurity auditor...

[TASK]
Review this login form code:
```

---

## Example 1 — Role Changes Output Depth

### Without Role

```
What are the risks of storing passwords in plain text?
```

**Typical output:** "Storing passwords in plain text is dangerous because if someone hacks your database, they can see all the passwords." — Generic, shallow.

---

### With Security Expert Role

```
You are a senior application security engineer with 10 years of experience in OWASP security practices and incident response. You have reviewed breaches at major companies and understand attack vectors deeply.

What are the risks of storing passwords in plain text? Assume the audience is a development team that has never experienced a breach.
```

**Expected output (much richer):**
- Breach impact: full credential exposure, credential stuffing attacks across other sites
- Regulatory consequences: GDPR Article 32, PCI DSS requirement 8.2.1
- Real-world examples: RockYou (2009, 32M plain-text passwords), Adobe (2013)
- Attack chain: database dump → immediate password visibility → account takeover
- Defense: bcrypt with cost factor ≥12, argon2id, never log passwords even in debug

The same question produces fundamentally different depth with a role.

---

## Example 2 — The Rubber Duck Debugging Role

A creative use of role prompting for code review.

```
You are a meticulous senior Python developer doing a code review. You are known for finding edge cases others miss. You ask clarifying questions before suggesting fixes.

Review the following function and identify all issues, including edge cases, before suggesting a fix:

```python
def get_discount(price, discount_percent):
    discount = price * discount_percent / 100
    final_price = price - discount
    return final_price
```
```

**Expected output:** The model should identify:
- No input validation (negative price? discount > 100%?)
- No handling of non-numeric inputs
- Float precision issues with currency
- No docstring / type hints
- Should the function round? To how many decimals?

---

## Example 3 — System Instruction in Google AI Studio

**How to set a System Instruction in Google AI Studio:**
1. Open AI Studio → Create new prompt → Freeform
2. Look for "System Instructions" panel at the top
3. Enter your role/persona there
4. Your task goes in the regular prompt area

### System Instruction:
```
You are an experienced MCA exam question setter at an Indian university. 
You design questions that test deep conceptual understanding, not memorization.
Every question you create includes:
1. A clear context statement
2. The question itself
3. The expected reasoning path (for the answer key)
4. The marks allocation and bloom's taxonomy level

Format all output in markdown.
```

### User Prompt:
```
Create 3 exam questions on the topic of Database Normalization for a 2nd year MCA exam.
Target difficulty: Medium to Hard.
```

**Expected output:** Three structured questions, each with context, the question, answer key reasoning, marks, and bloom's level — exactly matching the system instruction format.

---

## Example 4 — Multi-Persona Roleplay for Idea Exploration

This technique uses role prompting to explore multiple perspectives on one topic.

```
I want you to explore the following topic from three expert perspectives, one at a time.

Perspectives:
1. A Silicon Valley startup founder who believes AI will create more jobs than it destroys
2. An Oxford labor economist who has studied technological unemployment for 20 years
3. A manufacturing worker who has experienced automation replacing colleagues

Topic: "Will AI-driven automation cause widespread unemployment by 2035?"

For each perspective:
- Speak in first person ("I believe...")
- Draw on the background of that persona
- Include 2 specific pieces of evidence or examples
- Be willing to disagree with the other perspectives

Begin with Perspective 1.
```

This technique is particularly powerful for:
- Exploring policy debates
- Generating diverse arguments for essays
- Understanding stakeholder views in product design

---

## Building Effective Roles: A Framework

```
[EXPERTISE LEVEL]    "You are a senior..." / "You are an expert..."
[DOMAIN]             "...database architect..." / "...legal copywriter..."
[SPECIALIZATION]     "...specializing in PostgreSQL performance tuning..."
[EXPERIENCE CONTEXT] "...who has worked at Fortune 500 companies..."
[BEHAVIORAL TRAIT]   "...you always explain tradeoffs before recommendations."
[AUDIENCE CONTEXT]   "Your audience is first-year MCA students."
```

**Example using full framework:**
```
You are a senior machine learning engineer specializing in NLP and transformer architectures, 
who has worked at Google Brain and published papers at NeurIPS. You always explain concepts 
using analogies before diving into technical details. Your audience today is final-year MCA 
students who know Python but have no prior deep learning experience.

Explain the attention mechanism in transformers.
```

---

## Role Prompt Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| "Be a helpful assistant" | Too vague — the model is already that | Specify the exact domain and behavior |
| "You are omniscient" | Model may overclaim or hallucinate | Be specific; acknowledge limitations explicitly |
| Conflicting roles | "Be both a skeptic and an enthusiast" | Give one coherent persona |
| Role without task context | Role alone doesn't tell the model what to do | Always pair role with explicit task |

---

*Previous: [Chain-of-Thought ←](./02_chain_of_thought.md)*  
*Next: [Self-Consistency →](./04_self_consistency.md)*  
*Back to [Topic 2 README](./README.md)*
