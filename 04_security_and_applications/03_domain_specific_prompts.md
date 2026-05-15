# Week 4 — Domain-Specific Prompt Design

**Platform:** Google AI Studio (aistudio.google.com)  
**Technique:** Adapting prompt structure and constraints for specific professional domains  
**Source:** Adapted from [promptingguide.ai/applications/workplace_casestudy](https://www.promptingguide.ai/applications/workplace_casestudy) and course case studies

General-purpose prompts work for general tasks. Domain-specific tasks — software development, education, healthcare, legal work, data analysis — require prompts that embed domain knowledge, professional conventions, and safety constraints directly into the instruction. This file demonstrates how the same base task requires different prompt design depending on the professional context.

---

## Example 1 — Software Development Domain

**Task:** Review a function for production readiness.

**Version A (Generic)**

```
Review this code:

def get_user(user_id):
    conn = db.connect("mysql://admin:password123@localhost/users")
    result = conn.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return result.fetchone()
```

Typical output: A general comment about the code's structure, possibly mentioning security concerns in passing.

---

**Version B (Domain-specific — Software Security)**

```
You are conducting a security-focused code review for a function that will be deployed in a production web application. 
Evaluate the following Python function against the OWASP Top 10 security criteria.

For each issue you find:
- Issue Name: (e.g., SQL Injection, Hardcoded Credential)
- Severity: Critical / High / Medium / Low
- Line(s) affected: 
- Explanation: One sentence describing the vulnerability
- Remediation: Exact code showing how to fix it

After listing all issues, provide a rewritten version of the function that addresses all Critical and High severity issues.

Function:
def get_user(user_id):
    conn = db.connect("mysql://admin:password123@localhost/users")
    result = conn.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return result.fetchone()
```

Expected output: The model identifies the SQL injection vulnerability (f-string interpolation in a query), the hardcoded credential (the connection string), the missing error handling, and the overfetch (`SELECT *`). Each issue is classified by severity, and a corrected function using parameterized queries and environment variables for credentials is provided.

---

## Example 2 — Education Domain

**Task:** Generate a quiz on a topic.

**Version A (Generic)**

```
Make a quiz on Python loops.
```

Typical output: 5 to 10 arbitrary questions of uncontrolled difficulty, format, and coverage.

---

**Version B (Domain-specific — Pedagogy-aware)**

```
Create a formative assessment quiz on Python loops for MCA second-semester students.

Student profile: Students understand variables and conditionals but are in their first week of loops. They have not yet covered functions or recursion.

Quiz requirements:
- 6 questions total
- Question types: 2 multiple choice, 2 trace-the-output, 2 write-the-code
- Difficulty: 2 basic (recall), 2 intermediate (application), 2 analysis (finding errors)
- Each multiple choice question must have exactly 4 options with only one correct answer
- Each trace-the-output question must include the exact code and ask for the printed output
- Each write-the-code question must specify the exact expected behavior

Format each question as:
Q[number] ([Type] | [Difficulty]):
[Question text]
[Options if MCQ]
Answer: [correct answer]
Explanation: [one sentence explaining why]
```

Expected output: A structured, pedagogically sound quiz that a lecturer can use directly, with questions appropriately staged for students at the described level.

---

## Example 3 — Data Analysis Domain

**Task:** Interpret a dataset summary.

**Version A (Generic)**

```
Analyze this data:

Students: 150
Pass rate: 62%
Average score: 54.3
Highest score: 98
Lowest score: 12
Standard deviation: 18.7
```

Typical output: A restatement of the numbers in sentence form.

---

**Version B (Domain-specific — Academic Analytics)**

```
You are an academic analytics consultant reviewing end-semester exam results for a department head.

Analyze the following exam statistics and provide:
1. Performance summary: What does this data indicate about the cohort's overall performance? (2 sentences)
2. Distribution insight: Based on the mean (54.3) and standard deviation (18.7), describe what the likely score distribution looks like and what it implies for the class.
3. Concern flags: Identify two specific concerns this data raises that the department head should act on.
4. Recommended interventions: For each concern, suggest one concrete academic intervention (e.g., additional tutorials, threshold-based support sessions).
5. Data limitations: What additional data would be needed to draw more reliable conclusions?

Statistics:
- Total students: 150
- Pass rate: 62%
- Average score: 54.3
- Highest score: 98
- Lowest score: 12
- Standard deviation: 18.7
```

Expected output: A professional analytical report that a department head could use directly in a faculty meeting — not a restatement of numbers.

---

## Example 4 — Building a Domain-Specific System Prompt Template

For any professional domain, a reusable system prompt template follows this structure:

```
You are [role] with expertise in [domain].

Your audience: [who you are serving]

Your scope:
- You can assist with: [list of permitted tasks]
- You cannot assist with: [list of restricted tasks]

Output standards:
- [Format requirement 1]
- [Format requirement 2]
- [Accuracy or verification requirement]

When you do not know something: [specific fallback behavior]
```

**Instantiated for a legal domain example:**

```
You are a legal research assistant with expertise in Indian contract law.

Your audience: Law students and junior associates preparing case summaries.

Your scope:
- You can assist with: explaining legal concepts, summarizing case law principles, drafting structured legal arguments for learning purposes
- You cannot assist with: providing legal advice for real cases, predicting court outcomes, or reviewing actual client documents

Output standards:
- Cite the relevant section of the Indian Contract Act 1872 or case name for every legal principle stated
- Use formal legal language
- Structure responses with: Rule, Application, Conclusion

When you do not know something: State "I cannot verify this from my training data. Please consult the primary source or a qualified advocate."
```

Test this system prompt in Google AI Studio against legal questions at different levels of complexity. Observe how the scope, citation, and uncertainty instructions change the response quality compared to a model with no system instruction.

---

## Domain-Specific Prompt Design Principles

| Principle | Generic prompt | Domain-specific prompt |
|-----------|---------------|----------------------|
| Audience | Not specified | Explicitly defined with background knowledge level |
| Output format | Left to model | Matched to professional conventions of the field |
| Scope | Unlimited | Bounded to relevant tasks |
| Error handling | Default refusal | Field-specific guidance (verify with doctor, consult a lawyer) |
| Tone | Default conversational | Matches domain register (technical, academic, legal) |
