import pandas as pd
import os
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load problems
df = pd.read_csv("data/codeforces_problems.csv")
df = df[df['rating'].between(1200, 1800)]  # filter only rated problems

# Combine tag list into string for vectorizer
df['tag_str'] = df['tags'].apply(lambda x: " ".join(eval(x)))

# Vectorize tags
vectorizer = CountVectorizer()
tag_vectors = vectorizer.fit_transform(df['tag_str'])

# Load user tag profiles
tag_profiles = {
    "beginner": "data/tags/beginner_tags.json",
    "intermediate": "data/tags/intermediate_tags.json",
    "advanced": "data/tags/advanced_tags.json",
}

# Output folder
os.makedirs("data/recommendations", exist_ok=True)

print("\U0001F4E6 Loading data...")

for level, path in tag_profiles.items():
    if not os.path.exists(path):
        print(f"⚠️ Tag profile for {level} not found: skipping.")
        continue

    with open(path) as f:
        user_tags = json.load(f)

    # Count tags for all users in bracket
    tag_count = {}
    for tags in user_tags.values():
        for tag in tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1

    if not tag_count:
        print(f"⚠️ No tag matches found for {level} — skipping recommendations.")
        continue

    # Build tag profile string
    top_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:30]  # top 30 tags
    profile_tags = [tag for tag, _ in top_tags]
    profile_str = " ".join(profile_tags)

    print(f"\n🚀 Generating Recommendations for {level.title()} Users...")

    # Compute cosine similarity between profile and problems
    profile_vec = vectorizer.transform([profile_str])
    similarities = cosine_similarity(profile_vec, tag_vectors).flatten()

    df['similarity'] = similarities

    # Filter by rating range
    if level == "beginner":
        filtered = df[df['rating'].between(1200, 1399)]
    elif level == "intermediate":
        filtered = df[df['rating'].between(1400, 1599)]
    else:
        filtered = df[df['rating'].between(1600, 1799)]

    # Only keep problems that share at least 1 tag
    filtered = filtered[filtered['tags'].apply(lambda x: len(set(eval(x)).intersection(set(profile_tags))) > 0)]

    if filtered.empty:
        print(f"⚠️ No tag matches found — using all problems in rating range.")
        filtered = df[df['rating'].between(1200, 1799)]

    recs = filtered.sort_values(by="similarity", ascending=False).head(10)

    print(f"\n{level.title()} Recommendations:")
    print(recs[["contestId", "index", "name", "rating", "tags", "similarity"]])

    # Save
    recs.to_csv(f"data/recommendations/{level}_recommendations.csv", index=False)

print("\n✅ All recommendations saved in 'data/recommendations/' folder.")


