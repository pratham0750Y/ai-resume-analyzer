def make_roadmap(missing_skills, skill_df):
    """Rule-based roadmap: one week per missing skill, using its learning topic."""
    topics = dict(zip(skill_df["skill"], skill_df["learning_topic"]))
    return [f"Week {i}: {topics[s]}" for i, s in enumerate(missing_skills, start=1)]
