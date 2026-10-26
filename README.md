# AI Resume Analyzer and Job Recommendation System

Upload a PDF/DOCX resume, pick a target job role, and get: extracted skills, match score for 5 roles,
top-3 role recommendations, missing skills and a weekly learning roadmap.

## Run
```
pip install -r requirements.txt
streamlit run app.py
```

## How it works (one function per step)
| Step | File | Function | What it does |
|---|---|---|---|
| 1 | resume_parser.py | extract_text | Reads text from PDF (pypdf) or DOCX (python-docx) |
| 2 | text_cleaner.py | clean_text | Lowercase, remove symbols, keep c++ / c# / .net |
| 3 | skill_extractor.py | find_skills | Searches the text for skills listed in data/skill_dictionary.csv |
| 4 | job_matcher.py | match_roles | TF-IDF + cosine similarity between resume skills and each role's skills |
| 5 | roadmap_generator.py | make_roadmap | One week per missing skill |
| 6 | llm_feedback.py | ask_ai | Sends the skill results + your question to the AI model and returns advice |
| - | app.py | - | Streamlit page that calls the functions in order |

Missing skills = role's required skills that were not found in the resume (a list comprehension in app.py).

## Datasets
* `data/skill_dictionary.csv` - 36 skills with category and learning topic
* `data/job_roles.csv` - 5 roles with required skills (separated by `|`)

## Limitations
Keyword matching misses synonyms and skills not in the dictionary; scanned PDFs are not supported;
scores are estimates, not recruiter decisions.

## AI feedback (developer setup)
The app uses Google Gemini behind the scenes; users just see "Ask AI" and never enter a key.
1. Get a free API key at https://aistudio.google.com/apikey
2. Open the `.env` file and set `GEMINI_API_KEY=your_key_here`
3. Run the app. Only skills, role and score are sent to the AI, never the resume text.

The model name is one line in `llm_feedback.py` (`MODEL`) - change it if Google retires the model.
Never upload your real `.env` to GitHub (it is already listed in `.gitignore`).
