# Project: Diary Idea Research

This directory contains a skill for researching niche diary app and journaling web service ideas.

## Local Skills

The following skill is available **only in this directory**:

- **research-diary-idea** (`SKILL.md`): Research tool that mines Reddit, Hacker News, and Qiita
  for user pain points and emerging trends in the diary/journaling space, then synthesizes
  actionable product ideas with feasibility scores.

## Directory Structure

```
research-diary-idea-skills/
├── SKILL.md              # Skill definition (use this skill for diary idea research)
├── CLAUDE.md             # This file
├── .env                  # QIITA_TOKEN (do not commit)
├── scripts/
│   ├── fetch_reddit.py   # Scrapes diary-related Reddit posts
│   ├── fetch_hn.py       # Queries HN Algolia API for journaling posts
│   └── fetch_qiita.py    # Fetches Qiita articles via API v2
├── references/
│   ├── diary-subreddits.md    # Target subreddits + research tips
│   ├── hn-search-guide.md     # HN query terms + interpretation guide
│   ├── qiita-search-guide.md  # Qiita queries + Japan market context
│   ├── scoring-rubric.md      # 5-dimension idea scoring rubric
│   └── report-template.md     # Output report Markdown template
└── reports/
    └── {year}/
        └── {YYYY-MM-DD}/
            └── {HH-MM-SS}.md  # Generated research reports
```

## Usage

Simply ask Claude to research diary app ideas. Claude will:
1. Ask you the target year in Japanese
2. Run all three data sources
3. Synthesize 5–10 product ideas with scores
4. Save a report to `reports/`
