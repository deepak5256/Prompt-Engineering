# Week 3 — Prompt Chaining

**Platform:** Google AI Studio (aistudio.google.com) — use separate prompts in sequence  
**Technique:** Prompt chaining — passing the output of one prompt as input to the next  
**Source:** Examples adapted from [promptingguide.ai/techniques/prompt_chaining](https://www.promptingguide.ai/techniques/prompt_chaining)

Prompt chaining breaks a complex task into a sequence of simpler prompts, where each prompt's output becomes the next prompt's input. This technique is useful when a single prompt is too large or complex, when different stages of a task require different instructions, or when you want to verify intermediate results before proceeding.

---

## Example 1 — Three-Step Documentation Generator

This example demonstrates a three-step chain. Run each prompt in sequence on Google AI Studio, copying the output of each step into the next prompt.

**Input (paste this Python code as your starting point):**

```python
def calculate_bmi(weight_kg, height_m):
    if height_m <= 0:
        raise ValueError("Height must be positive")
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)
```

---

**Step 1 — Code Analysis**

Paste this prompt into Google AI Studio:

```
Analyze the following Python function and provide:
1. What the function computes (one sentence)
2. The parameters: name, type, and valid range for each
3. The return value: type and format
4. Edge cases handled
5. Edge cases NOT handled that could cause errors

Function:
def calculate_bmi(weight_kg, height_m):
    if height_m <= 0:
        raise ValueError("Height must be positive")
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)
```

Copy the output. This becomes the input for Step 2.

---

**Step 2 — Generate Docstring**

Paste this prompt, replacing [STEP 1 OUTPUT] with the actual output from Step 1:

```
Using the following function analysis, write a complete Python docstring in Google style.
The docstring must include: a one-line summary, an Args section, a Returns section, a Raises section, and one usage Example.

Function analysis:
[STEP 1 OUTPUT]

Output only the docstring text. Do not include the def statement or the function body.
```

Copy the output. This becomes the input for Step 3.

---

**Step 3 — Generate Unit Tests**

Paste this prompt, replacing [DOCSTRING] with the output from Step 2:

```
Based on the following function docstring, write pytest unit tests that cover:
1. A normal case with valid inputs
2. The boundary case for height (height = 0)
3. A case with a very high BMI value
4. A case with a very low BMI value

Docstring:
[DOCSTRING]

The original function signature is:
def calculate_bmi(weight_kg, height_m)

Output only the test code. Use descriptive test function names.
```

**Result of the chain:** Three separate, focused outputs that together constitute a complete documentation package for the function — analysis, docstring, and tests — each produced with a prompt optimized for that specific task.

---

## Example 2 — Why a Single Prompt Fails Here

**Version A (Single large prompt — try this first)**

```
For the following Python function:
1. Analyze what it does
2. Write a Google-style docstring
3. Write three pytest unit tests

def calculate_bmi(weight_kg, height_m):
    if height_m <= 0:
        raise ValueError("Height must be positive")
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)
```

Typical problems with this approach:
- The analysis section is brief because the model budgets tokens across all three tasks
- The docstring may reference analysis details that were not fully explored
- The tests may miss edge cases that a dedicated test-generation prompt would catch

---

**Version B (Chain — compare the quality)**

Run the three-step chain from Example 1 and compare the depth and quality of each section against Version A.

**What to observe:**
- Is the analysis in Step 1 more detailed than the analysis section in Version A?
- Does the docstring in Step 2 match the analysis more accurately?
- Do the tests in Step 3 cover more edge cases?

---

## Example 3 — Conditional Chaining (Verification Step)

In production systems, prompt chains often include a verification step before proceeding.

**Step 1 — Generate SQL query**

```
Write a MySQL query to find all students who have enrolled in more than 3 courses and have an average grade above 75.

Database schema:
- students(student_id, name, email, enrollment_year)
- enrollments(enrollment_id, student_id, course_id, grade)
- courses(course_id, course_name, credits)
```

**Step 2 — Verify the query (paste Step 1 output as [QUERY])**

```
Review the following MySQL query for correctness. Check:
1. Does the JOIN logic correctly link students to their enrollments?
2. Does the GROUP BY correctly aggregate per student?
3. Does the HAVING clause correctly filter for both conditions (more than 3 courses AND average grade above 75)?
4. Are there any columns referenced that do not exist in the schema?

If the query is correct, respond: "Query is correct. Proceed."
If the query has errors, list each error and provide the corrected query.

Schema:
- students(student_id, name, email, enrollment_year)
- enrollments(enrollment_id, student_id, course_id, grade)
- courses(course_id, course_name, credits)

Query to review:
[QUERY]
```

This verification step catches errors before the query is used downstream. In automated pipelines, you can branch the chain based on whether the verifier returns "correct" or "has errors."

---

## Key Principle

Prompt chaining is the correct approach when:
- A task has more than two or three distinct phases
- Different phases benefit from different instructions or constraints
- You need to inspect or validate intermediate results
- A single prompt produces inconsistent quality because it tries to do too much at once
