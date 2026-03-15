#!/usr/bin/env python3
"""
fetch_reddit.py - Fetch posts from diary/journaling-related subreddits using Reddit's public JSON API.

Usage:
    python scripts/fetch_reddit.py --year 2025 --output /tmp/reddit_raw.json
    python scripts/fetch_reddit.py --year 2025 --limit 50 --output /tmp/reddit_raw.json

No authentication required (uses Reddit's public JSON API).
"""

import argparse
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta


DIARY_SUBREDDITS = [
    "Journaling",
    "bulletjournal",
    "bujo",
    "Diary",
    "journalchallenge",
    "selfimprovement",
    "getdisciplined",
    "productivity",
    "Mindfulness",
    "ADHD",
    "DecidingToBeBetter",
    "TheGirlSurvivalGuide",
    "mentalhealth",
    "lifehacks",
    "nosurf",
]

# Flairs and keywords that signal pain points
PAIN_SIGNAL_KEYWORDS = [
    "help", "advice", "question", "rant", "frustrated", "can't find",
    "looking for", "recommendation", "issue", "problem", "struggle",
    "disappointed", "wish", "need", "overwhelmed", "confused",
    "how do", "suggest", "tips", "anyone else", "stopped", "quit", "gave up",
]

# Diary/journaling relevance keywords — used to filter noise from broad subreddits
DIARY_RELEVANCE_KEYWORDS = [
    "journal", "journaling", "diary", "habit", "daily", "writing", "note",
    "reflection", "mood", "tracking", "bullet", "log", "streak", "entry",
    "bujo", "planner", "routine", "morning pages", "gratitude", "mindful",
]

# Subreddits where almost all posts are diary-relevant (no extra filtering needed)
DIARY_CORE_SUBREDDITS = {
    "Journaling", "bulletjournal", "bujo", "Diary", "journalchallenge",
}

HEADERS = {
    "User-Agent": "DiaryIdeaResearch/1.0 (educational research tool)",
}


def compute_filter_year_range(target_year: int) -> tuple[int, int]:
    """
    Return (start_timestamp, end_timestamp) for client-side year filtering.

    If target_year == current year (year not yet complete), use past 12 months from today.
    If target_year < current year (full year has passed), use Jan 1 to Dec 31 of that year.
    """
    now = datetime.now(timezone.utc)
    current_year = now.year

    if target_year >= current_year:
        end_dt = now
        start_dt = now - timedelta(days=365)
    else:
        start_dt = datetime(target_year, 1, 1, tzinfo=timezone.utc)
        end_dt = datetime(target_year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

    return int(start_dt.timestamp()), int(end_dt.timestamp())


def fetch_subreddit_posts(subreddit: str, limit: int = 25, sort: str = "top",
                          target_year: int | None = None) -> list[dict]:
    """Fetch posts from a subreddit using Reddit's public JSON API.

    When target_year is the current year (not yet complete), uses t=year (past 12 months).
    For past years, uses t=all and applies client-side filtering.
    """
    current_year = datetime.now(timezone.utc).year
    time_filter = "year" if target_year is None or target_year >= current_year - 1 else "all"
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}&t={time_filter}"
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            posts = data.get("data", {}).get("children", [])
            return [p["data"] for p in posts]
    except Exception as e:
        print(f"  Warning: Failed to fetch r/{subreddit}: {e}")
        return []


def is_diary_relevant(post: dict, subreddit: str) -> bool:
    """Check if a post is relevant to diary/journaling.

    Posts from core journaling subreddits are always relevant.
    Posts from broader subreddits (productivity, lifehacks) are filtered by keywords.
    """
    if subreddit in DIARY_CORE_SUBREDDITS:
        return True
    title = post.get("title", "").lower()
    selftext = post.get("selftext", "").lower()
    return any(kw in title or kw in selftext for kw in DIARY_RELEVANCE_KEYWORDS)


def is_pain_point(post: dict) -> bool:
    """Heuristic: does this post signal a user pain point?"""
    title = post.get("title", "").lower()
    flair = (post.get("link_flair_text") or "").lower()
    return any(kw in title or kw in flair for kw in PAIN_SIGNAL_KEYWORDS)


def filter_by_range(post: dict, start_ts: int, end_ts: int) -> bool:
    """Filter posts within the given timestamp range."""
    created = post.get("created_utc", 0)
    return start_ts <= created <= end_ts


def score_post(post: dict) -> int:
    """Simple engagement score combining upvotes and comment count."""
    return post.get("score", 0) + post.get("num_comments", 0) * 3


def main():
    parser = argparse.ArgumentParser(description="Fetch diary/journaling subreddit posts for idea research")
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year for filtering posts (default: current year)")
    parser.add_argument("--limit", type=int, default=25,
                        help="Max posts to fetch per subreddit (default: 25)")
    parser.add_argument("--output", type=str, default="/tmp/reddit_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--subreddits", type=str, default=None,
                        help="Comma-separated subreddit list (default: built-in diary list)")
    args = parser.parse_args()

    subreddits = args.subreddits.split(",") if args.subreddits else DIARY_SUBREDDITS
    target_year = args.year

    start_ts, end_ts = compute_filter_year_range(target_year)
    from datetime import datetime as _dt
    start_label = _dt.fromtimestamp(start_ts, tz=timezone.utc).strftime("%Y-%m-%d")
    end_label = _dt.fromtimestamp(end_ts, tz=timezone.utc).strftime("%Y-%m-%d")
    print(f"Date range: {start_label} to {end_label}")
    print(f"Fetching posts from {len(subreddits)} subreddits...")

    all_posts = []
    pain_posts = []

    for sub in subreddits:
        print(f"  Fetching r/{sub}...")
        posts = fetch_subreddit_posts(sub, limit=args.limit, sort="top", target_year=target_year)

        for post in posts:
            if not filter_by_range(post, start_ts, end_ts):
                continue

            # Filter out non-diary posts from broad subreddits
            if not is_diary_relevant(post, sub):
                continue

            entry = {
                "subreddit": sub,
                "title": post.get("title", ""),
                "selftext": post.get("selftext", "")[:500],
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "flair": post.get("link_flair_text", ""),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "created_utc": post.get("created_utc", 0),
                "engagement_score": score_post(post),
                "is_pain_point": is_pain_point(post),
            }
            all_posts.append(entry)
            if entry["is_pain_point"]:
                pain_posts.append(entry)

        time.sleep(1)  # be polite to Reddit's API

    # Sort by engagement
    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    pain_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(all_posts),
        "pain_point_posts": len(pain_posts),
        "subreddits_searched": subreddits,
        "top_pain_points": pain_posts[:50],
        "all_posts": all_posts[:100],
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Fetched {len(all_posts)} posts, {len(pain_posts)} flagged as pain points.")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
