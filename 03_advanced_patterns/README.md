# Topic 3: Advanced Patterns & RAG Systems

**Course:** Prompt Engineering: Principles, Techniques & Applications  
**Institution:** Chanakya University — School of Engineering  
**Instructor:** Mr. Deepak B  

---

## Learning Objectives

By the end of this topic, you will be able to:
- Apply the ReAct (Reason + Act) framework for multi-step agent behavior
- Design and implement prompt chains for complex workflows
- Use meta-prompting to generate and refine prompts programmatically
- **Build and run a complete Retrieval-Augmented Generation (RAG) system from scratch**

---

## Topics Covered

| File | Concept | Difficulty |
|------|---------|------------|
| [01_react_reasoning_pattern.md](./01_react_reasoning_pattern.md) | ReAct: Reasoning + Acting | Intermediate |
| [02_prompt_chaining.md](./02_prompt_chaining.md) | Prompt Chaining | Intermediate |
| [03_meta_prompting.md](./03_meta_prompting.md) | Meta-Prompting | Advanced |
| [04_retrieval_augmented_generation.md](./04_retrieval_augmented_generation.md) | RAG — Full Theory | Advanced |
| [rag_system/](./rag_system/) | **Working RAG System** | **Lab Project** |

---

## Week 3 Assignment: Build a RAG System


### Quick Overview

Build a **Retrieval-Augmented Generation (RAG) system** that:
1. Accepts documents (PDF, TXT, or plain text) as a knowledge base
2. Embeds them into a vector store (ChromaDB)
3. Answers user questions using only the uploaded documents
4. Runs locally on your computer

### Reference Implementation

A fully working reference implementation is in [`rag_system/`](./rag_system/). Study it, understand every component, then build your own variant.

**To run the reference system:**
```bash
cd 03_advanced_patterns/rag_system
pip install -r requirements.txt
set GEMINI_API_KEY=your_key_here
python app.py
# Open http://localhost:8000
```

### Submission
- Deploy your system and submit the **live URL** on DigiCampus


---

## Conceptual Overview

### From Prompting to Systems

Topics 1 and 2 focused on single-prompt techniques. Topic 3 shifts to **prompt-driven systems** — architectures where prompts are components in a larger pipeline.

```
Single Prompt:   User → LLM → Answer
Prompt Chain:    User → LLM₁ → Output₁ → LLM₂ → Output₂ → Final
ReAct Agent:     User → (Thought → Action → Observation)ₙ → Final
RAG System:      User → Retriever → Relevant Docs → LLM → Grounded Answer
```

### The RAG Revolution

RAG (Retrieval-Augmented Generation) solves the fundamental limitation of LLMs: **they only know what was in their training data**. With RAG:

- You give the model your own documents as a live knowledge base
- The model retrieves relevant information before answering
- Answers are grounded in your data, not general training knowledge
- The model cannot hallucinate about your specific domain

This is how enterprise AI systems are built today — not by fine-tuning a model, but by giving it access to a retrieval system over your proprietary data.

---

*Back to [main repository](../README.md)*
