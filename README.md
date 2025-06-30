 powerbi dashboard link
 ps://acrobat.adobe.com/id/urn:aaid:sc:VA6C2:d2f919f1-ed41-42b1-931c-dd12ac9d0866

Codeforces Tag Analytics: A User-Specific Problem Recommender System
📌 Project Overview

This project presents a personalized problem recommendation system based on user performance and problem-solving tags from Codeforces. The goal is to analyze submission data and suggest tailored practice problems using intelligent techniques such as tag frequency analysis and cosine similarity. The final recommendations are visualized using a Power BI dashboard.

🧠 Problem Statement

Competitive programmers on platforms like Codeforces often face the challenge of selecting practice problems that match their current skill level. This project aims to automate personalized recommendations based on user profiles built from submission history.

🔧 Technologies & Tools Used

Python: Main language used for scripting, data manipulation, and integration

Requests: For fetching data from the Codeforces API

Pandas: For cleaning, filtering, grouping, and analyzing data

NumPy: For mathematical operations and similarity computations

Codeforces API: To fetch problems, user info, and user submission data

Cosine Similarity (via NumPy): For matching user tag vectors to problem tag vectors

Power BI: For building an interactive dashboard for insights and recommendations

📈 Key Steps (Day-wise Breakdown)

✅ Day 1: Data Collection (Python)

Goal: Collect all Codeforces problems with tags and difficulty ratings

Method:

Used the Codeforces problemset.problems API endpoint

Stored details like contestId, name, tags, rating, solvedCount

Saved results as codeforces_problems.csv

Also: Used user.info API to fetch users and their ratings. Stored in codeforces_users.csv

✅ Day 2: Tag Profiling (Python)

Goal: Build user tag profiles from their past submissions

Method:

Used user.status API to fetch recent problems solved by each user

Extracted all tags from those problems

Counted frequency of each tag per user

Grouped users into: Beginner (1200-1399), Intermediate (1400-1599), Advanced (1600-1799)

Created JSON files: beginner_tags.json, etc.

Output: Clean tag profile datasets for each group

✅ Day 3: Recommendation Engine (Python)

Goal: Recommend problems based on user's tag preferences

Method:

Read in codeforces_problems.csv and tag profiles

For each problem, created a binary tag vector

Created a tag vector for each user group based on tag frequency

Used cosine similarity (manually using dot product & norms) to compute relevance

Filtered problems by appropriate rating range and sorted by similarity score

Exported beginner_recommendations.csv, etc.

Why Cosine Similarity?
It captures how close two tag vectors are in direction (not size), which is perfect for comparing tag preference profiles.

✅ Day 4: Dashboard Creation (Power BI)

Goal: Create a visual, interactive summary of user and tag behavior

Steps:

Imported all CSVs (recommendations, codeforces_users, and tag_profiles)

Built:

Clustered Bar Chart: tag distribution by user group

Donut/Stacked Charts: tag contribution by group

Table: top recommendations with contestId, name, tags, similarity

Legend Table: for interpreting custom tag symbols (optional)

Bonus: Added a page title, slicers, and clean formatting for recruiter-ready visuals

📊 Outputs

codeforces_problems.csv and codeforces_users.csv: Raw data from API

beginner_tags.json, etc.: User tag frequencies

recommendations/beginner.csv, etc.: Final problem recommendations

realistic_tag_profiles.csv: Power BI–ready tag summary

Power BI dashboard: All visualizations in one clean report

🏁 Conclusion

This project demonstrates how data from real-world APIs can be transformed into intelligent, personalized recommendations using vector similarity, user segmentation, and visual analytics. It combines coding, logic, and storytelling — the complete data analyst package.

