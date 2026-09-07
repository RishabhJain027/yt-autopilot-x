# YT-Autopilot-X | Autonomous YouTube Channel Operating System

A production-grade, multi-agent autonomous YouTube operating system built with Python, FastAPI, SQLAlchemy, Pillow, FFmpeg, edge-tts, and TailwindCSS.

Designed strictly per the **YT-Autopilot-X Architectural Specification Blueprint**.

---

## Key Architecture & Capabilities

1. **28-Stage Autonomous State Machine**:
   - Manages complete lifecycle from DISCOVERY_QUEUED -> RESEARCHING -> SCRIPTING -> RENDERING -> QA_PENDING -> REVIEW_PENDING / APPROVED -> UPLOADING -> PUBLISHED -> ANALYTICS_PENDING -> LEARNING_READY -> ARCHIVED.
   - Immutable audit trail recorded for every single state transition.

2. **6 Machine Quality Gates (Human-In-The-Loop Review Studio)**:
   - **Gate A (Factuality)**: Minimum 90% confidence on all factual claims with evidence desk source URLs.
   - **Gate B (Rights & Provenance)**: Verifies CC0/Commercial licenses and generates SHA-256 asset checksums.
   - **Gate C (Duplicate Content)**: Enforces script & topic uniqueness against recent channel uploads.
   - **Gate D (Safety & Policy)**: YouTube Community Guidelines compliance filter.
   - **Gate E (Synthetic Media Disclosure)**: Automatically applies status.containsSyntheticMedia = True flag.
   - **Gate F (Render Integrity)**: Container, video stream, audio stream, and duration checks.

3. **Enterprise Security & Policy Compliance**:
   - **Zero Gmail Passwords**: Exclusively Google OAuth 2.0 with AES-256 GCM encrypted token storage (CredentialVault).
   - **Zero Fake Engagement**: Strictly NO bot views, proxy manipulation, or artificial traffic engines.
   - **SSRF Protection**: Safe URL fetcher blocks internal subnets (127.0.0.1, 10.0.0.0/8, 192.168.0.0/16, 169.254.169.254).
   - **Log Redaction**: Automatic regex-based token and key scrubbing in JSON log streams.

4. **Resource & Quota Protection**:
   - **Daily Quota Manager**: Strict tracking against YouTube API 10,000 units/day limit with real-time deductions.
   - **Cost Budget Guard**: Enforces daily ( default) and monthly expenditure caps.
   - **Circuit Breaker**: Auto-trips to HALTED on consecutive API failures or quota exhaustion.

---

## Directory Structure

`
Youtube-Automation/
├── apps/
│   ├── api/
│   │   ├── routes/          # FastAPI REST endpoints
│   │   └── main.py          # FastAPI application entrypoint
│   └── dashboard/
│       └── public/          # Single-Page Application (SPA) dashboard
├── database/
│   ├── connection.py        # Async SQLite database engine & sessionmaker
│   └── schema.py            # SQLAlchemy async database models
├── packages/
│   ├── config/              # Pydantic v2 settings & environment configuration
│   └── logger/              # Structured JSON logging & token redaction
├── prompts/                 # Versioned prompt engineering templates
├── python/
│   ├── agents/              # AI Agents (Niche, Brand, Trend, Research, Script, QA, etc.)
│   ├── pipelines/           # 28-State Machine, Orchestrator, Hourly Tick
│   ├── research/            # Evidence Desk & SSRF-safe URL fetcher
│   ├── schemas/             # Pydantic data contracts
│   └── services/            # Vault, Quota Manager, Budget Guard, TTS, Image, YouTube
├── scheduler/
│   └── daemon.py            # APScheduler automated cron daemon
├── scripts/
│   └── cli.py               # Master CLI entrypoint
├── storage/                 # Database, renders, audio, thumbnails
├── tests/                   # Unit & integration test suites
└── run_tests.py             # Test suite runner
`

---

## Quick Start & CLI Commands

### 1. Initialize Database & Seed First Channel
`ash
python scripts/cli.py bootstrap
`

### 2. Check System Telemetry & Quota Status
`ash
python scripts/cli.py status
`

### 3. Execute an End-to-End Dry Run (Topic -> Script -> TTS -> FFmpeg -> QA Gates)
`ash
python scripts/cli.py dry-run
`

### 4. Run Test Suite
`ash
python run_tests.py
`

### 5. Launch the Web Dashboard & API Server
`ash
python scripts/cli.py serve --host 0.0.0.0 --port 8000
`
Open **http://localhost:8000** to access the Single-Pane Control Room Web Dashboard.

---

## Web Dashboard Workspace Views

1. **Pipeline Board**: Live 5-column Kanban board tracking productions across all 28 states.
2. **Review & Approval Studio**: Audio/video inspector, 6 Quality Gate verdicts, and one-click Approval.
3. **Trend Hub**: Niche and Trend Opportunity Matrices with formula scoring.
4. **Channel Fleet**: Multi-channel brand manager, persona voices, and OAuth authentication.
5. **Rights & Provenance**: Immutable SHA-256 asset ledger and license verification.
6. **Evidence Desk**: Real-time factual claims database with primary source citations.
7. **Learning Engine**: 7-day and 30-day analytics retrospective recommendations.
8. **Audit & Logs**: Live ISO-8601 structured system event stream.
