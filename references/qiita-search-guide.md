# Qiita Search Guide — 日記・ジャーナリングアプリ

This file documents the Qiita search queries used by `fetch_qiita.py` and explains how to interpret results for diary/journaling idea research from a Japanese developer perspective.

---

## Built-in Query List

These queries are used by default in `fetch_qiita.py`:

| Query | What it surfaces |
|-------|-----------------|
| `日記 アプリ` | General diary app development articles |
| `日記 開発` | Developer-created diary tools — personal projects, OSS |
| `ジャーナリング アプリ` | Journaling-specific app coverage |
| `習慣 記録 アプリ` | Habit tracking + recording apps |
| `振り返り ツール` | Retrospective / reflection tools (popular in agile-adjacent communities) |
| `バレットジャーナル デジタル` | Digital bullet journal implementations |
| `ライフログ アプリ` | Life logging apps — quantified self from Japanese perspective |
| `感情 記録 アプリ` | Emotion/mood tracking apps |
| `日記 AI` | AI-enhanced diary tools — growing interest |
| `気分 トラッキング` | Mood/mental state tracking |
| `日記 サービス開発` | Web services built around diary functionality |
| `継続 習慣化 アプリ` | Habit continuation / streak apps |
| `メモ アプリ 個人開発` | Indie memo/note apps |
| `毎日書く 日記` | Daily writing diary — consistency-focused articles |
| `気軽 日記 続けられる` | Low-pressure journaling (the core concept of this project!) |

---

## Interpreting Qiita Results

### Qiita engagement signals

- **likes_count**: Basic engagement metric
- **stocks_count**: "Bookmarks" — higher quality signal, means readers found it useful enough to save
- **comments_count**: Discussion depth

The `engagement_score` formula weights stocks 2x and comments 3x, because on Qiita, stocking is a deliberate act of saving for later use.

### High-value article types on Qiita for this domain

- **個人開発の振り返り**: Indie developers sharing what they built and what problems they faced — often contains honest user feedback they received
- **アプリを1年続けた / 挫折した**: "I kept using X for a year" or "I gave up on X" articles — rich with real usage data
- **日記習慣化のコツ**: Tips for making diary a habit — reveals what friction points exist
- **技術選定**: Tech stack comparisons — reveals what developers think is missing from existing tools

### Japan-market specific considerations

- Japanese users often prefer **standalone apps** over cloud-connected ones due to privacy culture
- **シンプル (simplicity)** is a dominant value — overly complex apps are frequently criticized
- **継続できる (can continue)** is a common desire phrase — the low-pressure angle resonates deeply
- **手書き感 (handwriting feel)** is valued in the Japanese diary market — digital tools that mimic this may have advantage
- The concept of **ほぼ日手帳** (Hobonichi) has strong cultural mindshare — digital analogues are sought

---

## Supplemental Queries (run manually if needed)

If standard queries return sparse results:

```
育児日記 アプリ
旅行記録 アプリ
感謝日記
3行日記
読書記録 アプリ
```
