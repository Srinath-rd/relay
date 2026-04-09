# Relay

A personal social media monitoring agent that eliminates doomscrolling. Polls Reddit, Hacker News, and RSS feeds every 15 minutes, classifies posts via a local LLM (Ollama), and routes content by priority.

## How It Works

Every 15 minutes, Relay fetches posts from your configured sources, runs them through a local LLM with your personal interest profile, and routes them:

| Bucket | What it means | Delivery |
|---|---|---|
| **Very Interesting** | Time-sensitive, actionable — options ideas, breaking AI/cloud news | Instant push notification (Ntfy.sh) |
| **Interesting** | Worth reading, not urgent | Daily email digest + web dashboard |
| **Good** | Informational, low priority | Daily email digest + web dashboard |
| **Skip** | Noise | Archived |

Over time, the system learns your taste via a feedback loop — you rate posts on the web dashboard, and those ratings are stored and used as RAG context for future classifications.

## Architecture

```mermaid
flowchart TD
    SCHED[⏱️ APScheduler\nevery 15 min]

    SCHED --> RF[Reddit Fetcher\nPRAW]
    SCHED --> HN[HN Fetcher\nFirebase API]
    SCHED --> RSS[RSS Fetcher\nfeedparser]

    RF & HN & RSS --> DEDUP{Dedup Check\nSQLite}

    DEDUP -->|already seen| ARCH1[archived]
    DEDUP -->|new post| LLM

    LLM["🧠 LLM Classifier\nOllama — local\n─────────────────\npreferences.md\n+ post content\n+ recent ratings"]

    LLM --> VI[very_interesting]
    LLM --> INT[interesting]
    LLM --> GOOD[good]
    LLM --> SKIP[skip]

    VI --> PUSH[📱 Ntfy.sh\nPush Notification]
    INT --> DQ[(Digest Queue\nSQLite)]
    GOOD --> DQ
    SKIP --> ARCH2[archived]

    DQ -->|daily 08:00| EMAIL[📧 Email Digest\nSMTP / Gmail]

    DQ --> DASH[🖥️ Web Dashboard\nFastAPI + Jinja2]
    DASH -->|rate posts| RATINGS[(Ratings\nSQLite)]
    RATINGS -->|injected as\nfew-shot examples| LLM

    style LLM fill:#4f46e5,color:#fff
    style PUSH fill:#16a34a,color:#fff
    style EMAIL fill:#0369a1,color:#fff
    style DASH fill:#b45309,color:#fff
    style VI fill:#dc2626,color:#fff
    style INT fill:#ea580c,color:#fff
    style GOOD fill:#65a30d,color:#fff
```

## Stack

- **LLM**: Ollama (local) — `llama3.1:8b` now, `llama3.3:70b` on 48GB+ hardware
- **Sources**: Reddit (PRAW), Hacker News (Firebase API), RSS (feedparser)
- **Storage**: SQLite + SQLAlchemy
- **Recommendation**: Feedback loop — user ratings injected as few-shot examples into future prompts
- **Push**: Ntfy.sh
- **Email**: SMTP (Gmail)
- **Dashboard**: FastAPI + Jinja2
- **Scheduler**: APScheduler (15-min poll loop)

## Build Phases

- **Phase 1 (MVP)**: Reddit → LLM classifier → Ntfy.sh push notification
- **Phase 2**: HN + RSS fetchers, email digest, web dashboard, feedback UI
- **Phase 3**: ChromaDB RAG — system learns your preferences over time
- **Phase 4**: Per-source prompt tuning, YouTube fetcher

## Setup

> Coming soon — scaffold in progress (MLT-111)

## Requirements

- Python 3.11+
- [Ollama](https://ollama.ai) running locally
- Reddit API credentials (free)
- Ntfy.sh account (free)
- Gmail app password for digest emails
