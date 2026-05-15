# Prompt Engineering: Principles, Techniques & Applications

> **Open Educational Resource** — Free for anyone to learn, fork, and build on.  
> Originally created for MCA students at Chanakya University — School of Engineering.  
> Mr. Deepak B

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/deepak5256/Prompt-Engineering/pulls)

---

## Where Does Prompt Engineering Fit?

Understanding where this skill sits in the modern developer career ladder:

```
Frontend Dev     =  HTML + CSS + JS + React + Git
Backend Dev      =  JS/Python + MongoDB/SQL + API
Software Dev     =  Frontend + Backend + System Design
Full Stack Dev   =  Software Dev + Deployment
AI Developer     =  Full Stack Dev + Prompting + LLM Integration
AI Engineer      =  AI Developer + RAG + Vector DB + LangChain + Cloud
```

> **This course takes you from zero to AI Engineer.** By Topic 3, you will have built and deployed a production-style RAG system — the core skill of an AI Engineer.

---

## About This Repository

This is a **free, open-access curriculum** covering Prompt Engineering from the ground up — all the way to building and deploying a production RAG system.

You **do not** need to be a Chanakya University student to use this. Whether you are:
- A developer learning to integrate LLMs into your projects
- A student taking an AI/ML course anywhere in the world
- A professional looking to move into AI Engineering
- A hobbyist exploring what modern AI can do

...this repository is for you. Everything here is free and runs on free-tier APIs.

**What you'll be able to build after completing this:**
- Precise, reliable prompts for any LLM (ChatGPT, Gemini, Claude)
- A working RAG system that answers questions from your own documents
- A deployed AI web application with a real public URL

---

## Repository Structure

```
prompt-engineering/
│
├── 01_foundations/                    # Topic 1: Foundations of Prompt Engineering
│   ├── README.md
│   ├── 01_zero_shot_prompting.md
│   ├── 02_prompt_anatomy.md
│   ├── 03_output_format_control.md
│   └── 04_temperature_and_parameters.md
│
├── 02_core_techniques/                # Topic 2: Core Prompting Techniques
│   ├── README.md
│   ├── 01_few_shot_prompting.md
│   ├── 02_chain_of_thought.md
│   ├── 03_role_and_system_prompts.md
│   └── 04_self_consistency.md
│
├── 03_advanced_patterns/              # Topic 3: Advanced Patterns & RAG Systems
│   ├── README.md
│   ├── 01_react_reasoning_pattern.md
│   ├── 02_prompt_chaining.md
│   ├── 03_meta_prompting.md
│   ├── 04_retrieval_augmented_generation.md   ← Full RAG theory
│   └── rag_system/                            ← Working RAG implementation
│       ├── README.md
│       ├── requirements.txt
│       ├── app.py                             ← FastAPI backend
│       ├── rag_engine.py                      ← Core RAG pipeline
│       ├── ingest.py                          ← Document ingestion
│       ├── config.py                          ← Configuration
│       ├── sample_docs/                       ← Sample knowledge base
│       └── frontend/                          ← Browser UI
│           └── index.html
│
├── 04_security_and_applications/      # Topic 4: Security, Ethics & Domain Applications
│   ├── README.md
│   ├── 01_prompt_injection_and_defense.md
│   ├── 02_hallucination_mitigation.md
│   ├── 03_domain_specific_prompts.md
│   └── 04_ethics_and_responsible_ai.md
│
├── assignments/                       # Assignment briefs and rubrics
│   ├── week1_assignment.md
│   ├── week2_assignment.md
│   ├── week3_rag_assignment.md        ← Current assignment
│   └── week4_assignment.md
│
└── README.md                          ← You are here
```

---

## Topic Map

| # | Topic | Key Concepts | Lab |
|---|-------|-------------|-----|
| **1** | [Foundations](./01_foundations/) | Zero-shot, Anatomy, Formatting, Temperature | Google AI Studio |
| **2** | [Core Techniques](./02_core_techniques/) | Few-shot, Chain-of-Thought, Role Prompts, Self-Consistency | AI Studio + ChatGPT |
| **3** | [Advanced Patterns & RAG](./03_advanced_patterns/) | ReAct, Prompt Chaining, Meta-Prompting, **RAG Systems** | Python + FastAPI |
| **4** | [Security & Applications](./04_security_and_applications/) | Injection Defense, Hallucination, Ethics, Domain Apps | Code Review |

---

## Quick Start

### For Students (No Setup)
Open any `.md` file in any topic folder. Copy the prompts into [Google AI Studio](https://aistudio.google.com) and run them directly.

### For the RAG System Lab (Topic 3)
```bash
# 1. Clone the repository
git clone https://github.com/deepak5256/Prompt-Engineering.git
cd Prompt-Engineering

# 2. Navigate to the RAG system
cd 03_advanced_patterns/rag_system

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set your Google Gemini API key
set GEMINI_API_KEY=your_key_here   # Windows
# export GEMINI_API_KEY=your_key   # Mac/Linux

# 6. Run the application
python app.py

# 7. Open browser at http://localhost:8000
```

---

## Platforms Used in This Course

| Platform | URL | Used For |
|----------|-----|---------|
| Google AI Studio | [aistudio.google.com](https://aistudio.google.com) | All prompting exercises |
| Google Gemini API | [ai.google.dev](https://ai.google.dev) | RAG system backend |
| GitHub | [github.com](https://github.com) | Code repository |
| DigiCampus | [digicampus.in](https://digicampus.in) | Assignment submission |

---

## Course Textbook Reference

This repository accompanies the course textbook:  
**"Prompt Engineering: Principles, Techniques & Applications"** — Mr. Deepak B, Chanakya University, 2026

The textbook is available through the university library portal and DigiCampus resources.

---

*Last updated: May 2026 | Chanakya University MCA Programme*
