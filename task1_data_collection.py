import requests
import json
import time
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (as required)
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords (case-insensitive matching)
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Store collected posts
collected_posts = []

def get_category(title):
    """
    Determine category based on keywords in title
    """
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None  # If no keyword matched


def fetch_json(url):
    """
    Fetch JSON data with error handling
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


# Step 1: Fetch top story IDs
top_story_ids = fetch_json(TOP_STORIES_URL)

if not top_story_ids:
    print("Failed to fetch top stories.")
    exit()

# Limit to first 500 IDs
top_story_ids = top_story_ids[:500]

# Dictionary to track how many posts collected per category
category_counts = {cat: 0 for cat in CATEGORIES}

# Step 2: Fetch story details and categorize
for story_id in top_story_ids:
    # Stop if all categories reached 25 posts
    if all(count >= 25 for count in category_counts.values()):
        break

    story = fetch_json(ITEM_URL.format(story_id))

    if not story:
        continue

    title = story.get("title", "")
    category = get_category(title)

    # Skip if no category matched
    if not category:
        continue

    # Skip if category already has 25 posts
    if category_counts[category] >= 25:
        continue

    # Extract required fields
    post_data = {
        "post_id": story.get("id"),
        "title": title,
        "subreddit": category,  # Assigned category
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by", "unknown"),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    collected_posts.append(post_data)
    category_counts[category] += 1

    # Sleep AFTER finishing each category batch
    if category_counts[category] == 25:
        print(f"Collected 25 posts for category: {category}")
        time.sleep(2)

# Step 3: Save to JSON file
# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# File name with current date
date_str = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date_str}.json"

# Save file
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(collected_posts, f, indent=4)

# Final output
print(f"Collected {len(collected_posts)} posts. Saved to {file_path}")


