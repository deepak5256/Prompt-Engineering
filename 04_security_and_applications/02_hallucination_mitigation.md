# Week 4 — Hallucination Mitigation

**Platform:** Google AI Studio (aistudio.google.com)  
**Technique:** Designing prompts that reduce or expose model hallucinations  
**Source:** Adapted from [promptingguide.ai/risks/factuality](https://www.promptingguide.ai/risks/factuality) and [promptingguide.ai/prompts/truthfulness/identify-hallucination](https://www.promptingguide.ai/prompts/truthfulness/identify-hallucination)

Hallucination refers to a model generating confident, fluent, but factually incorrect or fabricated information. It is not a bug that will be fixed — it is a structural property of how large language models work. Prompt engineering can significantly reduce hallucination by constraining what the model can claim and how it must handle uncertainty.

---

## Example 1 — The Hallucination Demonstration

Run this prompt on Google AI Studio to observe hallucination directly. Ask about a fictional or obscure entity:

**Prompt:**

```
Tell me about the research contributions of Dr. Priya Nair from Chanakya University in the field of natural language processing.
```

If this person does not have a public profile in the model's training data, it will likely generate plausible-sounding but completely fabricated details — publications, years, conference names, and co-authors that do not exist. The output will be confident and grammatically fluent.

**Why this happens:** The model predicts the most statistically likely next token given the context. For a question about a researcher, the most likely tokens are names of papers, conferences, and research areas — real or invented.

---

## Example 2 — Forcing Uncertainty Acknowledgment

**Version A (Open question — hallucination-prone)**

```
What are the exact provisions of India's Digital Personal Data Protection Act 2023 regarding data breach notification timelines?
```

The model may state specific timelines with confidence — some correct, some invented or outdated.

---

**Version B (Uncertainty-aware prompt)**

```
Answer the following question about India's Digital Personal Data Protection Act 2023.

Rules you must follow:
1. If you are certain of a fact, state it and cite the relevant section number.
2. If you are uncertain or your training data may be incomplete, state: "I am not certain — please verify this against the official gazette or the MeitY website."
3. Do not present uncertain information as if it were confirmed fact.
4. Do not fabricate section numbers, timelines, or dates.

Question: What are the provisions regarding data breach notification timelines?
```

Expected output: The model states what it knows with appropriate confidence labels and explicitly flags anything that requires verification. The output is less authoritative-sounding but far more reliable for academic or professional use.

---

## Example 3 — Grounding the Model with Provided Context

The most reliable way to prevent hallucination on specific factual questions is to provide the source material in the prompt. The model then answers based on your text, not on its training data.

**Version A (No context — hallucination risk)**

```
Based on the latest research, what is the accuracy of transformer models on the SQuAD 2.0 benchmark?
```

The model may state outdated benchmark numbers or fabricate values.

---

**Version B (Context-grounded)**

```
Answer the question using only the information provided in the text below. 
If the text does not contain the answer, respond: "The provided text does not contain this information."
Do not use any knowledge from outside the provided text.

Text:
"As of 2023, several transformer-based models have surpassed human-level performance on SQuAD 2.0. The ALBERT model achieved an F1 score of 90.9, while human performance is estimated at 89.5 F1."

Question: What F1 score did the ALBERT model achieve on SQuAD 2.0?
```

Expected output: `The ALBERT model achieved an F1 score of 90.9 on SQuAD 2.0.`

Because the answer is in the provided text, the model cannot fabricate it. If you ask a question not in the text:

```
Question: What is the accuracy of GPT-4 on SQuAD 2.0?
```

Expected output: `The provided text does not contain this information.`

This pattern — providing context and restricting the model to that context — is the foundation of Retrieval-Augmented Generation (RAG), the dominant approach to building factually reliable AI systems.

---

## Example 4 — Hallucination Detection Prompt

You can ask the model to evaluate its own previous output for hallucination risk.

**Step 1 — Get a potentially hallucinated response**

Run this prompt:

```
Briefly describe the history of the Python programming language, including its creator, year of release, and the key design principles that guided its development.
```

Save the output.

**Step 2 — Audit the output**

Paste the Step 1 output into this audit prompt:

```
You are a fact-checking assistant. Review the following text about the Python programming language.

For each factual claim you identify:
1. State the claim
2. Classify it as: Verified (you are confident this is correct), Uncertain (you are not fully confident), or Likely Incorrect (you believe this contradicts known facts)
3. If Uncertain or Likely Incorrect, explain what a reader should verify

Text to review:
[PASTE STEP 1 OUTPUT HERE]
```

This two-step chain — generate, then audit — is a basic form of automated fact-checking. It does not eliminate hallucination but makes the reliability of each claim explicit.

---

## Hallucination Mitigation Techniques Summary

| Technique | How it works | Best used for |
|-----------|-------------|---------------|
| Uncertainty instruction | Tell the model to state when it is unsure | Factual questions where you cannot provide source material |
| Context grounding | Provide source text; restrict model to it | Specific documents, policies, technical specifications |
| Citation requirement | Require the model to cite a section or source for each claim | Legal, medical, regulatory questions |
| Self-audit | Generate, then ask the model to verify its own output | Any high-stakes content where errors are costly |
| Reduced temperature | Lower temperature reduces creative (and often incorrect) token choices | Factual queries where precision matters |
| Human verification | Treat model output as a draft, not a final fact | All high-stakes applications |
