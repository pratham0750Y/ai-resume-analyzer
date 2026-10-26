import pandas as pd
import streamlit as st

from resume_parser import extract_text
from text_cleaner import clean_text
from skill_extractor import find_skills
from job_matcher import match_roles
from roadmap_generator import make_roadmap
from llm_feedback import ask_ai

st.title("AI Resume Analyzer and Job Recommendation System")

# Load the two CSV datasets
skill_df = pd.read_csv("data/skill_dictionary.csv")
roles_df = pd.read_csv("data/job_roles.csv")

# 1. Upload resume and choose target role
file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
target = st.selectbox("Target role", roles_df["role"])

if file is not None:
    st.write("Uploaded file:", file.name)

    # 2. Pipeline: extract -> clean -> find skills -> match roles
    raw_text = extract_text(file)
    clean = clean_text(raw_text)
    found = find_skills(clean, skill_df)
    ranking = match_roles(found, roles_df)

    # 3. Skills found
    st.subheader("Skills found")
    st.write(", ".join(found) if found else "No skills found")

    # 4. Match score chart + top 3 roles
    st.subheader("Match score for each role")
    st.bar_chart(ranking.set_index("role"))
    st.subheader("Top 3 recommended roles")
    for i, row in ranking.head(3).iterrows():
        st.write(f"{i + 1}. {row['role']} - {row['match_score']}%")

    # 5. Missing skills for the target role
    required = roles_df[roles_df["role"] == target]["required_skills"].iloc[0].split("|")
    missing = [s for s in required if s not in found]
    st.subheader(f"Missing skills for {target}")
    st.write(", ".join(missing) if missing else "None - you have all required skills!")

    # 6. Learning roadmap
    st.subheader("Suggested learning roadmap")
    roadmap = make_roadmap(missing, skill_df)
    for step in roadmap:
        st.write(step)

    # 7. Downloadable report (plain text)
    score = ranking[ranking["role"] == target]["match_score"].iloc[0]
    report = (f"Target role: {target}\nMatch score: {score}%\n"
              f"Skills found: {', '.join(found)}\nMissing skills: {', '.join(missing)}\n"
              + "\n".join(roadmap))
    st.download_button("Download report", report, file_name="report.txt")

    # 8. AI feedback: answers a question using the analysis results
    st.subheader("Ask AI")
    question = st.text_input("Your question", value="How can I improve my resume for this role?")

    if st.button("Get AI answer"):
        # Only the skill results are sent to the AI - not the resume text or personal details
        prompt = (
            "You are a friendly career coach for students. Use ONLY the information below.\n"
            f"Target role: {target}\nMatch score (an estimate): {score}%\n"
            f"Skills found in resume: {', '.join(found)}\n"
            f"Missing required skills: {', '.join(missing) or 'none'}\n\n"
            f"Student question: {question}\n\n"
            "Answer in under 150 words with clear, practical steps. Do not judge age, gender or other "
            "personal traits. Remind them a missing keyword does not always mean missing ability."
        )
        with st.spinner("AI is thinking..."):
            try:
                answer = ask_ai(prompt)
                if answer is None:
                    st.warning("AI feedback is not set up yet. Add the API key to the .env file.")
                else:
                    st.write(answer)
            except Exception as e:
                st.error(f"AI error: {e}")

    st.caption("Match scores are estimates for learning guidance only, not hiring decisions. "
               "Missing keywords do not always mean missing ability. It just may not be in your resume")
