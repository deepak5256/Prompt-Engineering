# Self-Consistency Decoding

**Topic:** Core Techniques  
**Technique:** Self-Consistency — sampling multiple reasoning paths and voting on the answer  
**Platform:** Google AI Studio (Temperature > 0) or API  
**Source:** [Wang et al. 2022 — "Self-Consistency Improves Chain of Thought Reasoning"](https://arxiv.org/abs/2203.11171)  

---

## Theory

**Self-consistency** is an ensemble technique for LLM reasoning. Instead of generating one CoT answer, you generate **multiple answers** (at Temperature > 0) and take the **majority vote** as the final answer.

### Why It Works

CoT prompting generates one reasoning path. But reasoning problems often have multiple valid paths to the same answer. When you:
1. Sample N independent reasoning chains (Temperature 0.7–1.0)
2. Extract the final answer from each chain
3. Select the most frequent answer

...you get a result that is more robust than any single chain. Wrong answers tend to come from different errors (cancelling each other out), while correct answers concentrate.

```
Query: What is 15% of 240?

Run 1: 240 × 0.15 = 36   → Answer: 36
Run 2: 240 ÷ 100 × 15 = 36 → Answer: 36
Run 3: 15% of 200=30, 15% of 40=6, total=36 → Answer: 36
Run 4: 10% of 240=24, 5% of 240=12, 24+12=36 → Answer: 36
Run 5: 240 × 0.15 = 35   → Answer: 35 (arithmetic error)

Majority vote: 36 (4 out of 5) → Final Answer: 36
```

### Self-Consistency vs Simple CoT

| Approach | Accuracy (typical) | Cost | Use Case |
|----------|-------------------|------|---------|
| Direct answer | Baseline | 1x | Simple tasks |
| Zero-shot CoT | +10–20% | 2–3x tokens | General reasoning |
| Few-shot CoT | +15–30% | 3–5x tokens | Complex reasoning |
| Self-consistency (N=5) | +20–40% | 5–10x tokens | High-stakes reasoning |
| Self-consistency (N=20) | +25–45% | 20x tokens | Research/critical decisions |

---

## Example 1 — Manual Self-Consistency (Simulated in AI Studio)

Since Google AI Studio doesn't automatically run multiple chains, you can simulate this by:

**Step 1:** Set Temperature to 0.9

**Step 2:** Run this prompt 5 times, recording each final answer:

```
A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?

Think through this carefully, step by step. Show your reasoning.

Final answer (in cents):
```

**What you'll observe:**
- Some runs produce: "The ball costs 5 cents" (correct — via algebra)
- Some runs produce: "The ball costs 10 cents" (wrong — the intuitive but incorrect answer)
- Self-consistency selects whichever is majority

> This is the famous "CRT cognitive reflection test" question. Humans (and unconstrained LLMs) frequently answer 10 cents intuitively. CoT + self-consistency reliably produces 5 cents.

**Correct reasoning:**
```
Let ball = x cents
Bat = x + 100 cents
x + (x + 100) = 110
2x = 10
x = 5

Ball = 5 cents, Bat = 105 cents.
Check: 5 + 105 = 110 ✓, 105 - 5 = 100 ✓
```

---

## Example 2 — Implementing Self-Consistency via API (Python)

This is a production-ready pattern for using self-consistency programmatically.

```python
"""
self_consistency.py
Demonstrates the self-consistency technique using the Google Gemini API.
Institution: Chanakya University — School of Engineering
Author: Mr. Deepak B
"""

import google.generativeai as genai
import os
import re
from collections import Counter

# Configure API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_final_answer(text: str) -> str:
    """Extract the final numerical answer from a reasoning chain."""
    # Look for patterns like "Answer: X" or "= X" at the end
    patterns = [
        r"(?:final answer|answer)[:\s]+(\d+\.?\d*)",
        r"(?:therefore|thus|so)[,\s]+(?:the answer is\s+)?(\d+\.?\d*)",
        r"=\s*(\d+\.?\d*)\s*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1)
    # Fallback: last number in text
    numbers = re.findall(r"\d+\.?\d*", text)
    return numbers[-1] if numbers else "unknown"

def self_consistent_answer(question: str, n_samples: int = 5) -> dict:
    """
    Generate multiple CoT reasoning chains and return the majority-vote answer.
    
    Args:
        question: The reasoning question to answer
        n_samples: Number of independent chains to generate
    
    Returns:
        dict with final_answer, all_answers, confidence, and reasoning_chains
    """
    cot_prompt = f"""
{question}

Let's think through this step by step. Show all your reasoning before giving the final answer.
At the end, write "Final answer: [number]"
"""
    
    answers = []
    chains = []
    
    print(f"Generating {n_samples} independent reasoning chains...\n")
    
    for i in range(n_samples):
        response = model.generate_content(
            cot_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,  # Non-zero for diversity
                max_output_tokens=512,
            )
        )
        chain = response.text
        answer = extract_final_answer(chain)
        
        answers.append(answer)
        chains.append(chain)
        print(f"Chain {i+1}: Answer = {answer}")
    
    # Majority vote
    vote_counts = Counter(answers)
    final_answer, vote_count = vote_counts.most_common(1)[0]
    confidence = vote_count / n_samples
    
    return {
        "final_answer": final_answer,
        "confidence": f"{confidence:.0%}",
        "vote_distribution": dict(vote_counts),
        "all_reasoning_chains": chains
    }

# --- Demo ---
if __name__ == "__main__":
    question = """
    A store offers a 20% discount on a laptop priced at ₹50,000. 
    After the discount, an additional 18% GST is applied. 
    What is the final price a customer pays?
    """
    
    result = self_consistent_answer(question, n_samples=5)
    
    print("\n" + "="*50)
    print(f"FINAL ANSWER (majority vote): ₹{result['final_answer']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Vote distribution: {result['vote_distribution']}")
```

**Expected output:**
```
Generating 5 independent reasoning chains...

Chain 1: Answer = 47200
Chain 2: Answer = 47200
Chain 3: Answer = 47200
Chain 4: Answer = 47200
Chain 5: Answer = 47000  (one chain with arithmetic error)

==================================================
FINAL ANSWER (majority vote): ₹47200
Confidence: 80%
Vote distribution: {'47200': 4, '47000': 1}
```

**Correct reasoning:**
- Original price: ₹50,000
- 20% discount: ₹10,000 → Discounted price: ₹40,000
- 18% GST on ₹40,000: ₹7,200
- Final price: ₹47,200

---

## When to Use Self-Consistency

| Use Self-Consistency | Don't Use Self-Consistency |
|---------------------|--------------------------|
| High-stakes numerical answers | Simple factual Q&A |
| Medical/financial decisions | Creative writing |
| Logic puzzles and math | Classification tasks |
| Ambiguous reasoning problems | Real-time applications (latency) |
| When CoT alone gives inconsistent answers | Low-budget deployments |

---

## Key Insight

Self-consistency is a meta-technique: it doesn't change **how** the model reasons — it changes **how many times** it reasons and **how** you select the final answer. It's the simplest form of ensemble learning applied to LLMs.

The practical lesson: when accuracy is more important than speed and cost, generate multiple chains and vote.

---

*Previous: [Role & System Prompts ←](./03_role_and_system_prompts.md)*  
*Next Topic: [Advanced Patterns & RAG →](../03_advanced_patterns/README.md)*  
*Back to [Topic 2 README](./README.md)*
