import requests
import pandas as pd
import time
import os
import json

# Create 'data' folder if missing
os.makedirs("data/tags", exist_ok=True)

# Load users from Day 1
df = pd.read_csv("data/codeforces_users.csv")

# Rating Brackets
beginner = df[(df['rating'] >= 1200) & (df['rating'] < 1400)].head(20)  # batch of 20
intermediate = df[(df['rating'] >= 1400) & (df['rating'] < 1600)].head(20)
advanced = df[(df['rating'] >= 1600) & (df['rating'] < 1800)].head(20)

# Fetch tags from submissions

def fetch_tags_from_submissions(user_list, bracket_name):
    all_tags = {}
    for handle in user_list['handle']:
        print(f"🔍 Fetching {bracket_name} tags for: {handle}")
        try:
            url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=100"
            res = requests.get(url)
            data = res.json()
            if data['status'] != 'OK':
                continue

            submissions = data['result']
            tags_set = set()

            for sub in submissions:
                problem = sub.get('problem', {})
                tags = problem.get('tags', [])
                tags_set.update(tags)

            all_tags[handle] = list(tags_set)
        except Exception as e:
            print(f"⚠️ Failed for {handle}: {e}")
            continue

        time.sleep(1.2)  # Increased delay to avoid rate limits

    # Save tags as JSON
    with open(f"data/tags/{bracket_name}_tags.json", "w") as f:
        json.dump(all_tags, f)

    print(f"✅ Saved {bracket_name} tag profile with {len(all_tags)} users.\n")

# Run in batches of 20 each
print(f"👶 Beginner Users: {len(beginner)}")
print(f"🧠 Intermediate Users: {len(intermediate)}")
print(f"💪 Advanced Users: {len(advanced)}")

fetch_tags_from_submissions(beginner, "beginner")
fetch_tags_from_submissions(intermediate, "intermediate")
fetch_tags_from_submissions(advanced, "advanced")


