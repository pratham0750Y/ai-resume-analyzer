import re

def find_skills(clean_resume, skill_df):
    """Return the list of dictionary skills that appear in the cleaned resume text."""
    found = []
    for skill in skill_df["skill"]:
        
        pattern = r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])"
        if re.search(pattern, clean_resume):
            found.append(skill)
    return found
