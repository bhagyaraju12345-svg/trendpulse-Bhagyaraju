import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Step 1 — Setup
# -------------------------------

file_path = "data/trends_analysed.csv"

# Check if file exists
if not os.path.exists(file_path):
    print("File not found. Please run Task 3 first.")
    exit()

# Load data
df = pd.read_csv(file_path)

# Create outputs folder if it doesn't exist
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Helper function to shorten long titles
def shorten_title(title, max_len=50):
    return title[:max_len] + "..." if len(title) > max_len else title

# -------------------------------
# Chart 1 — Top 10 Posts by Score
# -------------------------------

top_posts = df.sort_values(by="score", ascending=False).head(10)

titles = [shorten_title(t) for t in top_posts["title"]]
scores = top_posts["score"]

plt.figure()
plt.barh(titles, scores)
plt.xlabel("Score")
plt.ylabel("Post Title")
plt.title("Top 10 Posts by Score")
plt.gca().invert_yaxis()  # highest score on top

plt.tight_layout()
plt.savefig("outputs/chart1_top_posts.png")
plt.close()

# -------------------------------
# Chart 2 — Posts per Subreddit
# -------------------------------

subreddit_counts = df["subreddit"].value_counts()

plt.figure()
plt.bar(subreddit_counts.index, subreddit_counts.values)
plt.xlabel("Subreddit")
plt.ylabel("Number of Posts")
plt.title("Posts per Subreddit")

plt.tight_layout()
plt.savefig("outputs/chart2_subreddits.png")
plt.close()

# -------------------------------
# Chart 3 — Score vs Comments
# -------------------------------

# Separate popular and non-popular posts
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure()
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# -------------------------------
# Bonus — Dashboard
# -------------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 (Dashboard)
axes[0].barh(titles, scores)
axes[0].set_title("Top Posts")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# Chart 2 (Dashboard)
axes[1].bar(subreddit_counts.index, subreddit_counts.values)
axes[1].set_title("Subreddit Count")
axes[1].set_xlabel("Subreddit")
axes[1].set_ylabel("Posts")

# Chart 3 (Dashboard)
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

# Overall title
fig.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("Charts saved successfully in outputs/ folder.")
