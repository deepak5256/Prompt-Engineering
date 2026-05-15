# Topic 4: Security, Ethics & Domain Applications

**Institution:** Chanakya University — School of Engineering  
**Instructor:** Mr. Deepak B  

---

## Topics Covered

| File | Concept |
|------|---------|
| [01_prompt_injection_and_defense.md](./01_prompt_injection_and_defense.md) | Prompt Injection Attacks & Defenses |
| [02_hallucination_mitigation.md](./02_hallucination_mitigation.md) | Hallucination: Causes & Mitigation |
| [03_domain_specific_prompts.md](./03_domain_specific_prompts.md) | Domain-Specific Prompt Patterns |
| [04_ethics_and_responsible_ai.md](./04_ethics_and_responsible_ai.md) | Ethics & Responsible AI |

---

## Why Security Matters in Prompt Engineering

LLMs are deployed in production systems handling real data and real users. Prompt engineering at the system level introduces unique attack surfaces:

- **Prompt injection**: Malicious user input overrides system instructions
- **Indirect injection**: Malicious content in retrieved documents (relevant for RAG) hijacks the model
- **Data exfiltration**: Attacker extracts system prompt or other users' data
- **Jailbreaking**: Bypassing safety guardrails through clever instruction framing

Understanding these attacks is as important as understanding how to write effective prompts. Every prompt engineer must think adversarially about their prompts.

---

*Back to [main repository](../README.md)*
