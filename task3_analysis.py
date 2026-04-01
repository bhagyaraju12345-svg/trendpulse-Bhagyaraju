import pandas as pd
import numpy as np
import os

# -------------------------------
# Step 1 — Load and Explore Data
# -------------------------------

file_path = "data/trends_clean.csv"

# Check if file exists
if not os.path.exists(file_path):
    print("File not found. Please run Task 2 first.")
    exit()

# Load CSV into DataFrame
df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}")

# Display first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate averages using pandas
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {int(avg_score)}")
print(f"Average comments: {int(avg_comments)}")

# -------------------------------
# Step 2 — Analysis with NumPy
# -------------------------------

scores = df["score"].values
comments = df["num_comments"].values

print("\n--- NumPy Stats ---")

# Mean, Median, Standard Deviation
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print(f"Mean score   : {int(mean_score)}")
print(f"Median score : {int(median_score)}")
print(f"Std deviation: {int(std_score)}")

# Max and Min
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Subreddit with most posts
subreddit_counts = df["subreddit"].value_counts()
top_subreddit = subreddit_counts.idxmax()
top_count = subreddit_counts.max()

print(f"\nMost posts from: {top_subreddit} ({top_count} posts)")

# Post with most comments
max_comments_index = np.argmax(comments)
top_post_title = df.iloc[max_comments_index]["title"]
top_post_comments = comments[max_comments_index]

print(f'\nMost commented post: "{top_post_title}" — {top_post_comments} comments')

# -------------------------------
# Step 3 — Add New Columns
# -------------------------------

# Engagement = comments per upvote (avoid division by zero using +1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if score > average score
df["is_popular"] = df["score"] > avg_score

# -------------------------------
# Step 4 — Save the Result
# -------------------------------

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
