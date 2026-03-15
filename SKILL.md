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

---

## Step 1: Confirm the Target Year

**If the user has already specified a year** (e.g., "2025年を調査して" or "for 2024"), extract it
directly and skip asking. Otherwise, **ask in Japanese before doing anything else:**

> 調査対象の年号を教えてください（例：2025年）。
> 未入力の場合は現在の年（{CURRENT_YEAR}）を使用します。

If the user skips, types "skip", or enters nothing meaningful, use the current calendar year.
Save this as `TARGET_YEAR`.

**Date range logic (apply to all data sources):**

- If `TARGET_YEAR` >= current year → search the **past 12 months from today**
- If `TARGET_YEAR` < current year → search **Jan 1 to Dec 31** of that year

---

## Step 2: Gather Data

Run all three sources **in parallel** to save time.

### 2a. Reddit

```bash
python scripts/fetch_reddit.py --year TARGET_YEAR --output /tmp/reddit_raw.json
```

Target subreddits and what to look for: `references/diary-subreddits.md`

### 2b. Hacker News

```bash
python scripts/fetch_hn.py --year TARGET_YEAR --output /tmp/hn_raw.json
```

Query terms and interpretation: `references/hn-search-guide.md`

### 2c. Qiita

```bash
python scripts/fetch_qiita.py --year TARGET_YEAR --output /tmp/qiita_raw.json
```

Query terms and Japan market context: `references/qiita-search-guide.md`
`QIITA_TOKEN` is read from `.env`. If missing, falls back to 60 req/hr unauthenticated.

---

## Step 3: Synthesize Ideas

From the raw data, extract 5–10 specific, actionable product ideas.

For idea evaluation criteria and signal strength by source combination, see:
→ `references/idea-criteria.md`

For each idea, write:
- **Title**: Short product concept name
- **Problem**: What pain it solves (quote or paraphrase real user language)
- **Solution concept**: What the app/service does
- **Evidence**: Count of Reddit posts / HN threads / Qiita articles for this pain

---

## Step 4: Score Each Idea

Apply the 5-dimension scoring to each idea. Be honest — a score of 3 is useful calibration.

→ Scoring rubric: `references/scoring-rubric.md`

---

## Step 5: Save the Report

Save to:

```
reports/{TARGET_YEAR}/{YYYYMMDD}/{HHMMSS}.md
```

Use the template in `references/report-template.md`. Create parent directories as needed.
Tell the user the saved file path.

---

## Step 6: Post-Execution Review and Auto-Improvement

After saving the report, check for issues and apply fixes.

### 6a. Check Script Results

- Any errors, warnings, or empty output from the three fetch scripts?
- Did date range filtering apply correctly?
- Silent failures (no error but sparse data) → note in report and flag for manual follow-up

### 6b. Identify Bugs

**Scripts (`scripts/`):** date range errors, missing error handling, zero-result queries,
encoding issues (especially Qiita Japanese), rate limiting (429 → adjust `time.sleep()`)

**References (`references/`):** stale subreddit lists, outdated HN query terms,
miscalibrated scoring rubric

**SKILL.md:** unclear or missing instructions that caused problems

### 6c. Apply Fixes

1. Fix script bugs in `scripts/`
2. Update `references/` if query lists or rubrics need refreshing
3. Update `SKILL.md` or `CLAUDE.md` if workflow or structure changed

### 6d. Report to User

Tell the user what was checked, what was fixed, and any known limitations.
If nothing needed fixing, say: "No issues found."
