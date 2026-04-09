# Relay — Context

## What it is
A personal social media monitoring agent that polls platforms every 15 minutes, classifies posts via a local LLM (Ollama), and routes content by priority bucket — eliminating doomscrolling.

**Buckets:**
- **Very Interesting** → Immediate Ntfy.sh push notification to phone
- **Interesting** → Daily email digest + web dashboard
- **Good** → Daily email digest + web dashboard (lower priority)
- **Skip** → Archived

## Current Status
- Architecture designed and planned
- Linear project created: https://linear.app/minla/project/relay-2108dcefae83
- 17 Linear issues created (MLT-108 through MLT-124)
- No code written yet

## Stack
- Python 3.11+, Ollama (llama3.1:8b now → llama3.3:70b on new hardware)
- PRAW (Reddit), HN Firebase API, feedparser (RSS)
- SQLite + SQLAlchemy, ChromaDB (RAG), APScheduler
- Ntfy.sh (push), SMTP/Gmail (email digest)
- FastAPI + Jinja2 (web dashboard)

## Hardware
- Current: 16GB Mac → use llama3.1:8b
- In 1 week: 48GB MacBook Pro → upgrade to llama3.3:70b
- In 1 month: 96GB Mac Studio

## Build Phases
### Phase 1 — MVP (start here)
- MLT-111: Project scaffolding
- MLT-110: Reddit fetcher (PRAW)
- MLT-108: SQLite store
- MLT-109: LLM classifier (Ollama)
- MLT-114: Ntfy.sh push notifications
- MLT-112: APScheduler 15-min loop
- MLT-115: Unit tests (>90% coverage)

### Phase 2 — Full Sources + Digest
- MLT-113: HN fetcher
- MLT-119: RSS fetcher
- MLT-116: Email digest + SMTP
- MLT-117: FastAPI web dashboard
- MLT-118: Feedback rating UI
- MLT-120: Dockerfile

### Phase 3 — Recommendation Engine
- MLT-121: ChromaDB + embeddings
- MLT-122: RAG retriever

### Phase 4 — Polish
- MLT-123: Per-source prompt tuning
- MLT-124: YouTube fetcher

## How to Resume
1. Check Linear: https://linear.app/minla/project/relay-2108dcefae83
2. Start with Phase 1 issues (all marked Todo)
3. Confirm Ollama is running: `ollama list`
4. Begin with MLT-111 (scaffolding) then MLT-110 (Reddit fetcher)
