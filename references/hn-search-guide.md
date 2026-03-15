# Hacker News Search Guide — Diary & Journaling

This file documents the HN search queries used by `fetch_hn.py` and explains how to interpret results for diary/journaling idea research.

---

## Built-in Query List

These queries are used by default in `fetch_hn.py`:

| Query | What it surfaces |
|-------|-----------------|
| `journaling app` | Show HN / Ask HN about journaling tools, often includes honest UX feedback |
| `diary app` | Direct discussions about personal diary software |
| `habit tracker` | Apps for tracking daily behaviors (often paired with journaling) |
| `daily journal` | Discussions about daily writing practice |
| `reflection app` | Retrospective / review tools — strong signal for journaling UX ideas |
| `mood tracking` | Emotional state tracking apps — adjacent to diary functionality |
| `life logging` | Quantified self / lifelogging discussions |
| `bullet journal digital` | Demand for digital BuJo experiences |
| `personal knowledge management` | PKM — note-taking tools with diary overlap (Obsidian, Logseq, etc.) |
| `second brain app` | Zettelkasten / knowledge base tools with diary workflow overlap |
| `note taking app` | Broad note-taking — filter for personal/daily use |
| `self improvement app` | Behavior change apps with journaling components |
| `daily note` | Obsidian/Logseq "daily note" pattern — strong tech user signal |
| `gratitude journal` | Specific journaling format with proven retention |
| `writing habit` | Habit-formation around writing — pain points around consistency |
| `journaling productivity` | Intersection of journaling and productivity workflows |
| `mental health journaling` | Therapeutic journaling apps — regulation/ethics considerations |
| `AI journal` | LLM-enhanced diary applications — hot emerging area |
| `PKM app` | Personal Knowledge Management — broad but overlapping audience |

---

## Interpreting HN Results

### High-value post types

- **Show HN**: Developers launching diary/journaling tools. Check comment criticism carefully — HN users are direct about UX problems.
- **Ask HN**: "What journaling app do you use?" threads are gold — aggregated user frustrations and requirements.
- **Discussion threads** with 50+ comments about productivity tools usually contain deep debate about what existing apps get wrong.

### Signals to look for

- Posts where the top comment says "I tried X but quit because..."
- Feature requests in comment threads (users describing their ideal tool)
- Developers mentioning they built their own tool because nothing else fit
- Discussions about privacy, local-first, or offline-only as requirements

### Filtering notes

The `diary_relevant` field in the output uses keyword matching. Some posts about "daily notes" might be general note-taking (Obsidian workflow discussions) rather than personal diary — use judgment when reviewing.

---

## Supplemental Queries (run manually if needed)

If standard queries return sparse results for a given year:

```
"Ask HN: journaling"
"Show HN: diary"
"personal CRM"
"digital minimalism journal"
"offline first notes"
"local first journal"
```
