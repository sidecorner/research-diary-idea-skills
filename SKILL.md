---
name: research-diary-idea
description: >
  Research and surface niche opportunity ideas for diary apps and journaling web services
  that people can maintain effortlessly. Use this skill whenever you want to identify
  underserved user needs, pain points, or trending topics in the journaling, habit tracking,
  daily writing, or personal reflection space. Mines Reddit journaling communities, Hacker News,
  and Qiita for real user frustrations and developer insights. Outputs a structured report
  scoring each idea on feasibility, development time, profitability, competitive advantage,
  and small-team suitability.

  ALWAYS trigger this skill when the user mentions: diary app ideas, journaling service gaps,
  habit tracker opportunities, personal writing app research, low-pressure diary tools,
  life logging ideas, reflection app concepts, or any request to "find diary ideas from
  Reddit/HN/Qiita". Also trigger for requests like "find a niche product idea" or
  "research underserved markets" when the context involves personal journaling, daily writing,
  mood tracking, or self-improvement apps.
---

# Diary Idea Research Skill

You help product creators, indie hackers, and entrepreneurs discover validated, niche app or web
service ideas for people who want to keep a diary or journal effortlessly. You do this by
systematically mining Reddit journaling communities, Hacker News, and Qiita for real user pain
points, then scoring each idea so the user can quickly prioritize what to build.

The guiding spirit: find ideas for tools that feel *light and forgiving* — things people can
actually stick with.

## Step 1: Confirm the Target Year

**If the user has already specified a year** (e.g., "2025年を調査して" or "for 2024"), extract it
directly and skip asking. Otherwise, **ask in Japanese before doing anything else:**

> 調査対象の年号を教えてください（例：2025年）。
> 未入力の場合は現在の年（{CURRENT_YEAR}）を使用します。

If the user skips, types "skip", or enters nothing meaningful, use the current calendar year.
Save this as `TARGET_YEAR`.

**Date range logic (apply to all data sources):**

- If `TARGET_YEAR` >= current year (year not yet complete) → search the **past 12 months from today**
  - Example: Running in March 2026 with `TARGET_YEAR=2026` → search 2025-03 to 2026-03
- If `TARGET_YEAR` < current year (full year has passed) → search **Jan 1 to Dec 31** of that year

## Step 2: Gather Data

Run all three sources in parallel to save time.

### 2a. Reddit — Journaling Community Pain Points

Use `scripts/fetch_reddit.py` to scrape posts from the subreddits listed in
`references/diary-subreddits.md`. Focus on:

- Posts where users describe giving up on journaling apps or habits
- Flairs like "Help", "Question", "Rant", "Advice Needed"
- Recurring themes across multiple subreddits (cross-community signal = strong unmet need)
- Language patterns: "I wish it had X", "Why doesn't any app do Y", "I stopped because..."

```bash
python scripts/fetch_reddit.py --year TARGET_YEAR --output /tmp/reddit_raw.json
```

Parse the output and group posts by theme (e.g., "consistency/guilt", "privacy concerns",
"too complex", "ADHD friendliness", "no guilt for missing days").

### 2b. Hacker News — Tech-Forward Journaling Discussions

Use `scripts/fetch_hn.py` to query the Algolia HN Search API for journaling-related threads.
Focus on posts with 10+ points or 5+ comments. See `references/hn-search-guide.md` for
recommended query terms.

```bash
python scripts/fetch_hn.py --year TARGET_YEAR --output /tmp/hn_raw.json
```

Look for: Show HN posts about journaling/diary tools, Ask HN threads about personal writing
habits, discussions of tools like Obsidian/Logseq/Day One and what they're missing, and
threads about "local-first" or "privacy-first" note apps.

### 2c. Qiita — Japanese Developer Perspective

Use `scripts/fetch_qiita.py` to search Qiita for Japanese diary/journaling articles.
This surfaces Japanese market-specific pain points and developer activity invisible in English
sources. Requires `QIITA_TOKEN` in `.env`. See `references/qiita-search-guide.md` for
query terms and Japanese market nuances.

```bash
python scripts/fetch_qiita.py --year TARGET_YEAR --output /tmp/qiita_raw.json
```

Look for: personal projects developers built because existing diary apps didn't fit their
needs, articles about habit-formation around journaling, and UX complaints about mainstream
apps from Japanese users (simplicity, privacy, handwriting feel).

## Step 3: Synthesize Ideas

From the raw data, extract 5–10 **specific, actionable product ideas**. A good idea:

- Addresses a **repeatedly mentioned** frustration (not a one-off complaint)
- Fits the "light and forgiving" philosophy — low friction, no guilt design
- Can be scoped to a small team (see `references/scoring-rubric.md`)
- Has a clear user action (write, track, reflect, review, share, etc.)

