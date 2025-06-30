import requests
import pandas as pd
import time
import os

# 🔹 Create 'data' folder if missing
os.makedirs("data", exist_ok=True)

# 🔹 Step 1: Fetch All Problems with Tags & Difficulty
def fetch_problems():
    url = "https://codeforces.com/api/problemset.problems"
    res = requests.get(url)
    data = res.json()

    problems = data['result']['problems']
    stats = data['result']['problemStatistics']

    problem_list = []
    for p, s in zip(problems, stats):
        if 'rating' in p:  # only keep problems with difficulty
            problem_list.append({
                'contestId': p.get('contestId'),
                'index': p.get('index'),
                'name': p.get('name'),
                'tags': p.get('tags'),
                'rating': p.get('rating'),
                'solvedCount': s.get('solvedCount')
            })

    df = pd.DataFrame(problem_list)
    df.to_csv('data/codeforces_problems.csv', index=False)
    print(f"✅ Saved {len(df)} problems to CSV")
    return df

# 🔹 Step 2: Fetch User Info (Rating + Handle)
def fetch_user_info(handles):
    all_users = []
    for handle in handles:
        url = f"https://codeforces.com/api/user.info?handles={handle}"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                user = res.json()['result'][0]
                all_users.append({
                    'handle': user.get('handle'),
                    'rating': user.get('rating', 0),
                    'maxRating': user.get('maxRating', 0),
                    'rank': user.get('rank', 'unrated'),
                    'maxRank': user.get('maxRank', 'unrated'),
                    'contribution': user.get('contribution', 0),
                })
        except:
            continue
        time.sleep(0.5)  # avoid API spam

    df = pd.DataFrame(all_users)
    df.to_csv('data/codeforces_users.csv', index=False)
    print(f"✅ Saved {len(df)} users to CSV")
    return df

# 🔹 Dynamic Handle Fetcher from Codeforces API
def get_handles_by_rating(min_rating=1200, max_rating=1800, max_users=80):
    url = "https://codeforces.com/api/user.ratedList?activeOnly=true"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()['result']
            filtered = [
                user['handle'] for user in data
                if 'rating' in user and min_rating <= user['rating'] <= max_rating
            ]
            return filtered[:max_users]
    except:
        print("⚠️ Could not fetch handles")
    return []

# 🔹 Run all steps
if __name__ == "__main__":
    print("🚀 Fetching problems...")
    fetch_problems()

    print("🧠 Fetching user handles in range 1200–1800...")
    print("🧠 Fetching 40 users per rating bracket...")

    beginner_handles = get_handles_by_rating(1200, 1399, 40)
    intermediate_handles = get_handles_by_rating(1400, 1599, 40)
    advanced_handles = get_handles_by_rating(1600, 1799, 40)

    sample_handles = beginner_handles + intermediate_handles + advanced_handles

    print(f"✅ Fetched {len(sample_handles)} handles total.")

    print(f"✅ Fetched {len(sample_handles)} handles.")

    print("🚀 Fetching user data...")
    fetch_user_info(sample_handles)
    df = pd.read_csv("data/codeforces_users.csv")
    print("📊 Rating Summary:")
    print("Beginner:", len(df[(df['rating'] >= 1200) & (df['rating'] < 1400)]))
    print("Intermediate:", len(df[(df['rating'] >= 1400) & (df['rating'] < 1600)]))
    print("Advanced:", len(df[(df['rating'] >= 1600) & (df['rating'] < 1800)]))



