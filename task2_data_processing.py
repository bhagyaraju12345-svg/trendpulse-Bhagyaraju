import pandas as pd
import os
import glob

# Step 1 — Find the latest JSON file in the data/ folder
# This avoids hardcoding the filename
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in data/ folder.")
    exit()

# Get the most recent file
latest_file = max(json_files, key=os.path.getctime)

# Load JSON into DataFrame
df = pd.read_json(latest_file)

print(f"Loaded {len(df)} posts from {latest_file}")

# -------------------------------
# Step 2 — Data Cleaning
# -------------------------------

# 1. Remove duplicates based on post_id
before = len(df)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove rows with missing critical values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types
# Convert score and num_comments to integers
df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

# 4. Remove low-quality posts (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Clean whitespace in title column
df["title"] = df["title"].str.strip()

# -------------------------------
# Step 3 — Save Clean Data
# -------------------------------

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# Save as CSV
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# -------------------------------
# Summary — Posts per subreddit
# -------------------------------
print("\nPosts per subreddit:")
print(df["subreddit"].value_counts())