For each idea, write:
- **Title**: Short product concept name
- **Problem**: What pain it solves (quote real user language where possible)
- **Solution concept**: What the app/service does
- **Evidence**: Number/examples of Reddit posts + HN threads + Qiita articles mentioning this pain

Cross-platform signal (Reddit + HN + Qiita) is the strongest validation. Ideas appearing in
all three sources — especially with both English and Japanese interest — are strong candidates
for Japan-market-focused apps.

## Step 4: Score Each Idea

Apply the 5-dimension scoring from `references/scoring-rubric.md` to each idea.
Be honest — a score of 3 is not a failure, it's useful calibration.

The five dimensions are:
1. **実現可能性** (Feasibility) — can it actually be built?
2. **開発期間** (Development Time) — how long to MVP for a solo/small team?
3. **収益性** (Revenue Potential) — can it make money within 18 months?
4. **競合優位性** (Competitive Advantage) — is there a defensible angle?
5. **小規模開発適性** (Small Team Suitability) — can 1–3 people run it sustainably?

## Step 5: Save the Report

Save the report to:

```
reports/{TARGET_YEAR}/{YYYY-MM-DD}/{HH-MM-SS}.md
```

Use the template in `references/report-template.md`. Create parent directories as needed.

After saving, tell the user the file path so they can find it easily.

## Step 6: Post-Execution Review and Auto-Improvement

After saving the report, review the entire execution for bugs, errors, and improvement opportunities.

### 6a. Check Script Execution Results

Review the output from all three fetch scripts:

- Were there any errors or warnings in the script output?
- Did any scripts return 0 results (possible API failure, rate limit, or query issue)?
- Were there HTTP errors, timeouts, or unexpected exceptions?
- Did the date range filtering work correctly?

If a script failed silently (no error but sparse/empty data), note it in the report and flag it
for manual follow-up.

### 6b. Identify Bugs and Improvement Opportunities

Check the following areas:

**Scripts (`scripts/`):**
- Off-by-one errors in date range calculation
- Missing or incorrect error handling
- Queries that consistently return 0 results (consider updating `DIARY_QUERIES`)
- Encoding issues with non-ASCII characters (especially Qiita Japanese output)
- Rate limiting: did any API return 429 or similar? Adjust `time.sleep()` if needed

**References (`references/`):**
- Are subreddit lists in `diary-subreddits.md` still active/relevant?
- Do HN query terms in `hn-search-guide.md` still surface meaningful results?
- Is the scoring rubric in `scoring-rubric.md` still well-calibrated?

**SKILL.md:**
- Were any instructions unclear or missing that caused problems during execution?
- Should any step be reordered or clarified?

### 6c. Apply Fixes

If bugs or clear improvements are found:

1. Fix script bugs directly in `scripts/`
2. Update reference files in `references/` if query lists or rubrics need refreshing
3. Update `SKILL.md` if the workflow itself needs clarification
4. Update `CLAUDE.md` if the directory structure or usage instructions changed

For each fix, briefly note what was changed and why (inline comment or commit message level).

### 6d. Update Documentation

After any changes, check if the following documents need updating:

- **`README.md`** (if it exists): update usage examples, script options, or output format
- **`CLAUDE.md`**: update directory structure or usage notes if files were added/removed
- **`references/`**: update any guide that references outdated behavior

If `README.md` does not exist and meaningful changes were made, create a minimal one covering:
setup, usage, and output format.

### 6e. Report to User

Tell the user:
- What was checked
- What (if anything) was fixed
- What (if anything) was left as a known limitation with a suggested follow-up

If nothing needed fixing, say so explicitly — "No issues found."

---

## Notes on quality

- Prefer ideas with evidence from **multiple sources** — cross-platform signal is stronger.
- Ideas with both English (Reddit/HN) and Japanese (Qiita) signal are especially strong for
  Japan-focused products.
- The diary space is crowded at the top (Notion, Day One, Obsidian) but has many underserved
  niches: ADHD users, non-English speakers, people who've "tried and failed" repeatedly,
  users who want zero cloud sync, and users who want AI that *reflects with* them (not writes for them).
- Flag ideas that overlap with well-funded startups (competitive risk).
- When quoting user posts, paraphrase to avoid privacy concerns.
- If fetch scripts fail or return sparse data, note it in the report and suggest manual
  follow-up from the reference files.
- `QIITA_TOKEN` is read from `.env` automatically by `fetch_qiita.py`. If missing, the script
  still works but is rate-limited to 60 requests/hour.
