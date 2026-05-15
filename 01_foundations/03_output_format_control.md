# Output Format Control

**Topic:** Foundations of Prompt Engineering  
**Technique:** Structured output specification — controlling what the model returns  
**Platform:** Google AI Studio ([aistudio.google.com](https://aistudio.google.com))  

---

## Theory

One of the most valuable skills in prompt engineering is **format control** — the ability to make a model return data in an exact structure. This matters because:

1. **Downstream processing:** Code needs predictable formats (JSON, CSV, lists)
2. **Readability:** Tables are better than paragraphs for comparison data
3. **Consistency:** Same format across multiple runs = reliable pipeline

The model can produce virtually any format if you specify it precisely. The key is to either:
- **Describe** the format in words ("Return a JSON object with keys...")
- **Show** the format with a template ("Answer in this format:\nName: ...\nAge: ...")

---

## Supported Output Formats

| Format | When to Use | Example Use Case |
|--------|------------|-----------------|
| Plain text | Narrative, explanation | Blog post, story |
| Markdown | Documentation, GitHub | README, technical docs |
| JSON | APIs, databases, code | Config files, data extraction |
| CSV | Spreadsheets, data analysis | Survey results, product lists |
| Table (Markdown) | Comparison, reference | Feature comparison |
| Numbered list | Sequential steps | Instructions, tutorials |
| Bullet list | Non-sequential items | Features, considerations |
| Code block | Programming output | Functions, scripts |
| XML | Structured data interchange | Legacy systems, configs |

---

## Example 1 — JSON Output

### Version A (No Format Specified)

```
Extract the key information from this job posting:
Position: Senior Data Scientist at TechCorp.
Required skills: Python, SQL, TensorFlow. 
Salary: $120,000-$150,000. Remote work available.
```

**Typical output:** A paragraph: "The position is for a Senior Data Scientist at TechCorp requiring Python, SQL, and TensorFlow skills with a salary range of $120,000 to $150,000..."

---

### Version B (JSON Format Required)

```
Extract the key information from the following job posting and return it as valid JSON.
Use exactly these keys: position, company, skills (array), salary_min, salary_max, remote.

Job posting:
Position: Senior Data Scientist at TechCorp.
Required skills: Python, SQL, TensorFlow.
Salary: $120,000-$150,000. Remote work available.

JSON output:
```

**Expected output:**
```json
{
  "position": "Senior Data Scientist",
  "company": "TechCorp",
  "skills": ["Python", "SQL", "TensorFlow"],
  "salary_min": 120000,
  "salary_max": 150000,
  "remote": true
}
```

This output can be directly parsed by `json.loads()` in Python.

---

## Example 2 — Markdown Table

### Version A (Prose)

```
Compare Python, JavaScript, and Java for web backend development.
```

Output: A dense paragraph with no clear visual hierarchy.

---

### Version B (Structured Table)

```
Compare Python, JavaScript, and Java for web backend development.
Format your response as a markdown table with these columns:
Language | Primary Framework | Performance | Learning Curve | Best For

Include exactly one row per language. Use concise phrases (max 5 words per cell).
```

**Expected output:**

| Language | Primary Framework | Performance | Learning Curve | Best For |
|----------|-----------------|-------------|----------------|---------|
| Python | Django / FastAPI | Moderate | Low | Data + APIs |
| JavaScript | Node.js / Express | High | Medium | Real-time apps |
| Java | Spring Boot | High | High | Enterprise systems |

---

## Example 3 — Structured Step-by-Step Output

### Version A (Unstructured)

```
How do I deploy a Python app to the cloud?
```

Output: A wall of text covering multiple cloud providers with no clear steps.

---

### Version B (Numbered Steps with Code)

```
Provide step-by-step instructions for deploying a Python Flask app to Google Cloud Run.

Format each step as:
Step N: [Short title]
Command: [The exact terminal command to run, in a code block]
Note: [One sentence explaining what this step does]

Include exactly 5 steps from app containerization to live URL.
```

**Expected output:**
```
Step 1: Create a Dockerfile
Command:
```
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```
Note: This file tells Cloud Run how to package your application.

Step 2: Build the container image
...
```

---

## Example 4 — Schema-Driven Extraction

This is critical for NLP pipelines where you need consistent structured data.

### The Prompt

```
You are a data extraction assistant. Extract structured information from the following medical note and return valid JSON matching the schema below.

Schema:
{
  "patient_age": <integer>,
  "chief_complaint": <string>,
  "symptoms": <array of strings>,
  "duration": <string>,
  "severity": "mild" | "moderate" | "severe"
}

Medical note:
"Patient is a 34-year-old female presenting with a chief complaint of persistent headache. She reports throbbing pain behind the right eye and sensitivity to light for the past 3 days. She rates pain as 7/10."

JSON:
```

**Expected output:**
```json
{
  "patient_age": 34,
  "chief_complaint": "persistent headache",
  "symptoms": ["throbbing pain behind right eye", "sensitivity to light"],
  "duration": "3 days",
  "severity": "severe"
}
```

---

## Advanced: Enforcing Format with Templates

Show the model exactly what you want by including a fill-in template:

```
Analyze the following product review and fill in this template exactly:

TEMPLATE:
Product: [product name]
Overall Rating: [1-5 stars]
Positive Points:
- [point 1]
- [point 2]
Negative Points:
- [point 1]
- [point 2]
Recommendation: [Buy / Avoid / Research more]

Review:
"The Sony WH-1000XM5 headphones have incredible noise cancellation — the best I've ever experienced. 
Sound quality is rich and detailed. However, the build feels slightly less premium than the previous 
generation, and the carrying case is flimsy. At $349, they're expensive but worth it for frequent travelers."

Fill in the template:
```

---

## Common Format Control Mistakes

| Mistake | Effect | Fix |
|---------|--------|-----|
| Not specifying format at all | Model chooses its own structure | Always specify format explicitly |
| Saying "use JSON" without a schema | Model invents its own keys | Provide the exact key names |
| Asking for a table without column names | Inconsistent columns | Name every column |
| "Brief" without a number | Model decides what "brief" means | "In exactly 50 words" |
| Mixing format with content | Model confuses structure with task | Use clear section labels |

---

*Previous: [Prompt Anatomy ←](./02_prompt_anatomy.md)*  
*Next: [Temperature & Parameters →](./04_temperature_and_parameters.md)*  
*Back to [Topic 1 README](./README.md)*
