import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os

INPUT_FILE = "job_postings_sample.csv"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# Clean text fields
for col in ["job_title", "city", "skills"]:
    df[col] = df[col].fillna("").astype(str).str.strip()

# Convert comma-separated skills into individual rows
skill_rows = []
for _, row in df.iterrows():
    skills = [skill.strip().title() for skill in row["skills"].split(",") if skill.strip()]
    for skill in skills:
        skill_rows.append({
            "job_title": row["job_title"],
            "city": row["city"],
            "skill": skill
        })

skills_df = pd.DataFrame(skill_rows)
skills_df.to_csv(os.path.join(OUTPUT_DIR, "cleaned_skill_data.csv"), index=False)

# Top 10 skills overall
top_skills = skills_df["skill"].value_counts().head(10)
top_skills.to_csv(os.path.join(OUTPUT_DIR, "top_10_skills.csv"))

plt.figure(figsize=(10, 6))
top_skills.sort_values().plot(kind="barh")
plt.title("Top 10 In-Demand Skills")
plt.xlabel("Number of Job Postings")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "top_10_skills.png"))
plt.close()

# Skill demand by city
city_skill = pd.crosstab(skills_df["city"], skills_df["skill"])
city_skill.to_csv(os.path.join(OUTPUT_DIR, "skill_vs_city_matrix.csv"))

plt.figure(figsize=(14, 7))
plt.imshow(city_skill, aspect="auto")
plt.colorbar(label="Skill Mentions")
plt.xticks(range(len(city_skill.columns)), city_skill.columns, rotation=75)
plt.yticks(range(len(city_skill.index)), city_skill.index)
plt.title("Skill Demand Heatmap by City")
plt.xlabel("Skills")
plt.ylabel("City")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "skill_city_heatmap.png"))
plt.close()

# Skill vs role matrix
role_skill = pd.crosstab(skills_df["job_title"], skills_df["skill"])
role_skill.to_csv(os.path.join(OUTPUT_DIR, "skill_vs_role_matrix.csv"))

plt.figure(figsize=(14, 6))
plt.imshow(role_skill, aspect="auto")
plt.colorbar(label="Skill Mentions")
plt.xticks(range(len(role_skill.columns)), role_skill.columns, rotation=75)
plt.yticks(range(len(role_skill.index)), role_skill.index)
plt.title("Skill vs Role Matrix")
plt.xlabel("Skills")
plt.ylabel("Job Role")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "skill_role_matrix.png"))
plt.close()

# Job demand by role and city
role_demand = df["job_title"].value_counts()
city_demand = df["city"].value_counts()
role_demand.to_csv(os.path.join(OUTPUT_DIR, "role_demand.csv"))
city_demand.to_csv(os.path.join(OUTPUT_DIR, "city_demand.csv"))

# Simple recommendations based on the dataset
recommendations = []
for skill, count in top_skills.items():
    recommendations.append(
        f"Develop {skill}: it appears in {count} skill mentions in this dataset."
    )

with open(os.path.join(OUTPUT_DIR, "job_demand_recommendation.txt"), "w", encoding="utf-8") as f:
    f.write("Job Demand Recommendations\n")
    f.write("==========================\n\n")
    for item in recommendations:
        f.write("- " + item + "\n")

print("Analysis completed successfully.")
print("Check the outputs folder for CSV files and visuals.")
